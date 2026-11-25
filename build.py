# Generator stron TECHBET: python build.py
import html, json, os
from PIL import Image

DOM_URL = 'https://techbet.lublin.pl/'
ROK = '2026'
TEL = '573 132 369'
TEL_H = 'tel:+48573132369'
MAIL = 'biuro@techbet.lublin.pl'

def czytaj(p):
    return open(p, encoding='utf8').read()

CSS = (czytaj('_zrodla/style.css').replace('<!--BADGE_STYLE-->', czytaj('badge_style.part').replace('<style>', '').replace('</style>', ''))
       + czytaj('badge_style.part').replace('<style>', '').replace('</style>', '') + czytaj('_zrodla/style_podstrony.css') + czytaj('_zrodla/style_media.css') + czytaj('_zrodla/style_podstrony_media.css'))
BADGE = czytaj('badge_link.part')
e = html.escape

def rozmiar(p):
    return Image.open(p).size

# ---------- dane zdjec ----------
INW = [('i1', 'Konstrukcja żelbetowa', 'Zbrojenie stropu'), ('i2', 'Zbrojenie słupów', 'Prace na wysokości'),
       ('i4', 'Budynek wielokondygnacyjny', 'Dźwigi wieżowe na budowie'), ('i5', 'Szkielet budynku', 'Stan surowy otwarty'),
       ('i6', 'Budynek mieszkalny', 'Elewacja z balkonami'), ('i3', 'Odbiór płyty', 'Ekipa na budowie')]
DOM = [('d1', 'Dom z drewnianą elewacją', 'Stan wykończony'), ('d2', 'Dom z tarasem', 'Bryła z dużymi przeszkleniami'),
       ('d3', 'Dom piętrowy', 'Elewacja z okładziną drewnianą'), ('d4', 'Dom w bieli', 'Prosta, nowoczesna bryła'),
       ('d5', 'Wnętrze domu', 'Salon ze schodami'), ('d6', 'Wnętrze domu', 'Strefa dzienna z kuchnią')]
OPIS = {k: (t, p) for k, t, p in INW + DOM}

# realizacje (poglądowe): typ obiektu, zakres, zdjecia
REAL_INW = [
    ('Budynek wielokondygnacyjny', 'Konstrukcja żelbetowa, stan surowy otwarty', ['i4', 'i5']),
    ('Konstrukcja żelbetowa', 'Zbrojenie i betonowanie słupów oraz stropów', ['i1', 'i2']),
    ('Budynek mieszkalny wielorodzinny', 'Od płyty fundamentowej po elewację', ['i3', 'i6']),
]
REAL_DOM = [
    ('Dom jednorodzinny z drewnianą elewacją', 'Stan deweloperski', ['d1', 'd5']),
    ('Dom z tarasem i dużymi przeszkleniami', 'Stan deweloperski', ['d2', 'd6']),
    ('Dom piętrowy', 'Stan deweloperski', ['d3', 'd4']),
]

def kafle(L, P):
    o = ''
    for k, t, p in L:
        w, h = rozmiar(f'img/{k}-720.webp')
        o += (f'      <article class="kafel"><button data-big="{P}img/{k}-1600.webp" data-opis="{e(t)}" aria-label="Powiększ: {e(t)}">'
              f'<img src="{P}img/{k}-720.webp" width="{w}" height="{h}" loading="lazy" alt="{e(t)} - {e(p.lower())}"></button>'
              f'<h3>{e(t)}</h3><p>{e(p)}</p></article>\n')
    return o

def karty(L, P):
    o = '<div class="realizacje">\n'
    for typ, zakres, zdj in L:
        o += f'  <article class="real">\n    <div class="mini">\n      <div class="tor">'
        for k in zdj:
            w, h = rozmiar(f'img/{k}-720.webp')
            t, p = OPIS[k]
            o += (f'<button data-big="{P}img/{k}-1600.webp" data-opis="{e(typ)} - {e(p.lower())}" aria-label="Powiększ: {e(typ)}">'
                  f'<img src="{P}img/{k}-720.webp" srcset="{P}img/{k}-720.webp 720w, {P}img/{k}-1600.webp 1600w" sizes="(max-width:760px) 92vw, (max-width:1180px) 46vw, 30vw" '
                  f'width="{w}" height="{h}" loading="lazy" alt="{e(typ)} - {e(p.lower())}"></button>')
        o += (f'</div>\n      <span class="licz">1 / {len(zdj)}</span>'
              f'<button class="mp" aria-label="Poprzednie zdjęcie"></button><button class="mn" aria-label="Następne zdjęcie"></button>\n    </div>\n'
              f'    <h3>{e(typ)}</h3>\n    <p>{e(zakres)}</p>\n  </article>\n')
    return o + '</div>'

def srcset(P, n, szer=(640, 1024, 1600, 2000)):
    return ', '.join(f'{P}img/{n}-{s}.webp {s}w' for s in szer)

# ---------- wspolne elementy ----------
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <path id="b-glif" fill-rule="evenodd" d="M48 172H234C277 172 300 195 300 234C300 252 293 264 279 270C294 276 300 290 300 309C300 347 277 368 237 368H48ZM108 212H229C237 212 241 216 241 224V234C241 242 237 246 229 246H108ZM108 290H229C237 290 241 294 241 302V314C241 322 237 326 229 326H108Z"/>
  </defs>
