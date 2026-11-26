# Generator stron TECHBET: python build.py
import html, json, os
from PIL import Image

DOM_URL = 'https://techbet.lublin.pl/'
ROK = '2026'
TEL = '573 132 369'
TEL_H = 'tel:+48573132369'
MAIL = 'biuro@techbet.lublin.pl'
# wizytowka firmy w Google Maps (TECHBET - KONSTRUKCJE ZELBETOWE)
GMAPS_CID = '6404524912836694314'
GMAPS_LINK = f'https://maps.google.com/?cid={GMAPS_CID}'
GMAPS_EMBED = f'https://maps.google.com/maps?cid={GMAPS_CID}&hl=pl&output=embed'

def czytaj(p):
    return open(p, encoding='utf8').read()

BADGE_CSS = czytaj('badge_style.part').replace('<style>', '').replace('</style>', '')
CSS = czytaj('_zrodla/style.css') + BADGE_CSS + czytaj('_zrodla/style_media.css')
BADGE = czytaj('badge_link.part')
e = html.escape

def rozmiar(p):
    return Image.open(p).size

# ---------- zdjecia (poglądowe, do wymiany na zdjecia TECHBET) ----------
INW = {'n1': 'Zbrojenie ścian i słupów', 'n2': 'Szalunki i słupy żelbetowe', 'n3': 'Konstrukcja żelbetowa budynku',
       'n4': 'Budynek w stanie surowym', 'n5': 'Budowa z dźwigiem wieżowym', 'n6': 'Budynek wielorodzinny w budowie'}
DOM = {'d1': 'Dom z drewnianą elewacją', 'd2': 'Dom z tarasem i przeszkleniami', 'd3': 'Dom piętrowy',
       'd4': 'Dom w bieli', 'd5': 'Wnętrze domu - salon ze schodami', 'd6': 'Wnętrze domu - strefa dzienna'}

REAL_INW = [
    ('Budynek mieszkalny wielorodzinny', 'Konstrukcja żelbetowa, stan surowy', ['n6', 'n5']),
    ('Konstrukcja żelbetowa', 'Zbrojenie, szalunki i betonowanie słupów oraz stropów', ['n2', 'n1']),
    ('Budynek usługowo-mieszkalny', 'Od fundamentów po stan surowy zamknięty', ['n3', 'n4']),
]
REAL_DOM = [
    ('Dom jednorodzinny z drewnianą elewacją', 'Stan deweloperski', ['d1', 'd5']),
    ('Dom z tarasem i dużymi przeszkleniami', 'Stan deweloperski', ['d2', 'd6']),
    ('Dom piętrowy', 'Stan deweloperski', ['d3', 'd4']),
]
# ogloszenia o prace - w WordPressie dodawane w panelu; pusta lista = komunikat o braku ofert
OFERTY = []

def opis(k):
    return INW.get(k) or DOM.get(k)

def foto(P, k, tekst, sizes='(max-width:760px) 92vw, (max-width:1140px) 46vw, 30vw'):
    w, h = rozmiar(f'img/{k}-720.webp')
    return (f'<button class="foto" data-big="{P}img/{k}-1600.webp" data-opis="{e(tekst)}" aria-label="Powiększ: {e(tekst)}">'
            f'<img class="bw" src="{P}img/{k}-720.webp" srcset="{P}img/{k}-720.webp 720w, {P}img/{k}-1600.webp 1600w" sizes="{sizes}" '
            f'width="{w}" height="{h}" loading="lazy" alt="{e(tekst)}"></button>')

def karty_proste(P, lista):
    # strona glowna: jedno zdjecie na karte
    o = '<div class="siatka">\n'
    for typ, zakres, zdj in lista:
        o += f'  <article class="karta">{foto(P, zdj[0], typ)}<h3>{e(typ)}</h3><p>{e(zakres)}</p></article>\n'
    return o + '</div>'

def karty(P, lista):
    o = '<div class="siatka">\n'
    for typ, zakres, zdj in lista:
        o += '  <article class="karta">\n    <div class="mini">\n      <div class="tor">'
        for k in zdj:
            o += foto(P, k, f'{typ} - {opis(k).lower()}')
        o += (f'</div>\n      <span class="licz">1 / {len(zdj)}</span>'
              f'<button class="mp" aria-label="Poprzednie zdjęcie"></button><button class="mn" aria-label="Następne zdjęcie"></button>\n    </div>\n'
              f'    <h3>{e(typ)}</h3>\n    <p>{e(zakres)}</p>\n  </article>\n')
    return o + '</div>'

def srcset(P, n, szer=(640, 1024, 1600, 2000)):
    return ', '.join(f'{P}img/{n}-{s}.webp {s}w' for s in szer if os.path.exists(f'img/{n}-{s}.webp'))

