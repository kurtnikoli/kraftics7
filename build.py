#!/usr/bin/env python3
"""Build the 4 Kraftics HTML pages, each fully self-contained with embedded base64 assets."""
import base64
import pathlib
import textwrap
import re

ROOT = pathlib.Path(__file__).parent

def b64(name):
    return base64.b64encode((ROOT / "assets" / name).read_bytes()).decode()

K_WHITE = "data:image/png;base64," + b64("k_white.png")
K_BLACK = "data:image/png;base64," + b64("k_black.png")
WORDMARK_WHITE = "data:image/png;base64," + b64("wordmark_white.png")
WORDMARK_BLACK = "data:image/png;base64," + b64("wordmark_black.png")
FAVICON = "data:image/png;base64," + b64("favicon.png")

# ------------------------------------------------------------------ THEME CSS
THEME_CSS = r"""
:root{
  --ink:#100F0A;
  --ink-2:#1a1812;
  --yellow:#F4E11A;
  --yellow-2:#FFE633;
  --cream:#F3EEDF;
  --white:#FFFFFF;
  --magenta:#FF3DA5;
  --cyan:#27D3E0;
  --purple:#9B6BFF;
  --lime:#C3F03A;
  --orange:#FF8A3D;
  --blue:#4DA2FF;
  --hd:62px;
  --shadow-hard:6px 7px 0 var(--ink);
  --shadow-mag:6px 7px 0 var(--magenta);
  --shadow-cyan:6px 7px 0 var(--cyan);
  --shadow-lime:6px 7px 0 var(--lime);
  --shadow-purple:6px 7px 0 var(--purple);
  --shadow-orange:6px 7px 0 var(--orange);
  --shadow-blue:6px 7px 0 var(--blue);
  --shadow-white:6px 7px 0 var(--white);
  --shadow-yellow:6px 7px 0 var(--yellow);
}
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:'Hanken Grotesk',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  background:var(--yellow);
  color:var(--ink);
  -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility;
  overflow-x:hidden;
  min-height:100dvh;
  font-size:17px;
  line-height:1.55;
}
a{color:inherit;text-decoration:none}
button{font:inherit;border:0;background:none;cursor:pointer;color:inherit}
img{max-width:100%;display:block}

h1,h2,h3,h4,.font-display{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;letter-spacing:-0.02em;line-height:1}
.font-mono{font-family:'JetBrains Mono',ui-monospace,Menlo,monospace;letter-spacing:.02em}
.container{width:min(1240px,92vw);margin-inline:auto}

/* ===== HEADER (folder-tab) ===== */
.hd{
  position:fixed;top:0;left:0;right:0;height:var(--hd);
  background:var(--ink);color:#fff;z-index:90;
  display:flex;align-items:center;
  transition:box-shadow .25s ease, background .3s ease;
}
.hd.scrolled{box-shadow:0 12px 30px -16px rgba(0,0,0,.55);backdrop-filter:blur(8px)}
.hd::before,.hd::after{
  content:"";position:absolute;bottom:-22px;width:22px;height:22px;
  background:radial-gradient(circle at top right,transparent 22px,var(--ink) 22.5px);
  pointer-events:none;
}
.hd::before{left:0;background:radial-gradient(circle at top left,transparent 22px,var(--ink) 22.5px)}
.hd::after{right:0;background:radial-gradient(circle at top right,transparent 22px,var(--ink) 22.5px)}
.hd .container{display:flex;align-items:center;gap:32px;width:min(1280px,94vw)}
.brand{display:flex;align-items:center;gap:10px}
.brand img.k{height:34px;width:auto}
.brand img.wm{height:26px;width:auto;margin-top:2px}
.nav{display:flex;align-items:center;gap:6px;margin-left:auto}
.nav a{
  position:relative;font-weight:600;font-size:14.5px;letter-spacing:.01em;
  padding:8px 14px;color:#fff;border-radius:10px;
}
.nav a::after{
  content:"";position:absolute;left:14px;right:14px;bottom:2px;height:2px;
  background:var(--yellow);transform:scaleX(0);transform-origin:left;
  transition:transform .35s cubic-bezier(.6,.1,.3,1);
}
.nav a:hover::after,.nav a.active::after{transform:scaleX(1)}
.nav a.active{color:var(--yellow)}
.hd .nav a.cta, a.cta{
  display:inline-flex;align-items:center;gap:8px;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:15px;
  padding:9px 18px;border-radius:999px;background:var(--yellow);color:var(--ink);
  border:2.5px solid var(--ink);box-shadow:3px 4px 0 rgba(255,255,255,.18);
  transition:background .2s, transform .2s, box-shadow .2s, color .2s;
  margin-left:8px;
}
.hd .nav a.cta::after{display:none}
.hd .nav a.cta:hover, a.cta:hover{background:var(--magenta);color:#fff;transform:translateY(-2px);box-shadow:3px 6px 0 rgba(255,255,255,.25)}
.burger{display:none;margin-left:auto;width:38px;height:38px;border:2px solid #fff;border-radius:10px;align-items:center;justify-content:center}
.burger span{display:block;width:18px;height:2px;background:#fff;position:relative}
.burger span::before,.burger span::after{content:"";position:absolute;left:0;width:18px;height:2px;background:#fff}
.burger span::before{top:-6px}
.burger span::after{top:6px}

/* scroll progress bar */
.progress{
  position:fixed;top:var(--hd);left:0;height:3px;background:var(--yellow);z-index:88;
  width:0;transform-origin:left;will-change:transform;
}
@supports (animation-timeline:scroll()){
  .progress{
    width:100%;transform:scaleX(0);
    animation:prog linear;
    animation-timeline:scroll(root);
  }
  @keyframes prog{to{transform:scaleX(1)}}
}

/* ===== BUTTONS ===== */
.btn{
  display:inline-flex;align-items:center;gap:10px;
  font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:18px;
  padding:14px 26px;border-radius:999px;border:2.5px solid var(--ink);
  background:var(--white);color:var(--ink);
  box-shadow:var(--shadow-hard);
  transition:transform .2s ease, box-shadow .2s ease, background .25s ease;
  white-space:nowrap;
}
.btn:hover{transform:translate(-2px,-3px);box-shadow:10px 11px 0 var(--ink)}
.btn .arr{display:inline-block;transition:transform .25s}
.btn:hover .arr{transform:translateX(4px)}
.btn.mag{background:var(--magenta);color:#fff}
.btn.cyan{background:var(--cyan);color:var(--ink)}
.btn.lime{background:var(--lime);color:var(--ink)}
.btn.dark{background:var(--ink);color:#fff}
.btn.yellow{background:var(--yellow);color:var(--ink)}

/* eyebrow pill */
.eyebrow{
  display:inline-flex;align-items:center;gap:10px;
  background:var(--ink);color:var(--cream);
  padding:8px 18px 8px 14px;border-radius:999px;border:2.5px solid var(--ink);
  font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.04em;text-transform:uppercase;
  box-shadow:3px 4px 0 var(--ink);
}
.eyebrow .star{color:var(--yellow);font-size:14px;display:inline-block}

/* highlight boxes */
.hl{
  position:relative;display:inline-block;padding:0 .22em;border-radius:14px;
  transform:rotate(-1.5deg);color:var(--ink);
  background:var(--magenta);box-shadow:3px 4px 0 var(--ink);overflow:hidden;
  isolation:isolate;
}
.hl.cyan{background:var(--cyan)}
.hl.purple{background:var(--purple);color:#fff}
.hl.lime{background:var(--lime)}
.hl.orange{background:var(--orange);color:#fff}
.hl::after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.55) 48%,transparent 66%);
  transform:translateX(-120%);
  animation:shimmer 4.4s ease-in-out infinite;
  z-index:-1;mix-blend-mode:overlay;
}
@keyframes shimmer{0%,20%{transform:translateX(-120%)}55%,100%{transform:translateX(120%)}}

/* ===== HERO ===== */
.hero{padding:calc(var(--hd) + 56px) 0 80px;position:relative;overflow:hidden}
.hero h1{
  font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
  font-size:clamp(48px,8.4vw,128px);line-height:.96;letter-spacing:-.015em;
  margin:24px 0 28px;
}
.hero .sub{
  font-size:clamp(17px,1.5vw,21px);max-width:720px;line-height:1.55;color:#1a1812;opacity:.88;
}
.hero .ctas{display:flex;flex-wrap:wrap;gap:14px;margin-top:36px}
.trust{display:inline-flex;align-items:center;gap:10px;margin-top:30px;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:13px}
.trust .dot{width:10px;height:10px;border-radius:50%;background:#1aa84d;box-shadow:0 0 0 4px rgba(26,168,77,.18);animation:pulseDot 2.2s ease-in-out infinite}
@keyframes pulseDot{0%,100%{box-shadow:0 0 0 4px rgba(26,168,77,.18)}50%{box-shadow:0 0 0 8px rgba(26,168,77,.05)}}

/* doodles */
.doodles{position:absolute;inset:0;pointer-events:none;z-index:1}
.doodle{position:absolute;animation:float 7s ease-in-out infinite;transition:translate .35s cubic-bezier(.2,.6,.2,1);will-change:translate,transform}
.doodle.d2{animation-duration:9s;animation-delay:-2s}
.doodle.d3{animation-duration:11s;animation-delay:-4s}
.doodle.spin{animation:spin 22s linear infinite}
@keyframes float{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-18px) rotate(6deg)}}
@keyframes spin{to{transform:rotate(360deg)}}
@supports (animation-timeline:scroll()){
  .doodle.drift{animation:drift linear;animation-timeline:scroll(root);}
  @keyframes drift{to{transform:translateY(-280px) rotate(180deg)}}
}

/* idle pulse on hero buttons */
.hero .ctas .btn{animation:idlePulse 4.6s ease-in-out infinite}
.hero .ctas .btn:nth-child(2){animation-delay:.6s}
.hero .ctas .btn:nth-child(3){animation-delay:1.2s}
.hero .ctas .btn:hover{animation:none}
@keyframes idlePulse{0%,100%{transform:none}50%{transform:scale(1.018)}}

/* ===== MARQUEE ===== */
.marquee{
  background:var(--ink);color:#fff;padding:18px 0;
  transform:rotate(-2deg);margin:30px -3vw;overflow:hidden;
  border-block:2.5px solid var(--ink);
}
.marquee.alt{transform:rotate(1.6deg);background:var(--magenta);color:#fff}
.marquee.cyan{background:var(--cyan);color:var(--ink)}
.marquee.lime{background:var(--lime);color:var(--ink)}
.marquee-track{display:flex;gap:54px;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:30px;white-space:nowrap;animation:march 30s linear infinite;will-change:transform}
.marquee.fast .marquee-track{animation-duration:18s}
.marquee-track .dot{display:inline-block;width:14px;height:14px;border-radius:50%;background:var(--yellow);align-self:center}
.marquee.alt .marquee-track .dot{background:#fff}
.marquee.cyan .marquee-track .dot,.marquee.lime .marquee-track .dot{background:var(--ink)}
@keyframes march{to{transform:translateX(-50%)}}
@supports (animation-timeline:scroll()){
  .marquee.scrolly .marquee-track{animation:march 22s linear infinite, marchBoost linear;animation-timeline:auto, scroll(root);}
  @keyframes marchBoost{to{translate:-60px 0}}
}

/* ===== SECTION HEADINGS ===== */
.section{padding:96px 0;position:relative}
.section.dark{background:var(--ink);color:#fff}
.section-eyebrow{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:13px;letter-spacing:.18em;text-transform:uppercase;opacity:.7}
.section h2{
  font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
  font-size:clamp(38px,5.4vw,72px);line-height:1;letter-spacing:-.01em;
  margin:14px 0 32px;
}
.section .lead{font-size:18px;max-width:660px;line-height:1.55;opacity:.85}

/* ===== CARDS ===== */
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:54px}
.cards.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.cards.six{grid-template-columns:repeat(3,minmax(0,1fr))}
.card{
  background:var(--ink);color:#fff;border:2.5px solid var(--ink);border-radius:22px;
  padding:28px 26px 30px;display:flex;flex-direction:column;gap:14px;
  box-shadow:var(--shadow-mag);
  transition:transform .35s cubic-bezier(.4,.1,.2,1),box-shadow .35s;
  position:relative;overflow:hidden;
}
.card.cyan{box-shadow:var(--shadow-cyan)}
.card.lime{box-shadow:var(--shadow-lime)}
.card.purple{box-shadow:var(--shadow-purple)}
.card.orange{box-shadow:var(--shadow-orange)}
.card.blue{box-shadow:var(--shadow-blue)}
.card.yellow{box-shadow:var(--shadow-yellow)}
.card:hover{transform:translate(-3px,-5px);box-shadow:10px 12px 0 var(--magenta)}
.card.cyan:hover{box-shadow:10px 12px 0 var(--cyan)}
.card.lime:hover{box-shadow:10px 12px 0 var(--lime)}
.card.purple:hover{box-shadow:10px 12px 0 var(--purple)}
.card.orange:hover{box-shadow:10px 12px 0 var(--orange)}
.card.blue:hover{box-shadow:10px 12px 0 var(--blue)}
.card.yellow:hover{box-shadow:10px 12px 0 var(--yellow)}
.card .icon{
  width:54px;height:54px;border-radius:14px;background:var(--magenta);color:var(--ink);
  display:flex;align-items:center;justify-content:center;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:24px;
  box-shadow:2px 3px 0 #000;
}
.card .icon svg{width:28px;height:28px;stroke:var(--ink);fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.card.purple .icon svg, .card.orange .icon svg, .card.blue .icon svg{stroke:#fff}
.card .idx{position:absolute;top:18px;right:22px;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.12em;color:rgba(255,255,255,.35);font-weight:700}
.card.cyan .icon{background:var(--cyan)}
.card.lime .icon{background:var(--lime)}
.card.purple .icon{background:var(--purple);color:#fff}
.card.orange .icon{background:var(--orange);color:#fff}
.card.blue .icon{background:var(--blue);color:#fff}
.card.yellow .icon{background:var(--yellow)}
.card h3{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:24px;margin:6px 0 4px;letter-spacing:-.005em}
.card p{margin:0;font-size:15.5px;line-height:1.5;opacity:.84}
.card .arrow{margin-top:auto;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;display:inline-flex;align-items:center;gap:6px;color:var(--magenta)}
.card.cyan .arrow{color:var(--cyan)}
.card.lime .arrow{color:var(--lime)}
.card.purple .arrow{color:var(--purple)}

/* yellow card variant (for explore section) */
.card.solid{background:var(--yellow);color:var(--ink);box-shadow:var(--shadow-hard)}
.card.solid:hover{box-shadow:10px 12px 0 var(--ink)}
.card.solid .icon{background:var(--ink);color:var(--yellow)}
.card.solid .arrow{color:var(--ink)}

/* ===== REVEAL ===== */
.reveal{opacity:0;transform:translateY(40px);transition:opacity .65s ease, transform .65s cubic-bezier(.4,.1,.2,1)}
.reveal.in{opacity:1;transform:none}
.reveal.r2{transition-delay:.08s}
.reveal.r3{transition-delay:.16s}
.reveal.r4{transition-delay:.24s}
.reveal.r5{transition-delay:.32s}
.reveal.r6{transition-delay:.4s}

@supports (animation-timeline:view()){
  /* native scroll-driven enhancements */
  .reveal{animation:revealUp linear both;animation-timeline:view();animation-range:entry 0% cover 32%;}
  @keyframes revealUp{from{opacity:0;transform:translateY(48px)}to{opacity:1;transform:none}}

  .card{animation:cardIn linear both;animation-timeline:view();animation-range:entry 0% cover 28%;}
  @keyframes cardIn{from{opacity:0;transform:translateY(60px) rotate(-2deg) scale(.96)}to{opacity:1;transform:none}}

  .section h2{animation:titlePop linear both;animation-timeline:view();animation-range:entry 0% cover 30%;}
  @keyframes titlePop{from{opacity:0;transform:scale(.92) translateY(20px)}to{opacity:1;transform:none}}

  .hl{animation:hlPop linear both;animation-timeline:view();animation-range:entry 5% cover 22%;}
  @keyframes hlPop{from{transform:rotate(-1.5deg) scale(.7)}50%{transform:rotate(-1.5deg) scale(1.08)}to{transform:rotate(-1.5deg) scale(1)}}

  .scrolly-tilt{animation:scrollyTilt linear both;animation-timeline:view();animation-range:cover 0% cover 100%;}
  @keyframes scrollyTilt{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}

  .scale-on-view{animation:scaleOnView linear both;animation-timeline:view();animation-range:entry 0% cover 40%;}
  @keyframes scaleOnView{from{transform:scale(.6);opacity:0}to{transform:scale(1);opacity:1}}
}

/* ===== NOTICING / DARK BAND ===== */
.notice{background:var(--ink);color:#fff;padding:84px 0;text-align:center;position:relative;overflow:hidden}
.notice h2{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(34px,5vw,64px);line-height:1.05;margin:0 0 18px}
.notice p{max-width:680px;margin:0 auto;font-size:17px;opacity:.78;line-height:1.55}
.notice .bigK{position:absolute;right:-60px;top:-20px;width:280px;opacity:.06}
.notice .bigK2{position:absolute;left:-60px;bottom:-40px;width:240px;opacity:.06;transform:rotate(-12deg)}

/* ===== STATS BAND ===== */
.stats{background:var(--cream);padding:64px 0;border-block:3px solid var(--ink)}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-items:center}
.stat{text-align:center}
.stat .v{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(34px,4vw,54px);line-height:1}
.stat .l{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin-top:8px;opacity:.7}

/* ===== SCATTER PILLS ===== */
.scatter{position:relative;height:480px;margin:50px 0 10px}
.scatter .pill{
  position:absolute;display:inline-flex;align-items:center;gap:8px;
  background:var(--yellow);color:var(--ink);
  padding:11px 18px;border-radius:999px;border:2.5px solid var(--ink);
  font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:16px;
  box-shadow:4px 5px 0 var(--ink);
  opacity:0;transform:scale(.4);
  transition:opacity .55s ease, transform .55s cubic-bezier(.5,1.6,.4,1);
}
.scatter.in .pill{opacity:1;transform:scale(1)}
.scatter .pill.c2{background:var(--magenta);color:#fff}
.scatter .pill.c3{background:var(--cyan);color:var(--ink)}
.scatter .pill.c4{background:var(--lime);color:var(--ink)}
.scatter .pill.c5{background:var(--purple);color:#fff}
.scatter .pill.c6{background:var(--orange);color:#fff}
.scatter .pill.c7{background:var(--blue);color:#fff}
.scatter .pill.c8{background:var(--white);color:var(--ink)}

/* ===== CONTACT FORM ===== */
.form-wrap{
  background:var(--cream);color:var(--ink);
  border:3px solid var(--ink);border-radius:28px;
  box-shadow:10px 12px 0 var(--magenta);
  padding:36px;
}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.field{display:flex;flex-direction:column;gap:8px;margin-top:18px}
.field label{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.field input,.field select,.field textarea{
  font:inherit;font-size:16px;color:var(--ink);
  background:#fff;border:2.5px solid var(--ink);border-radius:14px;
  padding:14px 16px;outline:none;transition:transform .15s, box-shadow .15s;
}
.field textarea{min-height:130px;resize:vertical}
.field input:focus,.field select:focus,.field textarea:focus{transform:translate(-1px,-1px);box-shadow:3px 4px 0 var(--ink)}
.pill-toggles{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.pill-toggle{
  padding:10px 16px;border:2.5px solid var(--ink);border-radius:999px;background:#fff;
  font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:14.5px;
  transition:transform .15s, box-shadow .15s, background .15s;
}
.pill-toggle.on{background:var(--ink);color:#fff;box-shadow:3px 4px 0 var(--magenta)}
.honey{position:absolute;left:-9999px;opacity:0;pointer-events:none}
.submit{margin-top:26px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.form-status{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:13px}
.form-status.ok{color:#0a7a3a}
.form-status.err{color:#b8113b}

/* ===== FOOTER ===== */
.foot{background:var(--ink);color:#fff;padding:80px 0 36px;position:relative;overflow:hidden}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:40px;align-items:start}
.foot .wm{height:64px;width:auto;margin-bottom:22px}
.foot h4{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--yellow);margin:0 0 16px}
.foot ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;font-size:15.5px}
.foot a:hover{color:var(--yellow)}
.foot .tag{max-width:380px;opacity:.78;font-size:15.5px;line-height:1.55}
.foot-bottom{margin-top:54px;padding-top:24px;border-top:1px solid #2a2820;display:flex;justify-content:space-between;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.06em;opacity:.7;flex-wrap:wrap;gap:10px}
.foot .gigK{position:absolute;right:-100px;bottom:-100px;width:480px;opacity:.05;pointer-events:none}

/* page transition curtain */
.curtain{
  position:fixed;inset:0;background:var(--ink);z-index:120;pointer-events:none;
  clip-path:circle(0% at 50% 50%);
  transition:clip-path .55s cubic-bezier(.7,0,.3,1);
}
.curtain.in{clip-path:circle(150% at 50% 50%);pointer-events:auto}
.curtain.out{clip-path:circle(0% at 50% 50%);transition-duration:.45s}

/* ===== SCROLL-DRIVEN SPLASH (index landing only) ===== */
/* The splash-host is 180vh tall. .splash-stick sticks at top for ~1 viewport
   so the user can scroll-morph the K mark, wordmark, and tag away before
   they reach the home page below. JS sets --p (0 .. 1) based on scroll. */
.splash-host{
  height:180vh;position:relative;background:#0a0907;margin-top:calc(var(--hd) * -1);isolation:isolate;
}
.splash-stick{
  position:sticky;top:0;height:100vh;width:100%;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:radial-gradient(circle at 50% 40%, #1a1812 0%, #0a0907 75%);
  overflow:hidden;text-align:center;padding:24px;--p:0;
}
.splash-orb{position:absolute;border-radius:50%;filter:blur(140px);pointer-events:none;will-change:transform}
.splash-orb.o1{width:560px;height:560px;background:var(--magenta);top:-160px;left:-160px;opacity:.32;animation:orbA 9s ease-in-out infinite}
.splash-orb.o2{width:560px;height:560px;background:var(--cyan);bottom:-180px;right:-180px;opacity:.32;animation:orbB 11s ease-in-out infinite}
.splash-orb.o3{width:380px;height:380px;background:var(--lime);top:55%;left:30%;opacity:.22;animation:orbC 7s ease-in-out infinite}
@keyframes orbA{0%,100%{transform:none}50%{transform:translate(80px,60px) scale(1.2)}}
@keyframes orbB{0%,100%{transform:none}50%{transform:translate(-90px,-50px) scale(1.15)}}
@keyframes orbC{0%,100%{transform:none}50%{transform:translate(-30px,30px) scale(.85)}}
.splash-grid{
  position:absolute;inset:0;opacity:.07;pointer-events:none;
  background-image:linear-gradient(to right, #fff 1px, transparent 1px), linear-gradient(to bottom, #fff 1px, transparent 1px);
  background-size:80px 80px;
  -webkit-mask-image:radial-gradient(circle at center, #000 30%, transparent 80%);
  mask-image:radial-gradient(circle at center, #000 30%, transparent 80%);
}
.splash-content{position:relative;z-index:3;max-width:780px}
.splash-eyebrow{
  display:inline-flex;align-items:center;gap:10px;
  font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.28em;text-transform:uppercase;
  color:rgba(255,255,255,.62);margin-bottom:36px;
  padding:8px 16px;border:1px solid rgba(255,255,255,.18);border-radius:999px;backdrop-filter:blur(8px);
}
.splash-eyebrow .star{color:var(--yellow)}
.splash-bigk{
  width:clamp(160px,18vw,240px);height:auto;display:block;margin:0 auto;
  will-change:transform,opacity;filter:drop-shadow(0 20px 60px rgba(244,225,26,.18));
  transform: scale(calc(1 - var(--p) * 0.55)) rotate(calc(var(--p) * 540deg)) translateY(calc(var(--p) * -120px));
  opacity: calc(1 - var(--p) * 1.3);
}
.splash-bigwm{
  height:clamp(48px,5vw,80px);width:auto;display:block;margin:34px auto 18px;
  will-change:transform,opacity;
  transform: translateY(calc(var(--p) * -80px)) scale(calc(1 - var(--p) * 0.4));
  opacity: calc(1 - var(--p) * 1.9);
}
.splash-tag{
  font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
  font-size:clamp(22px,2.6vw,38px);line-height:1.1;letter-spacing:-.02em;
  color:#fff;margin:14px auto 10px;max-width:640px;
  will-change:transform,opacity;
  transform: translateY(calc(var(--p) * -60px));
  opacity: calc(1 - var(--p) * 1.9);
}
.splash-tag .hl{display:inline-block;padding:0 .18em;border-radius:8px;transform:rotate(-1.5deg)}
.splash-tag .hl.mag{background:var(--magenta);color:var(--ink)}
.splash-tag .hl.cyan{background:var(--cyan);color:var(--ink)}
.splash-tag .hl.purple{background:var(--purple);color:#fff}
.splash-sub{
  font-family:'Hanken Grotesk',sans-serif;font-size:15.5px;
  color:rgba(255,255,255,.62);margin:6px auto 0;max-width:520px;line-height:1.55;
  opacity: calc(1 - var(--p) * 2.4);
}
.splash-eyebrow{opacity: calc(1 - var(--p) * 2.4)}
.scroll-hint{
  position:absolute;bottom:48px;left:50%;transform:translateX(-50%);
  font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.32em;text-transform:uppercase;
  color:rgba(255,255,255,.55);display:flex;flex-direction:column;align-items:center;gap:14px;z-index:3;
  opacity: calc(1 - var(--p) * 3);
}
.scroll-hint .mouse{
  width:24px;height:38px;border:1.5px solid rgba(255,255,255,.55);border-radius:14px;position:relative;
}
.scroll-hint .mouse::after{
  content:"";position:absolute;top:7px;left:50%;width:3px;height:7px;background:rgba(255,255,255,.7);
  border-radius:2px;transform:translateX(-50%);animation:mouseDot 1.4s ease-in-out infinite;
}
@keyframes mouseDot{0%,100%{transform:translate(-50%,0);opacity:1}50%{transform:translate(-50%,12px);opacity:.3}}
/* Mask the page header behind the splash until user scrolls into the second viewport */
.splash-host ~ .hd{transition: opacity .35s ease}
body.splash-active .hd{opacity:0;pointer-events:none}

/* sticky watermark K */
.watermark{
  position:fixed;right:-90px;bottom:-90px;width:380px;
  opacity:.06;pointer-events:none;z-index:1;will-change:transform;
  transform:rotate(0deg);
}
@supports (animation-timeline:scroll()){
  .watermark{animation:wmRotate linear;animation-timeline:scroll(root);}
  @keyframes wmRotate{from{transform:rotate(0deg) scale(1)}to{transform:rotate(540deg) scale(1.35)}}
}

/* ===== ADVANCED SCROLL-DRIVEN ANIMATIONS ===== */
@supports (animation-timeline:view()) and (animation-timeline:scroll()){
  /* Hero text scales down and fades as user scrolls past */
  .hero h1{
    animation: heroOutH1 linear both;
    animation-timeline: view();
    animation-range: exit 0% exit 100%;
  }
  @keyframes heroOutH1{
    from{transform:none;opacity:1;letter-spacing:-.015em}
    to{transform:translateY(-90px) scale(.7);opacity:.18;letter-spacing:.04em}
  }
  .hero .sub{
    animation: heroOutSub linear both;
    animation-timeline: view();
    animation-range: exit 0% exit 70%;
  }
  @keyframes heroOutSub{
    from{transform:none;opacity:1}
    to{transform:translateY(-60px);opacity:0}
  }
  .hero .ctas{
    animation: heroOutCtas linear both;
    animation-timeline: view();
    animation-range: exit 0% exit 85%;
  }
  @keyframes heroOutCtas{
    from{transform:none;opacity:1}
    to{transform:translateY(-40px) scale(.9);opacity:.2}
  }

  /* 3D card entries override the simpler card-in */
  .card{
    animation: card3d linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 36%;
  }
  @keyframes card3d{
    from{opacity:0;transform:perspective(900px) translateY(80px) rotateY(22deg) rotateX(8deg) scale(.92)}
    60%{opacity:1;transform:perspective(900px) translateY(0) rotateY(-3deg) rotateX(-1deg) scale(1.02)}
    to{opacity:1;transform:perspective(900px) translateY(0) rotateY(0) rotateX(0) scale(1)}
  }
  .cards .card:nth-child(even){animation-name:card3dAlt}
  @keyframes card3dAlt{
    from{opacity:0;transform:perspective(900px) translateY(80px) rotateY(-22deg) rotateX(8deg) scale(.92)}
    60%{opacity:1;transform:perspective(900px) translateY(0) rotateY(3deg) rotateX(-1deg) scale(1.02)}
    to{opacity:1;transform:perspective(900px) translateY(0) rotateY(0) rotateX(0) scale(1)}
  }

  /* Section h2 slides in from left dramatically */
  .section h2{
    animation: bigEntry linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 40%;
  }
  @keyframes bigEntry{
    from{opacity:0;transform:translateX(-80px) rotate(-2deg) scale(.9)}
    to{opacity:1;transform:none}
  }

  /* Stat numbers POP on view */
  .stat .v{
    animation: statPop linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 50%;
  }
  @keyframes statPop{
    from{opacity:0;transform:scale(.35) rotate(-12deg);color:var(--magenta)}
    55%{transform:scale(1.18) rotate(2deg);color:var(--magenta)}
    to{opacity:1;transform:scale(1) rotate(0);color:var(--ink)}
  }
  .stat:nth-child(2) .v{animation-name:statPop2}
  @keyframes statPop2{
    from{opacity:0;transform:scale(.35) rotate(12deg);color:var(--cyan)}
    55%{transform:scale(1.18) rotate(-2deg);color:var(--cyan)}
    to{opacity:1;transform:scale(1) rotate(0);color:var(--ink)}
  }
  .stat:nth-child(3) .v{animation-name:statPop3}
  @keyframes statPop3{
    from{opacity:0;transform:scale(.35) rotate(-12deg);color:var(--purple)}
    55%{transform:scale(1.18) rotate(2deg);color:var(--purple)}
    to{opacity:1;transform:scale(1) rotate(0);color:var(--ink)}
  }
  .stat:nth-child(4) .v{animation-name:statPop4}
  @keyframes statPop4{
    from{opacity:0;transform:scale(.35) rotate(12deg);color:var(--lime)}
    55%{transform:scale(1.18) rotate(-2deg);color:var(--lime)}
    to{opacity:1;transform:scale(1) rotate(0);color:var(--ink)}
  }

  /* Doodle parallax layers (different speeds) */
  .doodle.drift{
    animation: drift linear;
    animation-timeline: scroll(root);
  }
  @keyframes drift{to{transform:translateY(-420px) rotate(220deg)}}
  .doodle.d2.drift{
    animation: drift2 linear;
    animation-timeline: scroll(root);
  }
  @keyframes drift2{to{transform:translateY(-260px) rotate(-180deg)}}

  /* Marquee gets extra translateX boost from page scroll */
  .marquee.scrolly .marquee-track{
    animation: march 22s linear infinite, marqueeBoost linear;
    animation-timeline: auto, scroll(root);
  }
  @keyframes marqueeBoost{to{translate:-260px 0}}

  /* Dark "notice" section: big text pulse on view */
  .notice h2{
    animation: noticePop linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 50%;
  }
  @keyframes noticePop{
    from{opacity:0;transform:scale(.7) translateY(40px);letter-spacing:.08em}
    60%{opacity:1;transform:scale(1.04) translateY(0);letter-spacing:-.02em}
    to{opacity:1;transform:scale(1) translateY(0);letter-spacing:-.005em}
  }

  /* Eyebrow rotates in */
  .eyebrow{
    animation: eyebrowIn linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 22%;
  }
  @keyframes eyebrowIn{
    from{opacity:0;transform:rotate(-6deg) translateX(-30px) scale(.85)}
    to{opacity:1;transform:none}
  }

  /* Big background K in notice tilts with scroll */
  .notice .bigK, .notice .bigK2{
    animation: noticeKfloat linear;
    animation-timeline: view();
    animation-range: cover 0% cover 100%;
  }
  @keyframes noticeKfloat{from{transform:rotate(-15deg) scale(.9)}to{transform:rotate(25deg) scale(1.2)}}

  /* Buttons in hero get a final flourish */
  .hero .ctas .btn{
    animation: idlePulse 4.6s ease-in-out infinite, btnRiseIn linear both;
    animation-timeline: auto, view();
    animation-range: auto, entry 0% cover 30%;
  }
  @keyframes btnRiseIn{from{opacity:0;transform:translateY(30px) rotate(-3deg)}to{opacity:1;transform:none}}
}

/* ===== STICKY PILLAR SHOWCASE (sticky CSS based) ===== */
.pillar-sticky{padding:120px 0;position:relative}
.pillar-sticky .container{display:grid;grid-template-columns:1fr 1.1fr;gap:60px;align-items:start}
.pillar-sticky .stuck{position:sticky;top:calc(var(--hd) + 40px)}
.pillar-sticky h2{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(38px,5vw,62px);line-height:1;margin:0 0 18px}
.pillar-sticky .lead{font-size:17px;opacity:.85;line-height:1.55;max-width:440px}
.pillar-list{display:flex;flex-direction:column;gap:24px}
.pillar-row{
  background:var(--ink);color:#fff;border-radius:22px;padding:32px 28px 32px;
  border:2.5px solid var(--ink);box-shadow:var(--shadow-mag);
  display:grid;grid-template-columns:auto 1fr auto;gap:22px;align-items:center;
  transition:transform .35s, box-shadow .35s;
}
.pillar-row.cyan{box-shadow:var(--shadow-cyan)}
.pillar-row.lime{box-shadow:var(--shadow-lime)}
.pillar-row:hover{transform:translate(-4px,-6px);box-shadow:12px 14px 0 var(--magenta)}
.pillar-row.cyan:hover{box-shadow:12px 14px 0 var(--cyan)}
.pillar-row.lime:hover{box-shadow:12px 14px 0 var(--lime)}
.pillar-row .badge{width:62px;height:62px;border-radius:18px;background:var(--magenta);color:var(--ink);display:flex;align-items:center;justify-content:center;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:24px;box-shadow:2px 3px 0 #000;flex-shrink:0}
.pillar-row .badge svg{width:30px;height:30px;stroke:var(--ink);fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.pillar-row.cyan .badge{background:var(--cyan)}
.pillar-row.lime .badge{background:var(--lime)}
.pillar-row h3{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:26px;margin:0 0 4px}
.pillar-row p{margin:0;font-size:15px;line-height:1.5;opacity:.84}
.pillar-row .go{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:18px;color:var(--magenta)}
.pillar-row.cyan .go{color:var(--cyan)}
.pillar-row.lime .go{color:var(--lime)}
@media (max-width:920px){.pillar-sticky .container{grid-template-columns:1fr}.pillar-sticky .stuck{position:relative;top:auto}}

/* ===== UTILITIES ===== */
.row{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.muted{opacity:.78}
.spacer{height:60px}
.center{text-align:center}
.tag-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.tag{
  padding:7px 14px;border-radius:999px;background:#fff;color:var(--ink);
  border:2.5px solid var(--ink);font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:14px;
}

/* responsive */
@media (max-width:920px){
  .cards,.cards.six{grid-template-columns:repeat(2,minmax(0,1fr))}
  .form-row{grid-template-columns:1fr}
  .foot-grid{grid-template-columns:1fr;gap:34px}
  .stats-grid{grid-template-columns:repeat(2,1fr);gap:30px}
}
@media (max-width:680px){
  .nav{display:none}
  .nav.open{display:flex;position:absolute;top:62px;left:0;right:0;background:var(--ink);flex-direction:column;padding:18px;gap:6px;border-bottom:3px solid var(--yellow)}
  .nav.open a{padding:12px 14px}
  .burger{display:inline-flex}
  .cards,.cards.six,.cards.two{grid-template-columns:1fr}
  .stats-grid{grid-template-columns:1fr;gap:24px}
  .hero{padding-top:calc(var(--hd) + 32px);padding-bottom:48px}
  .form-wrap{padding:24px}
}

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  .reveal{opacity:1;transform:none}
  .scatter .pill{opacity:1;transform:none}
}
"""

