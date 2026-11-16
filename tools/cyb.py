#!/usr/bin/env python3
"""Outil unique du site Team Trail 7C.

Toutes les données (codes, registre, athlètes) sont dans src/*.json.enc, chiffrées avec le code coach.
Le code coach se passe par la variable d'environnement CYB_COACH (jamais dans un fichier du dépôt).

  CYB_COACH=... python3 tools/cyb.py open <nom>      # déchiffre src/<nom>.json.enc -> work/<nom>.json (à éditer)
  CYB_COACH=... python3 tools/cyb.py seal <nom>      # rechiffre work/<nom>.json -> src/<nom>.json.enc
  CYB_COACH=... python3 tools/cyb.py build [nom...]  # régénère les pages du registre (toutes, ou celles des athlètes cités)
  CYB_COACH=... python3 tools/cyb.py check           # contrôle : destinataires, déchiffrement, fuites en clair
work/ est ignoré par git. Ne jamais committer de texte en clair.
"""
import json, re, os, sys, base64, hashlib, glob
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import templates as T
N = 600000
B64 = lambda x: base64.b64encode(x).decode(); UB = base64.b64decode
RX = re.compile(r'(<script id="p" type="application/json">)(.*?)(</script>)', re.S)
def norm(c): return c.lower().replace(' ', '').replace('-', '').encode()
def kdf(code, salt, n=N, l=32): return hashlib.pbkdf2_hmac('sha256', norm(code), salt, n, dklen=l)
def slot_id(code, n=N): return kdf(code, b'cyb-id-v1', n, 8).hex()

# ---- chiffrement mono-destinataire (sources) ----
def enc1(text, code):
    s, iv = os.urandom(16), os.urandom(12)
    return {'s': B64(s), 'i': B64(iv), 'c': B64(AESGCM(kdf(code, s)).encrypt(iv, text.encode(), None)), 'n': N}
def dec1(P, code): return AESGCM(kdf(code, UB(P['s']), P['n'])).decrypt(UB(P['i']), UB(P['c']), None).decode()

# ---- chiffrement multi-destinataires (pages) ----
def enc_multi(html, codes):
    key, iv = os.urandom(32), os.urandom(12)
    k = []
    for c in codes:
        s, i2 = os.urandom(16), os.urandom(12)
        k.append({'d': slot_id(c), 's': B64(s), 'i': B64(i2), 'c': B64(AESGCM(kdf(c, s)).encrypt(i2, key, None))})
    return {'k': k, 'i': B64(iv), 'c': B64(AESGCM(key).encrypt(iv, html.encode(), None)), 'n': N}
def dec_page(P, code):
    if 'k' in P:
        sl = [x for x in P['k'] if x['d'] == slot_id(code, P['n'])]
        if not sl: return None
        sl = sl[0]
        key = AESGCM(kdf(code, UB(sl['s']), P['n'])).decrypt(UB(sl['i']), UB(sl['c']), None)
        return AESGCM(key).decrypt(UB(P['i']), UB(P['c']), None).decode()
    try: return dec1(P, code)
    except Exception: return None
def read_payload(path): return json.loads(RX.search(open(path, encoding='utf-8').read()).group(2))

def coach():
    c = os.environ.get('CYB_COACH')
    if not c: sys.exit('CYB_COACH manquant (code coach : claude/03_Acces_site.md dans le projet Coaching).')
    return c
def src(name, code): return json.loads(dec1(json.load(open(f'{ROOT}/src/{name}.json.enc')), code))
def write_src(name, data, code):
    os.makedirs(f'{ROOT}/src', exist_ok=True)
    json.dump(enc1(json.dumps(data, ensure_ascii=False, indent=1), code), open(f'{ROOT}/src/{name}.json.enc', 'w'))

def write_page(path, html, codes, coach_code):
    full = f'{ROOT}/{path}'
    shell = open(f'{ROOT}/tools/shell.html', encoding='utf-8').read()
    if os.path.exists(full):
        try:
            cur = open(full, encoding='utf-8').read(); a, b = shell.split('@@PAYLOAD@@')
            same_shell = cur.startswith(a) and cur.endswith(b)
            P = read_payload(full)
            same_rcpt = sorted(x['d'] for x in P.get('k', [])) == sorted(slot_id(c) for c in codes)
            if same_shell and same_rcpt and dec_page(P, coach_code) == html: return False   # rien n'a changé : on ne touche pas
        except Exception: pass
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(shell.replace('@@PAYLOAD@@', json.dumps(enc_multi(html, codes))))
    return True

HUB = 'p/5c08340fa6736971/index.html'   # tableau de bord du coach