# ---------- logo ----------
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <path id="b-glif" fill-rule="evenodd" d="M48 172H234C277 172 300 195 300 234C300 252 293 264 279 270C294 276 300 290 300 309C300 347 277 368 237 368H48ZM108 212H229C237 212 241 216 241 224V234C241 242 237 246 229 246H108ZM108 290H229C237 290 241 294 241 302V314C241 322 237 326 229 326H108Z"/>
  </defs>
</svg>'''

def logo_svg(extra=''):
    return (f'<svg viewBox="40 90 1070 290" aria-hidden="true"{extra}><rect x="48" y="97" width="233" height="45" fill="#9c9b9b"/><use href="#b-glif" fill="#fff"/>'
            '<text x="350" y="358" font-family="Archivo,sans-serif" font-size="196" font-weight="400" textLength="745" lengthAdjust="spacingAndGlyphs">'
            '<tspan fill="#9c9b9b">TECH</tspan><tspan fill="#fff">BET</tspan></text></svg>')

MENU = [('', 'Strona główna'), ('inwestycje/', 'Inwestycje'), ('domy/', 'Domy'), ('o-firmie/', 'O firmie'),
        ('opinie/', 'Opinie'), ('kariera/', 'Kariera'), ('kontakt/', 'Kontakt')]

def naglowek(P, akt):
    li = ''
    for h, n in MENU:
        kl = []
        if h == akt:
            kl.append('akt')
        if h == 'domy/':
            kl.append('md')
        a = (f' class="{" ".join(kl)}"' if kl else '') + (' aria-current="page"' if h == akt else '')
        li += f'      <li><a href="{P}{h}"{a}>{n}</a></li>\n'
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="{P or './'}" aria-label="TECHBET - strona główna">{logo_svg()}</a>
    <ul class="menu" id="menu">
{li}      <li class="tel-m"><a href="{TEL_H}">Biuro: {TEL}</a></li>
    </ul>
    <a class="btn btn-b" href="{P}kontakt/">Zapytaj o wycenę</a>
    <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span></button>
  </div>
</header>'''

def stopka(P):
    return f'''<footer class="stopka">
  <div class="wrap">
    <div>
      <a class="logo" href="{P or './'}" aria-label="TECHBET - strona główna">{logo_svg()}</a>
      <p>Firma budowlana z Lublina. Konstrukcje żelbetowe, inwestycje budowlane i domy do stanu deweloperskiego.</p>
    </div>
    <div><h3>Strona</h3><ul><li><a href="{P}inwestycje/">Inwestycje</a></li><li><a href="{P}domy/">Domy</a></li><li><a href="{P}o-firmie/">O firmie</a></li><li><a href="{P}opinie/">Opinie</a></li><li><a href="{P}kariera/">Kariera</a></li><li><a href="{P}kontakt/">Kontakt</a></li></ul></div>
    <div><h3>Biuro</h3><ul><li><a href="{TEL_H}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
    <div><h3>Adres</h3><p>ul. Mełgiewska 30F<br>20-234 Lublin</p><p style="margin-top:8px"><a href="{GMAPS_LINK}" rel="noopener">Wizytówka w Google Maps</a></p></div>
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
    'logo': DOM_URL + 'img/logo-192.png', 'image': DOM_URL + 'img/hero-1600.webp',
    'description': 'Firma budowlana z Lublina: konstrukcje żelbetowe, inwestycje budowlane oraz domy do stanu deweloperskiego. Wykonanie, organizacja budowy i dostawy materiałów.',
    'slogan': 'Twoja przyszłość. Nasza odpowiedzialność.',
    'telephone': '+48573132369', 'email': MAIL, 'hasMap': GMAPS_LINK,
    'address': {'@type': 'PostalAddress', 'streetAddress': 'ul. Mełgiewska 30F', 'postalCode': '20-234', 'addressLocality': 'Lublin', 'addressCountry': 'PL'},
    'geo': {'@type': 'GeoCoordinates', 'latitude': 51.2485789, 'longitude': 22.6245753},
    'taxID': '9462686367', 'vatID': 'PL9462686367', 'areaServed': 'Lublin',
}

def okruszki_ld(sciezka, nazwa):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Strona główna', 'item': DOM_URL},
        {'@type': 'ListItem', 'position': 2, 'name': nazwa, 'item': DOM_URL + sciezka}]}

def okruszki(P, nazwa):
    return f'<nav class="okr" aria-label="Okruszki"><ol><li><a href="{P}">Strona główna</a></li><li><span aria-current="page">{nazwa}</span></li></ol></nav>'

def strona(sciezka, tytul, opis_s, akt, tresc, ld, preload=''):
    P = '../' if sciezka else ''
    ldj = json.dumps({'@context': 'https://schema.org', '@graph': ld}, ensure_ascii=False, indent=1)
    doc = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(tytul)}</title>
<meta name="description" content="{e(opis_s)}">
<meta name="robots" content="noindex, nofollow" data-podglad>
<link rel="canonical" href="{DOM_URL}{sciezka}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{e(tytul)}">
<meta property="og:description" content="{e(opis_s)}">
<meta property="og:url" content="{DOM_URL}{sciezka}">
<meta property="og:image" content="{DOM_URL}img/hero-1600.webp">
<meta name="theme-color" content="#000000">
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
      <div class="cala"><button class="btn btn-b" type="submit">Wyślij zapytanie</button></div>
      <p class="cala wynik" id="wynik" aria-live="polite"></p>
    </form>'''