# ------------------------------------------------------------------ COMMON JS
COMMON_JS = r"""
(()=>{
  // === Scroll-driven splash (index landing). Other pages have no splash at all.
  const splashHost  = document.getElementById('splash-host');
  const splashStick = document.getElementById('splash-stick');
  if(splashHost && splashStick){
    document.body.classList.add('splash-active');
    const updateSplash = ()=>{
      const rect = splashHost.getBoundingClientRect();
      // p: how far we've scrolled into the splash-host. 0 at top of host, 1 when stick releases.
      const total = splashHost.offsetHeight - window.innerHeight;
      const scrolled = Math.max(0, -rect.top);
      const p = Math.min(1, Math.max(0, scrolled / Math.max(1,total)));
      splashStick.style.setProperty('--p', p.toFixed(4));
      // Once mostly scrolled past, re-enable the page header.
      if(p > 0.55){
        document.body.classList.remove('splash-active');
      } else {
        document.body.classList.add('splash-active');
      }
    };
    let st=false;
    window.addEventListener('scroll', ()=>{
      if(st) return;
      st=true;
      requestAnimationFrame(()=>{updateSplash(); st=false;});
    }, {passive:true});
    window.addEventListener('resize', updateSplash);
    updateSplash();
  }

  // === Cursor-reactive doodle parallax. Each .doodle drifts a little
  //     based on mouse position, weighted by data-parallax (default 1).
  const doodles = document.querySelectorAll('.doodle');
  if(doodles.length){
    let mx = window.innerWidth/2, my = window.innerHeight/2;
    let raf=false;
    const apply = ()=>{
      const cx = window.innerWidth/2, cy = window.innerHeight/2;
      const dx = (mx - cx) / cx;  // -1..1
      const dy = (my - cy) / cy;
      doodles.forEach(d=>{
        const s = parseFloat(d.dataset.parallax || '1');
        // 'translate' (the individual CSS prop) keeps 'transform' free for keyframe animations
        d.style.translate = (dx * 24 * s).toFixed(2)+'px ' + (dy * 24 * s).toFixed(2)+'px';
      });
      raf=false;
    };
    window.addEventListener('mousemove', e=>{
      mx = e.clientX; my = e.clientY;
      if(!raf){ raf=true; requestAnimationFrame(apply); }
    }, {passive:true});
    // Touch fallback: nudge from device orientation if available
    window.addEventListener('deviceorientation', e=>{
      mx = window.innerWidth/2 + (e.gamma||0) * 4;
      my = window.innerHeight/2 + (e.beta||0) * 2;
      if(!raf){ raf=true; requestAnimationFrame(apply); }
    });
  }

  // === Page transition curtain
  const curtain = document.querySelector('.curtain');
  if(curtain){
    requestAnimationFrame(()=>curtain.classList.remove('in'));
    document.addEventListener('click', e=>{
      const a = e.target.closest('a');
      if(!a) return;
      const href = a.getAttribute('href') || '';
      if(!href.endsWith('.html') || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey) return;
      if(a.origin && a.origin !== location.origin) return;
      e.preventDefault();
      curtain.classList.add('in');
      setTimeout(()=>{ location.href = href; }, 480);
    });
  }

  // === Header scroll state + JS fallback progress (when scroll-timeline unsupported)
  const hd = document.querySelector('.hd');
  const prog = document.querySelector('.progress');
  const supportsScrollTimeline = CSS && CSS.supports && CSS.supports('animation-timeline:scroll()');
  let ticking = false;
  function onScroll(){
    if(ticking) return;
    ticking = true;
    requestAnimationFrame(()=>{
      const y = window.scrollY;
      if(hd) hd.classList.toggle('scrolled', y>20);
      if(!supportsScrollTimeline && prog){
        const docH = document.documentElement.scrollHeight - window.innerHeight;
        prog.style.width = (docH>0 ? (y/docH*100) : 0) + '%';
      }
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  // === Reveal observer (fallback / progressive)
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(en=>{
      if(en.isIntersecting){
        en.target.classList.add('in');
        if(en.target.classList.contains('scatter')){
          en.target.querySelectorAll('.pill').forEach((p,i)=> p.style.transitionDelay = (i*0.06)+'s');
        }
      }
    });
  }, {threshold:.15, rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.reveal, .scatter').forEach(el=> io.observe(el));

  // === Mobile nav
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  if(burger && nav){
    burger.addEventListener('click', ()=> nav.classList.toggle('open'));
    nav.addEventListener('click', e=>{ if(e.target.tagName==='A') nav.classList.remove('open'); });
  }

  // === Pill toggles (interest field)
  document.querySelectorAll('.pill-toggle').forEach(p=>{
    p.addEventListener('click', ()=> p.classList.toggle('on'));
  });

  // === Contact form -> Discord webhook
  const form = document.getElementById('contact-form');
  if(form){
    const statusEl = form.querySelector('.form-status');
    const WEBHOOK = 'https://discord.com/api/webhooks/1521226169632948417/HGOAwERYCvvjd1uSSEF8nzMaX_p5xZyWla9EEJY-aGeYzPLxku7A52QTDnEg277IBdPj';
    form.addEventListener('submit', async e=>{
      e.preventDefault();
      if(form.elements['company_url'].value){ return; } // honeypot
      const data = new FormData(form);
      const interests = [...form.querySelectorAll('.pill-toggle.on')].map(p=>p.textContent.trim()).join(', ') || 'Not specified';
      const embed = {
        title: 'New Kraftics inquiry',
        color: 0xFF3DA5,
        fields: [
          {name:'Name',  value:data.get('name')||'—', inline:true},
          {name:'Email', value:data.get('email')||'—', inline:true},
          {name:'Brand / Company', value:data.get('brand')||'—', inline:true},
          {name:'Website', value:data.get('website')||'—', inline:true},
          {name:'Interested in', value:interests, inline:false},
          {name:'Budget', value:data.get('budget')||'—', inline:true},
          {name:'Timeline', value:data.get('timeline')||'—', inline:true},
          {name:'Goals', value:(data.get('goals')||'—').slice(0,1000), inline:false},
        ],
        timestamp: new Date().toISOString(),
        footer: {text:'kraftics.com'}
      };
      const payload = JSON.stringify({content:null, embeds:[embed], username:'Kraftics site'});
      const fd = new FormData();
      fd.append('payload_json', payload);
      statusEl.textContent = 'Sending...';
      statusEl.className = 'form-status';
      try{
        const r = await fetch(WEBHOOK, {method:'POST', body:fd});
        if(r.ok){
          statusEl.textContent = 'Thanks. We will get back to you within 1 business day.';
          statusEl.className = 'form-status ok';
          form.reset();
          form.querySelectorAll('.pill-toggle.on').forEach(p=>p.classList.remove('on'));
        } else {
          throw new Error('webhook ' + r.status);
        }
      } catch(err){
        statusEl.innerHTML = 'Could not send. Email us directly at <a href="mailto:hi@kraftics.com" style="color:inherit;text-decoration:underline">hi@kraftics.com</a>.';
        statusEl.className = 'form-status err';
      }
    });
  }
})();
"""