</svg>'''

MENU = [('inwestycje/', 'Inwestycje'), ('domy/', 'Domy'), ('o-firmie/', 'O firmie'), ('kontakt/', 'Kontakt')]

def naglowek(P, akt):
    li = ''
    for h, n in MENU:
        a = ' class="akt" aria-current="page"' if h == akt else ''
        li += f'      <li><a href="{P}{h}"{a}>{n}</a></li>\n'
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="{P or './'}" aria-label="TECHBET - strona główna">
      <svg viewBox="40 90 1070 290" role="img" aria-hidden="true"><rect x="48" y="97" width="233" height="45" fill="#9c9b9b"/><use href="#b-glif" fill="#111213"/><text x="350" y="358" font-family="Archivo,sans-serif" font-size="196" font-weight="400" textLength="745" lengthAdjust="spacingAndGlyphs"><tspan fill="#8a8989">TECH</tspan><tspan fill="#111213">BET</tspan></text></svg>
    </a>
    <ul class="menu" id="menu">
{li}      <li class="tel-m"><a href="{TEL_H}">Biuro: {TEL}</a></li>
    </ul>
    <a class="tel" href="{TEL_H}">{TEL}</a>
    <a class="btn btn-c" href="{P}kontakt/">Zapytaj o wycenę</a>
    <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span></button>
  </div>
</header>'''

def stopka(P):
    return f'''<footer class="stopka">
  <div class="wrap">
    <div>
      <a class="logo" href="{P or './'}" aria-label="TECHBET - strona główna"><svg viewBox="40 90 1070 290" aria-hidden="true"><rect x="48" y="97" width="233" height="45" fill="#9c9b9b"/><use href="#b-glif" fill="#fff"/><text x="350" y="358" font-family="Archivo,sans-serif" font-size="196" font-weight="400" textLength="745" lengthAdjust="spacingAndGlyphs"><tspan fill="#9c9b9b">TECH</tspan><tspan fill="#fff">BET</tspan></text></svg></a>
      <p>Firma budowlana z Lublina. Inwestycje budowlane i domy do stanu deweloperskiego.</p>
    </div>
    <div><h3>Strona</h3><ul><li><a href="{P}inwestycje/">Inwestycje</a></li><li><a href="{P}domy/">Domy</a></li><li><a href="{P}o-firmie/">O firmie</a></li><li><a href="{P}kontakt/">Kontakt</a></li></ul></div>
    <div><h3>Biuro</h3><ul><li><a href="{TEL_H}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
    <div><h3>Adres</h3><p>ul. Mełgiewska 30F<br>20-234 Lublin</p></div>
    <div class="spod"><span>© <span id="rok">{ROK}</span> TECHBET sp. z o.o. <a href="{P}polityka-prywatnosci/">Polityka prywatności</a>. Zdjęcia poglądowe: Unsplash.</span>{BADGE}</div>
  </div>
</footer>

<div class="mob" id="mob"><a href="{TEL_H}">Zadzwoń</a><a href="{P}kontakt/">Zapytaj o wycenę</a></div>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Powiększone zdjęcie">
  <img alt="">
  <p></p>
  <button class="zam" aria-label="Zamknij"></button>
  <button class="pop" aria-label="Poprzednie zdjęcie"></button>
  <button class="nast" aria-label="Następne zdjęcie"></button>
</div>
<script src="{P}app.js" defer></script>'''

FIRMA = {
    '@type': 'GeneralContractor', '@id': DOM_URL + '#firma', 'name': 'TECHBET',
    'legalName': 'TECHBET Spółka z ograniczoną odpowiedzialnością', 'url': DOM_URL,
    'logo': DOM_URL + 'img/logo-192.png', 'image': DOM_URL + 'img/i-hero-1600.webp',
    'description': 'Firma budowlana z Lublina: inwestycje budowlane oraz domy do stanu deweloperskiego. Wykonanie, organizacja budowy i dostawy materiałów.',
    'telephone': '+48573132369', 'email': MAIL,
    'address': {'@type': 'PostalAddress', 'streetAddress': 'ul. Mełgiewska 30F', 'postalCode': '20-234', 'addressLocality': 'Lublin', 'addressCountry': 'PL'},
    'taxID': '9462686367', 'vatID': 'PL9462686367', 'areaServed': 'Lublin',
}

def okruszki_ld(sciezka, nazwa):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Strona główna', 'item': DOM_URL},
        {'@type': 'ListItem', 'position': 2, 'name': nazwa, 'item': DOM_URL + sciezka}]}

def okruszki(P, nazwa):
    return f'<nav class="okr" aria-label="Okruszki"><ol><li><a href="{P}">Strona główna</a></li><li><span aria-current="page">{nazwa}</span></li></ol></nav>'

def strona(sciezka, tytul, opis, akt, tresc, ld, preload='', theme='#ffffff'):
    P = '../' if sciezka else ''
    ldj = json.dumps({'@context': 'https://schema.org', '@graph': ld}, ensure_ascii=False, indent=1)
    doc = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(tytul)}</title>
<meta name="description" content="{e(opis)}">
<meta name="robots" content="noindex, nofollow" data-podglad>
<link rel="canonical" href="{DOM_URL}{sciezka}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{e(tytul)}">
<meta property="og:description" content="{e(opis)}">
<meta property="og:url" content="{DOM_URL}{sciezka}">
<meta property="og:image" content="{DOM_URL}img/i-hero-1600.webp">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="{P}img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{P}img/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="{P}img/apple-touch-icon.png">
<link rel="preload" href="{P}fonts/archivo-rdzen.woff2" as="font" type="font/woff2" crossorigin>
{preload}<style>
{CSS.replace('url(fonts/', 'url(' + P + 'fonts/')}
</style>
<script type="application/ld+json">
{ldj}
</script>
</head>
<body>
{SPRITE}