DANE = f'''<ul class="dane">
        <li><b>Biuro</b><a href="{TEL_H}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><b>Tomasz Kosikowski</b><a href="tel:+48509709840">509 709 840</a><br><a href="mailto:t.kosikowski@techbet.lublin.pl">t.kosikowski@techbet.lublin.pl</a></li>
        <li><b>Adres</b><span>ul. Mełgiewska 30F, 20-234 Lublin</span></li>
      </ul>'''

def licznik():
    # liczby przykladowe - do podmiany na dane TECHBET
    return '''<section class="licznik" aria-label="TECHBET w liczbach">
  <div class="wrap">
    <div class="poz"><b data-do="40">40</b><span>zrealizowanych inwestycji</span></div>
    <div class="poz"><b class="m" data-do="25">25</b><span>zbudowanych domów</span></div>
    <div class="poz"><b data-do="7">7</b><span>lat na budowach</span></div>
    <p class="przyp">Liczby przykładowe - wpiszemy prawdziwe dane TECHBET.</p>
  </div>
</section>'''

def loga_dev():
    li = ''.join('<li>Logo dewelopera</li>' for _ in range(6))
    return f'''<ul class="loga">{li}</ul>
    <p class="uwaga">Miejsce na logotypy deweloperów, dla których TECHBET budował - uzupełnimy po otrzymaniu listy i plików logo.</p>'''

def opinie_blok(P, pelny=False):
    dop = ('<p class="dop">Szczególnie zależy nam na opiniach inwestorów prywatnych, dla których budowaliśmy domy. '
           'Kolejne opinie klientów dodamy w tym miejscu.</p>')
    return f'''<div class="opinie">
      <div class="ocena">
        <div><b>5,0</b><div class="gw" aria-label="Ocena 5 na 5"><i></i><i></i><i></i><i></i><i></i></div></div>
        <p>Średnia ocen w wizytówce TECHBET w Google (3 opinie, stan na 26.11.2026).</p>
        <a class="btn btn-o" href="{GMAPS_LINK}" rel="noopener">{'Wystaw opinię w Google' if pelny else 'Opinie w Google'} <i class="str"></i></a>
      </div>
      <figure class="cyt">
        <blockquote>„Super firma”</blockquote>
        <figcaption>Marcin M., opinia w Google</figcaption>
        {dop}
      </figure>
    </div>'''

