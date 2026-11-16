"""Modèles uniques du site Team Trail 7C : fiche, GOOO, prévisionnel.
Modifier un modèle ici change la page de TOUS les athlètes (et du groupe) au prochain build.
Aucune donnée personnelle dans ce fichier : les données sont dans src/*.json.enc."""
import html, os
E = lambda s: html.escape(str(s), quote=False)
D = os.path.dirname(os.path.abspath(__file__))
CSS_SAISON = open(f'{D}/css/saison.css').read()
CSS_FICHE = open(f'{D}/css/fiche.css').read()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">'
         '<link rel="icon" href="/favicon.svg" type="image/svg+xml">')

# Code couleur Nolio (permanent) + « autre sport » (cyan, validé le 11/11/2026)
SPORT = {'ef': ('#9e9e9e', 'EF'), 'sl': ('#ffc107', 'Sortie longue'), 'fartlek': ('#ff9800', 'Fartlek'),
         'seuil': ('#e53935', 'VMA / seuil'), 'cotes': ('#3f51b5', 'Côtes'), 'tapis': ('#795548', 'Tapis'),
         'renfo': ('#8e44ad', 'Renfo'), 'velo': ('#e91e63', 'Vélo'), 'backyard': ('#cddc39', 'Boucles Backyard'),
         'autre': ('#00acc1', 'Autre sport'), 'compet': ('#c2410c', 'Course'), 'off': ('#43a047', 'OFF')}
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
      "e.textContent=d>0?(' · dans '+Math.ceil(d/7)+' semaines'):'';});"
      "document.querySelectorAll('.tl-now').forEach(e=>{const c=Math.floor((new Date()-new Date(e.dataset.d0+'T00:00:00'))/6048e5)+1;"
      "if(c>=1&&c<=+e.dataset.nw){e.style.gridColumn=c;e.hidden=false;}});</script>")

MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
CSS_FRISE = """
.tl{min-width:0;max-width:100%;overflow:hidden;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:14px 0 12px;}
.tl-h{padding:0 16px 8px;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;}
.tl-h h2{font-family:var(--display);font-size:1.35rem;font-weight:600;margin:0;}
.tl-h span{font-size:13px;color:var(--muted);}
.tl-sc{overflow-x:auto;-webkit-overflow-scrolling:touch;padding:0 16px 6px;}
.tl-g{display:grid;grid-template-columns:repeat(var(--nw),minmax(15px,1fr));min-width:calc(var(--nw) * 15px);row-gap:3px;}
.tl-m{font-size:11.5px;font-weight:700;color:var(--muted);border-left:1px solid var(--line);padding-left:4px;white-space:nowrap;overflow:hidden;}
.tl-b{height:22px;border-radius:4px;color:#fff;font-size:11px;font-weight:700;padding:3px 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-right:2px;}
.tl-now{grid-row:1/-1;border-left:2px dashed var(--accent);opacity:.6;pointer-events:none;}
.tl-j{font-size:11.5px;line-height:1.2;padding:16px 4px 2px 0;position:relative;min-width:0;}
.tl-j::before{position:absolute;top:0;left:0;font-size:13px;line-height:1;color:var(--mc);content:"■";}
.tl-j.star::before{content:"★";font-size:16px;top:-2px;}
.tl-j b{display:block;font-family:var(--display);font-size:13.5px;font-weight:700;}
.tl-j span{color:var(--muted);}
.tl-lg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12px;color:var(--muted);padding:6px 16px 0;}
.tl-lg i{font-style:normal;color:var(--mc);margin-right:4px;}
.tl-hint{display:none;font-size:12px;color:var(--muted);padding:0 16px 4px;}
@media(max-width:700px){.tl-hint{display:block;}}
"""
import datetime as _dt
def _d(iso): return _dt.date.fromisoformat(iso[:10])
JCOL = {'course': '#c2410c', 'test': '#e53935', 'etape': '#2e7d32', 'gros': '#b45309', 'decision': '#4f5f8a', 'nouveau': '#2f6f8f', 'allegee': '#8a8f94', 'vacances': '#8a8f94'}
def frise(blocs, jalons, titre="L'année d'un coup d'œil", sous=''):
    """Frise chronologique horizontale (une colonne par semaine). blocs : nom, c, debut, fin_d ; jalons : iso, court/evt, date, qui, type, etoile."""
    d0 = _d(blocs[0]['debut']); d0 -= _dt.timedelta(days=d0.weekday())
    d1 = max([_d(blocs[-1]['fin_d'])] + [_d(j['iso']) for j in jalons if j.get('iso')])
    nw = (d1 - d0).days // 7 + 1; W = 7
    col = lambda iso: max(1, min(nw, (_d(iso) - d0).days // 7 + 1))
    o = []
    # mois
    y, m = d0.year, d0.month
    while _dt.date(y, m, 1) <= d1:
        c0 = col(max(_dt.date(y, m, 1), d0).isoformat()); ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        c1 = col(min(_dt.date(ny, nm, 1) - _dt.timedelta(days=1), d1).isoformat()) + 1
        lab = (MOIS[m - 1] + (f' {str(y)[2:]}' if (m == 1 or not o) and c1 - c0 >= 4 else '')) if c1 - c0 >= 3 else ''
        o.append(f'<div class="tl-m" style="grid-row:1;grid-column:{c0}/{c1}">{lab}</div>'); y, m = ny, nm
    for b in blocs:
        o.append(f'<div class="tl-b" style="grid-row:2;grid-column:{col(b["debut"])}/{col(b["fin_d"]) + 1};background:{b["c"]}" title="{E(b["nom"])}">{E(b["nom"])}</div>')
    rows = []
    for j in sorted([j for j in jalons if j.get('iso') and j['type'] != 'decision'], key=lambda j: j['iso']):  # frise : courses et grands jalons seulement
        c = col(j['iso']); r = next((i for i, last in enumerate(rows) if last < c), None)
        if r is None: rows.append(0); r = len(rows) - 1
        rows[r] = c + W - 1
        qui = f' · {E(j["qui"])}' if j.get('qui') else ''
        cls = 'tl-j star' if j['type'] == 'course' else 'tl-j'
        o.append(f'<div class="{cls}" style="grid-row:{3 + r};grid-column:{c}/span {W};--mc:{JCOL.get(j["type"], "#5d6b77")}"><b>{E(j.get("court") or j["evt"])}</b><span>{E(j["date"])}{qui}</span></div>')
    o.append(f'<div class="tl-now" data-d0="{d0.isoformat()}" data-nw="{nw}" hidden></div>')
    lg = ''.join(f'<span><i style="--mc:{JCOL[k]}">{"★" if k == "course" else "■"}</i>{l}</span>' for k, l in [('course', 'course'), ('test', 'test'), ('etape', 'étape'), ('gros', 'gros week-end')] if any(j['type'] == k for j in jalons))
    return (f'<section class="tl"><div class="tl-h"><h2>{titre}</h2><span>{E(sous)}</span></div><p class="tl-hint">Fais glisser la frise vers la droite →</p>'
            f'<div class="tl-sc"><div class="tl-g" style="--nw:{nw + W + 2}">{"".join(o)}</div></div><div class="tl-lg">{lg}<span>pointillé : aujourd\'hui</span></div></section>')

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

# ---------- Identité Team Trail 7C (16/11/2026) : habillage commun, contenu inchangé ----------
LOGO = '<svg class="tt-mark" viewBox="0 0 100 100" aria-hidden="true"><polygon points="0,84 18,46 30,62 52,22 74,60 84,48 100,84" fill="#9db8a5"/><polygon points="52,22 45,36 52,33 59,37" fill="#eef3ef"/><polygon points="31,64 39,64 33,90 25,90" fill="#8a6d3b"/><line x1="28.3" y1="74" x2="36.3" y2="74" stroke="#5e4826" stroke-width="1.5"/><line x1="26.3" y1="82" x2="34.3" y2="82" stroke="#5e4826" stroke-width="1.5"/><path d="M24.5,89 L33.5,89 L39,95 L39,98 L24.5,98 Z" fill="#3b2a18"/><polygon points="42,64 50,64 53,90 45,90" fill="#8a6d3b"/><line x1="43.4" y1="74" x2="51.4" y2="74" stroke="#5e4826" stroke-width="1.5"/><line x1="44.3" y1="82" x2="52.3" y2="82" stroke="#5e4826" stroke-width="1.5"/><path d="M44.5,89 L53.5,89 L59,95 L59,98 L44.5,98 Z" fill="#3b2a18"/><polygon points="53,64 61,64 58,90 50,90" fill="#8a6d3b"/><line x1="51.6" y1="74" x2="59.6" y2="74" stroke="#5e4826" stroke-width="1.5"/><line x1="50.7" y1="82" x2="58.7" y2="82" stroke="#5e4826" stroke-width="1.5"/><path d="M49.5,89 L58.5,89 L64,95 L64,98 L49.5,98 Z" fill="#3b2a18"/><polygon points="64,64 72,64 78,90 70,90" fill="#8a6d3b"/><line x1="66.7" y1="74" x2="74.7" y2="74" stroke="#5e4826" stroke-width="1.5"/><line x1="68.7" y1="82" x2="76.7" y2="82" stroke="#5e4826" stroke-width="1.5"/><path d="M69.5,89 L78.5,89 L84,95 L84,98 L69.5,98 Z" fill="#3b2a18"/><path d="M19,60 C19,22 81,22 81,60 Z" fill="#55693a"/><path d="M24,57 C24,33 38,25 49,25 C38,30 31,42 31,57 Z" fill="#fff" opacity=".16"/><path d="M46,59 L46,27 Q50,19.5 54,27 L54,59 Z" fill="#3b4a28"/><line x1="50" y1="24" x2="50" y2="58" stroke="#6f8450" stroke-width="1.2"/><path d="M12,61 Q50,74 88,61 L83,55.5 Q50,66 17,55.5 Z" fill="#3b4a28"/><path d="M17,55.5 Q50,66 83,55.5" fill="none" stroke="#7d9358" stroke-width="1.3"/><circle cx="23.5" cy="49" r="1.9" fill="#d9c46a"/><circle cx="76.5" cy="49" r="1.9" fill="#d9c46a"/><path d="M17,56 L14.5,68" stroke="#6b4a2a" stroke-width="2.2" stroke-linecap="round" fill="none"/><path d="M83,56 L85.5,68" stroke="#6b4a2a" stroke-width="2.2" stroke-linecap="round" fill="none"/><circle cx="50" cy="44" r="9.5" fill="#e9dca4" stroke="#9a7d1f" stroke-width="1.6"/><text x="50" y="48.3" text-anchor="middle" font-family="Barlow Condensed,Arial Narrow,sans-serif" font-weight="700" font-size="13" fill="#3b4a28">7C</text></svg>'
THEME = """
:root{--bg:#f4f2ee;--paper:#fff;--ink:#16302a;--muted:#68776f;--line:#e1ddd4;--soft:#ebe7df;--accent:#c4552f;
 --display:"Inter Tight","Inter",system-ui,-apple-system,"Segoe UI",sans-serif;--body:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;}
body{color:#36463f;font-size:15.5px;line-height:1.6;}
.title{font-weight:800;letter-spacing:-.04em;line-height:1.02;color:var(--ink);}
.sec>h2,.tl-h h2{font-weight:800;letter-spacing:-.03em;color:var(--ink);font-size:1.55rem;}
h3{letter-spacing:-.02em;color:var(--ink);}
.eyebrow{color:var(--accent);font-weight:700;letter-spacing:.16em;font-size:11.5px;}
.card,.tl,.blk,.doc,.goal,.week,.tbl-box,.frise-box,.season-box,.soon li,.mb{border-radius:0;}
.card,.tl,.week,.tbl-box{border-color:var(--line);}
.doc{border-top:3px solid var(--ink);}
.tt-site{border-bottom:1px solid #d8d4cb;background:#f8f7f4;}
.tt-in{max-width:76rem;margin-inline:auto;padding-inline:max(20px,env(safe-area-inset-left,0px));}
.tt-site .tt-in{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:76px;}
.tt-brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:#16302a;}
.tt-mark{width:52px;height:52px;flex:none;}
.tt-brand b{display:block;font-family:var(--display);font-weight:800;font-size:19px;letter-spacing:-.03em;line-height:1;}
.tt-brand b em{font-style:normal;color:#c4552f;}
.tt-brand small{display:block;font-size:9.5px;font-weight:600;letter-spacing:.2em;color:#68776f;margin-top:4px;}
.tt-nav{display:flex;gap:28px;}
.tt-nav a{font-size:14px;font-weight:500;color:#68776f;text-decoration:none;padding:6px 0;border-bottom:2px solid transparent;}
.tt-nav a.on{color:#16302a;font-weight:600;border-bottom-color:#c4552f;}
.tt-foot{border-top:1px solid #d8d4cb;background:#ecebe6;margin-top:8px;}
.tt-foot .tt-in{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-block:26px;font-size:13px;color:#68776f;}
.tt-foot b{color:#16302a;font-weight:700;}
.tt-foot a{color:#16302a;font-weight:600;text-decoration:none;border-bottom:1px solid #16302a;}
@media(max-width:700px){.tt-site .tt-in{flex-direction:column;align-items:flex-start;gap:6px;padding-block:14px 0;min-height:0;}
 .tt-mark{width:44px;height:44px;}.tt-nav{gap:22px;}.tt-nav a{padding:8px 0 10px;}}
"""
HEADER = ('<header class="tt-site"><div class="tt-in"><a class="tt-brand" href="/">' + LOGO +
          '<span><b>TEAM TRAIL <em>7C</em></b><small>COURSE À PIED · TRAIL · ULTRA</small></span></a>'
          '<nav class="tt-nav" aria-label="Navigation du site"><a href="/">Accueil</a><a href="/ressources/">Ressources</a>'
          '<a class="on" aria-current="page" href="/coaching/">Coaching</a></nav></div></header>')
FOOTER = ('<footer class="tt-foot"><div class="tt-in"><span><b>TEAM TRAIL 7C</b> · Courir avec méthode, progresser avec plaisir.</span>'
          '<a href="#">Retour en haut ↑</a></div></footer>')

def doc(title, css, body):
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{E(title)}</title>\n{FONTS}\n<style>{css}{THEME}</style>\n</head>\n<body>\n{HEADER}\n<div class="wrap">\n{body}\n</div>\n{FOOTER}\n{CD}\n</body>\n</html>\n')

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
    for i, b in enumerate(g['blocs'] if not d.get('accueil') else [], 1):
        if i == 1: o.append('<section class="sec"><h2>Les blocs</h2><div class="blocs">')
        pts = ''.join(f'<li>{E(p)}</li>' for p in b['points'])
        o.append(f'''<article class="blk"><div class="blk-top" style="background:{b['c']}"></div><div class="blk-body">
<div class="blk-h"><h3>{E(b['nom'])}</h3><span class="blk-num">{i:02d}</span></div><p class="dates">{E(b['dates'])} · {E(b['sem'])} · {b['nsem']} semaines</p>
<p><b>Mission :</b> {E(b['mission'])}</p><ul>{pts}</ul>{f'<div class="who"><b>Fin de bloc :</b> {E(b["fin"])}</div>' if b.get('fin') else ''}
{f'<p class="note">Volume : {E(b["volume"])}</p>' if b.get('volume') else ''}</div></article>''')
        if i == len(g['blocs']): o.append('</div></section>')
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
    return doc(f"GOOO · {d['titre']}", CSS_SAISON + EXTRA + CSS_FRISE, '\n'.join(o))

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
            ad = [(a, b) for a, b in w.get('adaptations', []) if b]
            o.append('<div class="adapt"><h3>Adaptations individuelles</h3>' + (('<table class="adapt-tbl"><tbody>'
                     + ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b in ad) + '</tbody></table>') if ad else '<p class="note">Pas d\'adaptation particulière cette semaine : cadre commun pour tous.</p>') + '</div>')
        o.append('</div></article>')
    o.append('<div class="legend">' + ''.join(f'<span><i style="background:{SPORT[k][0]}"></i>{SPORT[k][1]}</span>' for k in used) + '</div>')
    if p.get('ensuite'): o.append(f'<p class="note">{E(p["ensuite"])}</p>')
    o.append('<p class="note">Une semaine manquée ne se rattrape pas : on reprend le fil.</p>')
    return doc(f"Prévisionnel · {d['titre']}", CSS_SAISON + EXTRA + CSS_FRISE, '\n'.join(o))

# ---------- Fiche individuelle ----------
def fiche(d, links):
    f = d['fiche']; o = []
    if links.get('groupe'): o.append(f'<a href="{links["groupe"]}" class="back">← Groupe Ultra 2027</a>')
    o.append(f'<header><div class="eyebrow">Espace personnel</div><h1 class="title">{E(d["titre"])}</h1><p class="lede">{E(f["objectif"])}</p></header>')
    fr = f.get('frise') or (d.get('gooo') and {'blocs': d['gooo']['blocs'], 'jalons': d['gooo']['jalons']})
    if fr: o.append(frise(fr['blocs'], fr['jalons'], 'Mon année', fr.get('periode') or d.get('gooo', {}).get('periode', '')))
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
    return doc('Mon espace · Team Trail 7C', CSS_FICHE + CSS_FRISE, '\n'.join(o))

# ---------- Accueil du groupe ----------
_sa = CSS_SAISON
CSS_BLOCS = _sa[_sa.find('/* Blocs cartes */'):_sa.find('/* Tableau semaines */')]
CSS_GROUPE = open(f'{D}/css/groupe.css').read() + CSS_BLOCS + CSS_FRISE + '.tg{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:1px 6px;border-radius:3px;color:#fff;background:var(--tc);vertical-align:1px;}'
def groupe(d, links):
    h = d['accueil']; g = d['gooo']; o = []
    o.append(f'''<header><div class="eyebrow">Dossier collectif</div>
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
    o.append(frise(g['blocs'], g['jalons'], "L'année d'un coup d'œil", g.get('periode', '')))
    o.append(f'<section class="sec"><h2>La saison en {len(g["blocs"])} blocs</h2><div class="blocs">')
    for i, b in enumerate(g['blocs'], 1):
        pts = ''.join(f'<li>{E(p)}</li>' for p in b.get('points', []))
        o.append(f'''<article class="blk"><div class="blk-top" style="background:{b['c']}"></div><div class="blk-body">
<div class="blk-h"><h3>{E(b['nom'])}</h3><span class="blk-num">{i:02d}</span></div><p class="dates">{E(b['dates'])} · {E(b['sem'])}</p>
<p><b>Mission :</b> {E(b['mission'])}</p>{f'<ul>{pts}</ul>' if pts else ''}{f'<span class="ms-tag" style="--mc:{b["c"]}">★ {E(b["fin"])}</span>' if b.get('fin') else ''}</div></article>''')
    o.append('</div></section>')
    o.append(f'''<section class="sec"><h2>Les pages du dossier</h2><p class="note">Pages réservées au groupe, accessibles avec ton code.</p><div class="docs">
<a class="doc hero" style="--dc:var(--accent)" href="{links['gooo']}"><h3>GOOO du groupe</h3><p>Le but de chaque semaine, les jalons et les règles communes.</p><span class="arr">→</span></a>
<a class="doc" style="--dc:var(--ok)" href="{links['prev']}"><h3>Prévisionnel</h3><p>Les 4 prochaines semaines : cadre commun + adaptations individuelles.</p><span class="arr">→</span></a></div></section>''')
    return doc(f"{d['titre']} {h['annee']}", CSS_GROUPE, '\n'.join(o))


# ---------- Tableau de bord du coach (généré par l'outil depuis le 16/11/2026) ----------
def hub(groupe, athletes):
    """groupe : [(titre, lien, maj)] ; athletes : [(nom, lien, statut, maj)]"""
    card = lambda t, l, sub: (f'<a class="doc" style="--dc:var(--accent)" href="{l}"><h3>{E(t)}</h3>'
                              f'<p>{E(sub)}</p><span class="arr">→</span></a>')
    o = ['<header><div class="eyebrow">Accès coach</div><h1 class="title">Tableau de <span>bord</span></h1>'
         '<p class="lede">Le groupe, puis chaque athlète : le GOOO et le prévisionnel se trouvent dans leur page. '
         'La date indique la dernière mise à jour de leur plan.</p></header>']
    o.append('<section class="sec"><h2>Groupe Ultra 2027</h2><div class="docs">'
             + ''.join(card(t, l, f'Mis à jour le {m}' if m else '') for t, l, m in groupe) + '</div></section>')
    o.append('<section class="sec"><h2>Athlètes</h2><div class="docs">'
             + ''.join(card(n, l, ' · '.join(x for x in (st, f'mis à jour le {m}' if m else '') if x)) for n, l, st, m in athletes)
             + '</div></section>')
    o.append('<section class="sec"><h2>Cet appareil</h2><p class="note">Si tu as coché « Garder ce code sur cet appareil », il y est enregistré. Ce bouton l\'efface.</p>'
             '<button class="kbtn" id="forget">Oublier ce code sur cet appareil</button></section>')
    o.append("<script>document.getElementById('forget').onclick=function(){try{localStorage.removeItem('cyb-keep');sessionStorage.removeItem('cyb-codes')}catch(e){}location.href='/coaching/#reset'};</script>")
    css = CSS_FICHE + '.kbtn{justify-self:start;font:inherit;font-weight:700;font-size:15px;padding:12px 16px;border:1.5px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer;}.kbtn:hover{background:var(--ink);color:#fff;}'
    return doc('Tableau de bord · Team Trail 7C', css, '\n'.join(o))