{naglowek(P, akt)}

<main>
{tresc}
</main>

{stopka(P)}
</body>
</html>
'''
    doc = doc.replace('{P}', P)
    out = os.path.join(sciezka, 'index.html') if sciezka else 'index.html'
    if sciezka:
        os.makedirs(sciezka, exist_ok=True)
    open(out, 'w', encoding='utf8', newline='\n').write(doc)
    print('ok', out, len(doc))

def formularz(P):
    return f'''<form id="form" novalidate>
      <div class="cala"><span class="sr">Czego dotyczy zapytanie</span><div class="wybor" role="radiogroup" aria-label="Czego dotyczy zapytanie"><label><input type="radio" name="typ" value="inwestycja" checked> Inwestycja</label><label><input type="radio" name="typ" value="dom"> Dom</label></div></div>
      <div><label for="f-imie">Imię i nazwisko</label><input id="f-imie" name="imie" autocomplete="name"></div>
      <div><label for="f-tel">Telefon</label><input id="f-tel" name="tel" type="tel" autocomplete="tel"></div>
      <div><label for="f-mail">E-mail</label><input id="f-mail" name="mail" type="email" autocomplete="email"></div>
      <div><label for="f-miejsce">Miejscowość budowy</label><input id="f-miejsce" name="miejsce"></div>
      <div class="cala"><label for="f-wiad">Opis inwestycji lub domu</label><textarea id="f-wiad" name="wiad" placeholder="Rodzaj budynku, powierzchnia, planowany termin"></textarea></div>
      <div class="cala"><label for="f-plik">Projekt lub rysunki (PDF, JPG, PNG, ZIP - opcjonalnie, można kilka plików)</label><input id="f-plik" name="plik" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.zip"></div>
      <div class="cala"><label class="zgoda"><input type="checkbox" name="zgoda" required> <span>Zgadzam się na przetwarzanie moich danych w celu odpowiedzi na zapytanie. Szczegóły w <a href="{P}polityka-prywatnosci/">polityce prywatności</a>.</span></label></div>
      <div class="cala"><button class="btn btn-c" type="submit">Wyślij zapytanie</button></div>
      <p class="cala info wynik" id="wynik" aria-live="polite"></p>
    </form>'''

DANE = f'''<ul class="dane">
        <li><b>Biuro</b><a href="{TEL_H}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><b>Tomasz Kosikowski</b><a href="tel:+48509709840">509 709 840</a><br><a href="mailto:t.kosikowski@techbet.lublin.pl">t.kosikowski@techbet.lublin.pl</a></li>
        <li><b>Adres</b><span>ul. Mełgiewska 30F, 20-234 Lublin</span></li>
      </ul>'''

ZNAK_INW = '<svg viewBox="40 90 270 285" aria-hidden="true"><rect x="48" y="97" width="233" height="45" fill="#9c9b9b"/><use href="#b-glif" fill="#fff"/></svg>'
ZNAK_DOM = '<svg viewBox="40 90 270 285" aria-hidden="true"><rect x="48" y="97" width="233" height="45" fill="#a24f22"/><use href="#b-glif" fill="#111213"/></svg>'

# ================= strona glowna =================
P = ''
glowna = f'''<section class="hero">
  <div class="pas">
    <div class="wrap">
      <h1>Firma budowlana z Lublina&nbsp;- inwestycje i domy do stanu deweloperskiego</h1>
      <p>ul. Mełgiewska 30F, Lublin</p>
    </div>
  </div>
  <div class="drogi">
    <a class="droga d-inw" href="inwestycje/">
      <img src="img/i-hero-1024.webp" srcset="{srcset(P, 'i-hero')}" sizes="(max-width:760px) 100vw, max(50vw, 130vh)" width="2000" height="1334" alt="Budynek w konstrukcji z dźwigami wieżowymi" fetchpriority="high">
      <div class="tresc">
        <div class="znak">{ZNAK_INW}<h2>Inwestycje</h2></div>
        <p>Budynki i obiekty realizowane od organizacji budowy, przez wykonawstwo, po dostawy materiałów.</p>
        <span class="btn btn-b">Zobacz inwestycje <i class="str"></i></span>
      </div>
    </a>
    <a class="droga d-dom" href="domy/">
      <img src="img/d-hero-1024.webp" srcset="{srcset(P, 'd-hero')}" sizes="(max-width:760px) 100vw, max(50vw, 130vh)" width="2000" height="1677" alt="Nowoczesny dom jednorodzinny z drewnianą elewacją" fetchpriority="high">
      <div class="tresc">
        <div class="znak">{ZNAK_DOM}<h2>Domy</h2></div>
        <p>Budujemy domy do stanu deweloperskiego - z wykonaniem, organizacją prac i dostawami materiałów.</p>
        <span class="btn btn-m">Zobacz domy <i class="str"></i></span>
      </div>
    </a>
  </div>
</section>

<section class="sek s-inw">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Inwestycje</h2></div>
      <div>
        <p>Prowadzimy inwestycje budowlane w Lublinie i okolicy. Bierzemy na siebie całą budowę: organizację prac, wykonawstwo i dostawy materiałów, tak żeby inwestor miał jednego partnera od fundamentów po odbiór.</p>
      </div>
    </div>
    <div class="tasma" data-galeria="inw">
{kafle(INW, P)}    </div>
    <div class="nawig"><a class="btn btn-b" href="inwestycje/">Więcej o inwestycjach <i class="str"></i></a><div class="strz"><button class="pop" aria-label="Poprzednie"></button><button class="nast" aria-label="Następne"></button></div></div>
  </div>