# ================= strona glowna =================
P = ''
glowna = f'''<section class="hero">
  <img src="img/hero-1024.webp" srcset="{srcset(P, 'hero', (640, 1024, 1600, 2000, 2800))}" sizes="max(100vw, 150vh)" width="2800" height="1867" alt="Zbrojenie słupów żelbetowych na budowie" fetchpriority="high">
  <div class="srodek">
    <span class="duze-logo">{logo_svg(' role="img"')}</span>
    <h1><span class="sr">TECHBET - firma budowlana z Lublina. </span>Twoja przyszłość. Nasza odpowiedzialność.</h1>
    <p class="pod">Firma budowlana z Lublina: konstrukcje żelbetowe, inwestycje budowlane i domy do stanu deweloperskiego.</p>
    <div class="akcje"><a class="btn btn-o" href="#realizacje">Zobacz realizacje</a></div>
  </div>
</section>

<section class="drogi" aria-label="Inwestycje i domy">
  <a class="droga d-inw" href="inwestycje/">
    <img class="bw" src="img/inw-1024.webp" srcset="{srcset(P, 'inw')}" sizes="(max-width:760px) 128vw, 62vw" width="2000" height="1333" loading="lazy" alt="Budynek w budowie z dźwigami wieżowymi">
    <div class="tresc"><h2>Inwestycje</h2><p>Konstrukcje żelbetowe i budynki - organizacja budowy, wykonawstwo, dostawy materiałów.</p><span class="wiecej">Zobacz inwestycje</span></div>
  </a>
  <a class="droga d-dom" href="domy/">
    <img class="bw" src="img/d-hero-1024.webp" srcset="{srcset(P, 'd-hero')}" sizes="(max-width:760px) 128vw, 62vw" width="2000" height="1677" loading="lazy" alt="Nowoczesny dom jednorodzinny z drewnianą elewacją">
    <div class="tresc"><h2>Domy</h2><p>Domy jednorodzinne do stanu deweloperskiego - z wykonaniem, organizacją prac i materiałami.</p><span class="wiecej">Zobacz domy</span></div>
  </a>
</section>

{licznik()}

<section class="sek" id="realizacje">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Realizacje</h2></div>
      <p>Wybrane budowy TECHBET, osobno inwestycje i domy. Zdjęcia po kliknięciu można powiększyć.</p>
    </div>
    <div class="zakl" role="tablist" aria-label="Rodzaj realizacji">
      <button role="tab" id="z-inw" aria-controls="p-inw" aria-selected="true">Inwestycje</button>
      <button role="tab" id="z-dom" class="md" aria-controls="p-dom" aria-selected="false" tabindex="-1">Domy</button>
    </div>
    <div class="panel" id="p-inw" role="tabpanel" aria-labelledby="z-inw">
      {karty_proste(P, REAL_INW)}
      <div class="nawig"><a class="btn btn-o" href="inwestycje/">Wszystkie inwestycje <i class="str"></i></a></div>
    </div>
    <div class="panel m" id="p-dom" role="tabpanel" aria-labelledby="z-dom" hidden>
      {karty_proste(P, REAL_DOM)}
      <div class="nawig"><a class="btn btn-m" href="domy/">Wszystkie domy <i class="str"></i></a></div>
    </div>
    <p class="uwaga">Zdjęcia poglądowe - zastąpimy je zdjęciami z realizacji TECHBET, także ujęciami z drona.</p>
  </div>
</section>

<section class="sek t2">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Budowaliśmy dla</h2></div>
      <p>Deweloperzy, dla których TECHBET wykonywał konstrukcje i budynki.</p>
    </div>
    {loga_dev()}
  </div>
</section>

<section class="sek m">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Opinie</h2></div>
      <p>Co mówią o nas inwestorzy.</p>
    </div>
    {opinie_blok(P)}
  </div>
</section>

<section class="sek t2 cta">
  <div class="wrap">
    <div><span class="belka"></span><h2>Planują Państwo budowę?</h2></div>
    <div><p>Prześlij projekt albo opisz inwestycję lub dom - odpowiemy z wyceną i zakresem prac.</p><a class="btn btn-b" href="kontakt/">Zapytaj o wycenę <i class="str"></i></a></div>
  </div>
</section>'''

strona('', 'TECHBET Lublin - konstrukcje żelbetowe, inwestycje i domy do stanu deweloperskiego',
       'TECHBET, firma budowlana z Lublina: konstrukcje żelbetowe, inwestycje budowlane oraz domy do stanu deweloperskiego. Twoja przyszłość. Nasza odpowiedzialność.',
       '', glowna,
       [dict(FIRMA), {'@type': 'WebSite', '@id': DOM_URL + '#strona', 'url': DOM_URL, 'name': 'TECHBET', 'inLanguage': 'pl-PL', 'publisher': {'@id': DOM_URL + '#firma'}}],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, "hero", (640, 1024, 1600, 2000, 2800))}" imagesizes="max(100vw, 150vh)" fetchpriority="high">\n')

