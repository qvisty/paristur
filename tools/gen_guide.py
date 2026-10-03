#!/usr/bin/env python3
# Genererer guide.html (printbar rejseguide) ud fra sitets sider. Køres fra repo-roden.
import re

PAGES = [
 ('index.html',      '🏠', 'Basen & tjeklisten'),
 ('kvarteret.html',  '📍', 'Kvarteret'),
 ('oplevelser.html', '🎡', 'Mathildes ønskeseddel & oplevelser'),
 ('spisesteder.html','🍽️', 'Spisesteder & små perler'),
 ('dagsplaner.html', '📅', 'Dagsplaner'),
 ('parloer.html',    '🗣️', 'Parlør'),
 ('praktisk.html',   '🧳', 'Praktisk'),
]

def extract(fn):
    s = open(fn).read()
    m = re.search(r'</nav>\s*<div class="wrap">(.*?)\n</div>\s*<footer', s, re.S)
    assert m, fn
    c = m.group(1)
    c = re.sub(r'<section>\s*<h2>🗺️ Kortet[^<]*</h2>.*?</section>', '', c, flags=re.S)
    c = re.sub(r'<section>\s*<h2>🗺️ Kvarteret omkring jer</h2>.*?</section>', '', c, flags=re.S)
    c = re.sub(r'<div class="quick">.*?</div>\s*', '', c, count=1, flags=re.S)
    c = re.sub(r'<section>\s*<h2>📚 Ferie-hjælperens sider</h2>.*?</section>', '', c, flags=re.S)
    # Overskrift og underrubrik må ikke skilles ad af et sideskift.
    c = re.sub(r'(<h2>[^<]*</h2>)\s*(<p class="sub">.*?</p>)', r'<div class="h2wrap">\1\2</div>', c, flags=re.S)
    c = re.sub(r'(<h2>[^<]*</h2>)(?!</div>)', r'<div class="h2wrap">\1</div>', c)
    return c.strip()

chapters, toc = [], []
for i, (fn, ic, titel) in enumerate(PAGES, 1):
    chapters.append(f'''<section class="chapter" id="kap{i}">
<div class="chaphead"><span class="chapnum">Kapitel {i}</span><h1>{ic} {titel}</h1></div>
{extract(fn)}
</section>''')
    toc.append(f'<li><a href="#kap{i}">{ic} {titel}</a></li>')

base_css = re.search(r'<style>(.*?)</style>', open('index.html').read(), re.S).group(1)
opl_css = re.search(r'<style>.*?(  \.wish\{.*?)\n  /\* ---------- mobil', open('oplevelser.html').read(), re.S).group(1)
spis_css = re.search(r'(  \.rest\{.*?\.gem\{[^}]*\})', open('spisesteder.html').read(), re.S).group(1)
parl_css = re.search(r'(  \.parl\{.*?)\n  @media print', open('parloer.html').read(), re.S).group(1)