</section>

<section class="sek s-dom">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Domy</h2></div>
      <div>
        <p>Budujemy domy do stanu deweloperskiego. Zajmujemy się wykonaniem, organizacją prac i dostawami materiałów - Państwo dostają gotowy budynek i jasny zakres prac już na etapie wyceny.</p>
      </div>
    </div>
    <div class="tasma" data-galeria="dom">
{kafle(DOM, P)}    </div>
    <div class="nawig"><a class="btn btn-m" href="domy/">Więcej o budowie domów <i class="str"></i></a><div class="strz"><button class="pop" aria-label="Poprzednie"></button><button class="nast" aria-label="Następne"></button></div></div>
  </div>
</section>

<section class="sek s-zak">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--czern)"></span><h2>Jak prowadzimy budowę</h2></div>
      <div>
        <p>TECHBET to firma budowlana z siedzibą przy ul. Mełgiewskiej w Lublinie. Inwestycje i domy prowadzimy tak samo: jeden wykonawca, jedna osoba odpowiedzialna za budowę i zakres prac ustalony przed startem.</p>
        <p><a class="btn btn-c" href="o-firmie/">O firmie <i class="str"></i></a></p>
      </div>
    </div>
    <div class="trzy">
      <div><h3>Kompleksowe wykonanie</h3><p>Od fundamentów po stan deweloperski - wszystkie etapy budowy w jednych rękach.</p></div>
      <div><h3>Organizacja budowy</h3><p>Harmonogram, ekipy i dostawy materiałów planujemy sami, żeby budowa nie stała.</p></div>
      <div><h3>Jasny zakres prac</h3><p>Przed podpisaniem umowy wiadomo, co dokładnie wykonujemy i co jest w cenie.</p></div>
    </div>
  </div>
</section>

<section class="s-dron">
  <div class="dron">
    <figure><button data-big="img/i3-1600.webp" data-opis="Budowa z góry" aria-label="Powiększ zdjęcie budowy z góry"><img src="img/i3-1600.webp" srcset="img/i3-720.webp 720w, img/i3-1600.webp 1600w" sizes="(max-width:900px) 100vw, 58vw" width="1600" height="1067" loading="lazy" alt="Ekipa budowy na płycie fundamentowej, widok z góry"></button></figure>
    <div class="opis">
      <span class="belka"></span>
      <h2>Nasze budowy z lotu ptaka</h2>
      <p>Kierownik budowy fotografuje nasze realizacje dronem. W portfolio każda inwestycja i każdy dom mogą mieć zdjęcia z góry - widać skalę, postęp prac i jakość wykonania.</p>
    </div>
  </div>
</section>

<section class="sek s-kon">
  <div class="wrap kon">
    <div>
      <span class="belka"></span>
      <h2>Porozmawiajmy o budowie</h2>
      <p>Prześlij projekt albo opisz inwestycję - odpowiemy z wyceną i zakresem prac.</p>
      {DANE}
    </div>
    {formularz(P)}
  </div>
</section>'''

strona('', 'TECHBET Lublin - inwestycje budowlane i domy do stanu deweloperskiego',
       'TECHBET, firma budowlana z Lublina: inwestycje budowlane oraz domy do stanu deweloperskiego. Wykonanie, organizacja budowy i dostawy materiałów.',
       '', glowna,
       [dict(FIRMA), {'@type': 'WebSite', '@id': DOM_URL + '#strona', 'url': DOM_URL, 'name': 'TECHBET', 'inLanguage': 'pl-PL', 'publisher': {'@id': DOM_URL + '#firma'}}],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, "i-hero")}" imagesizes="(max-width:760px) 100vw, max(50vw, 130vh)" fetchpriority="high">\n',
       theme='#111213')

# ================= inwestycje =================
P = '../'
inw = f'''<section class="ph ph-inw">
  <div class="tx">
    {okruszki(P, 'Inwestycje')}
    <span class="belka"></span>
    <h1>Inwestycje budowlane w Lublinie</h1>
    <p class="lead">Prowadzimy budowy od organizacji placu i harmonogramu, przez wykonawstwo, po dostawy materiałów. Inwestor ma po naszej stronie jednego wykonawcę i jedną osobę odpowiedzialną za budowę.</p>
    <a class="btn btn-b" href="{P}kontakt/?typ=inwestycja">Zapytaj o wycenę inwestycji <i class="str"></i></a>
  </div>
  <figure><img src="{P}img/i-hero-1024.webp" srcset="{srcset(P, 'i-hero')}" sizes="(max-width:760px) 150vh, max(59vw, 140vh)" width="2000" height="1334" alt="Budynek w konstrukcji z dźwigami wieżowymi" fetchpriority="high"></figure>
</section>

<section class="sek s-bia">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--czern)"></span><h2>Zakres prac</h2></div>
      <p>Przy inwestycji bierzemy na siebie te elementy, które najczęściej decydują o terminie i koszcie budowy. Zakres dla konkretnego obiektu ustalamy przed podpisaniem umowy.</p>
    </div>
    <ul class="wiersze">
      <li><h3>Organizacja budowy</h3><p>Przygotowanie placu budowy, harmonogram prac i koordynacja ekip na kolejnych etapach.</p></li>
      <li><h3>Wykonawstwo</h3><p>Roboty budowlane od fundamentów i konstrukcji po stan, który został ustalony w umowie.</p></li>
      <li><h3>Dostawy materiałów</h3><p>Zamawiamy i dowozimy materiały w rytmie budowy, tak żeby prace nie czekały na dostawy.</p></li>
      <li><h3>Jeden partner</h3><p>Inwestor rozmawia z jednym wykonawcą, a nie z kilkoma firmami naraz.</p></li>
    </ul>
  </div>