# ================= inwestycje =================
P = '../'
inw = f'''<section class="ph">
  <img class="bw" src="{P}img/inw-1024.webp" srcset="{srcset(P, 'inw', (640, 1024, 1600, 2000, 2800))}" sizes="max(100vw, 150vh)" width="2800" height="1867" alt="Budynek w budowie z dźwigami wieżowymi" fetchpriority="high">
  <div class="wrap">
    {okruszki(P, 'Inwestycje')}
    <span class="belka"></span>
    <h1>Inwestycje budowlane i konstrukcje żelbetowe - Lublin</h1>
    <p class="lead">Prowadzimy budowy od organizacji placu i harmonogramu, przez wykonawstwo konstrukcji, po dostawy materiałów. Inwestor ma po naszej stronie jednego wykonawcę i jedną osobę odpowiedzialną za budowę.</p>
    <a class="btn btn-b" href="{P}kontakt/?typ=inwestycja">Zapytaj o wycenę inwestycji <i class="str"></i></a>
  </div>
</section>

<section class="sek">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Zakres prac</h2></div>
      <p>Przy inwestycji bierzemy na siebie te elementy, które najczęściej decydują o terminie i koszcie budowy. Zakres dla konkretnego obiektu ustalamy przed podpisaniem umowy.</p>
    </div>
    <ul class="wiersze">
      <li><h3>Konstrukcje żelbetowe</h3><p>Zbrojenie, szalunki i betonowanie fundamentów, ścian, słupów i stropów.</p></li>
      <li><h3>Organizacja budowy</h3><p>Przygotowanie placu budowy, harmonogram prac i koordynacja ekip na kolejnych etapach.</p></li>
      <li><h3>Dostawy materiałów</h3><p>Zamawiamy i dowozimy materiały w rytmie budowy, tak żeby prace nie czekały na dostawy.</p></li>
      <li><h3>Jeden partner</h3><p>Inwestor rozmawia z jednym wykonawcą, a nie z kilkoma firmami naraz.</p></li>
    </ul>
  </div>
</section>

<section class="sek t2">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Realizacje</h2></div>
      <p>Wybrane inwestycje prowadzone przez TECHBET. Zdjęcia w każdej karcie można przesuwać palcem albo myszą, a po kliknięciu powiększyć.</p>
    </div>
    {karty(P, REAL_INW)}
    <p class="uwaga">Zdjęcia poglądowe - zostaną zastąpione zdjęciami z realizacji TECHBET, także ujęciami z drona.</p>
  </div>
</section>

<section class="sek">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Budowaliśmy dla</h2></div>
      <p>Deweloperzy, dla których TECHBET wykonywał konstrukcje i budynki.</p>
    </div>
    {loga_dev()}
  </div>
</section>

<section class="sek t2">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Jak prowadzimy inwestycję</h2></div>
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

<section class="sek cta">
  <div class="wrap">
    <div><span class="belka"></span><h2>Planują Państwo inwestycję?</h2></div>
    <div><p>Prześlij projekt albo opisz obiekt - odpowiemy z wyceną i zakresem prac.</p><a class="btn btn-b" href="{P}kontakt/?typ=inwestycja">Zapytaj o wycenę <i class="str"></i></a></div>
  </div>
</section>'''

strona('inwestycje/', 'Inwestycje budowlane i konstrukcje żelbetowe Lublin - TECHBET',
       'Inwestycje budowlane i konstrukcje żelbetowe w Lublinie: organizacja budowy, wykonawstwo i dostawy materiałów. Realizacje TECHBET i deweloperzy, dla których budowaliśmy.',
       'inwestycje/', inw,
       [okruszki_ld('inwestycje/', 'Inwestycje'),
        {'@type': 'Service', 'name': 'Inwestycje budowlane i konstrukcje żelbetowe', 'serviceType': 'Generalne wykonawstwo, konstrukcje żelbetowe', 'areaServed': 'Lublin', 'provider': {'@id': DOM_URL + '#firma'}, 'url': DOM_URL + 'inwestycje/'},
        dict(FIRMA)],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, "inw", (640, 1024, 1600, 2000, 2800))}" imagesizes="max(100vw, 150vh)" fetchpriority="high">\n')

# ================= domy =================
domy = f'''<section class="ph m">
  <img class="bw" src="{P}img/d-hero-1024.webp" srcset="{srcset(P, 'd-hero')}" sizes="max(100vw, 120vh)" width="2000" height="1677" alt="Nowoczesny dom jednorodzinny z drewnianą elewacją" fetchpriority="high">
  <div class="wrap">
    {okruszki(P, 'Domy')}
    <span class="belka"></span>
    <h1>Domy do stanu deweloperskiego - Lublin i&nbsp;okolice</h1>
    <p class="lead">Budujemy domy jednorodzinne do stanu deweloperskiego. Zajmujemy się wykonaniem, organizacją prac i dostawami materiałów, a zakres prac jest jasny już na etapie wyceny.</p>
    <a class="btn btn-m" href="{P}kontakt/?typ=dom">Prześlij projekt do wyceny <i class="str"></i></a>
  </div>
</section>

<section class="sek m">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Co obejmuje stan deweloperski</h2></div>
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

<section class="sek t2 m">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Zbudowane domy</h2></div>
      <p>Domy zbudowane przez TECHBET. Zdjęcia w każdej karcie można przesuwać palcem albo myszą, a po kliknięciu powiększyć.</p>
    </div>
    {karty(P, REAL_DOM)}
    <p class="uwaga">Zdjęcia poglądowe - zostaną zastąpione zdjęciami domów zbudowanych przez TECHBET, także ujęciami z drona.</p>
  </div>
</section>

<section class="sek m">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Opinie inwestorów</h2></div>
      <p>Przy budowie domu najważniejsze jest zaufanie - dlatego pokazujemy, co mówią o nas inwestorzy.</p>
    </div>
    {opinie_blok(P)}
  </div>
</section>

<section class="sek t2 m">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Etapy budowy domu</h2></div>
      <p>Od przesłania projektu do odbioru domu gotowego do wykończenia.</p>
    </div>
    <ol class="etapy">
      <li><span class="nr">01</span><h3>Projekt do wyceny</h3><p>Przesyłają nam Państwo projekt domu - wystarczy formularz na stronie.</p></li>
      <li><span class="nr">02</span><h3>Wycena i zakres prac</h3><p>Przygotowujemy wycenę z wyraźnym zakresem: co jest w cenie, a co nie.</p></li>
      <li><span class="nr">03</span><h3>Umowa i harmonogram</h3><p>Ustalamy terminy kolejnych etapów i dostaw materiałów.</p></li>
      <li><span class="nr">04</span><h3>Stan surowy</h3><p>Fundamenty, ściany, stropy i dach - dom zamknięty przed zimą i deszczem.</p></li>
      <li><span class="nr">05</span><h3>Instalacje i tynki</h3><p>Instalacje, tynki, wylewki i elewacja według ustalonego zakresu.</p></li>
      <li><span class="nr">06</span><h3>Odbiór stanu deweloperskiego</h3><p>Przekazujemy dom gotowy do prac wykończeniowych.</p></li>
    </ol>
  </div>
</section>

<section class="sek cta m">
  <div class="wrap">
    <div><span class="belka"></span><h2>Mają Państwo projekt domu?</h2></div>
    <div><p>Prześlij go do wyceny - odpowiemy z zakresem prac i terminem.</p><a class="btn btn-m" href="{P}kontakt/?typ=dom">Prześlij projekt do wyceny <i class="str"></i></a></div>
  </div>
</section>'''

