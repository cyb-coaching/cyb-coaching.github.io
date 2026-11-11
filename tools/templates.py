"""Modèles uniques du site Team Trail 7C : fiche, GOOO, prévisionnel.
Modifier un modèle ici change la page de TOUS les athlètes (et du groupe) au prochain build.
Aucune donnée personnelle dans ce fichier : les données sont dans src/*.json.enc."""
import html, os
E = lambda s: html.escape(str(s), quote=False)
D = os.path.dirname(os.path.abspath(__file__))
CSS_SAISON = open(f'{D}/css/saison.css').read()
CSS_FICHE = open(f'{D}/css/fiche.css').read()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap">')

# Code couleur Nolio (permanent) + « autre sport » (cyan, validé le 11/11/2026)
SPORT = {'ef': ('#9e9e9e', 'EF'), 'sl': ('#ffc107', 'Sortie longue'), 'fartlek': ('#ff9800', 'Fartlek'),
         'seuil': ('#e53935', 'VMA / seuil'), 'cotes': ('#3f51b5', 'Côtes'), 'tapis': ('#795548', 'Tapis'),
         'renfo': ('#8e44ad', 'Renfo'), 'velo': ('#e91e63', 'Vélo'), 'backyard': ('#cddc39', 'Boucles Backyard'),
         'autre': ('#00acc1', 'Autre sport'), 'off': ('#43a047', 'OFF')}
TAGS = {'course': ('Course', '#c2410c'), 'etape': ('Étape', '#2e7d32'), 'test': ('Test', '#e53935'),
        'nouveau': ('Nouveau', '#2f6f8f'), 'decision': ('Décision', '#4f5f8a'), 'allegee': ('Allégée', '#8a8f94'),
        'gros': ('Gros week-end', '#b45309'), 'vacances': ('Vacances', '#8a8f94')}
EXTRA = """
.nav{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;font-weight:600;}
.nav a{text-decoration:none;}
.hero-ms{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;}
.tg{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:1px 6px;border-radius:3px;color:#fff;background:var(--tc);margin-right:6px;vertical-align:1px;}
.tbl-box td.goal{font-weight:600;}
.vol{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:13px;color:var(--muted);}
.vol b{font-family:var(--display);font-size:1.25rem;color:var(--ink);margin-right:4px;}
.vol .tot b{font-size:1.6rem;color:var(--accent);}
.ses .st small{font-weight:500;color:var(--muted);margin-left:6px;}
.wnew{font-size:13px;margin-top:6px;} .wnew b{color:#2f6f8f;margin-right:6px;font-size:11px;text-transform:uppercase;letter-spacing:.05em;}
.card{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:14px 16px;}
.card ul{margin:0;padding-left:1.1rem;display:grid;gap:6px;}
.mslist{list-style:none;margin:0;padding:0;display:grid;gap:6px;}
.mslist li{display:grid;grid-template-columns:6rem 1fr;gap:10px;font-size:14px;}
.mslist li span:first-child{font-weight:700;color:var(--accent);white-space:nowrap;}
.week-body.solo{grid-template-columns:1fr;}
.week-body.solo .cadre{border-right:0;}
@media(max-width:700px){
 .wk-tbl tr:not(.sep){display:grid!important;grid-template-columns:auto 1fr;column-gap:10px;align-items:baseline;padding:8px 14px!important;}
 .wk-tbl tr:not(.sep) td{width:auto!important;}
 .wk-tbl tr:not(.sep) td:nth-child(1){font-size:1.05rem;}
 .wk-tbl tr:not(.sep) td:nth-child(3),.wk-tbl tr:not(.sep) td:nth-child(4){grid-column:1/-1;margin-top:0!important;}
 .wk-tbl tr:not(.sep) td:nth-child(3){font-size:14.5px!important;}
}"""
CD = ("<script>document.querySelectorAll('[data-cd]').forEach(e=>{const d=(new Date(e.dataset.cd+'T00:00:00')-new Date())/864e5;"
      "e.textContent=d>0?(' · dans '+Math.ceil(d/7)+' semaines'):'';});</script>")