</section>

<section class="sek s-inw">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Realizacje</h2></div>
      <p>Wybrane inwestycje prowadzone przez TECHBET. Zdjęcia w każdej karcie można przesuwać palcem albo myszą, a po kliknięciu powiększyć.</p>
    </div>
    {karty(REAL_INW, P)}
    <p class="uwaga">Zdjęcia poglądowe - zostaną zastąpione zdjęciami z realizacji TECHBET, także ujęciami z drona.</p>
  </div>
</section>

<section class="sek s-jas">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--czern)"></span><h2>Jak prowadzimy inwestycję</h2></div>
      <p>Każda budowa ma swój harmonogram, ale kolejność kroków jest zawsze podobna.</p>
    </div>
    <ol class="etapy">
      <li><span class="nr">01</span><h3>Zapytanie i dokumentacja</h3><p>Przesyłają nam Państwo projekt albo opis inwestycji.</p></li>
      <li><span class="nr">02</span><h3>Wycena i zakres</h3><p>Ustalamy, co dokładnie wykonujemy, w jakim terminie i za jaką kwotę.</p></li>
      <li><span class="nr">03</span><h3>Umowa i harmonogram</h3><p>Zakres i terminy zapisujemy w umowie, planujemy ekipy i dostawy.</p></li>
      <li><span class="nr">04</span><h3>Budowa</h3><p>Prowadzimy prace etapami, z jedną osobą odpowiedzialną za budowę.</p></li>
      <li><span class="nr">05</span><h3>Zdjęcia z postępu</h3><p>Kierownik budowy fotografuje realizację, także dronem.</p></li>
      <li><span class="nr">06</span><h3>Odbiór</h3><p>Przekazujemy obiekt w stanie ustalonym w umowie.</p></li>
    </ol>
  </div>
</section>

<section class="sek s-bia cta">
  <div class="wrap">
    <div><span class="belka"></span><h2>Planują Państwo inwestycję?</h2></div>
    <div><p>Prześlij projekt albo opisz obiekt - odpowiemy z wyceną i zakresem prac.</p><a class="btn btn-c" href="{P}kontakt/?typ=inwestycja">Zapytaj o wycenę <i class="str"></i></a></div>
  </div>
</section>'''

strona('inwestycje/', 'Inwestycje budowlane Lublin - TECHBET',
       'Inwestycje budowlane w Lublinie: organizacja budowy, wykonawstwo i dostawy materiałów. Realizacje TECHBET i zapytanie o wycenę.',
       'inwestycje/', inw,
       [okruszki_ld('inwestycje/', 'Inwestycje'),
        {'@type': 'Service', 'name': 'Inwestycje budowlane', 'serviceType': 'Generalne wykonawstwo inwestycji budowlanych', 'areaServed': 'Lublin', 'provider': {'@id': DOM_URL + '#firma'}, 'url': DOM_URL + 'inwestycje/'},
        dict(FIRMA)],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, "i-hero")}" imagesizes="(max-width:760px) 150vh, max(59vw, 140vh)" fetchpriority="high">\n',
       theme='#111213')

# ================= domy =================
domy = f'''<section class="ph ph-dom">
  <div class="tx">
    {okruszki(P, 'Domy')}
    <span class="belka"></span>
    <h1>Domy do stanu deweloperskiego&nbsp;- Lublin i&nbsp;okolice</h1>
    <p class="lead">Budujemy domy jednorodzinne do stanu deweloperskiego. Zajmujemy się wykonaniem, organizacją prac i dostawami materiałów, a zakres prac jest jasny już na etapie wyceny.</p>
    <a class="btn btn-m" href="{P}kontakt/?typ=dom">Prześlij projekt do wyceny <i class="str"></i></a>
  </div>
  <figure><img src="{P}img/d-hero-1024.webp" srcset="{srcset(P, 'd-hero')}" sizes="(max-width:760px) 120vh, max(59vw, 120vh)" width="2000" height="1677" alt="Nowoczesny dom jednorodzinny z drewnianą elewacją" fetchpriority="high"></figure>
</section>

<section class="sek s-bia">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--miedz)"></span><h2>Co obejmuje stan deweloperski</h2></div>
      <p>Stan deweloperski to dom gotowy do prac wykończeniowych. Poniżej typowy zakres - dokładną listę prac dla Państwa projektu ustalamy przy wycenie i zapisujemy w umowie.</p>
    </div>
    <ul class="wiersze">
      <li><h3>Stan zero</h3><p>Roboty ziemne, fundamenty albo płyta fundamentowa, izolacje przeciwwilgociowe i kanalizacja pod posadzką.</p></li>
      <li><h3>Stan surowy otwarty</h3><p>Ściany nośne i działowe, stropy, schody konstrukcyjne, kominy, więźba dachowa.</p></li>
      <li><h3>Stan surowy zamknięty</h3><p>Pokrycie dachu, okna, drzwi zewnętrzne i brama garażowa.</p></li>
      <li><h3>Instalacje</h3><p>Instalacja elektryczna, wodno-kanalizacyjna, grzewcza i wentylacja - bez osprzętu i armatury.</p></li>
      <li><h3>Prace wewnętrzne</h3><p>Tynki ścian i sufitów, wylewki, ocieplenie poddasza.</p></li>
      <li><h3>Elewacja</h3><p>Ocieplenie ścian zewnętrznych i tynk elewacyjny albo okładzina według projektu.</p></li>
    </ul>
  </div>