# ------------------------------------------------------------------ HEADER / FOOTER

def header(active):
    items = [
        ("organic-marketing.html", "Organic Marketing"),
        ("ai-automation.html",     "AI Automation"),
        ("web-development.html",   "Web Development"),
    ]
    links = "\n            ".join(
        f'<a href="{h}" class="{"active" if h==active else ""}">{label}</a>'
        for h, label in items
    )
    return f"""
  <header class="hd">
    <div class="container">
      <a href="index.html" class="brand" aria-label="Kraftics home">
        <img src="{K_WHITE}" alt="" class="k">
        <img src="{WORDMARK_WHITE}" alt="Kraftics" class="wm">
      </a>
      <button class="burger" aria-label="Open menu"><span></span></button>
      <nav class="nav" aria-label="Primary">
        {links}
        <a href="index.html#partner" class="cta">Let's talk <span class="arr">&rarr;</span></a>
      </nav>
    </div>
  </header>
  <div class="progress" aria-hidden="true"></div>
"""

FOOTER = f"""
  <footer class="foot">
    <img src="{K_WHITE}" alt="" class="gigK" aria-hidden="true">
    <div class="container">
      <div class="foot-grid">
        <div>
          <img src="{WORDMARK_WHITE}" alt="Kraftics" class="wm">
          <p class="tag">Grow Smarter. Build Better. Scale Faster.</p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="organic-marketing.html">Organic Marketing</a></li>
            <li><a href="ai-automation.html">AI Automation</a></li>
            <li><a href="web-development.html">Web Development</a></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul>
            <li><a href="mailto:hi@kraftics.com">hi@kraftics.com</a></li>
            <li><a href="https://kraftics.com">kraftics.com</a></li>
            <li><a href="index.html#partner">Start a project</a></li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <span>© 2026 Kraftics. All rights reserved.</span>
        <span>kraftics.com</span>
      </div>
    </div>
  </footer>
"""