strona('domy/', 'Domy do stanu deweloperskiego Lublin - TECHBET',
       'Budowa domów do stanu deweloperskiego w Lublinie i okolicy: zakres prac, etapy budowy, realizacje i opinie. Prześlij projekt domu do wyceny.',
       'domy/', domy,
       [okruszki_ld('domy/', 'Domy'),
        {'@type': 'Service', 'name': 'Budowa domów do stanu deweloperskiego', 'serviceType': 'Budowa domów jednorodzinnych', 'areaServed': 'Lublin', 'provider': {'@id': DOM_URL + '#firma'}, 'url': DOM_URL + 'domy/'},
        dict(FIRMA)],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, "d-hero")}" imagesizes="max(100vw, 120vh)" fetchpriority="high">\n')

# ================= o firmie =================
ofirmie = f'''<section class="ph">
  <img class="bw" src="{P}img/n3-1024.webp" srcset="{srcset(P, 'n3', (720, 1024, 1600, 2000, 2800))}" sizes="max(100vw, 150vh)" width="2800" height="1867" alt="Konstrukcja żelbetowa budynku w budowie" fetchpriority="high">
  <div class="wrap">
    {okruszki(P, 'O firmie')}
    <span class="belka"></span>
    <h1>O firmie TECHBET</h1>
    <p class="lead">TECHBET to firma budowlana z Lublina, z siedzibą przy ul. Mełgiewskiej 30F. Wykonujemy konstrukcje żelbetowe, prowadzimy inwestycje budowlane i budujemy domy do stanu deweloperskiego.</p>
    <a class="btn btn-b" href="{P}kontakt/">Kontakt z biurem <i class="str"></i></a>
  </div>
</section>

<section class="sek">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Jedna firma, dwie drogi</h2></div>
      <p>Znak TECHBET to litera B z belką nad nią - jak strop nad ścianą. Pod tym samym znakiem prowadzimy dwa rodzaje budów: większe inwestycje i domy jednorodzinne.</p>
    </div>
    <div class="dwie">
      <a class="droga d-inw" href="{P}inwestycje/"><img class="bw" src="{P}img/n6-720.webp" srcset="{P}img/n6-720.webp 720w, {P}img/n6-1600.webp 1600w" sizes="(max-width:760px) 128vw, 62vw" width="720" height="480" loading="lazy" alt="Budynek wielorodzinny w budowie"><div class="tresc"><h2>Inwestycje</h2><p>Konstrukcje żelbetowe, organizacja budowy, wykonawstwo i dostawy materiałów.</p></div></a>
      <a class="droga d-dom" href="{P}domy/"><img class="bw" src="{P}img/d2-720.webp" srcset="{P}img/d2-720.webp 720w, {P}img/d2-1600.webp 1600w" sizes="(max-width:760px) 128vw, 62vw" width="720" height="480" loading="lazy" alt="Dom jednorodzinny z tarasem"><div class="tresc"><h2>Domy</h2><p>Domy jednorodzinne do stanu deweloperskiego.</p></div></a>
    </div>
  </div>
</section>

<section class="sek t2">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Jak pracujemy</h2></div>
      <p>Inwestycje i domy prowadzimy tak samo: jeden wykonawca, jedna osoba odpowiedzialna za budowę i zakres prac ustalony przed startem.</p>
    </div>
    <div class="trzy">
      <div><h3>Kompleksowe wykonanie</h3><p>Od fundamentów po stan deweloperski - wszystkie etapy budowy w jednych rękach.</p></div>
      <div><h3>Organizacja budowy</h3><p>Harmonogram, ekipy i dostawy materiałów planujemy sami, żeby budowa nie stała.</p></div>
      <div><h3>Jasny zakres prac</h3><p>Przed podpisaniem umowy wiadomo, co dokładnie wykonujemy i co jest w cenie.</p></div>
    </div>
  </div>
</section>

<section class="sek">
  <div class="wrap kon">
    <div>
      <span class="belka"></span>
      <h2>Budowy z lotu ptaka</h2>
      <p>Kierownik budowy fotografuje nasze realizacje dronem. Dzięki temu przy każdej inwestycji i każdym domu w portfolio można pokazać zdjęcia z góry - skalę budowy, postęp prac i jakość wykonania.</p>
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
       'TECHBET sp. z o.o. z Lublina: konstrukcje żelbetowe, inwestycje budowlane i domy do stanu deweloperskiego. Jak pracujemy, dane firmy i kontakt.',
       'o-firmie/', ofirmie,
       [okruszki_ld('o-firmie/', 'O firmie'), {'@type': 'AboutPage', 'url': DOM_URL + 'o-firmie/', 'name': 'O firmie TECHBET', 'about': {'@id': DOM_URL + '#firma'}}, dict(FIRMA)],
       preload=f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(P, 'n3', (720, 1024, 1600, 2000, 2800))}" imagesizes="max(100vw, 150vh)" fetchpriority="high">\n')

# ================= opinie =================
opinie = f'''<section class="pn">
  <div class="wrap">
    {okruszki(P, 'Opinie')}
    <span class="belka m"></span>
    <h1>Opinie o TECHBET</h1>
    <p class="lead">Co mówią o nas inwestorzy - zarówno przy inwestycjach, jak i przy budowie domów.</p>
  </div>