</section>

<section class="sek s-dom">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Zbudowane domy</h2></div>
      <p>Domy zbudowane przez TECHBET. Zdjęcia w każdej karcie można przesuwać palcem albo myszą, a po kliknięciu powiększyć.</p>
    </div>
    {karty(REAL_DOM, P)}
    <p class="uwaga">Zdjęcia poglądowe - zostaną zastąpione zdjęciami domów zbudowanych przez TECHBET, także ujęciami z drona.</p>
  </div>
</section>

<section class="sek s-bia">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--miedz)"></span><h2>Etapy budowy domu</h2></div>
      <p>Od przesłania projektu do odbioru domu gotowego do wykończenia.</p>
    </div>
    <ol class="etapy e-dom">
      <li><span class="nr">01</span><h3>Projekt do wyceny</h3><p>Przesyłają nam Państwo projekt domu - wystarczy formularz na stronie.</p></li>
      <li><span class="nr">02</span><h3>Wycena i zakres prac</h3><p>Przygotowujemy wycenę z wyraźnym zakresem: co jest w cenie, a co nie.</p></li>
      <li><span class="nr">03</span><h3>Umowa i harmonogram</h3><p>Ustalamy terminy kolejnych etapów i dostaw materiałów.</p></li>
      <li><span class="nr">04</span><h3>Stan surowy</h3><p>Fundamenty, ściany, stropy i dach - dom zamknięty przed zimą i deszczem.</p></li>
      <li><span class="nr">05</span><h3>Instalacje i tynki</h3><p>Instalacje, tynki, wylewki i elewacja według ustalonego zakresu.</p></li>
      <li><span class="nr">06</span><h3>Odbiór stanu deweloperskiego</h3><p>Przekazujemy dom gotowy do prac wykończeniowych.</p></li>
    </ol>
  </div>
</section>

<section class="sek s-jas cta cta-dom">
  <div class="wrap">
    <div><span class="belka"></span><h2>Mają Państwo projekt domu?</h2></div>
    <div><p>Prześlij go do wyceny - odpowiemy z zakresem prac i terminem.</p><a class="btn btn-m" href="{P}kontakt/?typ=dom">Prześlij projekt do wyceny <i class="str"></i></a></div>
  </div>
</section>'''

strona('domy/', 'Domy do stanu deweloperskiego Lublin - TECHBET',
       'Budowa domów do stanu deweloperskiego w Lublinie i okolicy: zakres prac, etapy budowy i realizacje. Prześlij projekt domu do wyceny.',
       'domy/', domy,
       [okruszki_ld('domy/', 'Domy'),
        {'@type': 'Service', 'name': 'Budowa domów do stanu deweloperskiego', 'serviceType': 'Budowa domów jednorodzinnych', 'areaServed': 'Lublin', 'provider': {'@id': DOM_URL + '#firma'}, 'url': DOM_URL + 'domy/'},
        dict(FIRMA)],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, "d-hero")}" imagesizes="(max-width:760px) 120vh, max(59vw, 120vh)" fetchpriority="high">\n',
       theme='#f5f0e8')

# ================= o firmie =================
w3, h3 = rozmiar('img/i3-1600.webp')
ofirmie = f'''<section class="ph ph-inw">
  <div class="tx">
    {okruszki(P, 'O firmie')}
    <span class="belka"></span>
    <h1>O firmie TECHBET</h1>
    <p class="lead">TECHBET to firma budowlana z Lublina, z siedzibą przy ul. Mełgiewskiej 30F. Prowadzimy inwestycje budowlane i budujemy domy do stanu deweloperskiego.</p>
    <a class="btn btn-b" href="{P}kontakt/">Kontakt z biurem <i class="str"></i></a>
  </div>
  <figure><img src="{P}img/i3-1600.webp" srcset="{P}img/i3-720.webp 720w, {P}img/i3-1600.webp 1600w" sizes="(max-width:760px) 150vh, max(59vw, 140vh)" width="{w3}" height="{h3}" alt="Ekipa budowy na płycie fundamentowej, widok z góry" fetchpriority="high"></figure>
</section>

<section class="sek s-bia">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--czern)"></span><h2>Jedna firma, dwie drogi</h2></div>
      <p>Znak TECHBET to litera B z belką nad nią - jak strop nad ścianą. Pod tym samym znakiem prowadzimy dwa rodzaje budów: większe inwestycje i domy jednorodzinne.</p>
    </div>
    <div class="dwie">
      <a class="di" href="{P}inwestycje/"><img src="{P}img/i4-1600.webp" srcset="{P}img/i4-720.webp 720w, {P}img/i4-1600.webp 1600w" sizes="(max-width:760px) 92vw, 46vw" width="1600" height="1067" loading="lazy" alt="Budynek wielokondygnacyjny z dźwigami wieżowymi"><div class="w"><h3>Inwestycje</h3><p>Organizacja budowy, wykonawstwo i dostawy materiałów.</p><span class="btn btn-b">Inwestycje <i class="str"></i></span></div></a>
      <a class="dd" href="{P}domy/"><img src="{P}img/d2-1600.webp" srcset="{P}img/d2-720.webp 720w, {P}img/d2-1600.webp 1600w" sizes="(max-width:760px) 92vw, 46vw" width="1600" height="1067" loading="lazy" alt="Dom jednorodzinny z tarasem"><div class="w"><h3>Domy</h3><p>Domy jednorodzinne do stanu deweloperskiego.</p><span class="btn btn-m">Domy <i class="str"></i></span></div></a>
    </div>
  </div>