# Card icons — distinct vector mark per service tile.
ICON_SVGS = {
    "broadcast":  '<svg viewBox="0 0 24 24"><path d="M5 12a7 7 0 0114 0"/><path d="M8.5 12a3.5 3.5 0 017 0"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/><path d="M12 14v6"/></svg>',
    "users":      '<svg viewBox="0 0 24 24"><circle cx="9" cy="10" r="3"/><path d="M3 19a6 6 0 0112 0"/><circle cx="17" cy="8" r="2.4"/><path d="M14 19a5 5 0 017-4.6"/></svg>',
    "slide":      '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="13" rx="2"/><path d="M3 9h18"/><path d="M8 14l2 2 5-5"/></svg>',
    "spark":      '<svg viewBox="0 0 24 24"><path d="M12 3v6M3 12h6M21 12h-6M12 21v-6"/><circle cx="12" cy="12" r="2.6"/></svg>',
    "globe":      '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.8 3.2 2.8 14 0 18M12 3c-2.8 3.2-2.8 14 0 18"/></svg>',
    "chart":      '<svg viewBox="0 0 24 24"><path d="M4 20V8M10 20V4M16 20v-8M22 20H2"/></svg>',
    "robot":      '<svg viewBox="0 0 24 24"><rect x="4" y="6" width="16" height="13" rx="3"/><path d="M12 3v3"/><circle cx="9" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="15" cy="12" r="1.4" fill="currentColor" stroke="none"/><path d="M9 16h6"/></svg>',
    "workflow":   '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="6" height="6" rx="1.5"/><rect x="15" y="4" width="6" height="6" rx="1.5"/><rect x="9" y="14" width="6" height="6" rx="1.5"/><path d="M9 7h6M6 10v4M18 10v4M6 14h12"/></svg>',
    "dashboard":  '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/><circle cx="15" cy="14" r="2"/></svg>',
    "leads":      '<svg viewBox="0 0 24 24"><path d="M4 7h16v10H4z"/><path d="M4 7l8 6 8-6"/><path d="M7 21l5-4 5 4"/></svg>',
    "social":     '<svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><path d="M8 8l3 8M16 8l-3 8"/></svg>',
    "plug":       '<svg viewBox="0 0 24 24"><path d="M9 3v5M15 3v5"/><rect x="6" y="8" width="12" height="6" rx="2"/><path d="M12 14v3a4 4 0 004 4"/></svg>',
    "browser":    '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/><circle cx="6.5" cy="6.5" r=".8" fill="currentColor" stroke="none"/><circle cx="9" cy="6.5" r=".8" fill="currentColor" stroke="none"/></svg>',
    "rocket":     '<svg viewBox="0 0 24 24"><path d="M12 3c5 0 9 4 9 9-3 0-5 1-7 3l-5-5c2-2 3-4 3-7z"/><circle cx="15" cy="9" r="1.4" fill="currentColor" stroke="none"/><path d="M5 19c0-2 1-3 3-3M3 21c0-3 2-5 5-5"/></svg>',
    "calendar":   '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><circle cx="12" cy="15" r="1.5" fill="currentColor" stroke="none"/></svg>',
    "tune":       '<svg viewBox="0 0 24 24"><path d="M4 8h10M16 8h4M4 16h4M10 16h10"/><circle cx="15" cy="8" r="2"/><circle cx="9" cy="16" r="2"/></svg>',
    "code":       '<svg viewBox="0 0 24 24"><path d="M9 8l-5 4 5 4M15 8l5 4-5 4M14 5l-4 14"/></svg>',
    "magnet":     '<svg viewBox="0 0 24 24"><path d="M4 5v7a8 8 0 0016 0V5h-5v7a3 3 0 01-6 0V5z"/></svg>',
}
def icon(name):
    return ICON_SVGS.get(name, ICON_SVGS["spark"])