def tag(t): l, c = TAGS[t]; return f'<span class="tg" style="--tc:{c}">{l}</span>'
def hm(m):
    if isinstance(m, (list, tuple)):
        return hm(m[0]) if m[0] == m[1] else f'{hm(m[0])} – {hm(m[1])}'
    h, r = divmod(int(m), 60); return f'{h} h {r:02d}' if h else f"{r}'"
def rng(s):  # durée d'une séance (min ou [min, max]) x nombre de séances
    m = s.get('min'); n = s.get('nb', 1)
    if m is None: return None
    a, b = (m, m) if not isinstance(m, (list, tuple)) else m
    return [a * n, b * n]
def add(ls):
    if any(x is None for x in ls): return None
    return [sum(x[0] for x in ls), sum(x[1] for x in ls)]
def doc(title, css, body):
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{E(title)}</title>\n{FONTS}\n<style>{css}</style>\n</head>\n<body>\n<div class="wrap">\n{body}\n</div>\n{CD}\n</body>\n</html>\n')

# ---------- GOOO (vue saison) ----------
def gooo(d, links):
    g = d['gooo']; o = []
    o.append(f'''<header><nav class="nav"><a href="{links['retour']}">← {E(links['retour_txt'])}</a><a href="{links['prev']}">Prévisionnel 4 semaines →</a></nav>
<div class="eyebrow" style="margin-top:14px">{E(d['titre'])} · vue saison · mise à jour le {E(g['maj'])}</div>
<h1 class="title">GOOO <span>{E(g['saison'])}</span></h1>
<p class="lede">{g['intro']}</p><div class="hero-ms">''')
    for ob in g['objectifs']:
        o.append(f'<span class="chip hot">Objectif {E(ob["niv"])} · {E(ob["nom"])} · {E(ob["date_txt"])}<span data-cd="{ob["date"]}"></span></span>')
    o.append('</div></header>')
    o.append(f'''<section class="frise-box"><div class="frise-h"><h2>La saison d'un coup d'œil</h2><span>{E(g['periode'])}</span></div><div class="frise">''')
    for b in g['blocs']:
        o.append(f'<div class="fb" style="--bc:{b["c"]};--f:{b["nsem"]}"><span class="wk">{E(b["sem"])}</span><b>{E(b["nom"])}</b><small>{E(b["dates"])}</small></div>')
    o.append('</div><div class="ms-row">' + ''.join(f'<span>★ <b>{E(j["evt"])}</b> {E(j["date"])}{(" (" + E(j["qui"]) + ")") if j.get("qui") else ""}</span>' for j in g['jalons'] if j.get('etoile')) + '</div></section>')
    o.append('<section class="sec"><h2>Les blocs</h2><div class="blocs">')
    for i, b in enumerate(g['blocs'], 1):
        pts = ''.join(f'<li>{E(p)}</li>' for p in b['points'])
        o.append(f'''<article class="blk"><div class="blk-top" style="background:{b['c']}"></div><div class="blk-body">
<div class="blk-h"><h3>{E(b['nom'])}</h3><span class="blk-num">{i:02d}</span></div><p class="dates">{E(b['dates'])} · {E(b['sem'])} · {b['nsem']} semaines</p>
<p><b>Mission :</b> {E(b['mission'])}</p><ul>{pts}</ul>{f'<div class="who"><b>Fin de bloc :</b> {E(b["fin"])}</div>' if b.get('fin') else ''}
{f'<p class="note">Volume : {E(b["volume"])}</p>' if b.get('volume') else ''}</div></article>''')
    o.append('</div></section>')
    o.append('<section class="sec"><h2>Le but de chaque semaine</h2><div class="tbl-box wk-tbl"><table><thead><tr><th>Sem.</th><th>Dates</th><th>But</th><th>Repère</th></tr></thead><tbody>')
    for b in g['blocs']:
        o.append(f'<tr class="sep" style="--bc:{b["c"]}"><td colspan="4">{E(b["nom"])}</td></tr>')
        for w in b.get('semaines', []):
            o.append(f'<tr><td class="wn">{E(w["n"])}</td><td>{E(w["dates"])}</td><td class="goal">{E(w["but"])}</td><td>{"".join(tag(t) for t in w.get("tags", []))}{E(w.get("rep", ""))}</td></tr>')
        if not b.get('semaines'):
            o.append('<tr><td class="wn">—</td><td></td><td class="goal">Semaines précisées à l\'approche du bloc</td><td></td></tr>')
    o.append('</tbody></table></div></section>')
    o.append('<section class="sec"><h2>Jalons et décisions</h2><div class="tbl-box"><table><thead><tr><th>Sem.</th><th>Date</th><th>Événement</th><th>Type</th></tr></thead><tbody>')
    for j in g['jalons']:
        qui = f' <small>({E(j["qui"])})</small>' if j.get('qui') else ''
        o.append(f'<tr><td class="wn">{E(j["sem"])}</td><td>{E(j["date"])}</td><td>{E(j["evt"])}{qui}</td><td>{tag(j["type"])}</td></tr>')
    o.append('</tbody></table></div>')
    if g.get('decisions'):
        o.append('<div class="card"><ul>' + ''.join(f'<li>{x}</li>' for x in g['decisions']) + '</ul></div>')
    o.append('<p class="note">Le détail des séances est dans Nolio. Les 4 prochaines semaines sont dans le Prévisionnel. Une semaine manquée ne se rattrape pas.</p></section>')
    return doc(f"GOOO · {d['titre']}", CSS_SAISON + EXTRA, '\n'.join(o))