</section>

<section class="sek s-jas">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka" style="background:var(--czern)"></span><h2>Jak pracujemy</h2></div>
      <p>Inwestycje i domy prowadzimy tak samo: jeden wykonawca, jedna osoba odpowiedzialna za budowę i zakres prac ustalony przed startem.</p>
    </div>
    <div class="trzy">
      <div><h3>Kompleksowe wykonanie</h3><p>Od fundamentów po stan deweloperski - wszystkie etapy budowy w jednych rękach.</p></div>
      <div><h3>Organizacja budowy</h3><p>Harmonogram, ekipy i dostawy materiałów planujemy sami, żeby budowa nie stała.</p></div>
      <div><h3>Jasny zakres prac</h3><p>Przed podpisaniem umowy wiadomo, co dokładnie wykonujemy i co jest w cenie.</p></div>
    </div>
  </div>
</section>

<section class="sek s-bia">
  <div class="wrap kon">
    <div>
      <span class="belka" style="background:var(--czern)"></span>
      <h2>Budowy z lotu ptaka</h2>
      <div class="tekst"><p>Kierownik budowy fotografuje nasze realizacje dronem. Dzięki temu przy każdej inwestycji i każdym domu w portfolio można pokazać zdjęcia z góry - skalę budowy, postęp prac i jakość wykonania.</p></div>
    </div>
    <div>
      <h2 class="sr">Dane firmy</h2>
      <table class="rej">
        <tr><th scope="row">Nazwa</th><td>TECHBET Spółka z ograniczoną odpowiedzialnością</td></tr>
        <tr><th scope="row">Adres</th><td>ul. Mełgiewska 30F, 20-234 Lublin</td></tr>
        <tr><th scope="row">KRS</th><td>0000770226</td></tr>
        <tr><th scope="row">NIP</th><td>946-268-63-67</td></tr>
        <tr><th scope="row">REGON</th><td>382493630</td></tr>
        <tr><th scope="row">Biuro</th><td><a href="{TEL_H}">{TEL}</a>, <a href="mailto:{MAIL}">{MAIL}</a></td></tr>
      </table>
    </div>
  </div>
</section>'''

strona('o-firmie/', 'O firmie - TECHBET, firma budowlana z Lublina',
       'TECHBET sp. z o.o. z Lublina: inwestycje budowlane i domy do stanu deweloperskiego. Jak pracujemy, dane firmy i kontakt.',
       'o-firmie/', ofirmie,
       [okruszki_ld('o-firmie/', 'O firmie'), {'@type': 'AboutPage', 'url': DOM_URL + 'o-firmie/', 'name': 'O firmie TECHBET', 'about': {'@id': DOM_URL + '#firma'}}, dict(FIRMA)],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{P}img/i3-720.webp 720w, {P}img/i3-1600.webp 1600w" imagesizes="(max-width:760px) 150vh, max(59vw, 140vh)" fetchpriority="high">\n',
       theme='#111213')

# ================= kontakt =================
MAPA = 'https://www.google.com/maps?q=Me%C5%82giewska+30F,+20-234+Lublin&hl=pl&z=15&output=embed'
kontakt = f'''<section class="pn">
  <div class="wrap">
    {okruszki(P, 'Kontakt')}
    <span class="belka"></span>
    <h1>Kontakt - TECHBET Lublin</h1>
    <p class="lead">Prześlij projekt albo opisz inwestycję lub dom - odpowiemy z wyceną i zakresem prac.</p>
  </div>
</section>

<section class="sek s-kon kontakt">
  <div class="wrap kon">
    <div>
      {DANE.replace('class="dane"', 'class="dane" style="margin-top:0"')}
      <table class="rej" style="margin-top:36px">
        <tr><th scope="row">Firma</th><td>TECHBET sp. z o.o.</td></tr>
        <tr><th scope="row">KRS</th><td>0000770226</td></tr>
        <tr><th scope="row">NIP</th><td>946-268-63-67</td></tr>
        <tr><th scope="row">REGON</th><td>382493630</td></tr>
      </table>
    </div>
    {formularz(P)}
  </div>
</section>

<section class="mapa" aria-label="Mapa dojazdu">
  <iframe src="{MAPA}" title="Mapa: TECHBET, ul. Mełgiewska 30F, Lublin" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  <div class="wrap dojazd">ul. Mełgiewska 30F, 20-234 Lublin</div>
</section>'''

strona('kontakt/', 'Kontakt - TECHBET Lublin, ul. Mełgiewska 30F',
       'Kontakt z firmą budowlaną TECHBET z Lublina: biuro 573 132 369, biuro@techbet.lublin.pl, ul. Mełgiewska 30F. Formularz zapytania z możliwością dołączenia projektu.',
       'kontakt/', kontakt,
       [okruszki_ld('kontakt/', 'Kontakt'), {'@type': 'ContactPage', 'url': DOM_URL + 'kontakt/', 'name': 'Kontakt - TECHBET', 'about': {'@id': DOM_URL + '#firma'}}, dict(FIRMA)])

# ================= polityka prywatnosci =================
polityka = f'''<section class="pn">
  <div class="wrap">
    {okruszki(P, 'Polityka prywatności')}
    <span class="belka"></span>
    <h1>Polityka prywatności</h1>
    <p class="lead">Jak TECHBET sp. z o.o. przetwarza dane osób, które kontaktują się z firmą przez stronę techbet.lublin.pl.</p>
  </div>