# Small inline doodle SVGs (these don't replace icon libraries, they're decorative stickers per the brief)
STAR_SVG  = '<svg viewBox="0 0 60 60" width="60" height="60" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M30 2 36 22 56 22 40 34 46 54 30 42 14 54 20 34 4 22 24 22Z"/></svg>'
SMILE_SVG = '<svg viewBox="0 0 64 64" width="64" height="64" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="28" fill="currentColor"/><circle cx="23" cy="27" r="3.2" fill="#100F0A"/><circle cx="41" cy="27" r="3.2" fill="#100F0A"/><path d="M20 38c3 6 9 9 12 9s9-3 12-9" fill="none" stroke="#100F0A" stroke-width="3.2" stroke-linecap="round"/></svg>'
SQUIG_SVG = '<svg viewBox="0 0 80 60" width="80" height="60" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"><path d="M6 36 C 18 14, 32 60, 44 30 S 68 6, 76 30"/></svg>'
SPARK_SVG = '<svg viewBox="0 0 40 40" width="40" height="40" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M20 0 L24 16 L40 20 L24 24 L20 40 L16 24 L0 20 L16 16Z"/></svg>'
BLOB_SVG = '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M52,8 C70,4 92,16 94,38 C96,60 80,76 64,82 C46,90 22,86 12,68 C2,50 10,28 24,16 C34,8 42,10 52,8Z"/></svg>'

