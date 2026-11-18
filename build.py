import html
from PIL import Image
d=open('src.html',encoding='utf8').read()
INW=[('i1','Konstrukcja żelbetowa','Zbrojenie stropu'),('i2','Zbrojenie słupów','Prace na wysokości'),('i4','Budynek wielokondygnacyjny','Dźwigi wieżowe na budowie'),('i5','Szkielet budynku','Stan surowy otwarty'),('i6','Budynek mieszkalny','Elewacja z balkonami'),('i3','Odbiór płyty','Ekipa na budowie')]
DOM=[('d1','Dom z drewnianą elewacją','Stan wykończony'),('d2','Dom z tarasem','Bryła z dużymi przeszkleniami'),('d3','Dom piętrowy','Elewacja z okładziną drewnianą'),('d4','Dom w bieli','Prosta, nowoczesna bryła'),('d5','Wnętrze domu','Salon ze schodami'),('d6','Wnętrze domu','Strefa dzienna z kuchnią')]
def kafle(L):
    o=''
    for k,t,p in L:
        w,h=Image.open(f'img/{k}-720.webp').size
        o+=f'      <article class="kafel"><button data-big="img/{k}-1600.webp" data-opis="{html.escape(t)}" aria-label="Powiększ: {html.escape(t)}"><img src="img/{k}-720.webp" width="{w}" height="{h}" loading="lazy" alt="{html.escape(t)} - {html.escape(p.lower())}"></button><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></article>\n'
    return o
d=d.replace('<!--INW-->',kafle(INW)).replace('<!--DOM-->',kafle(DOM))
d=d.replace('<!--BADGE_STYLE-->',open('badge_style.part',encoding='utf8').read().replace('<style>','').replace('</style>',''))
d=d.replace('<!--BADGE_LINK-->',open('badge_link.part',encoding='utf8').read())
open('index.html','w',encoding='utf8').write(d)
print('ok',len(d))