</section>

<section class="wrap polityka">
  <h2>Administrator danych</h2>
  <p>Administratorem danych osobowych jest TECHBET Spółka z ograniczoną odpowiedzialnością z siedzibą w Lublinie, ul. Mełgiewska 30F, 20-234 Lublin, KRS 0000770226, NIP 946-268-63-67. Kontakt w sprawie danych: <a href="mailto:{MAIL}">{MAIL}</a>, tel. {TEL}.</p>

  <h2>Jakie dane i w jakim celu</h2>
  <p>Przez formularz zapytania zbieramy dane, które Pan lub Pani wpisze: imię i nazwisko, telefon, adres e-mail, miejscowość budowy, opis inwestycji oraz dołączone pliki (np. projekt). Wykorzystujemy je wyłącznie po to, żeby odpowiedzieć na zapytanie i przygotować wycenę.</p>
  <p>Jeśli kontaktuje się Pan lub Pani z nami telefonicznie albo mailowo, przetwarzamy dane podane w tej korespondencji w tym samym celu.</p>

  <h2>Podstawa prawna</h2>
  <ul>
    <li>art. 6 ust. 1 lit. b RODO - działania przed zawarciem umowy na prośbę osoby, której dane dotyczą (wycena, oferta),</li>
    <li>art. 6 ust. 1 lit. f RODO - prawnie uzasadniony interes administratora, czyli prowadzenie korespondencji i ewentualne dochodzenie roszczeń.</li>
  </ul>

  <h2>Jak długo przechowujemy dane</h2>
  <p>Dane z zapytania przechowujemy przez czas potrzebny do odpowiedzi i rozmów o wycenie, a jeśli dojdzie do zawarcia umowy - przez czas jej realizacji i okres wymagany przepisami (np. podatkowymi) lub do przedawnienia roszczeń.</p>

  <h2>Odbiorcy danych</h2>
  <p>Dane mogą być przekazywane wyłącznie podmiotom, które obsługują techniczną stronę naszej działalności (dostawca hostingu i poczty e-mail), na podstawie umów powierzenia. Nie sprzedajemy danych i nie przekazujemy ich w celach marketingowych.</p>

  <h2>Prawa osoby, której dane dotyczą</h2>
  <p>Ma Pan lub Pani prawo dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przeniesienia oraz prawo sprzeciwu. Przysługuje też prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych (ul. Stawki 2, 00-193 Warszawa). Podanie danych jest dobrowolne, ale bez danych kontaktowych nie odpowiemy na zapytanie.</p>

  <h2>Pliki cookies i mapa</h2>
  <p>Strona nie używa plików cookies do statystyk ani reklam. Na podstronie Kontakt wyświetlana jest mapa Google Maps - jej dostawca, Google Ireland Limited, może przy tym zapisywać własne pliki cookies i przetwarzać adres IP zgodnie z <a href="https://policies.google.com/privacy?hl=pl" rel="noopener">polityką prywatności Google</a>.</p>

  <h2>Zmiany polityki</h2>
  <p>Polityka może być aktualizowana, np. przy zmianie usług na stronie. Aktualna wersja jest zawsze dostępna na tej podstronie.</p>
</section>'''

strona('polityka-prywatnosci/', 'Polityka prywatności - TECHBET Lublin',
       'Polityka prywatności strony techbet.lublin.pl: administrator danych TECHBET sp. z o.o., cel przetwarzania danych z formularza, prawa osób, pliki cookies.',
       '', polityka,
       [okruszki_ld('polityka-prywatnosci/', 'Polityka prywatności'), {'@type': 'WebPage', 'url': DOM_URL + 'polityka-prywatnosci/', 'name': 'Polityka prywatności'}, dict(FIRMA)])

# ================= sitemap, llms =================
adresy = ['', 'inwestycje/', 'domy/', 'o-firmie/', 'kontakt/', 'polityka-prywatnosci/']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for a in adresy:
    sm += f'  <url><loc>{DOM_URL}{a}</loc></url>\n'
open('sitemap.xml', 'w', encoding='utf8', newline='\n').write(sm + '</urlset>\n')

open('llms.txt', 'w', encoding='utf8', newline='\n').write(f'''# TECHBET sp. z o.o. - firma budowlana, Lublin

> TECHBET to firma budowlana z Lublina (ul. Mełgiewska 30F, 20-234 Lublin). Prowadzi inwestycje budowlane oraz buduje domy jednorodzinne do stanu deweloperskiego: wykonanie, organizacja budowy i dostawy materiałów.

## Oferta
- [Inwestycje]({DOM_URL}inwestycje/): organizacja budowy, wykonawstwo i dostawy materiałów przy inwestycjach budowlanych.
- [Domy]({DOM_URL}domy/): budowa domów do stanu deweloperskiego, zakres prac i etapy budowy.

## Firma
- [O firmie]({DOM_URL}o-firmie/): sposób pracy i dane rejestrowe (KRS 0000770226, NIP 946-268-63-67).
- [Kontakt]({DOM_URL}kontakt/): biuro tel. {TEL}, {MAIL}; formularz zapytania z możliwością dołączenia projektu.
''')
print('sitemap, llms ok')