</section>

<section class="sek m">
  <div class="wrap">
    {opinie_blok(P, pelny=True)}
  </div>
</section>

<section class="sek t2 cta">
  <div class="wrap">
    <div><span class="belka"></span><h2>Budowaliśmy dla Państwa?</h2></div>
    <div><p>Będzie nam miło, jeśli zostawią Państwo kilka słów w naszej wizytówce Google - to pomaga kolejnym inwestorom.</p><a class="btn btn-b" href="{GMAPS_LINK}" rel="noopener">Wystaw opinię w Google <i class="str"></i></a></div>
  </div>
</section>'''

strona('opinie/', 'Opinie o firmie budowlanej TECHBET Lublin',
       'Opinie inwestorów o firmie budowlanej TECHBET z Lublina: inwestycje budowlane i domy do stanu deweloperskiego. Ocena w Google i opinie klientów.',
       'opinie/', opinie,
       [okruszki_ld('opinie/', 'Opinie'), {'@type': 'WebPage', 'url': DOM_URL + 'opinie/', 'name': 'Opinie o TECHBET', 'about': {'@id': DOM_URL + '#firma'}}, dict(FIRMA)])

# ================= kariera =================
if OFERTY:
    lista = '<ul class="oferty">' + ''.join(
        f'<li><div><h3>{e(o["tytul"])}</h3><p>{e(o["opis"])}</p></div><a class="btn btn-o" href="mailto:{MAIL}?subject={e(o["tytul"])}">Aplikuj <i class="str"></i></a></li>'
        for o in OFERTY) + '</ul>'
else:
    lista = f'''<div class="brak">
      <div><h3>Obecnie nie prowadzimy rekrutacji.</h3><p>Aktualne ogłoszenia o pracę pojawią się w tym miejscu. Jeśli chcą Państwo z nami pracować, prosimy o przesłanie CV na adres biura - odezwiemy się, gdy pojawi się odpowiednie stanowisko.</p></div>
      <a class="btn btn-o" href="mailto:{MAIL}?subject=CV">Wyślij CV <i class="str"></i></a>
    </div>'''

kariera = f'''<section class="pn">
  <div class="wrap">
    {okruszki(P, 'Kariera')}
    <span class="belka"></span>
    <h1>Kariera w TECHBET</h1>
    <p class="lead">Szukamy ludzi, którzy lubią dobrze zrobioną robotę - na budowie i w biurze.</p>
  </div>
</section>

<section class="sek">
  <div class="wrap">
    <div class="glowa">
      <div><span class="belka"></span><h2>Aktualne oferty pracy</h2></div>
      <p>Tu publikujemy aktualne ogłoszenia o pracę w TECHBET - na budowach i w biurze w Lublinie.</p>
    </div>
    {lista}
  </div>
