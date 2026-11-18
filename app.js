(function(){
var d=document;
// menu mobilne
var bur=d.querySelector('.burger'),menu=d.getElementById('menu');
bur.addEventListener('click',function(){var o=bur.getAttribute('aria-expanded')!=='true';bur.setAttribute('aria-expanded',o);menu.classList.toggle('otw',o)});
menu.addEventListener('click',function(e){if(e.target.tagName==='A'){bur.setAttribute('aria-expanded','false');menu.classList.remove('otw')}});
// aktywna pozycja menu
var linki=[].slice.call(menu.querySelectorAll('a[href^="#"]'));
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){linki.forEach(function(a){a.classList.toggle('akt',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-45% 0px -50% 0px'});
  ['inwestycje','domy','o-firmie','kontakt'].forEach(function(id){var s=d.getElementById(id);if(s)io.observe(s)});
  var mob=d.getElementById('mob'),hero=d.querySelector('.hero');
  new IntersectionObserver(function(en){mob.classList.toggle('widac',!en[0].isIntersecting)}).observe(hero);
}
// tasmy: palec, mysz, strzalki
[].slice.call(d.querySelectorAll('.tasma')).forEach(function(t){
  var nav=t.nextElementSibling,krok=function(){var k=t.querySelector('.kafel');return k?k.getBoundingClientRect().width+parseFloat(getComputedStyle(t).columnGap||20):300};
  nav.querySelector('.pop').addEventListener('click',function(){t.scrollBy({left:-krok(),behavior:'smooth'})});
  nav.querySelector('.nast').addEventListener('click',function(){t.scrollBy({left:krok(),behavior:'smooth'})});
  var x0,s0,ruch=false,wcis=false;
  t.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;wcis=true;ruch=false;x0=e.clientX;s0=t.scrollLeft});
  window.addEventListener('pointermove',function(e){if(!wcis)return;var dx=e.clientX-x0;if(Math.abs(dx)>6){ruch=true;t.classList.add('ciag')}if(ruch)t.scrollLeft=s0-dx});
  window.addEventListener('pointerup',function(){if(!wcis)return;wcis=false;if(ruch){var k=krok();t.classList.remove('ciag');t.scrollTo({left:Math.round(t.scrollLeft/k)*k,behavior:'smooth'});setTimeout(function(){ruch=false},50)}});
  t.addEventListener('click',function(e){if(ruch){e.preventDefault();e.stopPropagation()}},true);
});
// powiekszenie
var lb=d.getElementById('lb'),li=lb.querySelector('img'),lp=lb.querySelector('p'),lista=[],nr=0;
function pokaz(){var b=lista[nr];li.src=b.dataset.big;li.alt=b.dataset.opis||'';lp.textContent=b.dataset.opis||''}
d.addEventListener('click',function(e){var b=e.target.closest('[data-big]');if(!b)return;var g=b.closest('.tasma');lista=g?[].slice.call(g.querySelectorAll('[data-big]')):[b];nr=lista.indexOf(b);pokaz();lb.classList.add('on');lb.querySelector('.zam').focus()});
function zamknij(){lb.classList.remove('on');li.removeAttribute('src')}
lb.querySelector('.zam').addEventListener('click',zamknij);
lb.querySelector('.pop').addEventListener('click',function(){nr=(nr-1+lista.length)%lista.length;pokaz()});
lb.querySelector('.nast').addEventListener('click',function(){nr=(nr+1)%lista.length;pokaz()});
lb.addEventListener('click',function(e){if(e.target===lb)zamknij()});
d.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;if(e.key==='Escape')zamknij();if(e.key==='ArrowRight')lb.querySelector('.nast').click();if(e.key==='ArrowLeft')lb.querySelector('.pop').click()});
var tx;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)lb.querySelector(dx<0?'.nast':'.pop').click()});
// formularz pokazowy
d.getElementById('form').addEventListener('submit',function(e){e.preventDefault();d.getElementById('wynik').textContent='To podgląd strony - formularz zacznie wysyłać zapytania po wdrożeniu.'});
d.getElementById('rok').textContent=new Date().getFullYear();
})();