def build(only=None):
    cc = coach(); reg = src('registre', cc); codes = reg['codes']
    changed = []
    for pg in reg['pages']:
        if only and pg['data'] not in only: continue
        data = src(pg['data'], cc)
        if data.get('membre_groupe'):   # frise d'un membre : blocs du groupe + jalons qui le concernent + jalons perso
            g = src('groupe', cc)['gooo']; pr = data['prenom']
            js = [dict(j, qui='') for j in g['jalons'] if pr in j.get('qui', '') or 'tout le groupe' in j.get('qui', '')]
            data['fiche']['frise'] = {'blocs': g['blocs'], 'jalons': js + data['fiche'].get('jalons_perso', []), 'periode': g.get('periode', '')}
        html = getattr(T, pg['tpl'])(data, pg.get('liens', {}))
        if write_page(pg['path'], html, [codes[r] for r in pg['pour']], cc): changed.append(pg['path'])
    # tableau de bord du coach (code coach seul), régénéré à chaque build
    gm = reg['groupe_ultra']['membres']; gp = reg['groupe_ultra']['page']
    def maj(dd): return (dd.get('prev') or {}).get('maj') or (dd.get('gooo') or {}).get('maj') or ''
    gd = src('groupe', cc)
    grp = [('Page du groupe', f'../{gp}/', maj(gd)), ('GOOO du groupe', f'../{gp}/plan/', (gd.get('gooo') or {}).get('maj', '')),
           ('Prévisionnel', f'../{gp}/previsionnel/', (gd.get('prev') or {}).get('maj', ''))]
    ath = []
    for pg in reg['pages']:
        if pg['tpl'] != 'fiche': continue
        dd = src(pg['data'], cc); n = pg['data']
        st = 'Groupe Ultra' if n in gm else ('invité du groupe' if 'groupe' in pg.get('liens', {}) else 'suivi individuel')
        ath.append((dd.get('titre', n), '../' + pg['path'].split('/')[1] + '/', st, maj(dd)))
    ath.sort(key=lambda x: ['Groupe Ultra', 'invité du groupe', 'suivi individuel'].index(x[2]))
    if write_page(HUB, T.hub(grp, ath), [codes['coach']], cc): changed.append(HUB)
    print('pages modifiées :', changed or 'aucune')

def check():
    cc = coach(); reg = src('registre', cc); codes = reg['codes']; ok = True
    by_id = {slot_id(c): n for n, c in codes.items()}
    for pg in reg['pages']:
        P = read_payload(f'{ROOT}/{pg["path"]}')
        got = sorted(by_id.get(x['d'], '?') for x in P['k'])
        if got != sorted(pg['pour']): print('DESTINATAIRES', pg['path'], got, '≠', sorted(pg['pour'])); ok = False
        for r in pg['pour']:
            if dec_page(P, codes[r]) is None: print('ÉCHEC', pg['path'], r); ok = False
    P = read_payload(f'{ROOT}/{HUB}')
    if [x['d'] for x in P.get('k', [])] != [slot_id(codes['coach'])] or dec_page(P, codes['coach']) is None:
        print('TABLEAU DE BORD : doit s\'ouvrir avec le seul code coach'); ok = False
    # fuite : aucun nom d'athlète ni code en clair dans les fichiers suivis par git
    words = [w for a in reg['athletes'].values() for w in a['nom'].split() if len(w) > 3] + list(codes.values())
    files = os.popen(f'git -C {ROOT} ls-files').read().split()
    for f in files:
        if f.startswith('src/') or f.endswith(('.png', '.jpg', '.svg', '.webp', '.ico')): continue
        t = open(f'{ROOT}/{f}', encoding='utf-8', errors='ignore').read()
        t = RX.sub('', t)
        for w in words:
            if w in t: print('FUITE', f, w[:3] + '…'); ok = False
    print('CONTRÔLE OK' if ok else 'CONTRÔLE EN ÉCHEC')
    return ok

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'open':
        os.makedirs(f'{ROOT}/work', exist_ok=True)
        json.dump(src(a[1], coach()), open(f'{ROOT}/work/{a[1]}.json', 'w'), ensure_ascii=False, indent=1); print(f'work/{a[1]}.json')
    elif a[0] == 'seal': write_src(a[1], json.load(open(f'{ROOT}/work/{a[1]}.json')), coach()); print(f'src/{a[1]}.json.enc')
    elif a[0] == 'build': build(a[1:] or None)
    elif a[0] == 'check': sys.exit(0 if check() else 1)
    else: sys.exit(__doc__)