def doodles_hero():
    return f"""
    <div class="doodles" aria-hidden="true">
      <div class="doodle drift"   data-parallax="1.6" style="top:18%;left:6%;color:var(--magenta)">{STAR_SVG}</div>
      <div class="doodle d2 drift" data-parallax="1.2" style="top:30%;right:8%;color:var(--cyan)">{SMILE_SVG}</div>
      <div class="doodle d3 spin"  data-parallax="2.2" style="bottom:14%;left:9%;color:var(--purple)">{SPARK_SVG}</div>
      <div class="doodle d2"      data-parallax="2.0" style="top:65%;right:14%;color:var(--lime)">{SQUIG_SVG}</div>
      <div class="doodle drift"   data-parallax="1.4" style="top:8%;right:28%;color:var(--orange)">{SPARK_SVG}</div>
      <div class="doodle d3"      data-parallax="0.8" style="bottom:24%;right:6%;color:var(--blue);opacity:.55">{BLOB_SVG}</div>
    </div>
    """

# ------------------------------------------------------------------ SPLASH (index only)
SPLASH_HTML = f"""
<section class="splash-host" id="splash-host">
  <div class="splash-stick" id="splash-stick">
    <span class="splash-orb o1"></span>
    <span class="splash-orb o2"></span>
    <span class="splash-orb o3"></span>
    <div class="splash-grid"></div>
    <div class="splash-content">
      <span class="splash-eyebrow"><span class="star">&#10022;</span> Welcome to Kraftics</span>
      <img src="{K_WHITE}" alt="" class="splash-bigk">
      <img src="{WORDMARK_WHITE}" alt="Kraftics" class="splash-bigwm">
      <p class="splash-tag">Grow <span class="hl mag">Smarter.</span> Build <span class="hl cyan">Better.</span> Scale <span class="hl purple">Faster.</span></p>
      <p class="splash-sub">Organic marketing, AI automation, and websites that do real work. Built for businesses that want growth on purpose, not by accident.</p>
    </div>
    <div class="scroll-hint" aria-hidden="true">
      <div class="mouse"></div>
      <span>Scroll to enter</span>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ PAGE SHELL
def shell(title, description, active, body, splash=False):
    splash_block = SPLASH_HTML if splash else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/png" href="{FAVICON}">
<style>{THEME_CSS}</style>
</head>
<body>
{splash_block}
<div class="curtain in" aria-hidden="true"></div>
<img src="{K_BLACK}" alt="" class="watermark" aria-hidden="true">
{header(active)}
{body}
{FOOTER}
<script>{COMMON_JS}</script>
</body>
</html>
"""

# ====================================================================== INDEX

INDEX_BODY = f"""
<main>
  <section class="hero">
    {doodles_hero()}
    <div class="container" style="position:relative;z-index:2">
      <span class="eyebrow"><span class="star">&#9733;</span> Organic Marketing &middot; AI Automation &middot; Web Development</span>
      <h1>Grow <span class="hl">Smarter.</span><br>Build <span class="hl cyan">Better.</span> Scale <span class="hl purple">Faster.</span></h1>
      <p class="sub">Kraftics builds the systems that help modern businesses capture attention, cut the busywork, and turn clicks into customers. Pick where you want to start.</p>
      <div class="ctas">
        <a class="btn mag" href="organic-marketing.html">Organic Marketing <span class="arr">&rarr;</span></a>
        <a class="btn cyan" href="ai-automation.html">AI Automation <span class="arr">&rarr;</span></a>
        <a class="btn lime" href="web-development.html">Web Development <span class="arr">&rarr;</span></a>
      </div>
      <div class="trust"><span class="dot"></span> Currently onboarding new partners</div>
    </div>
  </section>

  <div class="marquee scrolly" aria-hidden="true">
    <div class="marquee-track">
      <span>Organic reach</span><span class="dot"></span>
      <span>AI workflows</span><span class="dot"></span>
      <span>Conversion sites</span><span class="dot"></span>
      <span>Creator distribution</span><span class="dot"></span>
      <span>Live dashboards</span><span class="dot"></span>
      <span>Lead capture</span><span class="dot"></span>
      <span>Organic reach</span><span class="dot"></span>
      <span>AI workflows</span><span class="dot"></span>
      <span>Conversion sites</span><span class="dot"></span>
      <span>Creator distribution</span><span class="dot"></span>
      <span>Live dashboards</span><span class="dot"></span>
      <span>Lead capture</span><span class="dot"></span>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <span class="section-eyebrow reveal">// Three ways we help you grow</span>
      <h2 class="reveal">Three pillars.<br>One growth system.</h2>
      <p class="lead reveal">Each side stands on its own, and they get stronger when you stack them. Tap a card to see how it works.</p>

      <div class="cards">
        <a class="card reveal r2" href="organic-marketing.html">
          <div class="icon">{icon("broadcast")}</div>
          <h3>Organic Marketing</h3>
          <p>One brand message turned into hundreds of organic touchpoints, published by real creators across every major platform.</p>
          <span class="arrow">See how it works &rarr;</span>
        </a>
        <a class="card cyan reveal r3" href="ai-automation.html">
          <div class="icon">{icon("robot")}</div>
          <h3>AI Automation</h3>
          <p>Custom AI workflows and dashboards that connect your tools, handle repetitive work, and show what is working.</p>
          <span class="arrow">See how it works &rarr;</span>
        </a>
        <a class="card lime reveal r4" href="web-development.html">
          <div class="icon">{icon("browser")}</div>
          <h3>Web Development</h3>
          <p>Conversion-focused websites and landing pages, built to capture leads and plug into your systems.</p>
          <span class="arrow">See how it works &rarr;</span>
        </a>
      </div>
    </div>
  </section>

  <section class="pillar-sticky">
    <div class="container">
      <div class="stuck">
        <span class="section-eyebrow reveal">// Scroll to see how it stacks</span>
        <h2 class="reveal">One growth system. Three moving parts.</h2>
        <p class="lead reveal">Pick one to start. Stack the others when you are ready. Each one is built to compound on the next.</p>
        <div style="margin-top:28px"><a class="btn dark" href="#partner">Plan my system <span class="arr">&rarr;</span></a></div>
      </div>
      <div class="pillar-list">
        <a class="pillar-row" href="organic-marketing.html">
          <div class="badge">{icon("broadcast")}</div>
          <div><h3>Organic Marketing</h3><p>Creator-led distribution and UGC that turns one story into hundreds of native touchpoints, every week.</p></div>
          <span class="go">&rarr;</span>
        </a>
        <a class="pillar-row cyan" href="ai-automation.html">
          <div class="badge">{icon("robot")}</div>
          <div><h3>AI Automation</h3><p>Custom workflows and dashboards that connect your stack, handle the busywork, and surface what matters.</p></div>
          <span class="go">&rarr;</span>
        </a>
        <a class="pillar-row lime" href="web-development.html">
          <div class="badge">{icon("browser")}</div>
          <div><h3>Web Development</h3><p>Conversion-first sites and landing pages, wired into your CRM the moment they go live.</p></div>
          <span class="go">&rarr;</span>
        </a>
      </div>
    </div>
  </section>

  <section class="notice">
    <img src="{K_WHITE}" alt="" class="bigK">
    <img src="{K_WHITE}" alt="" class="bigK2">
    <div class="container">
      <h2 class="reveal">Every result starts with someone noticing you.</h2>
      <p class="reveal r2">Kraftics is named for that first spark of attention. The seconds before a stranger decides you matter. We design the systems that turn that spark into a habit, a click, and a customer.</p>
    </div>
  </section>

  <section class="section dark" id="partner" style="padding-top:90px">
    <div class="container">
      <span class="section-eyebrow reveal" style="color:var(--yellow)">// Partner with us</span>
      <h2 class="reveal">Tell us where you want to grow.</h2>
      <p class="lead reveal" style="opacity:.78">Drop a few details and we will follow up within one business day. Real humans on the other end.</p>

      <div class="form-wrap reveal r2" style="margin-top:36px">
        <form id="contact-form" autocomplete="off" novalidate>
          <input type="text" name="company_url" class="honey" tabindex="-1" autocomplete="off">
          <div class="form-row">
            <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" required></div>
            <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="f-brand">Brand or company</label><input id="f-brand" name="brand" required></div>
            <div class="field"><label for="f-web">Website (optional)</label><input id="f-web" name="website" type="url" placeholder="https://"></div>
          </div>
          <div class="field">
            <label>What are you interested in?</label>
            <div class="pill-toggles">
              <button type="button" class="pill-toggle">Organic Marketing</button>
              <button type="button" class="pill-toggle">AI Automation</button>
              <button type="button" class="pill-toggle">Web Development</button>
              <button type="button" class="pill-toggle">Not sure yet</button>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="f-budget">Budget</label>
              <select id="f-budget" name="budget">
                <option value="">Pick a range</option>
                <option>Under $2k / mo</option>
                <option>$2k - $5k / mo</option>
                <option>$5k - $10k / mo</option>
                <option>$10k+ / mo</option>
                <option>Project based</option>
              </select>
            </div>
            <div class="field">
              <label for="f-time">Timeline</label>
              <select id="f-time" name="timeline">
                <option value="">When do you want to start?</option>
                <option>This week</option>
                <option>Within 2 weeks</option>
                <option>This month</option>
                <option>Within a quarter</option>
                <option>Just exploring</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="f-goals">What does winning look like?</label>
            <textarea id="f-goals" name="goals" placeholder="A few sentences about your goals, audience, or the bottleneck you want to remove."></textarea>
          </div>
          <div class="submit">
            <button class="btn mag" type="submit">Send it <span class="arr">&rarr;</span></button>
            <span class="form-status" role="status" aria-live="polite"></span>
          </div>
        </form>
      </div>
    </div>
  </section>
</main>
"""