# ---------- Prévisionnel (4 semaines glissantes) ----------
def prev(d, links):
    p = d['prev']; groupe = d.get('type') == 'groupe'; o = []
    o.append(f'''<header><nav class="nav"><a href="{links['retour']}">← {E(links['retour_txt'])}</a><a href="{links['gooo']}">GOOO, vue saison →</a></nav>
<div class="eyebrow" style="margin-top:14px">{E(d['titre'])} · 4 semaines glissantes · mise à jour le {E(p['maj'])}</div>
<h1 class="title">Prévisionnel <span>{E(p['de'])} → {E(p['a'])}</span></h1>
<p class="lede">{p['intro']}</p>
<p class="lede">Seules les semaines <span class="stat fix" style="margin-left:0">Planifiée dans Nolio</span> sont fixées. Les semaines <span class="stat ind" style="margin-left:0">Indicative</span> montrent la direction et seront ajustées selon les retours. Le détail de chaque séance est dans Nolio.</p></header>''')
    if p.get('jalons'):
        o.append('<section class="card"><h2 style="font-family:var(--display);font-size:1.35rem;margin:0 0 8px">Les jalons</h2><ul class="mslist">'
                 + ''.join(f'<li><span>{E(a)}</span><span>{E(b)}</span></li>' for a, b in p['jalons']) + '</ul></section>')
    used = []
    for w in p['semaines']:
        fix = w['statut'] == 'fix'
        ses = [s for s in w['seances'] if s['k'] != 'off']
        tot = add([rng(s) for s in ses]); run = add([rng(s) for s in ses if s.get('course')])
        nrun = sum(s.get('nb', 1) for s in ses if s.get('course'))
        o.append(f'''<article class="week{'' if fix else ' draft'}"><div class="week-h"><div class="wnum">{E(w['n'])}</div>
<div class="wdates">{E(w['dates'])}</div><div class="wblock">{E(w['bloc'])}<span class="stat {'fix' if fix else 'ind'}">{'Planifiée dans Nolio' if fix else 'Indicative'}</span></div>
<div class="wgoal">{E(w['but'])}</div></div>''')
        if not fix: o.append('<p class="draftnote">Semaine indicative : non figée dans Nolio.</p>')
        o.append(f'''<div class="week-body{'' if groupe else ' solo'}"><div class="cadre">
<div class="vol"><span class="tot"><b>{hm(tot) if tot else hm(add([r for r in (rng(x) for x in ses) if r]) or [0, 0]) + ' +'}</b>{'au total' if tot else 'au total, plus une séance selon le profil'}</span><span><b>{hm(run) if run else '—'}</b>de course</span><span><b>{nrun}</b>sorties</span></div>''')
        if w.get('nouveau'): o.append(f'<div class="wnew"><b>Nouveauté</b>{E(w["nouveau"])}</div>')
        o.append(f'<h3 style="margin-top:12px">{"Cadre commun" if groupe else "Les séances de la semaine"}</h3><div class="ses-list">')
        for s in ses:
            if s['k'] not in used: used.append(s['k'])
            o.append(f'<div class="ses" style="--sc:{SPORT[s["k"]][0]}"><div class="st">{E(s["jour"])} · {E(s["titre"])}<small>{(str(s["nb"]) + " × ") if s.get("nb", 1) > 1 else ""}{hm(s["min"]) if s.get("min") is not None else ""}</small></div>'
                     + (f'<div class="sn">{E(s["note"])}</div>' if s.get('note') else '') + '</div>')
        o.append('</div></div>')
        if groupe:
            o.append('<div class="adapt"><h3>Adaptations individuelles</h3><table class="adapt-tbl"><tbody>'
                     + ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b in w.get('adaptations', [])) + '</tbody></table></div>')
        o.append('</div></article>')
    o.append('<div class="legend">' + ''.join(f'<span><i style="background:{SPORT[k][0]}"></i>{SPORT[k][1]}</span>' for k in used) + '</div>')
    if p.get('ensuite'): o.append(f'<p class="note">{E(p["ensuite"])}</p>')
    o.append('<p class="note">Une semaine manquée ne se rattrape pas : on reprend le fil.</p>')
    return doc(f"Prévisionnel · {d['titre']}", CSS_SAISON + EXTRA, '\n'.join(o))

