(function(){
var d=document;
// menu mobilne
var bur=d.querySelector('.burger'),menu=d.getElementById('menu');
bur.addEventListener('click',function(){var o=bur.getAttribute('aria-expanded')!=='true';bur.setAttribute('aria-expanded',o);menu.classList.toggle('otw',o)});
// pasek z telefonem po zjechaniu z pierwszego ekranu
var mob=d.getElementById('mob'),hero=d.querySelector('.hero,.ph,.pn');
if(mob&&hero&&'IntersectionObserver' in window){new IntersectionObserver(function(en){mob.classList.toggle('widac',!en[0].isIntersecting)}).observe(hero)}
// przesuwanie mysza (palec dziala natywnie)
function ciagnij(t,krok){
  var x0,s0,ruch=false,wcis=false;
  t.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;wcis=true;ruch=false;x0=e.clientX;s0=t.scrollLeft});
  window.addEventListener('pointermove',function(e){if(!wcis)return;var dx=e.clientX-x0;if(Math.abs(dx)>6){ruch=true;t.classList.add('ciag')}if(ruch)t.scrollLeft=s0-dx});
  window.addEventListener('pointerup',function(){if(!wcis)return;wcis=false;if(ruch){var k=krok();t.classList.remove('ciag');t.scrollTo({left:Math.round(t.scrollLeft/k)*k,behavior:'smooth'});setTimeout(function(){ruch=false},50)}});
  t.addEventListener('click',function(e){if(ruch){e.preventDefault();e.stopPropagation()}},true);
  t.addEventListener('dragstart',function(e){e.preventDefault()});
}
// tasmy na stronie glownej
[].slice.call(d.querySelectorAll('.tasma')).forEach(function(t){
  var nav=t.nextElementSibling,krok=function(){var k=t.querySelector('.kafel');return k?k.getBoundingClientRect().width+parseFloat(getComputedStyle(t).columnGap||20):300};
  nav.querySelector('.pop').addEventListener('click',function(){t.scrollBy({left:-krok(),behavior:'smooth'})});
  nav.querySelector('.nast').addEventListener('click',function(){t.scrollBy({left:krok(),behavior:'smooth'})});
  ciagnij(t,krok);
});
// galerie w kartach realizacji
[].slice.call(d.querySelectorAll('.mini')).forEach(function(m){
  var t=m.querySelector('.tor'),n=t.children.length,lz=m.querySelector('.licz'),bp=m.querySelector('.mp'),bn=m.querySelector('.mn');
  var krok=function(){return t.clientWidth};
  function stan(){var i=Math.round(t.scrollLeft/krok());lz.textContent=(i+1)+' / '+n;bp.disabled=i<=0;bn.disabled=i>=n-1}
  bp.addEventListener('click',function(){t.scrollBy({left:-krok(),behavior:'smooth'})});
  bn.addEventListener('click',function(){t.scrollBy({left:krok(),behavior:'smooth'})});
  t.addEventListener('scroll',function(){window.requestAnimationFrame(stan)},{passive:true});
  ciagnij(t,krok);stan();
});
// powiekszenie
var lb=d.getElementById('lb'),li=lb.querySelector('img'),lp=lb.querySelector('p'),lista=[],nr=0;
function pokaz(){var b=lista[nr];li.src=b.dataset.big;li.alt=b.dataset.opis||'';lp.textContent=b.dataset.opis||''}
d.addEventListener('click',function(e){var b=e.target.closest('[data-big]');if(!b)return;var g=b.closest('.tasma,.tor');lista=g?[].slice.call(g.querySelectorAll('[data-big]')):[b];nr=lista.indexOf(b);pokaz();lb.classList.add('on');lb.querySelector('.zam').focus()});
function zamknij(){lb.classList.remove('on');li.removeAttribute('src')}
lb.querySelector('.zam').addEventListener('click',zamknij);
lb.querySelector('.pop').addEventListener('click',function(){nr=(nr-1+lista.length)%lista.length;pokaz()});
lb.querySelector('.nast').addEventListener('click',function(){nr=(nr+1)%lista.length;pokaz()});
lb.addEventListener('click',function(e){if(e.target===lb)zamknij()});
d.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;if(e.key==='Escape')zamknij();if(e.key==='ArrowRight')lb.querySelector('.nast').click();if(e.key==='ArrowLeft')lb.querySelector('.pop').click()});
var tx;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)lb.querySelector(dx<0?'.nast':'.pop').click()});
// formularz: na wersji testowej bez wysylki
var f=d.getElementById('form');
if(f){
  var typ=(location.search.match(/[?&]typ=(dom|inwestycja)/)||[])[1];
  if(typ){var r=f.querySelector('input[name=typ][value='+typ+']');if(r)r.checked=true}
  f.addEventListener('submit',function(e){e.preventDefault();d.getElementById('wynik').textContent='To wersja testowa strony - formularz zacznie wysyłać zapytania po uruchomieniu strony pod adresem techbet.lublin.pl.'});
}
var rok=d.getElementById('rok');if(rok)rok.textContent=new Date().getFullYear();
})();