# ====================================================================== ORGANIC

def offering_explore(active, current):
    items = [
        ("organic-marketing.html", "Organic Marketing", "broadcast", "Earn attention you do not have to buy. Built on real creators, not ad spend.", "mag"),
        ("ai-automation.html",     "AI Automation",     "robot",     "Put the busywork on autopilot. Custom workflows that connect your stack.", "cyan"),
        ("web-development.html",   "Web Development",   "browser",   "Websites that do real work. Designed to capture leads and plug into your CRM.", "lime"),
    ]
    others = [it for it in items if it[0] != current]
    cards_html = ""
    for h,t,ic,desc,cls in others:
        cards_html += f"""
        <a class="card solid reveal r2" href="{h}">
          <div class="icon">{icon(ic)}</div>
          <h3>{t}</h3>
          <p>{desc}</p>
          <span class="arrow">Explore {t.lower()} &rarr;</span>
        </a>"""
    return f"""
  <section class="section dark" id="explore">
    <div class="container">
      <span class="section-eyebrow reveal" style="color:var(--yellow)">// Explore our other offerings</span>
      <h2 class="reveal">Stack the system.</h2>
      <p class="lead reveal" style="opacity:.78">The pieces work alone. They work better together. Here is where to go next.</p>
      <div class="cards two reveal">{cards_html}</div>
      <div class="row" style="margin-top:38px">
        <a class="btn mag" href="index.html#partner">Let's talk about your project <span class="arr">&rarr;</span></a>
      </div>
    </div>
  </section>
"""

def included_cards(items, accent_classes):
    """items: list of (idx_label, icon_name, title, body)."""
    out = ""
    classes = accent_classes
    for i,(n,ic,t,b) in enumerate(items):
        cls = classes[i % len(classes)]
        out += f"""
        <div class="card {cls} reveal r{(i%6)+1}">
          <span class="idx">{n}</span>
          <div class="icon">{icon(ic)}</div>
          <h3>{t}</h3>
          <p>{b}</p>
        </div>"""
    return out

def stats_band(stats):
    out = '<section class="stats"><div class="container"><div class="stats-grid">'
    for v,l in stats:
        out += f'<div class="stat reveal"><div class="v">{v}</div><div class="l">{l}</div></div>'
    out += '</div></div></section>'
    return out

ORGANIC_BODY = f"""
<main>
  <section class="hero">
    {doodles_hero()}
    <div class="container" style="position:relative;z-index:2">
      <span class="eyebrow"><span class="star">&#9733;</span> Organic Marketing</span>
      <h1>Earn attention you do not have to <span class="hl">buy.</span></h1>
      <p class="sub">Your message turned into hundreds of authentic touchpoints across TikTok, Instagram, YouTube, and more, published by real creators and tracked end to end.</p>
      <div class="ctas">
        <a class="btn mag" href="index.html#partner">Let's talk <span class="arr">&rarr;</span></a>
        <a class="btn dark" href="#explore">See other offerings <span class="arr">&rarr;</span></a>
      </div>
      <div class="trust"><span class="dot"></span> Booking 3 new brands this month</div>
    </div>
  </section>

  <div class="marquee alt scrolly" aria-hidden="true">
    <div class="marquee-track">
      <span>TikTok</span><span class="dot"></span>
      <span>Instagram</span><span class="dot"></span>
      <span>YouTube Shorts</span><span class="dot"></span>
      <span>UGC</span><span class="dot"></span>
      <span>Slideshows</span><span class="dot"></span>
      <span>Carousels</span><span class="dot"></span>
      <span>Reels</span><span class="dot"></span>
      <span>Facebook</span><span class="dot"></span>
      <span>TikTok</span><span class="dot"></span>
      <span>Instagram</span><span class="dot"></span>
      <span>YouTube Shorts</span><span class="dot"></span>
      <span>UGC</span><span class="dot"></span>
      <span>Slideshows</span><span class="dot"></span>
      <span>Carousels</span><span class="dot"></span>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <span class="section-eyebrow reveal">// What is included</span>
      <h2 class="reveal">Everything you need to <span class="hl">show up everywhere.</span></h2>
      <p class="lead reveal">Six moving parts working together to turn one brand into many organic touchpoints.</p>
      <div class="cards six">
        {included_cards([
            ("01","users",     "Creator Distribution","We match your brand with vetted creators in your niche and ship a steady cadence of native content across the platforms your buyers actually open."),
            ("02","broadcast", "UGC Campaigns","Authentic, on-brand video and photo from real users. We brief, source, review, and publish, then route the best assets into paid as raw material."),
            ("03","slide",     "Slideshows and Carousels","Static-format storytelling built for the feeds where it still wins. Scripted hooks, clean type, sticky pacing, and posting cadence baked in."),
            ("04","spark",     "AI Ad Creative","High-volume variant generation for paid social. Hooks, captions, voiceovers, and edits, refreshed weekly so you never run a stale ad."),
            ("05","globe",     "Multi-Platform Reach","TikTok, IG Reels, Shorts, Facebook, threads, X. One asset, reformatted for native delivery on each, posted from accounts that look like they belong there."),
            ("06","chart",     "Performance Reporting","A live dashboard for every campaign. Reach, watch time, saves, comments, conversions, and the top performers worth doubling down on."),
        ], ["","cyan","lime","purple","orange","blue"])}
      </div>
    </div>
  </section>

  <section class="section dark" style="overflow:hidden">
    <div class="container">
      <span class="section-eyebrow reveal" style="color:var(--yellow)">// Beyond one viral moment</span>
      <h2 class="reveal">Stop chasing one <span class="hl cyan">viral moment.</span></h2>
      <p class="lead reveal" style="opacity:.78">Real organic reach is hundreds of small, well-placed touches that compound. Here is what a single campaign month looks like.</p>
      <div class="scatter reveal">
        <span class="pill"     style="top:8%;left:6%">TikTok creator</span>
        <span class="pill c2"  style="top:12%;left:34%">Slideshow post</span>
        <span class="pill c3"  style="top:18%;left:62%">IG Reel</span>
        <span class="pill c4"  style="top:34%;left:18%">UGC review</span>
        <span class="pill c5"  style="top:30%;left:48%">YouTube Short</span>
        <span class="pill c6"  style="top:42%;left:74%">Carousel</span>
        <span class="pill c7"  style="top:58%;left:8%">FB clip</span>
        <span class="pill c8"  style="top:62%;left:38%">AI Ad variant</span>
        <span class="pill c2"  style="top:70%;left:66%">Trend remix</span>
        <span class="pill"     style="top:82%;left:24%">Comment hook</span>
        <span class="pill c5"  style="top:86%;left:54%">Pinned reply</span>
      </div>
    </div>
  </section>

  {stats_band([("100%","creator-led"),("Live","reporting"),("Yours","to keep"),("A&rarr;Z","handled")])}

  {offering_explore("organic", "organic-marketing.html")}
</main>
"""

# ====================================================================== AI AUTOMATION