# ---------- Fiche individuelle ----------
def fiche(d, links):
    f = d['fiche']; o = []
    if links.get('groupe'): o.append(f'<a href="{links["groupe"]}" class="back">← Groupe Ultra 2027</a>')
    o.append(f'<header><div class="eyebrow">Espace personnel</div><h1 class="title">{E(d["titre"])}</h1><p class="lede">{E(f["objectif"])}</p></header>')
    o.append('<section class="sec"><h2>Mes dates clés</h2><div class="card"><table class="dates">'
             + ''.join(f'<tr><td>{E(r[0])}</td><td>{E(r[1])}{(" <span class=tbc>(" + E(r[2]) + ")</span>") if len(r) > 2 and r[2] else ""}</td></tr>' for r in f['dates'])
             + '</table></div></section>')
    if f.get('reperes'):
        o.append('<section class="sec"><h2>Mes repères</h2><div class="card"><table class="dates">'
                 + ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b in f['reperes']) + '</table></div>'
                 + (f'<p class="note">{E(f["reperes_note"])}</p>' if f.get('reperes_note') else '') + '</section>')
    if f.get('consignes'):
        o.append('<section class="sec"><h2>Mes consignes</h2>')
        for c in f['consignes']:
            o.append(f'<div class="card"><h3 style="font-size:1.25rem">{E(c["titre"])}</h3><table class="dates">'
                     + ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b in c['lignes']) + '</table></div>')
        o.append('</section>')
    o.append('<section class="sec"><h2>Bientôt ici</h2><ul class="soon"><li><b>Mes courbes</b> : forme, charge, sommeil.</li>'
             '<li><b>Mon suivi</b> : bilan de mes séances et ajustements décidés avec mon coach.</li></ul></section>')
    if links.get('gooo'):
        o.append(f'''<section class="sec"><h2>Mes plans</h2><div class="docs">
<a class="doc" style="--dc:var(--accent)" href="{links['gooo']}"><h3>GOOO, vue saison</h3><p>Les blocs, le but de chaque semaine, les jalons.</p></a>
<a class="doc" style="--dc:var(--accent)" href="{links['prev']}"><h3>Prévisionnel</h3><p>Les 4 prochaines semaines.</p></a></div></section>''')
    if links.get('groupe'):
        o.append(f'''<section class="sec"><h2>Le groupe</h2><div class="docs"><a class="doc hero" style="--dc:var(--accent)" href="{links['groupe']}"><h3>Page du groupe</h3><p>Plan et prévisionnel des 4 semaines.</p></a></div></section>''')
    return doc('Mon espace · Team Trail 7C', CSS_FICHE, '\n'.join(o))