</section>'''

strona('kariera/', 'Kariera - praca w firmie budowlanej TECHBET Lublin',
       'Praca w firmie budowlanej TECHBET z Lublina: aktualne ogłoszenia o pracę na budowie i w biurze. Wyślij CV na biuro@techbet.lublin.pl.',
       'kariera/', kariera,
       [okruszki_ld('kariera/', 'Kariera'), {'@type': 'WebPage', 'url': DOM_URL + 'kariera/', 'name': 'Kariera w TECHBET', 'about': {'@id': DOM_URL + '#firma'}}, dict(FIRMA)])

# ================= kontakt =================
kontakt = f'''<section class="pn">
  <div class="wrap">
    {okruszki(P, 'Kontakt')}
    <span class="belka"></span>
    <h1>Kontakt - TECHBET Lublin</h1>
    <p class="lead">Prześlij projekt albo opisz inwestycję lub dom - odpowiemy z wyceną i zakresem prac.</p>
  </div>
</section>

<section class="sek">
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
  <iframe src="{GMAPS_EMBED}" loading="lazy" title="Mapa Google: TECHBET - konstrukcje żelbetowe, ul. Mełgiewska 30F, Lublin" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  <div class="wrap pasek"><p>TECHBET, ul. Mełgiewska 30F, 20-234 Lublin</p><a class="btn btn-o" href="{GMAPS_LINK}" rel="noopener">Otwórz wizytówkę w Google Maps <i class="str"></i></a></div>
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
  <p>Jeśli kontaktuje się Pan lub Pani z nami telefonicznie albo mailowo (także przesyłając CV), przetwarzamy dane podane w tej korespondencji w tym samym celu lub w celu rekrutacji.</p>

  <h2>Podstawa prawna</h2>
  <ul>
    <li>art. 6 ust. 1 lit. b RODO - działania przed zawarciem umowy na prośbę osoby, której dane dotyczą (wycena, oferta, rekrutacja),</li>
    <li>art. 6 ust. 1 lit. f RODO - prawnie uzasadniony interes administratora, czyli prowadzenie korespondencji i ewentualne dochodzenie roszczeń.</li>
  </ul>

  <h2>Jak długo przechowujemy dane</h2>
  <p>Dane z zapytania przechowujemy przez czas potrzebny do odpowiedzi i rozmów o wycenie, a jeśli dojdzie do zawarcia umowy - przez czas jej realizacji i okres wymagany przepisami (np. podatkowymi) lub do przedawnienia roszczeń. Dane z CV - do zakończenia rekrutacji.</p>

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
       'polityka', polityka,
       [okruszki_ld('polityka-prywatnosci/', 'Polityka prywatności'), {'@type': 'WebPage', 'url': DOM_URL + 'polityka-prywatnosci/', 'name': 'Polityka prywatności'}, dict(FIRMA)])

# ================= sitemap, llms =================
adresy = ['', 'inwestycje/', 'domy/', 'o-firmie/', 'opinie/', 'kariera/', 'kontakt/', 'polityka-prywatnosci/']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for a in adresy:
    sm += f'  <url><loc>{DOM_URL}{a}</loc></url>\n'
open('sitemap.xml', 'w', encoding='utf8', newline='\n').write(sm + '</urlset>\n')

open('llms.txt', 'w', encoding='utf8', newline='\n').write(f'''# TECHBET sp. z o.o. - firma budowlana, Lublin

> TECHBET to firma budowlana z Lublina (ul. Mełgiewska 30F, 20-234 Lublin). Wykonuje konstrukcje żelbetowe, prowadzi inwestycje budowlane oraz buduje domy jednorodzinne do stanu deweloperskiego: wykonanie, organizacja budowy i dostawy materiałów. Hasło: Twoja przyszłość. Nasza odpowiedzialność.

## Oferta
- [Inwestycje]({DOM_URL}inwestycje/): konstrukcje żelbetowe, organizacja budowy, wykonawstwo i dostawy materiałów przy inwestycjach budowlanych.
- [Domy]({DOM_URL}domy/): budowa domów do stanu deweloperskiego, zakres prac i etapy budowy.

## Firma
- [O firmie]({DOM_URL}o-firmie/): sposób pracy i dane rejestrowe (KRS 0000770226, NIP 946-268-63-67).
- [Opinie]({DOM_URL}opinie/): opinie inwestorów i ocena w Google.
- [Kariera]({DOM_URL}kariera/): aktualne ogłoszenia o pracę.
- [Kontakt]({DOM_URL}kontakt/): biuro tel. {TEL}, {MAIL}; formularz zapytania z możliwością dołączenia projektu; mapa z wizytówką Google.
''')
print('sitemap, llms ok')