AI_BODY = f"""
<main>
  <section class="hero">
    {doodles_hero()}
    <div class="container" style="position:relative;z-index:2">
      <span class="eyebrow"><span class="star">&#9733;</span> AI Automation</span>
      <h1>Put the busywork on <span class="hl cyan">autopilot.</span></h1>
      <p class="sub">Custom AI workflows and dashboards that connect your tools, run the repetitive tasks for you, and show exactly what is moving the needle.</p>
      <div class="ctas">
        <a class="btn cyan" href="index.html#partner">Let's talk <span class="arr">&rarr;</span></a>
        <a class="btn dark" href="#explore">See other offerings <span class="arr">&rarr;</span></a>
      </div>
      <div class="trust"><span class="dot"></span> 12 active workflows in production</div>
    </div>
  </section>

  <div class="marquee cyan scrolly" aria-hidden="true">
    <div class="marquee-track">
      <span>n8n</span><span class="dot"></span>
      <span>Make</span><span class="dot"></span>
      <span>Zapier</span><span class="dot"></span>
      <span>OpenAI</span><span class="dot"></span>
      <span>Airtable</span><span class="dot"></span>
      <span>Looker Studio</span><span class="dot"></span>
      <span>Power BI</span><span class="dot"></span>
      <span>GoHighLevel</span><span class="dot"></span>
      <span>n8n</span><span class="dot"></span>
      <span>Make</span><span class="dot"></span>
      <span>Zapier</span><span class="dot"></span>
      <span>OpenAI</span><span class="dot"></span>
      <span>Airtable</span><span class="dot"></span>
      <span>Looker Studio</span><span class="dot"></span>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <span class="section-eyebrow reveal">// What is included</span>
      <h2 class="reveal">Everything you need to <span class="hl cyan">move faster.</span></h2>
      <p class="lead reveal">Six building blocks for an operations system that runs itself and reports the truth.</p>
      <div class="cards six">
        {included_cards([
            ("01","robot",     "AI Workflows","Custom LLM workflows that draft, classify, summarize, and decide. Plugged into your inbox, CRM, and docs so the right action happens without a human babysitting it."),
            ("02","workflow",  "Workflow Automation","n8n, Make, and Zapier flows that move data, ping the right people, and stitch the apps you already pay for into a single pipeline."),
            ("03","dashboard", "Dashboards and Reporting","Looker Studio and Power BI boards that pull from your real systems. Refreshed live so the next decision is based on the truth, not a stale screenshot."),
            ("04","leads",     "CRM and Lead Management","Lead enrichment, scoring, and routing inside GoHighLevel, HubSpot, or your tool of choice. Hot leads land in front of the right person within minutes."),
            ("05","social",    "Social Media AI Systems","Content briefs, captions, comment replies, and scheduling generated and pushed from one place. Your accounts stay alive without anyone staring at a calendar."),
            ("06","plug",      "Tool Integrations","Connect the apps that are not talking to each other yet. APIs, webhooks, custom middleware, and a clear map of what moves where."),
        ], ["cyan","","lime","purple","orange","blue"])}
      </div>
    </div>
  </section>

  <section class="section dark">
    <div class="container">
      <span class="section-eyebrow reveal" style="color:var(--yellow)">// How it works</span>
      <h2 class="reveal">From messy stack to <span class="hl cyan">quiet machine,</span> in four moves.</h2>
      <div class="cards">
        <div class="card cyan reveal r2">
          <div class="icon">01</div><h3>Discovery</h3>
          <p>We map your tools, your data, and the work that should not need a human. The output is a one-page picture of the system we are building.</p>
        </div>
        <div class="card lime reveal r3">
          <div class="icon">02</div><h3>Strategy</h3>
          <p>We pick the workflows with the highest payoff first, agree on what "done" looks like, and lock in the metrics that will tell us it is working.</p>
        </div>
        <div class="card purple reveal r4">
          <div class="icon">03</div><h3>Build and Integrate</h3>
          <p>We ship the automations and dashboards, wired into the apps you already use. You get to watch them run before they go fully live.</p>
        </div>
        <div class="card orange reveal r5">
          <div class="icon">04</div><h3>Optimize and Scale</h3>
          <p>We track what is saving time, prune what is not, and keep adding workflows so the system gets smaller in workload and bigger in output.</p>
        </div>
      </div>
    </div>
  </section>

  {stats_band([("80%","less manual work"),("3x","faster turnaround"),("500+","hours saved"),("Live","dashboards"),])}

  {offering_explore("ai", "ai-automation.html")}
</main>
"""

# ====================================================================== WEB DEV

WEB_BODY = f"""
<main>
  <section class="hero">
    {doodles_hero()}
    <div class="container" style="position:relative;z-index:2">
      <span class="eyebrow"><span class="star">&#9733;</span> Web Development</span>
      <h1>Websites that do <span class="hl lime">real work.</span></h1>
      <p class="sub">Conversion-focused sites and landing pages, designed to capture leads, integrate with your CRM, and grow with your business.</p>
      <div class="ctas">
        <a class="btn lime" href="index.html#partner">Let's talk <span class="arr">&rarr;</span></a>
        <a class="btn dark" href="#explore">See other offerings <span class="arr">&rarr;</span></a>
      </div>
      <div class="trust"><span class="dot"></span> Average launch time: 3 weeks</div>
    </div>
  </section>

  <div class="marquee lime scrolly" aria-hidden="true">
    <div class="marquee-track">
      <span>Web Design</span><span class="dot"></span>
      <span>Landing Pages</span><span class="dot"></span>
      <span>Lead Capture</span><span class="dot"></span>
      <span>Booking Flows</span><span class="dot"></span>
      <span>CRM Integration</span><span class="dot"></span>
      <span>Conversion</span><span class="dot"></span>
      <span>Web Design</span><span class="dot"></span>
      <span>Landing Pages</span><span class="dot"></span>
      <span>Lead Capture</span><span class="dot"></span>
      <span>Booking Flows</span><span class="dot"></span>
      <span>CRM Integration</span><span class="dot"></span>
      <span>Conversion</span><span class="dot"></span>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <span class="section-eyebrow reveal">// What is included</span>
      <h2 class="reveal">Pages that look great <span class="hl lime">and pull weight.</span></h2>
      <p class="lead reveal">Six pieces of a site built to convert, not just to look pretty in a portfolio.</p>
      <div class="cards six">
        {included_cards([
            ("01","browser",   "Web Design","Identity-first design that signals what you do in five seconds. Clean type, real photography, and a layout your buyer can scan on a phone."),
            ("02","rocket",    "Landing Pages","Single-goal pages built around one offer. Hero, proof, objections, call to action. The kind of page paid traffic earns its keep on."),
            ("03","magnet",    "Lead Capture","Forms, calculators, gated guides, and chat handoffs that feel light but route every lead to the right place with full context attached."),
            ("04","calendar",  "Booking Flows","Calendars, intake questions, and confirmation flows that turn interest into a meeting on the calendar without back and forth email."),
            ("05","plug",      "CRM Integration","Every form, booking, and signup wired into HubSpot, GoHighLevel, or your CRM of choice. Source tags and UTMs preserved so reporting actually works."),
            ("06","tune",      "Conversion Optimization","Heat maps, session reviews, and A/B tests on the pages that matter most. We ship changes monthly and only keep what wins."),
        ], ["lime","","cyan","purple","orange","blue"])}
      </div>
    </div>
  </section>

  <section class="section dark">
    <div class="container">
      <span class="section-eyebrow reveal" style="color:var(--yellow)">// The process</span>
      <h2 class="reveal">From blank page to <span class="hl lime">live and selling.</span></h2>
      <div class="cards">
        <div class="card lime reveal r2">
          <div class="icon">01</div><h3>Discovery</h3>
          <p>We get clear on the goal, the audience, the offer, and the systems behind the site. Then we agree on what the homepage has to do.</p>
        </div>
        <div class="card cyan reveal r3">
          <div class="icon">02</div><h3>Design</h3>
          <p>You see the layout in real screens, not slides. We iterate fast, lock the system, and prep the assets that will scale across pages.</p>
        </div>
        <div class="card purple reveal r4">
          <div class="icon">03</div><h3>Build</h3>
          <p>We build the site fast and clean. Mobile first, fully responsive, ready to plug into your analytics, CRM, and ad pixels from day one.</p>
        </div>
        <div class="card orange reveal r5">
          <div class="icon">04</div><h3>Launch and Refine</h3>
          <p>We launch, watch the data, and ship monthly improvements. Pages that earned their slot stay, pages that did not get replaced.</p>
        </div>
      </div>
    </div>
  </section>

  {stats_band([("Built","to convert"),("CRM","connected"),("Fast","and responsive"),("Live","in weeks")])}

  {offering_explore("web", "web-development.html")}
</main>
"""

# ====================================================================== EMIT
def emit(name, title, desc, active, body, splash=False):
    out = shell(title, desc, active, body, splash=splash)
    # remove em-dashes just in case
    out = out.replace("—", "-").replace("–", "-")
    (ROOT / name).write_text(out, encoding="utf-8")
    print(name, len(out)//1024, "KB")

emit("index.html", "Kraftics - Grow Smarter. Build Better. Scale Faster.",
     "Kraftics builds organic marketing, AI automation, and conversion-focused websites for modern businesses.",
     "", INDEX_BODY, splash=True)
emit("organic-marketing.html", "Organic Marketing - Kraftics",
     "Earn attention you do not have to buy. Creator-led organic distribution across TikTok, Instagram, YouTube, and more.",
     "organic-marketing.html", ORGANIC_BODY)
emit("ai-automation.html", "AI Automation - Kraftics",
     "Custom AI workflows, automations, and live dashboards that connect your tools and cut the busywork.",
     "ai-automation.html", AI_BODY)
emit("web-development.html", "Web Development - Kraftics",
     "Conversion-focused websites and landing pages, designed to capture leads and integrate with your CRM.",
     "web-development.html", WEB_BODY)