# ---------- Accueil du groupe ----------
_sa = CSS_SAISON
CSS_BLOCS = _sa[_sa.find('/* Blocs cartes */'):_sa.find('/* Tableau semaines */')]
CSS_GROUPE = open(f'{D}/css/groupe.css').read() + CSS_BLOCS
def groupe(d, links):
    h = d['accueil']; g = d['gooo']; o = []
    o.append(f'''<header><a href="{links['retour']}" class="back">← Team Trail 7C</a><div class="eyebrow">Dossier collectif</div>
<h1 class="title">{E(d['titre'])} <span>{E(h['annee'])}</span></h1><p class="lede">{E(h['lede'])}</p></header>''')
    o.append('<section class="sec"><h2>Le groupe</h2><div class="membres">' + ''.join(
        f'<div class="mb"><strong>{E(m["nom"])}</strong><span class="obj" style="--mc:var({"--accent" if m.get("niv", "A") == "A" else "--idea"})">{E(m["obj"])}</span></div>' for m in h['membres']) + '</div></section>')
    o.append('<section class="sec"><h2>Objectifs</h2><div class="goals">')
    for ob in h['objectifs']:
        a = ob['niv'] == 'A'
        o.append(f'''<article class="goal"><div class="top" style="background:var({'--accent' if a else '--idea'})"></div><div class="body">
<span class="pill {'a' if a else 'b'}">Objectif {ob['niv']} · {'principal' if a else 'intermédiaire'}</span><h3>{E(ob['nom'])}</h3>
<p class="meta">{E(ob['meta'])}</p><p class="who"><b>{E(ob['qui'])}</b>{(' ' + E(ob['note'])) if ob.get('note') else ''}</p></div></article>''')
    o.append('</div></section>')
    o.append(f'<section class="sec"><h2>La saison en {len(g["blocs"])} blocs</h2><div class="blocs">')
    for i, b in enumerate(g['blocs'], 1):
        o.append(f'''<article class="blk"><div class="blk-top" style="background:{b['c']}"></div><div class="blk-body">
<div class="blk-h"><h3>{E(b['nom'])}</h3><span class="blk-num">{i:02d}</span></div><p class="dates">{E(b['dates'])} · {E(b['sem'])}</p>
<p>{E(b['mission'])}</p>{f'<span class="ms-tag" style="--mc:{b["c"]}">★ {E(b["fin"])}</span>' if b.get('fin') else ''}</div></article>''')
    o.append('</div></section>')
    o.append(f'''<section class="sec"><h2>Les pages du dossier</h2><p class="note">Pages réservées au groupe, accessibles avec ton code.</p><div class="docs">
<a class="doc hero" style="--dc:var(--accent)" href="{links['gooo']}"><h3>GOOO du groupe</h3><p>La saison semaine par semaine, les blocs en détail, les jalons.</p><span class="arr">→</span></a>
<a class="doc" style="--dc:var(--ok)" href="{links['prev']}"><h3>Prévisionnel</h3><p>Les 4 prochaines semaines : cadre commun + adaptations individuelles.</p><span class="arr">→</span></a></div></section>''')
    return doc(f"{d['titre']} {h['annee']}", CSS_GROUPE, '\n'.join(o))