GUIDE_CSS = '''
  .toolbar{position:sticky;top:0;z-index:100;background:var(--navy);color:#fff;padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
  .toolbar .btn{border:none;cursor:pointer;font-size:15px}
  .toolbar span{font-size:13.5px;color:#cfd5e6}
  .cover{min-height:88vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:linear-gradient(135deg,var(--navy),var(--navy2));color:#fff;border-radius:0 0 18px 18px;padding:40px 20px}
  .cover img{width:130px;height:130px;border-radius:26px;margin-bottom:26px}
  .cover h1{font-size:clamp(30px,5vw,46px);margin:0 0 10px}
  .cover p{font-size:17px;color:#d8dceb;margin:5px 0;max-width:560px}
  .cover .facts{justify-content:center;margin-top:22px}
  .tocpage{max-width:700px;margin:0 auto;padding:44px 20px}
  .tocpage h2{font-size:26px}
  .tocpage ol{font-size:17px;line-height:2.1;padding-left:26px}
  .tocpage a{text-decoration:none;color:var(--ink)}
  .chapter{max-width:1000px;margin:0 auto;padding:30px 18px;border-top:4px solid var(--line)}
  .chaphead{margin-bottom:8px}
  .chapnum{font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);font-weight:700}
  .chaphead h1{margin:2px 0 0;color:var(--navy);font-size:30px}
  @media print{
    @page{margin:14mm 12mm}
    body{background:#fff !important;padding-bottom:0 !important;font-size:12px}
    .toolbar,.tabbar{display:none !important}
    .cover{min-height:auto;height:250mm;border-radius:0;break-after:page;
      background:var(--navy) !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
    .tocpage{break-after:page}
    .chapter{break-before:page;border-top:none;padding:0 0 20px;max-width:none}
    .chapter:first-of-type{break-before:page}
    h2{break-after:avoid}
    h2,h3,h4{page-break-after:avoid}
    section{padding:14px 0 4px}
    .rec,.rest,.wish,.panel,.pcard,.callout,figure,.step,.imgs{break-inside:avoid;page-break-inside:avoid}
    .chk{break-inside:auto;page-break-inside:auto}
    .chk label{break-inside:avoid;page-break-inside:avoid}
    .day{break-inside:auto;page-break-inside:auto}
    .day .dhead{break-after:avoid-page;page-break-after:avoid}
    .h2wrap{break-inside:avoid;page-break-inside:avoid;break-after:avoid-page;page-break-after:avoid}
    .day .dhead{-webkit-print-color-adjust:exact;print-color-adjust:exact}
    .chapnum,.badge{-webkit-print-color-adjust:exact;print-color-adjust:exact}
    .wbtns,.lnk{display:none !important}
    a{color:inherit;text-decoration:none}
    .recs{grid-template-columns:1fr 1fr;gap:10px}
    .grid2{grid-template-columns:1fr 1fr;gap:10px}
    .tablewrap{overflow:visible;border:1px solid var(--line)}
    table{min-width:0;font-size:11px}
    .imgs{height:150px !important}
    #map,.bigmap,.legend{display:none !important}
  }
'''

html = f'''<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mathildes Paris-tur · rejseguide</title>
<meta name="description" content="Samlet, printbar rejseguide for Mathildes Paris-tur 6.-9. oktober 2026.">
<style>{base_css}
{opl_css}
{spis_css}
{parl_css}
{GUIDE_CSS}</style>
</head>
<body>
<div class="toolbar">
  <button class="btn" onclick="window.print()">🖨️ Print guiden / Gem som PDF</button>
  <span>Hele sitet samlet som rejseguide med sideskift pr. kapitel. Kort og knapper udelades automatisk på papir.</span>
  <a class="btn ghost" style="color:#fff;border-color:#fff;margin-left:auto" href="index.html">← Tilbage</a>
</div>

<div class="cover">
  <img src="img/icon-192.png" alt="">
  <h1>Mathildes Paris-tur</h1>
  <p><strong>Rejseguiden — planlagt efter Mathildes ønskeseddel</strong> · 6.–9. oktober 2026 · 3 voksne</p>
  <p>Basen: 67 Boulevard Richard-Lenoir, lejl. 45, 75011 Paris (11. arr.)<br>Vært: Antoine &amp; France · Indtjek kl. 15 · udtjek kl. 12</p>
  <p>✈️ Lander CDG tirsdag kl. 13.45 · 🛫 hjemrejse fredag kl. 20.40</p>
  <div class="facts"><span class="fact">🚇 Metro Richard-Lenoir (linje 5) — 1 minut fra døren</span></div>
</div>

<div class="tocpage">
  <h2>Indhold</h2>
  <ol>
{chr(10).join('    ' + t for t in toc)}
  </ol>
  <p class="small">Printet fra ferie-hjælperen på qvisty.github.io/paristur — dobbelttjek åbningstider og priser online.</p>
</div>

{chr(10).join(chapters)}

<footer><div class="wrap"><p>Mathildes Paris-tur · 67 Bd Richard-Lenoir · god tur! 🗼</p></div></footer>
</body>
</html>
'''
open('guide.html', 'w').write(html)
print('guide.html skrevet,', len(html), 'tegn')
