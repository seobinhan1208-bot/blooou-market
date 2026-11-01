<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Airless Hoops</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:ital,wght@0,500;0,600;0,700;1,700&family=Barlow:wght@400;500;600&display=swap">
<style>
/* Layout: full-screen 3D beach court, broadcast-style HUD in the corners, shot meter beside the player */
:root{
  --ink:#0d1117; --panel:rgba(12,17,26,.82); --line:#2a3445; --text:#eef2f7; --muted:#93a0b4;
  --orange:#f07b2a; --teal:#3fcf9f; --red:#ff5d5d; --amber:#ffc04d; --sun:#ffb347;
  --display:"Chakra Petch","Segoe UI",system-ui,sans-serif; --body:"Barlow","Segoe UI",system-ui,sans-serif;
  color-scheme:dark;
}
[hidden]{display:none!important}
html,body{height:100%;overflow:hidden}
body{background:var(--ink);color:var(--text);font-family:var(--body);font-size:15px}
#game{position:fixed;inset:0;display:block;width:100%;height:100%;touch-action:none;outline:none}
.hud{position:fixed;pointer-events:none;z-index:5}
.tl{top:calc(14px + env(safe-area-inset-top,0px));left:max(16px,env(safe-area-inset-left,0px))}
.tr{top:calc(14px + env(safe-area-inset-top,0px));right:max(16px,env(safe-area-inset-right,0px));text-align:right}
.bl{bottom:calc(14px + env(safe-area-inset-bottom,0px));left:max(16px,env(safe-area-inset-left,0px))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;backdrop-filter:blur(6px)}
.brand{font-family:var(--display);font-weight:700;font-size:20px;letter-spacing:.04em}
.chip{display:inline-flex;align-items:center;gap:8px;font-family:var(--display);font-size:13px;padding:4px 10px;border-radius:99px;border:1px solid var(--line)}
.chip i{width:10px;height:10px;border-radius:50%;display:inline-block}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;max-width:420px}
#rangeChip.three{border-color:var(--amber);color:var(--amber)}
.score{font-family:var(--display);font-size:44px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums}
.small{font-size:12px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;font-family:var(--display)}
.meters{display:grid;gap:10px;margin-top:10px;width:230px;text-align:left}
.bar{height:8px;border-radius:4px;background:#232c3b;overflow:hidden}
.bar b{display:block;height:100%;width:0;border-radius:4px;transition:width .15s,background .3s}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.big{font-family:var(--display);font-weight:700;font-size:22px;font-variant-numeric:tabular-nums}
.keys{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:13px;color:var(--muted)}
kbd{font-family:var(--display);font-size:12px;color:var(--text);background:#1f2836;border:1px solid #3a4558;border-bottom-width:2px;border-radius:5px;padding:1px 6px;text-align:center;min-width:18px}
#helpCard{transition:opacity .6s}
#helpCard.faded{opacity:0}
#helpTip{position:fixed;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:5;font-family:var(--display);font-size:12px;color:var(--muted);pointer-events:none;transition:opacity .6s}
#roster{display:block;margin-top:10px;width:230px;margin-left:auto;text-align:left}
#rosterList{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:5px;font-size:14px}
#rosterList li{display:flex;justify-content:space-between;gap:8px;align-items:center}
#rosterList li span:first-child{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#rosterList i{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:7px}
#rosterList b{font-family:var(--display);font-variant-numeric:tabular-nums}

/* shot meter, callouts */
#meter{position:fixed;left:calc(50% + 70px);top:30%;z-index:6;display:grid;justify-items:center;gap:6px;pointer-events:none}
#meter .track{position:relative;width:16px;height:130px;border-radius:8px;background:rgba(10,14,20,.75);border:2px solid rgba(255,255,255,.85);overflow:hidden}
#meter .zone{position:absolute;left:0;right:0;bottom:82%;height:18%;background:rgba(63,207,159,.55);border-top:2px solid #3fcf9f;border-bottom:2px solid #3fcf9f}
#meter #meterFill{position:absolute;left:0;right:0;bottom:0;height:0;background:#fff}
#grade{font-family:var(--display);font-weight:700;font-size:15px;letter-spacing:.06em;text-shadow:0 2px 8px rgba(0,0,0,.6);white-space:nowrap}
#flash{position:fixed;left:50%;top:24%;transform:translate(-50%,-50%) scale(.8);font-family:var(--display);font-weight:700;font-style:italic;font-size:clamp(36px,7vw,64px);letter-spacing:.04em;color:#fff;text-shadow:0 4px 0 rgba(0,0,0,.35),0 6px 30px rgba(255,140,40,.6);opacity:0;transition:opacity .25s,transform .25s;pointer-events:none;z-index:6;white-space:nowrap}
#flash.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
#three{position:fixed;left:50%;top:26%;z-index:7;pointer-events:none;display:grid;justify-items:center;transform:translate(-50%,-50%) scale(.4) rotate(-8deg);opacity:0;transition:transform .35s cubic-bezier(.2,1.6,.4,1),opacity .2s}
#three.on{opacity:1;transform:translate(-50%,-50%) scale(1) rotate(-4deg)}
#three b{font-family:var(--display);font-style:italic;font-weight:700;font-size:clamp(110px,22vw,190px);line-height:.85;color:var(--amber);-webkit-text-stroke:4px #1b1208;text-shadow:0 8px 0 #b0420f,0 12px 40px rgba(255,150,40,.7)}
#three span{font-family:var(--display);font-style:italic;font-weight:700;font-size:clamp(22px,4vw,34px);letter-spacing:.18em;background:#111;color:#fff;padding:4px 16px;border-radius:6px;margin-top:-6px}
#three small{font-family:var(--display);font-size:15px;color:#fff;margin-top:8px;text-shadow:0 2px 6px #000}
@media (prefers-reduced-motion:reduce){#three,#flash{transition:none}}
#toast{position:fixed;left:50%;bottom:calc(90px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);font-family:var(--display);font-size:15px;opacity:0;transition:opacity .3s;z-index:6;pointer-events:none;background:var(--panel);padding:6px 14px;border-radius:99px;border:1px solid var(--line);white-space:nowrap}
#toast.on{opacity:1}

/* start + lobby */
#start,#lobby{position:fixed;inset:0;z-index:20;display:grid;place-items:center;background:radial-gradient(ellipse at 50% 20%,rgba(255,170,90,.25),transparent 60%),rgba(8,11,17,.72);padding-inline:max(16px,env(safe-area-inset-left,0px)) max(16px,env(safe-area-inset-right,0px));overflow-y:auto}
#start{place-items:center start;background:linear-gradient(90deg,rgba(8,11,17,.9) 0%,rgba(8,11,17,.78) 42%,rgba(8,11,17,0) 66%)}
#start .box{max-width:600px}
@media (max-width:820px){ #start{place-items:start center;background:rgba(8,11,17,.8)} }
.pickHead{display:flex;justify-content:space-between;align-items:baseline;gap:10px;text-align:left}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
@media (max-width:520px){ .cards{grid-template-columns:repeat(2,minmax(0,1fr))} }
.pcard{position:relative;display:grid;gap:4px;padding:0 0 9px;border-radius:12px;border:2px solid #2c3648;background:linear-gradient(180deg,#1b2433,#121925);color:var(--text);cursor:pointer;text-align:left;overflow:hidden;font-family:var(--body)}
.pcard:hover{border-color:#4a5872}
.pcard.on{border-color:var(--sun);box-shadow:0 0 0 2px rgba(255,179,71,.3),0 10px 30px rgba(255,150,40,.25)}
.pcard .ph{aspect-ratio:4/5;width:100%;background:radial-gradient(ellipse at 50% 30%,var(--cc,#334),#0c1119 75%);display:grid;place-items:center;overflow:hidden}
.pcard .ph img{width:100%;height:100%;object-fit:cover;display:block}
.pcard .ph span{font-family:var(--display);font-size:12px;color:var(--muted)}
.pcard .ovr{position:absolute;top:6px;left:8px;font-family:var(--display);font-weight:700;font-size:24px;line-height:1;text-shadow:0 2px 6px #000}
.pcard .ovr small{display:block;font-size:10px;letter-spacing:.1em;color:#cfd6e2}
.pcard .num{position:absolute;top:8px;right:9px;font-family:var(--display);font-weight:700;font-size:14px;color:#fff;text-shadow:0 2px 6px #000}
.pcard .nm{font-family:var(--display);font-weight:700;font-size:15px;padding:0 9px;line-height:1.1}
.pcard .rl{font-size:12px;color:var(--muted);padding:0 9px}
.pcard .bars{display:grid;grid-template-columns:auto 1fr auto;gap:2px 6px;padding:2px 9px 0;font-family:var(--display);font-size:10px;color:#aeb8c8;align-items:center;font-variant-numeric:tabular-nums}
.pcard .bars i{height:4px;border-radius:2px;background:#273142;overflow:hidden;display:block}
.pcard .bars i b{display:block;height:100%;background:var(--cc,#f07b2a)}
#start .box,#lobby .box{max-width:520px;width:100%;text-align:center;display:grid;gap:16px;padding-block:20px}
#start h1{font-family:var(--display);font-style:italic;font-size:clamp(40px,9vw,72px);margin:0;line-height:.95;letter-spacing:.02em;text-wrap:balance}
#start h1 span{color:var(--sun)}
#start p,#lobby p{margin:0;color:#c6cfdc;line-height:1.5}
.btn{font-family:var(--display);font-weight:600;font-size:17px;padding:12px 26px;border-radius:10px;border:0;background:var(--orange);color:#fff;cursor:pointer;justify-self:center}
.btn:focus-visible,button:focus-visible{outline:2px solid var(--teal);outline-offset:3px}
.btn.ghost{background:transparent;border:1px solid #4a5568;color:var(--text)}
.namefield{display:grid;gap:6px;text-align:left;font-family:var(--display);font-size:13px;color:var(--muted);letter-spacing:.04em}
#start input{font-family:var(--body);font-size:16px;padding:10px 12px;border-radius:8px;border:1px solid #3a4558;background:#141b27;color:var(--text);min-width:0}
#start input:focus-visible{outline:2px solid var(--teal);outline-offset:1px}
.choice{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.or{display:flex;align-items:center;gap:12px;color:var(--muted);font-size:12px;font-family:var(--display);letter-spacing:.08em;text-transform:uppercase}
.or::before,.or::after{content:"";flex:1;height:1px;background:#3a4558}
.pinrow{display:flex;gap:10px}
#start .pinrow input{flex:1;font-family:var(--display);font-size:24px;letter-spacing:.2em;text-align:center}
#start #startErr{color:var(--red);font-size:14px}
.pin{justify-self:center;font-family:var(--display);font-weight:700;font-size:clamp(40px,12vw,92px);letter-spacing:.08em;line-height:1;white-space:nowrap;background:#f7f8fb;color:#141922;border-radius:16px;padding:14px 30px 10px;font-variant-numeric:tabular-nums}
.players{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;min-height:36px}
.pchip{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border-radius:99px;background:#1a2230;border:1px solid var(--line);font-family:var(--display);font-size:15px;animation:pop .3s ease-out}
.pchip i{width:10px;height:10px;border-radius:50%}
@keyframes pop{from{transform:scale(.6);opacity:0}to{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.pchip{animation:none}}
#start .keys{justify-content:center;grid-template-columns:auto auto auto auto;text-align:left;gap:8px 10px}

/* detail sheet */
#detail{position:fixed;inset:0;z-index:15;background:rgba(8,11,17,.92);overflow-y:auto;padding-block:calc(20px + env(safe-area-inset-top,0px)) calc(20px + env(safe-area-inset-bottom,0px));padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
#detail .wrap{max-width:1100px;margin:0 auto;display:grid;gap:18px}
#detail header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
#detail h2{font-family:var(--display);font-size:28px;margin:0}
.close{background:#1f2836;color:var(--text);border:1px solid #3a4558;border-radius:8px;padding:8px 14px;font-family:var(--display);cursor:pointer}
#cut{width:100%;height:auto;aspect-ratio:2/1;max-width:100%;background:#111823;border:1px solid var(--line);border-radius:12px;display:block}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.cols>section{min-width:0;background:#111823;border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.cols h3{font-family:var(--display);margin:0 0 10px;font-size:18px}
ol.steps{margin:0;padding-left:20px;display:grid;gap:8px;line-height:1.5;color:#d3dae5}
ol.steps b{color:var(--text)}
table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:7px 6px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:500;font-family:var(--display);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
td.r{color:var(--orange)} td.a{color:var(--teal)}
.note{font-size:12px;color:var(--muted)}

/* tournament */
#matchBar{position:fixed;left:50%;top:calc(14px + env(safe-area-inset-top,0px));transform:translateX(-50%);z-index:6;display:flex;align-items:stretch;font-family:var(--display);pointer-events:none;border-radius:12px;overflow:hidden;box-shadow:0 8px 28px rgba(0,0,0,.4);max-width:calc(100% - 32px)}
#matchBar .side{display:flex;align-items:center;gap:10px;padding:8px 16px;background:rgba(12,17,26,.92);min-width:0}
#matchBar .nm{font-weight:600;font-size:17px;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#matchBar .sc{font-weight:700;font-size:34px;font-variant-numeric:tabular-nums;min-width:24px;text-align:center;line-height:1}
#matchBar .mid{display:grid;place-items:center;align-content:center;padding:4px 14px;background:#f7f8fb;color:#141922;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;line-height:1.35;text-align:center}
#matchBar .mid b{font-size:15px}
#matchBar i{width:12px;height:12px;border-radius:50%;flex:none}
#bracket{position:fixed;left:max(16px,env(safe-area-inset-left,0px));top:calc(132px + env(safe-area-inset-top,0px));z-index:5;width:270px;max-height:calc(100% - 170px);overflow-y:auto;pointer-events:none}
#bracket ol{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:6px}
#bracket li{display:grid;gap:2px;font-size:14px;padding:7px 10px;border-radius:8px;background:rgba(255,255,255,.05);border:1px solid transparent}
#bracket li.live{background:rgba(240,123,42,.2);border-color:var(--orange)}
#bracket li.champ{background:rgba(255,192,77,.18);border-color:var(--amber)}
#bracket li .no{font-family:var(--display);font-size:11px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
#bracket li .line{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#bracket li .w{color:var(--teal);font-weight:600}
#bracket li .l{color:var(--muted);text-decoration:line-through}
#bracket .rule{font-size:12px;color:var(--muted);margin-top:2px}
body.spec #bracket{width:340px;top:calc(132px + env(safe-area-inset-top,0px))}
body.spec #bracket li{font-size:17px}
#count{position:fixed;left:50%;top:42%;transform:translate(-50%,-50%);font-family:var(--display);font-style:italic;font-weight:700;font-size:clamp(90px,18vw,180px);color:#fff;text-shadow:0 6px 0 rgba(0,0,0,.35),0 10px 40px rgba(240,123,42,.6);z-index:8;pointer-events:none}
#result{position:fixed;left:50%;top:40%;transform:translate(-50%,-50%);z-index:8;pointer-events:none;text-align:center;background:rgba(12,17,26,.9);border:1px solid var(--line);border-radius:16px;padding:18px 28px;display:grid;gap:6px;max-width:calc(100% - 32px)}
#resultText{font-family:var(--display);font-style:italic;font-weight:700;font-size:clamp(28px,5vw,48px);line-height:1.05}
#champ{position:fixed;inset:0;z-index:12;display:grid;place-items:center;background:radial-gradient(ellipse at 50% 35%,rgba(255,192,77,.35),transparent 60%),rgba(8,11,17,.55);padding-inline:max(16px,env(safe-area-inset-left,0px)) max(16px,env(safe-area-inset-right,0px))}
#champ .box{text-align:center;display:grid;gap:12px;justify-items:center}
#champName{font-family:var(--display);font-style:italic;font-weight:700;font-size:clamp(48px,11vw,120px);line-height:1;color:var(--amber);-webkit-text-stroke:3px #1b1208;text-shadow:0 8px 0 #b0420f,0 12px 40px rgba(255,150,40,.6)}
#champ p{margin:0;color:#e6ebf2;font-size:18px}
#pinBanner{position:fixed;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:6;background:#f7f8fb;color:#141922;border-radius:14px;padding:10px 18px;display:grid;pointer-events:none;box-shadow:0 8px 28px rgba(0,0,0,.35)}
#pinBanner span{font-family:var(--display);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#4a5568}
#pinBanner b{font-family:var(--display);font-size:clamp(28px,4vw,44px);letter-spacing:.08em;font-variant-numeric:tabular-nums;line-height:1.05}
#fsBtn{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:25}
.check{display:flex;gap:8px;align-items:center;justify-content:center;font-size:15px;color:#d3dae5;cursor:pointer}
.check input{width:18px;height:18px;accent-color:var(--orange)}
body.start .hud{display:none!important}
body.spec .bl, body.spec .tr .meters, body.spec #meter, body.spec #scoreCard, body.spec #ballChip, body.spec #rangeChip, body.spec #touch{display:none!important}

/* touch controls */
#touch{display:none}
@media (pointer:coarse){
  #touch{display:block}
  #touch .pad,#touch .acts{position:fixed;z-index:8;bottom:calc(16px + env(safe-area-inset-bottom,0px));display:grid;gap:8px}
  #touch .pad{left:max(16px,env(safe-area-inset-left,0px));grid-template-columns:repeat(3,52px)}
  #touch .acts{right:max(16px,env(safe-area-inset-right,0px));grid-template-columns:repeat(3,64px)}
  #touch button{height:52px;border-radius:12px;border:1px solid #3a4558;background:rgba(20,27,38,.8);color:var(--text);font-family:var(--display);font-size:14px;touch-action:none;user-select:none;-webkit-user-select:none}
  #touch button.shoot{background:rgba(240,123,42,.85);border-color:var(--orange);height:70px}
  .meters{width:170px}
  .bl{display:none}
}
@media (max-width:640px){ .tr .meters{display:none} .brand{font-size:16px} .score{font-size:34px} #roster{width:170px} #rangeChip,.bl{display:none} .tl{max-width:calc(100% - 185px)} .chips{max-width:100%} #meter{left:calc(50% + 50px)} }
#start .box>*,#lobby .box>*{min-width:0}
@media (max-width:520px){ #start .keys{grid-template-columns:auto 1fr auto 1fr;font-size:12px;gap:6px 6px} #start .pinrow input{font-size:20px;letter-spacing:.1em} .btn{padding:12px 18px} }
</style>

</head>
<body>
<canvas id="game" tabindex="0" aria-label="Third-person basketball game on a beach court"></canvas>
<div id="flash"></div>
<div id="three" aria-live="polite"><b>3</b><span>POINTER</span><small id="threeDist"></small></div>
<div id="toast"></div>
<div id="matchBar" hidden><div class="side"><i id="mbAc"></i><span class="nm" id="mbA"></span><span class="sc" id="mbAs">0</span></div><div class="mid"><b id="mbM">Match 1</b><span>First to 3</span></div><div class="side"><span class="sc" id="mbBs">0</span><span class="nm" id="mbB"></span><i id="mbBc"></i></div></div>
<div class="card" id="bracket" hidden><div class="small">Tournament bracket</div><div class="rule">Winner stays on · first to 3 baskets · loser is out</div><ol id="bracketList"></ol></div>
<div id="count" hidden></div>
<div id="result" hidden><div class="small">Match over</div><div id="resultText"></div><div class="small" id="resultNext"></div></div>
<div id="champ" hidden><div class="box"><div class="small">Tournament champion</div><div id="champName"></div><p id="champLine"></p><div class="choice" id="champHost" hidden><button class="btn" id="againBtn" type="button">New tournament</button><button class="btn ghost" id="freeBtn" type="button">Free shoot-around</button></div></div></div>
<div id="pinBanner" hidden><span>Join with game PIN</span><b id="pinBig"></b></div>
<button id="fsBtn" class="close" type="button" hidden>Full screen</button>
<div id="meter" hidden><div class="track"><i class="zone"></i><b id="meterFill"></b></div><span id="grade"></span></div>

<div class="hud tl card">
  <div class="brand">AIRLESS HOOPS</div>
  <div class="chips">
    <div class="chip" id="ballChip"><i id="ballDot"></i><span id="ballName">Regular ball · air 8 psi</span></div>
    <div class="chip" id="rangeChip"><span id="rangeText">Mid-range</span></div>
    <div class="chip" id="netChip"><i id="netDot" style="background:var(--muted)"></i><span id="netText">Solo practice</span></div>
  </div>
</div>

<div class="hud tr">
  <div class="card" id="scoreCard" style="display:inline-block;text-align:right">
    <div class="small">Points</div>
    <div class="score" id="score">0</div>
    <div class="small" id="shots">FG 0/0 · 3PT 0/0</div>
  </div>
  <div class="card" id="roster" hidden><div class="small" id="rosterTitle">On this court</div><ul id="rosterList"></ul></div>
  <div class="card meters">
    <div><div class="row"><span class="small">Bounce loudness</span><span class="big" id="db">-- dB</span></div><div class="bar"><b id="dbBar"></b></div></div>
    <div><div class="row"><span class="small">Neighbors, if indoors</span><span id="nbText" style="font-family:var(--display);font-size:13px">Calm</span></div><div class="bar"><b id="nbBar"></b></div></div>
    <div class="row"><span class="small">Energy kept</span><span class="big" id="keep">--</span></div>
  </div>
</div>

<div class="hud bl card" id="helpCard">
  <div class="keys">
    <kbd>W A S D</kbd><span>Move (dribble moves happen on their own) · Shift sprint</span>
    <kbd>Space</kbd><span>Hold: defense stance (protect the ball if you have it)</span>
    <kbd>Mouse</kbd><span>Turn the camera</span>
    <kbd>E</kbd><span>Hold, release in the green · layup near the rim</span>
    <kbd>⇧ E</kbd><span>Dunk (sprint + E within 5 m)</span>
    <kbd>T</kbd><span>Double-clutch slam dunk</span>
    <kbd>F</kbd><span>Block (jump with arms up)</span>
    <kbd>B</kbd><span>Show / hide the bracket</span>
    <kbd>P</kbd><span>See in Detail</span>
    <kbd>Q</kbd><span>Switch regular / airless ball</span>
    <kbd>R</kbd><span>Get the ball back</span>
    <kbd>H</kbd><span>Show / hide these controls</span>
  </div>
</div>

<div id="helpTip" class="hud">Press H for controls</div>
<div id="touch">
  <div class="pad">
    <span></span><button data-k="KeyW">▲</button><span></span>
    <button data-k="KeyA">◀</button><button data-k="KeyS">▼</button><button data-k="KeyD">▶</button>
  </div>
  <div class="acts">
    <button data-k="KeyE" class="shoot">Shoot</button><button data-k="KeyG" class="shoot">Dunk</button><button data-k="KeyT" class="shoot">2× Dunk</button>
    <button data-k="KeyF">Block</button><button data-k="Space">Defend</button><button data-k="KeyQ">Ball</button>
  </div>
</div>

<div id="start">
  <div class="box">
    <h1>AIRLESS <span>HOOPS</span></h1>
    <p>Pick a player and hit the beach court at sunset. Every bounce plays a sound: a regular basketball rings like a drum, and a 3D-printed airless ball lands with a soft thud.</p>
    <label for="nick" class="namefield">Your name<input id="nick" maxlength="16" placeholder="e.g. Jayden" autocomplete="off"></label>
    <div class="pickHead"><span class="small">Choose your player</span><span class="note" id="buildNote">Building players…</span></div>
    <div class="cards" id="cards"></div>
    <div class="choice">
      <button class="btn" id="hostBtn" type="button">Host a game</button>
      <button class="btn ghost" id="soloBtn" type="button">Practice alone</button>
    </div>
    <div class="or">or join a game</div>
    <form id="joinForm" class="pinrow">
      <input id="pinInput" inputmode="numeric" maxlength="7" placeholder="Game PIN" aria-label="Game PIN" autocomplete="off">
      <button class="btn" type="submit">Join</button>
    </form>
    <p id="startErr" role="alert" hidden></p>
    <div class="keys">
      <kbd>WASD</kbd><span>Move</span><kbd>Mouse</kbd><span>Camera</span>
      <kbd>E</kbd><span>Shoot / layup</span><kbd>⇧ E</kbd><span>Dunk</span>
      <kbd>T</kbd><span>Double clutch</span><kbd>F</kbd><span>Block</span>
      <kbd>Space</kbd><span>Defense</span><kbd>B</kbd><span>Bracket</span>
      <kbd>P</kbd><span>See in Detail</span><kbd>Q</kbd><span>Switch ball</span>
    </div>
    <p class="note">The host gets a 6-digit game PIN. Everyone who enters it joins the same court, and the host can start a 1v1 tournament.</p>
  </div>
</div>

<div id="lobby" hidden>
  <div class="box">
    <div class="small" id="lobbyRole">Your game PIN</div>
    <div class="pin" id="lobbyPin">000 000</div>
    <p id="lobbyHint">Connecting…</p>
    <div class="small" id="lobbyCount">1 player</div>
    <div class="players" id="lobbyPlayers"></div>
    <label class="check" id="presentWrap" hidden><input type="checkbox" id="presentChk" checked> I'm presenting on this screen (watch, don't play)</label>
    <div class="choice">
      <button class="btn" id="startTour" type="button" hidden>Start tournament</button>
      <button class="btn ghost" id="goCourt" type="button">Go to the court</button>
      <button class="btn ghost" id="leaveLobby" type="button">Leave</button>
    </div>
    <p class="note" id="tourHint"></p>
  </div>
</div>

<div id="detail" hidden>
  <div class="wrap">
    <header>
      <h2>How a basketball bounces</h2>
      <button class="close" id="closeDetail">Back to game (P)</button>
    </header>
    <canvas id="cut" width="1200" height="600" aria-label="Slow-motion cutaway of both balls hitting the floor"></canvas>
    <div class="cols">
      <section>
        <h3>Regular ball: an air spring</h3>
        <ol class="steps">
          <li><b>Impact.</b> The ball hits the floor and the bottom of the rubber shell flattens.</li>
          <li><b>Compression.</b> Flattening shrinks the space inside, so the trapped air (about 8 psi above outside air) gets squeezed and its pressure rises.</li>
          <li><b>Rebound.</b> The extra pressure pushes the shell back into a sphere and launches the ball up. About two-thirds of the energy comes back.</li>
          <li><b>Sound.</b> The tight shell and hollow air pocket ring like a drum. The ping goes into the air and the thud goes into the floor and down to the neighbors.</li>
        </ol>
      </section>
      <section>
        <h3>Airless ball: a structure spring</h3>
        <ol class="steps">
          <li><b>Impact.</b> The flexible TPU skin touches the floor.</li>
          <li><b>Compression.</b> The honeycomb lattice inside bends and buckles. The bending stores energy, so no air pressure is needed.</li>
          <li><b>Rebound.</b> The cells spring back to shape and push the ball up. A bit more energy turns into heat inside the plastic, so the bounce is a little lower.</li>
          <li><b>Sound.</b> No sealed air pocket means nothing rings. The open lattice soaks up vibration, so you hear a short, dull thud.</li>
        </ol>
      </section>
      <section>
        <h3>Your last bounces</h3>
        <table>
          <thead><tr><th></th><th>Regular</th><th>Airless</th></tr></thead>
          <tbody>
            <tr><td>Impact speed</td><td class="r" id="sRv">--</td><td class="a" id="sAv">--</td></tr>
            <tr><td>Rebound speed</td><td class="r" id="sRo">--</td><td class="a" id="sAo">--</td></tr>
            <tr><td>Energy kept</td><td class="r">67%</td><td class="a">56%</td></tr>
            <tr><td>Loudness</td><td class="r" id="sRd">--</td><td class="a" id="sAd">--</td></tr>
            <tr><td>Hand push to dribble</td><td class="r" id="sRp">--</td><td class="a" id="sAp">--</td></tr>
            <tr><td>Needs pumping</td><td class="r">Yes</td><td class="a">Never</td></tr>
          </tbody>
        </table>
        <p class="note">Bounce one of each ball (switch with Q) to fill this in. Energy and loudness numbers are model estimates, not lab measurements.</p>
      </section>
    </div>
  </div>
</div>

<script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>
<script>
// Online play without accounts: players connect straight to the host's browser (WebRTC through the free PeerJS service).
// The host's computer relays everyone's position, so keep the host's tab open for the whole game.
(function(){
  const PREFIX="airless-hoops-v1-";
  function makeRoom(name){
    return new Promise((resolve,reject)=>{
      if(typeof Peer==="undefined"){ reject(new Error("no-peerjs")); return; }
      const hubId=PREFIX+name, pres=new Map(), conns=new Map(), subs=[], changed=new Set();
      let own={}, ownJson="{}", dirty=true, myId=null, peer=null, hubConn=null, timer=null, done=false, snap=null;
      const notify=()=>{ snap=null; subs.slice().forEach(f=>{ try{ f({}); }catch(e){} }); };
      const finish=ok=>{ if(done) return; done=true; ok ? resolve(room) : reject(new Error("connect-failed")); };
      const room={ name,
        presence:async patch=>{ const n={ ...own }; for(const k in patch){ if(patch[k]===null) delete n[k]; else n[k]=patch[k]; } const j=JSON.stringify(n); if(j!==ownJson){ own=n; ownJson=j; dirty=true; snap=null; } },
        peers:()=>{ if(!snap){ snap=[{ peer:myId, sameTab:true, isMe:true, kind:"viewer", presence:own }]; for(const [k,v] of pres) if(k!==myId) snap.push({ peer:k, sameTab:false, isMe:false, kind:"viewer", presence:v }); } snap[0].presence=own; return snap; },
        onPeers:f=>{ subs.push(f); setTimeout(()=>f({}),0); return ()=>{ const i=subs.indexOf(f); if(i>=0) subs.splice(i,1); }; },
        connected:()=>true, emit:async()=>{}, on:()=>()=>{},
        leave:async()=>{ clearInterval(timer); try{ peer && peer.destroy(); }catch(e){} }
      };
      const send=(c,m)=>{ if(c && c.open){ try{ c.send(m); }catch(e){} } };
      const startHub=()=>{
        myId=peer.id;
        peer.on("connection",c=>{
          c.on("open",()=>{ conns.set(c.peer,c); const all={}; for(const [k,v] of pres) all[k]=v; all[myId]=own; send(c,{ t:"full", p:all }); });
          c.on("data",d=>{ if(d && d.t==="p" && d.p && typeof d.p==="object"){ pres.set(c.peer,d.p); changed.add(c.peer); notify(); } });
          const gone=()=>{ if(!conns.has(c.peer)) return; conns.delete(c.peer); pres.delete(c.peer); for(const x of conns.values()) send(x,{ t:"left", id:c.peer }); notify(); };
          c.on("close",gone); c.on("error",gone);
        });
        timer=setInterval(()=>{
          const out={}; let any=false;
          if(dirty){ out[myId]=own; dirty=false; any=true; }
          for(const k of changed){ if(pres.has(k)){ out[k]=pres.get(k); any=true; } } changed.clear();
          if(any) for(const c of conns.values()) send(c,{ t:"upd", p:out });
        },70);
        finish(true);
      };
      const startClient=()=>{
        peer=new Peer();
        peer.on("open",id=>{
          myId=id; hubConn=peer.connect(hubId,{ reliable:true });
          hubConn.on("open",()=>{ timer=setInterval(()=>{ if(dirty && hubConn.open){ send(hubConn,{ t:"p", p:own }); dirty=false; } },70); finish(true); });
          hubConn.on("data",d=>{ if(!d) return;
            if(d.t==="full"){ pres.clear(); for(const k in d.p) if(k!==myId) pres.set(k,d.p[k]); notify(); }
            else if(d.t==="upd"){ for(const k in d.p) if(k!==myId) pres.set(k,d.p[k]); notify(); }
            else if(d.t==="left"){ pres.delete(d.id); notify(); } });
          hubConn.on("close",()=>{ pres.clear(); notify(); });
        });
        peer.on("error",()=>finish(false));
        setTimeout(()=>finish(false),15000);
      };
      // whoever claims the game's ID first becomes the hub: that is the host, who made the PIN
      peer=new Peer(hubId);
      peer.on("open",startHub);
      peer.on("error",e=>{ if(myId) return; if(e && e.type==="unavailable-id"){ try{ peer.destroy(); }catch(_){} startClient(); } else finish(false); });
    });
  }
  const lobby={ join:name=>makeRoom(name), peers:()=>[], presence:async()=>{}, onPeers:()=>()=>{}, connected:()=>false };
  window.claude={ use:async n=> n==="room" ? lobby : null };
})();
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(() => {
const $ = id => document.getElementById(id);
const V3 = THREE.Vector3;
const G = 9.81, R = 0.12;                         // gravity m/s², ball radius m (size 7)
const BALLS = {
  regular:{ name:"Regular ball · air 8 psi", e:0.82, color:"#f07b2a", base:70 },
  airless:{ name:"Airless ball · TPU lattice", e:0.75, color:"#3fcf9f", base:55 }
};
// FIBA half court: baseline at z = -14, rim 1.575 m in front of it, 3-point arc 6.75 m... using NBA 7.24 m arc / 6.6 m corners
const BASE_Z = -14;
const RIM = { x:0, y:3.05, z:-12.425, r:0.2286 };
const BOARD_Z = -12.8;
const THREE_R = 7.24, CORNER_X = 6.6, CORNER_Z = RIM.z + Math.sqrt(THREE_R*THREE_R - CORNER_X*CORNER_X);
const FENCE = { x:9.6, zMin:-16, zMax:4 };
const PB = { x:9.1, zMin:-15.5, zMax:3.5 };
const HAND_Y = 0.9;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const lerp=(a,b,k)=>a+(b-a)*k;
function gauss(){ let u=0,v=0; while(!u) u=Math.random(); while(!v) v=Math.random(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function isThree(x,z){ if(z<CORNER_Z) return Math.abs(x)>CORNER_X; return Math.hypot(x-RIM.x,z-RIM.z)>THREE_R; }
function angleTo(a,b){ let d=b-a; return Math.atan2(Math.sin(d),Math.cos(d)); }

/* ---------- renderer & scene ---------- */
const canvas = $("game");
const renderer = new THREE.WebGLRenderer({ canvas, antialias:true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene();
const HORIZON = 0xf3cfaa;
scene.fog = new THREE.Fog(HORIZON, 90, 360);
const camera = new THREE.PerspectiveCamera(55, 1, 0.05, 1400);
function resize(){ const w=innerWidth,h=innerHeight; renderer.setSize(w,h,false); camera.aspect=w/h; camera.fov = w<h ? 72 : 55; camera.updateProjectionMatrix(); }
addEventListener("resize", resize); resize();

function tex(w,h,draw,rep){ const c=document.createElement("canvas"); c.width=w; c.height=h; draw(c.getContext("2d"),w,h); const t=new THREE.CanvasTexture(c); t.anisotropy=renderer.capabilities.getMaxAnisotropy(); if(rep){ t.wrapS=t.wrapT=THREE.RepeatWrapping; t.repeat.set(rep[0],rep[1]); } return t; }
function noiseDots(g,w,h,n,cols){ for(let i=0;i<n;i++){ g.fillStyle=cols[i%cols.length]; g.fillRect(Math.random()*w,Math.random()*h,1+Math.random()*1.5,1+Math.random()*1.5); } }

/* ---------- sky, sun, light ---------- */
const sunDir = new V3(-0.32,0.1,-1).normalize();
const sky = new THREE.Mesh(new THREE.SphereGeometry(900,32,20), new THREE.ShaderMaterial({
  side:THREE.BackSide, depthWrite:false, fog:false,
  uniforms:{ top:{value:new THREE.Color(0x2c5fa6)}, mid:{value:new THREE.Color(0x8ab6e2)}, hor:{value:new THREE.Color(HORIZON)}, sun:{value:sunDir} },
  vertexShader:"varying vec3 vDir; void main(){ vDir=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }",
  fragmentShader:"uniform vec3 top,mid,hor,sun; varying vec3 vDir; void main(){ vec3 d=normalize(vDir); float h=d.y; vec3 c=mix(hor,mid,smoothstep(0.0,0.2,h)); c=mix(c,top,smoothstep(0.2,0.8,h)); if(h<0.0) c=hor; float s=max(dot(d,sun),0.0); c+=vec3(1.0,0.5,0.2)*pow(s,7.0)*0.4; c+=vec3(1.0,0.8,0.55)*pow(s,80.0)*0.6; c=mix(c,vec3(1.0,0.96,0.85),smoothstep(0.9988,0.9993,s)); gl_FragColor=vec4(c,1.0); }"
}));
sky.renderOrder=-1; scene.add(sky);

scene.add(new THREE.HemisphereLight(0xd3e6ff, 0xe3c193, 0.62));
const sunL = new THREE.DirectionalLight(0xffe4bf, 1.05);
sunL.position.set(-22,30,-12); sunL.target.position.set(0,0,-6);
sunL.castShadow = true; sunL.shadow.mapSize.set(2048,2048);
Object.assign(sunL.shadow.camera,{ left:-17, right:17, top:17, bottom:-17, near:1, far:90 });
sunL.shadow.bias=-0.0004; sunL.shadow.normalBias=0.02;
scene.add(sunL, sunL.target);

/* ---------- beach and ocean ---------- */
const sandTex = tex(512,512,(g,w,h)=>{ g.fillStyle="#e2c696"; g.fillRect(0,0,w,h); noiseDots(g,w,h,26000,["#f1dcb3","#cfae7c","#e9d2a6","#bf9d6c"]); },[160,140]);
const sand = new THREE.Mesh(new THREE.PlaneGeometry(1600,700), new THREE.MeshLambertMaterial({ map:sandTex }));
sand.rotation.x=-Math.PI/2; sand.position.set(0,-0.06,-34+350); sand.receiveShadow=true; scene.add(sand);
const wet = new THREE.Mesh(new THREE.PlaneGeometry(1600,7), new THREE.MeshLambertMaterial({ map:sandTex, color:0xb59a78 }));
wet.rotation.x=-Math.PI/2; wet.position.set(0,-0.055,-30.5); scene.add(wet);

const waterNormal = tex(256,256,(g,w,h)=>{
  const H=(x,y)=>Math.sin(2*Math.PI*(3*x+1*y)/256)*1.0+Math.sin(2*Math.PI*(-2*x+5*y)/256)*0.7+Math.sin(2*Math.PI*(7*x-3*y)/256)*0.35+Math.sin(2*Math.PI*(1*x+9*y)/256)*0.3;
  const img=g.createImageData(w,h);
  for(let y=0;y<h;y++) for(let x=0;x<w;x++){ const dx=H(x+1,y)-H(x-1,y), dy=H(x,y+1)-H(x,y-1); const n=new V3(-dx*1.6,-dy*1.6,1).normalize(); const i=(y*w+x)*4; img.data[i]=(n.x*0.5+0.5)*255; img.data[i+1]=(n.y*0.5+0.5)*255; img.data[i+2]=(n.z*0.5+0.5)*255; img.data[i+3]=255; }
  g.putImageData(img,0,0);
},[140,70]);
const ocean = new THREE.Mesh(new THREE.PlaneGeometry(2000,900), new THREE.MeshPhongMaterial({ color:0x1d6d8c, specular:0xffe0b8, shininess:90, normalMap:waterNormal, normalScale:new THREE.Vector2(0.55,0.55) }));
ocean.rotation.x=-Math.PI/2; ocean.position.set(0,-0.1,-34-450); scene.add(ocean);
const foamTex = tex(512,64,(g,w,h)=>{ g.clearRect(0,0,w,h); for(let i=0;i<260;i++){ g.fillStyle=`rgba(255,255,255,${0.3+Math.random()*0.6})`; g.beginPath(); g.ellipse(Math.random()*w, h*0.25+Math.random()*h*0.5, 6+Math.random()*30, 2+Math.random()*5, 0, 0, Math.PI*2); g.fill(); } },[30,1]);
const foam = new THREE.Mesh(new THREE.PlaneGeometry(1600,3), new THREE.MeshBasicMaterial({ map:foamTex, transparent:true, opacity:0.75, depthWrite:false }));
foam.rotation.x=-Math.PI/2; foam.position.set(0,-0.04,-34.2); scene.add(foam);
// sunlight glitter path on the water, pointing at the sun
const glitTex = tex(128,512,(g,w,h)=>{ const gr=g.createLinearGradient(0,0,0,h); gr.addColorStop(0,"rgba(255,215,150,0.95)"); gr.addColorStop(0.5,"rgba(255,190,120,0.35)"); gr.addColorStop(1,"rgba(255,180,110,0)"); g.fillStyle=gr; g.fillRect(0,0,w,h); g.globalCompositeOperation="destination-in"; for(let i=0;i<1;i++){ const sg=g.createLinearGradient(0,0,w,0); sg.addColorStop(0,"rgba(0,0,0,0)"); sg.addColorStop(0.5,"rgba(0,0,0,1)"); sg.addColorStop(1,"rgba(0,0,0,0)"); g.fillStyle=sg; g.fillRect(0,0,w,h);} g.globalCompositeOperation="destination-out"; for(let i=0;i<2600;i++){ g.fillStyle="rgba(0,0,0,0.55)"; g.fillRect(Math.random()*w,Math.random()*h,2+Math.random()*10,1+Math.random()*2); } });
const glitter = new THREE.Group();
const gm = new THREE.Mesh(new THREE.PlaneGeometry(26,420), new THREE.MeshBasicMaterial({ map:glitTex, transparent:true, depthWrite:false, blending:THREE.AdditiveBlending, fog:false }));
gm.rotation.x=-Math.PI/2; gm.position.set(0,-0.07,-210); glitter.add(gm);
glitter.position.set(0,0,-36); glitter.rotation.y=Math.atan2(-sunDir.x,-sunDir.z); scene.add(glitter);

// clouds
const cloudTex = tex(256,128,(g,w,h)=>{ for(let i=0;i<14;i++){ const x=40+Math.random()*176, y=50+Math.random()*40, r=20+Math.random()*30; const gr=g.createRadialGradient(x,y,0,x,y,r); gr.addColorStop(0,"rgba(255,236,220,0.9)"); gr.addColorStop(1,"rgba(255,220,200,0)"); g.fillStyle=gr; g.fillRect(0,0,w,h);} });
[[-260,95,-520,220],[120,120,-600,260],[380,80,-480,180],[-520,140,-300,240],[560,150,-200,220],[0,170,-750,300]].forEach(([x,y,z,s])=>{ const sp=new THREE.Sprite(new THREE.SpriteMaterial({ map:cloudTex, transparent:true, opacity:0.85, fog:false, depthWrite:false })); sp.position.set(x,y,z); sp.scale.set(s,s*0.45,1); scene.add(sp); });

// distant coastal hills
const hillMat = new THREE.MeshLambertMaterial({ color:0x8796a8 });
[[260,-280,120,46],[360,-170,95,34],[170,-400,150,60],[460,-60,110,30],[-380,-460,140,38]].forEach(([x,z,r,h])=>{ const m=new THREE.Mesh(new THREE.SphereGeometry(1,24,12,0,Math.PI*2,0,Math.PI/2),hillMat); m.position.set(x,-4,z); m.scale.set(r,h,r*0.55); scene.add(m); });

// pier with a ferris wheel at the end
const wood = new THREE.MeshLambertMaterial({ color:0x8a6d52 });
const pier = new THREE.Group();
const deck = new THREE.Mesh(new THREE.BoxGeometry(12,0.7,280), wood); deck.position.set(0,4.5,-140); pier.add(deck);
for(let z=-6;z>-280;z-=14){ [-5,5].forEach(x=>{ const p=new THREE.Mesh(new THREE.CylinderGeometry(0.35,0.35,6,6),wood); p.position.set(x,1.5,z); pier.add(p); }); }
const pb = new THREE.Mesh(new THREE.BoxGeometry(16,6,14), new THREE.MeshLambertMaterial({ color:0xe8e1d4 })); pb.position.set(0,8,-268); pier.add(pb);
const wheel = new THREE.Group(); wheel.position.set(-2,22,-236); wheel.rotation.y=Math.PI/2;
wheel.add(new THREE.Mesh(new THREE.TorusGeometry(14,0.35,6,48), new THREE.MeshLambertMaterial({ color:0xf2f2f2 })));
for(let i=0;i<16;i++){ const a=i/16*Math.PI*2; const sp=new THREE.Mesh(new THREE.BoxGeometry(0.2,14,0.2), new THREE.MeshLambertMaterial({ color:0xdddddd })); sp.position.set(Math.cos(a)*7,Math.sin(a)*7,0); sp.rotation.z=a-Math.PI/2; wheel.add(sp);
  const cab=new THREE.Mesh(new THREE.BoxGeometry(1.4,1.4,1.4), new THREE.MeshLambertMaterial({ color:[0xe0533a,0xf2b33d,0x3aa0d8,0x52b36b][i%4] })); cab.position.set(Math.cos(a)*14,Math.sin(a)*14-0.9,0); wheel.add(cab); }
pier.add(wheel); pier.position.set(-78,0,-30); scene.add(pier);

// lifeguard tower
const tower = new THREE.Group();
const towerWhite = new THREE.MeshLambertMaterial({ color:0xf4f4f0 }), towerBlue = new THREE.MeshLambertMaterial({ color:0x6fb6e0 });
[[-1.2,-1.2],[1.2,-1.2],[-1.2,1.2],[1.2,1.2]].forEach(([x,z])=>{ const l=new THREE.Mesh(new THREE.CylinderGeometry(0.12,0.12,2.4,6),towerWhite); l.position.set(x,1.2,z); l.castShadow=true; tower.add(l); });
const deckT = new THREE.Mesh(new THREE.BoxGeometry(3.6,0.2,3.6),towerWhite); deckT.position.y=2.4; tower.add(deckT);
const cabin = new THREE.Mesh(new THREE.BoxGeometry(2.8,2.0,2.6),towerBlue); cabin.position.y=3.5; cabin.castShadow=true; tower.add(cabin);
const roof = new THREE.Mesh(new THREE.BoxGeometry(3.3,0.18,3.1),towerWhite); roof.position.y=4.6; tower.add(roof);
const win = new THREE.Mesh(new THREE.PlaneGeometry(2.0,0.8), new THREE.MeshLambertMaterial({ color:0x24384c })); win.position.set(0,3.8,-1.31); win.rotation.y=Math.PI; tower.add(win);
const ramp = new THREE.Mesh(new THREE.BoxGeometry(1,0.12,4),towerWhite); ramp.position.set(0,1.2,3.6); ramp.rotation.x=-0.58; tower.add(ramp);
tower.position.set(19,0,-26); tower.rotation.y=0.3; scene.add(tower);

/* ---------- palm trees ---------- */
const trunkTex = tex(256,64,(g,w,h)=>{ g.fillStyle="#8b6a48"; g.fillRect(0,0,w,h); for(let x=0;x<w;x+=16){ g.fillStyle="#6c5034"; g.fillRect(x,0,4,h); g.fillStyle="#a2805c"; g.fillRect(x+5,0,3,h);} noiseDots(g,w,h,1500,["#5d4430","#9c7a57"]); },[10,1]);
const trunkMat = new THREE.MeshLambertMaterial({ map:trunkTex });
const frondTex = tex(256,64,(g,w,h)=>{ g.clearRect(0,0,w,h); g.strokeStyle="#3d6b2c"; g.lineWidth=3; g.beginPath(); g.moveTo(0,h/2); g.lineTo(w,h/2); g.stroke();
  for(let x=6;x<w-4;x+=5){ const len=(h/2-3)*Math.sin(Math.PI*x/w)**0.6; const col=["#4f8a34","#3f7a2a","#5f9a3c"][x%3]; g.strokeStyle=col; g.lineWidth=3; [-1,1].forEach(sgn=>{ g.beginPath(); g.moveTo(x,h/2); g.lineTo(x+8,h/2+sgn*len); g.stroke(); }); } });
const frondMat = new THREE.MeshLambertMaterial({ map:frondTex, alphaTest:0.5, side:THREE.DoubleSide });
function frondGeo(L){
  const seg=12, pos=[], uv=[], idx=[];
  for(let i=0;i<=seg;i++){ const s=i/seg, x=s*L, y=0.55*s*L*0.5 - 1.15*s*s*L*0.5, w=0.55*Math.sin(Math.PI*Math.min(1,s*1.1))**0.7+0.04;
    pos.push(x,y,-w, x,y+0.06,0, x,y,w); uv.push(s,0, s,0.5, s,1); }
  for(let i=0;i<seg;i++){ const a=i*3; idx.push(a,a+3,a+1, a+1,a+3,a+4, a+1,a+4,a+2, a+2,a+4,a+5); }
  const g=new THREE.BufferGeometry(); g.setAttribute("position",new THREE.Float32BufferAttribute(pos,3)); g.setAttribute("uv",new THREE.Float32BufferAttribute(uv,2)); g.setIndex(idx); g.computeVertexNormals(); return g;
}
const frondGeos=[frondGeo(2.6),frondGeo(3.1),frondGeo(2.2)];
const coconutMat = new THREE.MeshLambertMaterial({ color:0x5a4026 });
function palm(x,z,h,lean,rot){
  const g=new THREE.Group(), pts=[];
  for(let i=0;i<=6;i++){ const t=i/6; pts.push(new V3(lean*t*t, t*h, 0)); }
  const curve=new THREE.CatmullRomCurve3(pts), tub=24, rad=8;
  const geo=new THREE.TubeGeometry(curve,tub,0.2,rad,false), p=geo.attributes.position, P=new V3(), Q=new V3();
  for(let v=0;v<p.count;v++){ const i=Math.floor(v/(rad+1)); curve.getPointAt(i/tub,P); Q.fromBufferAttribute(p,v).sub(P).multiplyScalar(1-0.45*i/tub); p.setXYZ(v,P.x+Q.x,P.y+Q.y,P.z+Q.z); }
  geo.computeVertexNormals();
  const trunk=new THREE.Mesh(geo,trunkMat); trunk.castShadow=true; g.add(trunk);
  const top=pts[6];
  for(let k=0;k<11;k++){ const f=new THREE.Mesh(frondGeos[k%3],frondMat); f.position.copy(top); f.rotation.y=k/11*Math.PI*2+Math.random()*0.3; f.rotation.z=0.25-Math.random()*0.35; f.castShadow=true; g.add(f); }
  for(let k=0;k<4;k++){ const c=new THREE.Mesh(new THREE.SphereGeometry(0.13,8,6),coconutMat); c.position.set(top.x+Math.cos(k*1.6)*0.18,top.y-0.18,top.z+Math.sin(k*1.6)*0.18); g.add(c); }
  g.position.set(x,0,z); g.rotation.y=rot; scene.add(g);
}
[[-12,-14,9,1.6,0.4],[-13.5,-5,10.5,-1.2,1.2],[-12.5,3,8.5,1.4,2.2],[12.5,-11,10,1.8,2.8],[13.5,-2,8.5,-1.4,0.2],[12.2,6,9.5,1.2,3.6],
 [-6,-21,11,2.2,1.9],[7,-22,9.5,-1.8,0.7],[-22,-18,10,1.5,4],[24,-12,11,2,5],[-28,6,9,1.2,2],[30,4,10,-1.5,1]].forEach(a=>palm(...a));

/* ---------- court ---------- */
const SLAB = { x0:-9.7, x1:9.7, z0:-16.1, z1:4.1 };
const slab = new THREE.Mesh(new THREE.BoxGeometry(SLAB.x1-SLAB.x0,0.14,SLAB.z1-SLAB.z0), new THREE.MeshLambertMaterial({ color:0xb9b2a6 }));
slab.position.set(0,-0.07,(SLAB.z0+SLAB.z1)/2); slab.receiveShadow=true; scene.add(slab);
const courtTex = tex(2048,2048,(g,W,H)=>{
  const sx=W/(SLAB.x1-SLAB.x0), sz=H/(SLAB.z1-SLAB.z0), X=x=>(x-SLAB.x0)*sx, Z=z=>(z-SLAB.z0)*sz;
  g.fillStyle="#3c8b79"; g.fillRect(0,0,W,H);
  g.fillStyle="#24598c"; g.fillRect(X(-7.5),Z(-14),15*sx,14*sz);
  g.fillStyle="#d4643f"; g.fillRect(X(-2.45),Z(-14),4.9*sx,5.8*sz);
  g.beginPath(); g.arc(X(0),Z(-8.2),1.8*sx,0,Math.PI); g.fill();
  g.fillStyle="#d4643f"; g.beginPath(); g.arc(X(0),Z(0),1.8*sx,Math.PI,2*Math.PI); g.fill();
  noiseDots(g,W,H,90000,["rgba(255,255,255,.05)","rgba(0,0,0,.05)"]);
  g.strokeStyle="#f7f3ea"; g.lineWidth=0.06*sx; g.lineCap="butt";
  g.strokeRect(X(-7.5),Z(-14),15*sx,14*sz);
  g.strokeRect(X(-2.45),Z(-14),4.9*sx,5.8*sz);
  g.beginPath(); g.arc(X(0),Z(-8.2),1.8*sx,0,Math.PI*2); g.stroke();
  g.beginPath(); g.arc(X(0),Z(RIM.z),1.25*sx,0,Math.PI); g.stroke();
  const th0=Math.asin((CORNER_Z-RIM.z)/THREE_R);
  g.beginPath(); g.moveTo(X(-CORNER_X),Z(BASE_Z)); g.lineTo(X(-CORNER_X),Z(CORNER_Z)); g.moveTo(X(CORNER_X),Z(BASE_Z)); g.lineTo(X(CORNER_X),Z(CORNER_Z)); g.stroke();
  g.beginPath(); g.arc(X(0),Z(RIM.z),THREE_R*sx,th0,Math.PI-th0); g.stroke();
  g.beginPath(); g.arc(X(0),Z(0),1.8*sx,Math.PI,2*Math.PI); g.stroke();
  [-2.45,2.45].forEach(x=>[-12.25,-11.4,-10.55,-9.7].forEach(z=>{ g.beginPath(); g.moveTo(X(x),Z(z)); g.lineTo(X(x+Math.sign(x)*0.15),Z(z)); g.stroke(); }));
  g.fillStyle="rgba(247,243,234,.9)"; g.font=`italic 700 ${0.62*sz}px "Chakra Petch", sans-serif`; g.textAlign="center"; g.textBaseline="middle";
  g.fillText("AIRLESS HOOPS", X(0), Z(-15.15));
  g.font=`700 ${0.42*sz}px "Chakra Petch", sans-serif`; g.fillStyle="rgba(247,243,234,.55)"; g.fillText("SUNSET BEACH COURT", X(0), Z(2.4));
});
const courtTop = new THREE.Mesh(new THREE.PlaneGeometry(SLAB.x1-SLAB.x0,SLAB.z1-SLAB.z0), new THREE.MeshLambertMaterial({ map:courtTex }));
courtTop.rotation.x=-Math.PI/2; courtTop.position.set(0,0.001,(SLAB.z0+SLAB.z1)/2); courtTop.receiveShadow=true; scene.add(courtTop);

// chain-link fence
const chainTex = tex(64,64,(g,w,h)=>{ g.clearRect(0,0,w,h); g.strokeStyle="#c9ccd0"; g.lineWidth=3; g.beginPath(); g.moveTo(0,0); g.lineTo(w,h); g.moveTo(w,0); g.lineTo(0,h); g.stroke(); });
chainTex.wrapS=chainTex.wrapT=THREE.RepeatWrapping;
const postMat = new THREE.MeshLambertMaterial({ color:0x3a5a4a });
function fence(x0,z0,x1,z1,hgt){
  const len=Math.hypot(x1-x0,z1-z0), t=chainTex.clone(); t.needsUpdate=true; t.repeat.set(len/0.22,hgt/0.22);
  const m=new THREE.Mesh(new THREE.PlaneGeometry(len,hgt), new THREE.MeshBasicMaterial({ map:t, transparent:true, opacity:0.55, side:THREE.DoubleSide, depthWrite:false }));
  m.position.set((x0+x1)/2,hgt/2,(z0+z1)/2); m.rotation.y=Math.atan2(-(z1-z0),x1-x0); scene.add(m);
  const n=Math.ceil(len/3);
  for(let i=0;i<=n;i++){ const k=i/n, p=new THREE.Mesh(new THREE.CylinderGeometry(0.045,0.045,hgt,8),postMat); p.position.set(lerp(x0,x1,k),hgt/2,lerp(z0,z1,k)); p.castShadow=true; scene.add(p); }
  const rail=new THREE.Mesh(new THREE.CylinderGeometry(0.035,0.035,len,6),postMat); rail.position.set((x0+x1)/2,hgt,(z0+z1)/2); rail.rotation.z=Math.PI/2; rail.rotation.y=Math.atan2(-(z1-z0),x1-x0); scene.add(rail);
}
fence(-FENCE.x,FENCE.zMin,FENCE.x,FENCE.zMin,3.4);
fence(-FENCE.x,FENCE.zMin,-FENCE.x,FENCE.zMax,3.4);
fence(FENCE.x,FENCE.zMin,FENCE.x,FENCE.zMax,3.4);
fence(-FENCE.x,FENCE.zMax,-1.2,FENCE.zMax,3.4);
fence(1.2,FENCE.zMax,FENCE.x,FENCE.zMax,3.4);

// bench and lamp posts
const benchWood = new THREE.MeshLambertMaterial({ color:0xa8794f });
const bench = new THREE.Group();
[0,0.14,0.28].forEach(z=>{ const b=new THREE.Mesh(new THREE.BoxGeometry(2.2,0.05,0.12),benchWood); b.position.set(0,0.46,z); b.castShadow=true; bench.add(b); });
[-0.9,0.9].forEach(x=>{ const l=new THREE.Mesh(new THREE.BoxGeometry(0.08,0.46,0.4), new THREE.MeshLambertMaterial({ color:0x333a44 })); l.position.set(x,0.23,0.14); bench.add(l); });
bench.position.set(8.9,0,-3.2); bench.rotation.y=Math.PI/2; scene.add(bench);
const lampMat = new THREE.MeshLambertMaterial({ color:0x2f3a46 });
[[-10.8,-16.5],[10.8,-16.5],[-10.8,4.6],[10.8,4.6]].forEach(([x,z])=>{ const p=new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.11,7,8),lampMat); p.position.set(x,3.5,z); p.castShadow=true; scene.add(p);
  const head=new THREE.Mesh(new THREE.BoxGeometry(0.9,0.18,0.4),lampMat); head.position.set(x-Math.sign(x)*0.4,7,z); scene.add(head);
  const bulb=new THREE.Mesh(new THREE.PlaneGeometry(0.7,0.25), new THREE.MeshBasicMaterial({ color:0xfff1c8 })); bulb.rotation.x=Math.PI/2; bulb.position.set(x-Math.sign(x)*0.4,6.9,z); scene.add(bulb); });

/* ---------- hoop ---------- */
const navy = new THREE.MeshStandardMaterial({ color:0x1d2c4a, roughness:.6, metalness:.2 });
const pad = new THREE.Mesh(new THREE.BoxGeometry(1.1,1.8,0.9), new THREE.MeshStandardMaterial({ color:0x24598c, roughness:.8 }));
pad.position.set(0,0.9,-15.5); pad.castShadow=true; scene.add(pad);
const pole = new THREE.Mesh(new THREE.BoxGeometry(0.22,3.9,0.22), navy); pole.position.set(0,1.95,-15.5); pole.castShadow=true; scene.add(pole);
const armB = new THREE.Mesh(new THREE.BoxGeometry(0.18,0.18,2.65), navy); armB.position.set(0,3.75,-14.2); armB.castShadow=true; scene.add(armB);
const brace = new THREE.Mesh(new THREE.BoxGeometry(0.1,0.1,2.2), navy); brace.position.set(0,3.1,-14.4); brace.rotation.x=-0.42; scene.add(brace);
const glass = new THREE.Mesh(new THREE.BoxGeometry(1.83,1.07,0.03), new THREE.MeshStandardMaterial({ color:0xe8f4ff, transparent:true, opacity:0.32, roughness:0.05, metalness:0.3 }));
glass.position.set(0,3.435,BOARD_Z-0.015); glass.castShadow=true; scene.add(glass);
const white = new THREE.MeshBasicMaterial({ color:0xffffff }), black=new THREE.MeshStandardMaterial({ color:0x111418 });
[[0,3.97,1.87,0.05],[0,2.9,1.87,0.05]].forEach(([x,y,w,h])=>{ const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,0.05),black); b.position.set(x,y,BOARD_Z-0.015); scene.add(b); });
[-0.935,0.935].forEach(x=>{ const b=new THREE.Mesh(new THREE.BoxGeometry(0.05,1.12,0.05),black); b.position.set(x,3.435,BOARD_Z-0.015); scene.add(b); });
[[0,3.1,0.59,0.05],[0,3.55,0.59,0.05]].forEach(([x,y,w,h])=>{ const b=new THREE.Mesh(new THREE.PlaneGeometry(w,h),white); b.position.set(x,y,BOARD_Z+0.002); scene.add(b); });
[-0.27,0.27].forEach(x=>{ const b=new THREE.Mesh(new THREE.PlaneGeometry(0.05,0.5),white); b.position.set(x,3.325,BOARD_Z+0.002); scene.add(b); });
const hoop = new THREE.Group(); hoop.position.set(0,RIM.y,BOARD_Z); scene.add(hoop);
const rimMat = new THREE.MeshStandardMaterial({ color:0xe2532a, metalness:.5, roughness:.35 });
const rim = new THREE.Mesh(new THREE.TorusGeometry(RIM.r,0.019,12,56), rimMat); rim.rotation.x=Math.PI/2; rim.position.z=RIM.z-BOARD_Z; rim.castShadow=true; hoop.add(rim);
const bracket = new THREE.Mesh(new THREE.BoxGeometry(0.14,0.04,0.16), rimMat); bracket.position.set(0,0,0.08); hoop.add(bracket);
const netGeo = (()=>{ const NR=14,NK=6,pts=[]; const P=(k,i)=>{ const a=(i+k*0.5)/NR*Math.PI*2, r=RIM.r-k*0.016; return [Math.cos(a)*r, -k*0.075, Math.sin(a)*r]; };
  for(let k=0;k<NK;k++) for(let i=0;i<NR;i++){ pts.push(...P(k,i),...P(k+1,i), ...P(k,i),...P(k+1,i-1)); }
  const g=new THREE.BufferGeometry(); g.setAttribute("position",new THREE.Float32BufferAttribute(pts,3)); return g; })();
const hoopNet = new THREE.LineSegments(netGeo, new THREE.LineBasicMaterial({ color:0xffffff, transparent:true, opacity:.9 }));
hoopNet.position.set(0,-0.01,RIM.z-BOARD_Z); hoop.add(hoopNet);
const rimPts = []; for(let i=0;i<40;i++){ const a=i/40*Math.PI*2; rimPts.push(new V3(RIM.x+Math.cos(a)*RIM.r,RIM.y,RIM.z+Math.sin(a)*RIM.r)); }

/* ---------- ball ---------- */
const regularTex = tex(1024,512,(g,w,h)=>{
  g.fillStyle="#d4652a"; g.fillRect(0,0,w,h);
  for(let k=0;k<40000;k++){ g.fillStyle=`rgba(${Math.random()<.5?60:255},${Math.random()<.5?30:140},0,.13)`; g.fillRect(Math.random()*w,Math.random()*h,2,2); }
  g.strokeStyle="#1b1310"; g.lineWidth=8;
  g.beginPath(); g.moveTo(0,h/2); g.lineTo(w,h/2); g.stroke();
  [0,w/2,w].forEach(x=>{ g.beginPath(); g.moveTo(x,0); g.lineTo(x,h); g.stroke(); });
  [w/4,3*w/4].forEach(cx=>{ [1,-1].forEach(sg=>{ g.beginPath(); for(let y=0;y<=h;y+=4){ const x=cx+sg*Math.cos((y/h)*Math.PI)*w*0.14; y?g.lineTo(x,y):g.moveTo(x,y);} g.stroke(); }); });
});
const airlessTex = tex(1024,512,(g,w,h)=>{
  g.fillStyle="#1d6b55"; g.fillRect(0,0,w,h);
  const s=18, hh=s*Math.sqrt(3);
  for(let row=-1;row<h/hh*2+2;row++) for(let col=-1;col<w/(s*3)+2;col++){
    const cx=col*s*3+(row%2?s*1.5:0), cy=row*hh/2;
    g.beginPath(); for(let a=0;a<6;a++){ const t=Math.PI/3*a; g.lineTo(cx+s*Math.cos(t)*0.86,cy+s*Math.sin(t)*0.86);} g.closePath();
    g.fillStyle="#0e3a2e"; g.fill(); g.strokeStyle="#bdf3df"; g.lineWidth=4; g.stroke();
  }
});
const matRegular = new THREE.MeshStandardMaterial({ map:regularTex, roughness:.7 });
const matAirless = new THREE.MeshStandardMaterial({ map:airlessTex, roughness:.5 });
const ballGeo = new THREE.SphereGeometry(R,48,32);
const ballMesh = new THREE.Mesh(ballGeo, matRegular); ballMesh.castShadow=true; scene.add(ballMesh);
const ring = new THREE.Mesh(new THREE.RingGeometry(0.9,1,48), new THREE.MeshBasicMaterial({ color:0xff5d5d, transparent:true, opacity:0, side:THREE.DoubleSide, depthWrite:false }));
ring.rotation.x=-Math.PI/2; ring.position.y=0.012; scene.add(ring);
let ringT=1, ringMax=1;

// Signed-distance sculpting + surface extraction + skin weights.
// Every function here is self-contained so it can be stringified into a Web Worker.
function sdfEval(job, x, y, z){
  const P=job.prims; let d=1e9;
  for(let i=0;i<P.length;i++){
    const q=P[i];
    if(q.bb && i>0){
      const b=q.bb;
      const dx=Math.max(b[0]-x,0,x-b[3]), dy=Math.max(b[1]-y,0,y-b[4]), dz=Math.max(b[2]-z,0,z-b[5]);
      const ad=Math.sqrt(dx*dx+dy*dy+dz*dz);
      if(q.op===0 && ad-q.k>d) continue;
      if(q.op===1 && ad>q.k+0.002) continue;
    }
    let px=x,py=y,pz=z; const m=q.m;
    if(m){ px=m[0]*x+m[1]*y+m[2]*z+m[3]; py=m[4]*x+m[5]*y+m[6]*z+m[7]; pz=m[8]*x+m[9]*y+m[10]*z+m[11]; }
    const p=q.p; let e;
    switch(q.t){
      case 1: { // round cone along local y from y0 to y1, radii r0 -> r1, cross-section scale sx, sz
        const sx=p[4]||1, sz=p[5]||1, lx=px/sx, lz=pz/sz;
        let rq=Math.sqrt(lx*lx+lz*lz), y0=p[0], y1=p[1], r0=p[2], r1=p[3];
        let hh=y1-y0, s=1; if(hh<0){ hh=-hh; s=-1; }
        const ay=(py-y0)*s, b=(r0-r1)/hh, a=Math.sqrt(Math.max(0,1-b*b)), kk=-b*rq+a*ay;
        if(kk<0) e=Math.sqrt(rq*rq+ay*ay)-r0;
        else if(kk>a*hh) e=Math.sqrt(rq*rq+(ay-hh)*(ay-hh))-r1;
        else e=rq*a+ay*b-r0;
        e*=Math.min(sx,sz); break; }
      case 2: { // ellipsoid centre p0..2 radii p3..5
        const ex=(px-p[0]), ey=(py-p[1]), ez=(pz-p[2]);
        const k0=Math.sqrt((ex/p[3])**2+(ey/p[4])**2+(ez/p[5])**2);
        const k1=Math.sqrt((ex/(p[3]*p[3]))**2+(ey/(p[4]*p[4]))**2+(ez/(p[5]*p[5]))**2);
        e = k1>1e-9 ? k0*(k0-1)/k1 : -Math.min(p[3],p[4],p[5]); break; }
      case 3: { // rounded box centre p0..2 half p3..5 radius p6
        const qx=Math.abs(px-p[0])-p[3]+p[6], qy=Math.abs(py-p[1])-p[4]+p[6], qz=Math.abs(pz-p[2])-p[5]+p[6];
        e=Math.sqrt(Math.max(qx,0)**2+Math.max(qy,0)**2+Math.max(qz,0)**2)+Math.min(Math.max(qx,qy,qz),0)-p[6]; break; }
      case 4: e=px*p[0]+py*p[1]+pz*p[2]-p[3]; break; // half space
      case 5: e=Math.sqrt((px-p[0])**2+(py-p[1])**2+(pz-p[2])**2)-p[3]; break; // sphere
      case 6: { // round cone between two points a(p0..2) b(p3..5), radii p6 -> p7
        const bx=p[3]-p[0], by=p[4]-p[1], bz=p[5]-p[2], L=Math.sqrt(bx*bx+by*by+bz*bz)||1e-6;
        const ux=bx/L, uy=by/L, uz=bz/L, wx=px-p[0], wy=py-p[1], wz=pz-p[2];
        const ay=wx*ux+wy*uy+wz*uz, rx=wx-ux*ay, ry=wy-uy*ay, rz=wz-uz*ay, rq=Math.sqrt(rx*rx+ry*ry+rz*rz);
        const r0=p[6], r1=p[7], b=(r0-r1)/L, a=Math.sqrt(Math.max(0,1-b*b)), kk=-b*rq+a*ay;
        if(kk<0) e=Math.sqrt(rq*rq+ay*ay)-r0;
        else if(kk>a*L) e=Math.sqrt(rq*rq+(ay-L)*(ay-L))-r1;
        else e=rq*a+ay*b-r0;
        break; }
      default: e=1e9;
    }
    if(q.n) e+=q.n*Math.sin(px*q.nf)*Math.sin(py*q.nf*1.31)*Math.sin(pz*q.nf*0.87);
    if(i===0){ d = q.op===1 ? -e : e; continue; }
    const k=q.k;
    if(q.op===0){ if(k>0){ const h=Math.max(k-Math.abs(d-e),0)/k; d=Math.min(d,e)-h*h*k*0.25; } else d=Math.min(d,e); }
    else if(q.op===1){ const ne=-e; if(k>0){ const h=Math.max(k-Math.abs(d-ne),0)/k; d=Math.max(d,ne)+h*h*k*0.25; } else d=Math.max(d,ne); }
    else { if(k>0){ const h=Math.max(k-Math.abs(d-e),0)/k; d=Math.max(d,e)+h*h*k*0.25; } else d=Math.max(d,e); }
  }
  return d-(job.off||0);
}
function sdfMesh(job){
  const ox=job.o[0], oy=job.o[1], oz=job.o[2], h=job.h, nx=job.n[0], ny=job.n[1], nz=job.n[2];
  const F=new Float32Array(nx*ny*nz);
  for(let k=0;k<nz;k++) for(let j=0;j<ny;j++){ const base=nx*(j+ny*k); for(let i=0;i<nx;i++) F[base+i]=sdfEval(job,ox+i*h,oy+j*h,oz+k*h); }
  const cx=nx-1, cy=ny-1, cz=nz-1, cellV=new Int32Array(cx*cy*cz).fill(-1), pos=[];
  const E=[[0,1],[2,3],[4,5],[6,7],[0,2],[1,3],[4,6],[5,7],[0,4],[1,5],[2,6],[3,7]];
  const C=[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]];
  const v=new Float32Array(8);
  for(let k=0;k<cz;k++) for(let j=0;j<cy;j++) for(let i=0;i<cx;i++){
    let mask=0;
    for(let c=0;c<8;c++){ const val=F[(i+C[c][0])+nx*((j+C[c][1])+ny*(k+C[c][2]))]; v[c]=val; if(val<0) mask|=1<<c; }
    if(mask===0||mask===255) continue;
    let sx=0,sy=0,sz=0,cnt=0;
    for(const [a,b] of E){ if((v[a]<0)!==(v[b]<0)){ const t=v[a]/(v[a]-v[b]); sx+=C[a][0]+(C[b][0]-C[a][0])*t; sy+=C[a][1]+(C[b][1]-C[a][1])*t; sz+=C[a][2]+(C[b][2]-C[a][2])*t; cnt++; } }
    cellV[i+cx*(j+cy*k)]=pos.length/3;
    pos.push(ox+(i+sx/cnt)*h, oy+(j+sy/cnt)*h, oz+(k+sz/cnt)*h);
  }
  const idx=[], cell=(i,j,k)=>cellV[i+cx*(j+cy*k)];
  for(let k=0;k<nz;k++) for(let j=0;j<ny;j++) for(let i=0;i<nx;i++){
    const f0=F[i+nx*(j+ny*k)];
    if(i<cx && j>0 && k>0 && j<cy && k<cz){ const f1=F[i+1+nx*(j+ny*k)]; if((f0<0)!==(f1<0)){ const a=cell(i,j-1,k-1),b=cell(i,j,k-1),c=cell(i,j,k),d=cell(i,j-1,k); if(a>=0&&b>=0&&c>=0&&d>=0){ if(f0<0) idx.push(a,b,c,a,c,d); else idx.push(a,c,b,a,d,c); } } }
    if(j<cy && i>0 && k>0 && i<cx && k<cz){ const f1=F[i+nx*(j+1+ny*k)]; if((f0<0)!==(f1<0)){ const a=cell(i-1,j,k-1),b=cell(i-1,j,k),c=cell(i,j,k),d=cell(i,j,k-1); if(a>=0&&b>=0&&c>=0&&d>=0){ if(f0<0) idx.push(a,b,c,a,c,d); else idx.push(a,c,b,a,d,c); } } }
    if(k<cz && i>0 && j>0 && i<cx && j<cy){ const f1=F[i+nx*(j+ny*(k+1))]; if((f0<0)!==(f1<0)){ const a=cell(i-1,j-1,k),b=cell(i,j-1,k),c=cell(i,j,k),d=cell(i-1,j,k); if(a>=0&&b>=0&&c>=0&&d>=0){ if(f0<0) idx.push(a,b,c,a,c,d); else idx.push(a,c,b,a,d,c); } } }
  }
  const nv=pos.length/3, P=new Float32Array(pos), N=new Float32Array(nv*3), AO=new Float32Array(nv), TR=new Float32Array(nv);
  const e=h*0.5;
  for(let q=0;q<nv;q++){
    const x=P[q*3],y=P[q*3+1],z=P[q*3+2];
    let gx=sdfEval(job,x+e,y,z)-sdfEval(job,x-e,y,z), gy=sdfEval(job,x,y+e,z)-sdfEval(job,x,y-e,z), gz=sdfEval(job,x,y,z+e)-sdfEval(job,x,y,z-e);
    const l=Math.sqrt(gx*gx+gy*gy+gz*gz)||1; gx/=l; gy/=l; gz/=l; N[q*3]=gx; N[q*3+1]=gy; N[q*3+2]=gz;
    // ambient occlusion from the distance field: creases and armpits come out darker
    let occ=0, w=1, wsum=0; const ds=job.aoD||[0.01,0.022,0.045,0.08];
    for(const dd of ds){ const s=sdfEval(job,x+gx*dd,y+gy*dd,z+gz*dd); occ+=w*Math.max(0,dd-s)/dd; wsum+=w; w*=0.6; }
    AO[q]=Math.max(0.3,Math.min(1,1-(occ/wsum)*(job.aoK||1.1)));
    if(job.trim){ let t=0; for(const tq of job.trim){ const sub={prims:[tq.prim]}; const dd=Math.abs(sdfEval(sub,x,y,z)); t=Math.max(t,1-Math.min(1,Math.max(0,(dd-tq.w*0.55)/(tq.w*0.45)))); } TR[q]=t; }
  }
  const out={ pos:P, nrm:N, ao:AO, idx:new Uint32Array(idx), trim:job.trim?TR:null };
  if(job.segs) Object.assign(out, sdfSkin(job.segs,P));
  return out;
}
function sdfSkin(segs,P){
  const nv=P.length/3, SI=new Uint16Array(nv*4), SW=new Float32Array(nv*4);
  for(let q=0;q<nv;q++){
    const x=P[q*3],y=P[q*3+1],z=P[q*3+2];
    let best=-1, bd=1e9, bt=0;
    for(let s=0;s<segs.length;s++){
      const g=segs[s], ax=g.a[0],ay=g.a[1],az=g.a[2], bx=g.c[0]-ax,by=g.c[1]-ay,bz=g.c[2]-az, L2=bx*bx+by*by+bz*bz||1e-9;
      let t=((x-ax)*bx+(y-ay)*by+(z-az)*bz)/L2; const tc=Math.max(0,Math.min(1,t));
      const dx=x-(ax+bx*tc), dy=y-(ay+by*tc), dz=z-(az+bz*tc);
      const d=Math.sqrt(dx*dx+dy*dy+dz*dz)/g.r;
      if(d<bd){ bd=d; best=s; bt=t; }
    }
    const g=segs[best], L=Math.sqrt((g.c[0]-g.a[0])**2+(g.c[1]-g.a[1])**2+(g.c[2]-g.a[2])**2)||1e-6;
    let w0=1, other=-1, w1=0;
    const zs=(g.bz||0.06)/L, ze=(g.ez||0.06)/L;
    if(g.par>=0 && bt<zs){ const u=Math.max(-1,bt/zs); w0=0.5+0.5*Math.max(0,u); if(u<0) w0=0.5*(1+u); other=segs[g.par].b; w1=1-w0; }
    else if(g.ch>=0 && bt>1-ze){ const u=(1-bt)/ze; w0=0.5+0.5*Math.max(0,u); if(u<0) w0=Math.max(0,0.5*(1+u)); other=segs[g.ch].b; w1=1-w0; }
    SI[q*4]=g.b; SW[q*4]=w0;
    if(other>=0){ SI[q*4+1]=other; SW[q*4+1]=w1; }
  }
  return { si:SI, sw:SW };
}


/* ---------- players: sculpted, skinned athletes built from distance fields ---------- */
const DIM={ UA:0.31, FA:0.27, SHX:0.2, SHY:0.47, NECK:0.55, HEAD:0.1, HIPX:0.1, TH:0.46, SH:0.44, PEL:1.008 };
const FINGER_LEN=[0.06,0.082,0.088,0.082,0.066];
const BONE_KEYS=["pelvis","torso","neck","head","sL","eL","wL","sR","eR","wR","hL","kL","aL","hR","kR","aR","fL0","fL1","fL2","fL3","fL4","fR0","fR1","fR2","fR3","fR4"];
// Six original players. Names, looks and numbers are invented for this game.
const ARCH=[
  { id:"ace", name:"Ace Morrow", pos:"PG", role:"Sharpshooter", num:14, height:"6'3\"", scale:0.98,
    r:{ shoot:96, speed:85, dunk:58, def:68 }, skin:"#cf9b78", hair:"fade", hairC:"#24160e", beard:"stubble", sleeve:"R", sleeveC:"#111318", band:null,
    body:{ W:0.97, M:0.9, L:0.93, belly:0, D:0.95 }, face:{ jaw:0.96, chin:1, nose:0.95, lips:0.95, brow:0.9, cheek:1 },
    jersey:"#1d3a6e", trim:"#f2b33d", numC:"#ffffff", shoe:"#f4f4f2", sole:"#f2b33d" },
  { id:"blaze", name:"Blaze Odum", pos:"SG", role:"High-Flyer", num:9, height:"6'6\"", scale:1.0,
    r:{ shoot:79, speed:91, dunk:97, def:73 }, skin:"#6a4228", hair:"buzz", hairC:"#120c09", beard:null, sleeve:null, band:"#e23d3d",
    body:{ W:1.05, M:1.08, L:1.06, belly:0, D:1.0 }, face:{ jaw:1.02, chin:1.05, nose:1.08, lips:1.12, brow:1.0, cheek:1.02 },
    jersey:"#c8102e", trim:"#15161a", numC:"#ffffff", shoe:"#15161a", sole:"#c8102e" },
  { id:"titan", name:"Titan Vale", pos:"C", role:"Paint Beast", num:50, height:"7'0\"", scale:1.08,
    r:{ shoot:54, speed:62, dunk:91, def:95 }, skin:"#8a5a3b", hair:"bald", hairC:"#140d09", beard:"full", sleeve:null, band:null,
    body:{ W:1.16, M:1.12, L:1.14, belly:0.45, D:1.14 }, face:{ jaw:1.12, chin:1.08, nose:1.12, lips:1.05, brow:1.12, cheek:1.05 },
    jersey:"#4b2e83", trim:"#c9c9cf", numC:"#ffffff", shoe:"#c9c9cf", sole:"#4b2e83" },
  { id:"flash", name:"Flash Ito", pos:"PG", role:"Speedster", num:1, height:"6'1\"", scale:0.96,
    r:{ shoot:83, speed:99, dunk:68, def:74 }, skin:"#e7c09c", hair:"bun", hairC:"#0e0d0f", beard:null, sleeve:null, band:null,
    body:{ W:0.93, M:0.88, L:0.95, belly:0, D:0.93 }, face:{ jaw:0.93, chin:0.95, nose:0.9, lips:0.92, brow:0.88, cheek:1.05 },
    jersey:"#0f8b8d", trim:"#ffffff", numC:"#ffffff", shoe:"#ffffff", sole:"#0f8b8d" },
  { id:"maestro", name:"Maestro Reyes", pos:"SF", role:"Playmaker", num:7, height:"6'8\"", scale:1.03,
    r:{ shoot:86, speed:84, dunk:86, def:84 }, skin:"#a8724c", hair:"afro", hairC:"#1a110b", beard:"stubble", sleeve:null, band:null,
    body:{ W:1.06, M:1.02, L:1.02, belly:0, D:1.02 }, face:{ jaw:1.0, chin:1.0, nose:1.02, lips:1.05, brow:1.0, cheek:1.0 },
    jersey:"#1e7a46", trim:"#ffffff", numC:"#ffffff", shoe:"#ffffff", sole:"#1e7a46" },
  { id:"rook", name:"Rook Halvorsen", pos:"PF", role:"Lockdown Defender", num:21, height:"6'9\"", scale:1.05,
    r:{ shoot:72, speed:80, dunk:82, def:97 }, skin:"#efcbae", hair:"curly", hairC:"#8a6334", beard:null, sleeve:"L", sleeveC:"#f4f4f2", band:null,
    body:{ W:1.04, M:1.0, L:1.03, belly:0, D:1.0 }, face:{ jaw:1.05, chin:1.04, nose:1.0, lips:0.95, brow:1.02, cheek:0.98 },
    jersey:"#f26b21", trim:"#1c2a4a", numC:"#1c2a4a", shoe:"#1c2a4a", sole:"#f26b21" }
];
const ARCH_BY_ID=Object.fromEntries(ARCH.map(a=>[a.id,a]));
const ovr=a=>Math.round((a.r.shoot+a.r.speed+a.r.dunk+a.r.def)/4);

function makeDriver(){
  const G=()=>new THREE.Group();
  const root=G(), pelvis=G(); pelvis.position.y=DIM.PEL; root.add(pelvis);
  const torso=G(); torso.position.y=0.04; pelvis.add(torso);
  const neck=G(); neck.position.y=DIM.NECK; torso.add(neck);
  const head=G(); head.position.y=DIM.HEAD; neck.add(head);
  const arm=sd=>{
    const s=G(); s.position.set(sd*DIM.SHX,DIM.SHY,0); torso.add(s);
    const e=G(); e.position.y=-DIM.UA; s.add(e);
    const w=G(); w.position.y=-DIM.FA; e.add(w);
    const palmPt=new THREE.Object3D(); palmPt.position.set(0,-0.065,-0.03); w.add(palmPt);
    const f=[]; const th=G(); th.position.set(sd*0.036,-0.028,-0.014); th.rotation.set(0,-sd*0.45,sd*0.55); w.add(th); f.push(th);
    for(let i=0;i<4;i++){ const g=G(); g.position.set(sd*(0.03-i*0.02),-0.1,0); w.add(g); f.push(g); }
    return { s,e,w,f,palmPt };
  };
  const leg=sd=>{ const h=G(); h.position.set(sd*DIM.HIPX,-0.02,0); pelvis.add(h); const k=G(); k.position.y=-DIM.TH; h.add(k); const a=G(); a.position.y=-DIM.SH; k.add(a); return { h,k,a }; };
  const d={ root,pelvis,torso,neck,head, L:arm(-1), R:arm(1), LL:leg(-1), RL:leg(1) };
  d.bones={ pelvis, torso, neck, head, sL:d.L.s, eL:d.L.e, wL:d.L.w, sR:d.R.s, eR:d.R.e, wR:d.R.w, hL:d.LL.h, kL:d.LL.k, aL:d.LL.a, hR:d.RL.h, kR:d.RL.k, aR:d.RL.a };
  d.L.f.forEach((g,i)=>d.bones["fL"+i]=g); d.R.f.forEach((g,i)=>d.bones["fR"+i]=g);
  return d;
}
function setBindPose(d){
  Object.values(d.bones).forEach(g=>{ if(!g.userData.r0) g.userData.r0=g.rotation.clone(); g.rotation.copy(g.userData.r0); });
  d.pelvis.position.y=DIM.PEL;
  d.L.s.rotation.set(0,0,-0.5); d.R.s.rotation.set(0,0,0.5);
  d.LL.h.rotation.set(0,0,-0.04); d.RL.h.rotation.set(0,0,0.04);
  d.root.updateMatrixWorld(true);
}
// bind-pose matrices of the driver skeleton, shared by every build
const BIND=(()=>{
  const d=makeDriver(); setBindPose(d);
  const w={}, inv={}, pos={};
  for(const k of BONE_KEYS){ const g=d.bones[k]; w[k]=g.matrixWorld.clone(); inv[k]=g.matrixWorld.clone().invert(); pos[k]=new THREE.Vector3().setFromMatrixPosition(g.matrixWorld); }
  return { w, inv, pos };
})();
const rowM=m=>{ const e=m.elements; return [e[0],e[4],e[8],e[12],e[1],e[5],e[9],e[13],e[2],e[6],e[10],e[14]]; };
function primBox(q){
  const p=q.p; let b;
  switch(q.t){
    case 1: { const r=Math.max(p[2],p[3])*Math.max(p[4]||1,p[5]||1); b=[-r,Math.min(p[0],p[1])-r,-r, r,Math.max(p[0],p[1])+r,r]; break; }
    case 2: b=[p[0]-p[3],p[1]-p[4],p[2]-p[5], p[0]+p[3],p[1]+p[4],p[2]+p[5]]; break;
    case 3: b=[p[0]-p[3],p[1]-p[4],p[2]-p[5], p[0]+p[3],p[1]+p[4],p[2]+p[5]]; break;
    case 5: b=[p[0]-p[3],p[1]-p[3],p[2]-p[3], p[0]+p[3],p[1]+p[3],p[2]+p[3]]; break;
    case 6: { const r=Math.max(p[6],p[7]); b=[Math.min(p[0],p[3])-r,Math.min(p[1],p[4])-r,Math.min(p[2],p[5])-r, Math.max(p[0],p[3])+r,Math.max(p[1],p[4])+r,Math.max(p[2],p[5])+r]; break; }
    default: return null;
  }
  const n=q.n||0; b=[b[0]-n,b[1]-n,b[2]-n,b[3]+n,b[4]+n,b[5]+n];
  if(!q.bone) return b;
  const M=BIND.w[q.bone], out=[1e9,1e9,1e9,-1e9,-1e9,-1e9], v=new THREE.Vector3();
  for(let i=0;i<8;i++){ v.set(i&1?b[3]:b[0], i&2?b[4]:b[1], i&4?b[5]:b[2]).applyMatrix4(M); out[0]=Math.min(out[0],v.x); out[1]=Math.min(out[1],v.y); out[2]=Math.min(out[2],v.z); out[3]=Math.max(out[3],v.x); out[4]=Math.max(out[4],v.y); out[5]=Math.max(out[5],v.z); }
  return out;
}
// q: primitive. t = type, bone = driver bone it lives on (world job) or null (local job), p = params, op 0 union 1 subtract 2 intersect, k = blend
const Q=(t,bone,p,op=0,k=0,x={})=>Object.assign({ t, bone, p, op, k }, x);
function finishJob(job){
  const prims=job.prims.map(q=>{ const o={ t:q.t, p:q.p, op:q.op, k:q.k }; if(q.n){ o.n=q.n; o.nf=q.nf; } if(q.bone) o.m=rowM(BIND.inv[q.bone]); o.bb=primBox(q); return o; });
  let bb=[1e9,1e9,1e9,-1e9,-1e9,-1e9];
  prims.forEach(o=>{ if(o.op===0 && o.bb){ for(let i=0;i<3;i++){ bb[i]=Math.min(bb[i],o.bb[i]); bb[i+3]=Math.max(bb[i+3],o.bb[i+3]); } } });
  if(job.clip){ for(let i=0;i<3;i++){ bb[i]=Math.max(bb[i],job.clip[i]); bb[i+3]=Math.min(bb[i+3],job.clip[i+3]); } }
  const h=job.h, pad=(job.off||0)+h*2;
  const o=[bb[0]-pad,bb[1]-pad,bb[2]-pad], n=[0,1,2].map(i=>Math.ceil((bb[i+3]-bb[i]+pad*2)/h)+1);
  const trim=job.trim ? job.trim.map(t=>({ w:t.w, prim:prims[job.prims.indexOf(t.prim)] || (()=>{ const q=t.prim, oo={ t:q.t, p:q.p, op:0, k:0 }; if(q.bone) oo.m=rowM(BIND.inv[q.bone]); return oo; })() })) : null;
  return { prims, h, o, n, off:job.off||0, aoK:job.aoK, aoD:job.aoD, trim, segs:job.segs||null };
}
// skin segments: each vertex follows the nearest bone and blends with its neighbour near joints
const SEG_DEF=[
  ["pelvis",null,0.15,-1, [0,-0.09,0],[0,0.06,0], 0.06,0],
  ["torso","pelvis",0.17,-1, [0,0,0],[0,0.53,0], 0.11,0],
  ["neck","torso",0.06,"head", [0,0,0],[0,0.1,0], 0.05,0.04],
  ["head","neck",0.1,-1, [0,0,0],[0,0.2,0], 0.04,0],
  ["sL","torso",0.05,"eL", [0,0,0],[0,-DIM.UA,0], 0.09,0.05], ["eL","sL",0.04,"wL", [0,0,0],[0,-DIM.FA,0], 0.05,0.03], ["wL","eL",0.035,-1, [0,0,0],[0,-0.1,0], 0.03,0],
  ["sR","torso",0.05,"eR", [0,0,0],[0,-DIM.UA,0], 0.09,0.05], ["eR","sR",0.04,"wR", [0,0,0],[0,-DIM.FA,0], 0.05,0.03], ["wR","eR",0.035,-1, [0,0,0],[0,-0.1,0], 0.03,0],
  ["hL","pelvis",0.08,"kL", [0,0,0],[0,-DIM.TH,0], 0.09,0.06], ["kL","hL",0.05,"aL", [0,0,0],[0,-DIM.SH,0], 0.06,0.04], ["aL","kL",0.045,-1, [0,0,0],[0,-0.04,-0.12], 0.03,0],
  ["hR","pelvis",0.08,"kR", [0,0,0],[0,-DIM.TH,0], 0.09,0.06], ["kR","hR",0.05,"aR", [0,0,0],[0,-DIM.SH,0], 0.06,0.04], ["aR","kR",0.045,-1, [0,0,0],[0,-0.04,-0.12], 0.03,0]
];
function segsFor(keys,extra=[],rad={}){
  const defs=SEG_DEF.filter(d=>keys.includes(d[0])).map(d=>rad[d[0]]?Object.assign([...d],{2:rad[d[0]][0],6:rad[d[0]][1]}):d).concat(extra);
  const idx=k=>defs.findIndex(d=>d[0]===k);
  return defs.map(d=>{
    const M=BIND.w[d[0]], a=new THREE.Vector3(...d[4]).applyMatrix4(M), c=new THREE.Vector3(...d[5]).applyMatrix4(M);
    return { b:BONE_KEYS.indexOf(d[0]), a:a.toArray(), c:c.toArray(), r:d[2], par:d[1]?idx(d[1]):-1, ch:typeof d[3]==="string"?idx(d[3]):-1, bz:d[6], ez:d[7] };
  });
}

/* ----- anatomy ----- */
function torsoPrims(B,grow=0){
  const W=B.W, M=B.M, D=B.D, g=grow;
  return [
    Q(2,"torso",[0,0.30,0.005, 0.15*W+g,0.19+g,0.11*D+g]),
    Q(2,"torso",[-0.07,0.36,-0.066, 0.078*M+g,0.062+g,0.048*M+g],0,0.04), Q(2,"torso",[0.07,0.36,-0.066, 0.078*M+g,0.062+g,0.048*M+g],0,0.04),
    Q(2,"torso",[0,0.13,-0.012, 0.128+0.035*B.belly+g,0.16+g,0.098+0.05*B.belly+g],0,0.06),
    Q(2,"torso",[-0.115,0.29,0.025, 0.062*M+g,0.14+g,0.065+g],0,0.05), Q(2,"torso",[0.115,0.29,0.025, 0.062*M+g,0.14+g,0.065+g],0,0.05),
    Q(2,"torso",[0,0.42,0.035, 0.13*W+g,0.08+g,0.07+g],0,0.05),
    Q(6,"torso",[-0.15*W,0.47,0.015, -0.035,0.565,0.012, 0.048*M+g,0.042+g],0,0.04), Q(6,"torso",[0.15*W,0.47,0.015, 0.035,0.565,0.012, 0.048*M+g,0.042+g],0,0.04),
    Q(2,"pelvis",[0,0.0,0.0, 0.155+g,0.11+g,0.105+g],0,0.07),
    Q(2,"pelvis",[-0.065,-0.05,0.05, 0.075+g,0.085+g,0.062+g],0,0.04), Q(2,"pelvis",[0.065,-0.05,0.05, 0.075+g,0.085+g,0.062+g],0,0.04)
  ];
}
function armPrims(B,sd){
  const s=sd<0?"L":"R", M=B.M;
  return [
    Q(2,"s"+s,[sd*0.012,-0.035,0, 0.066*M,0.088,0.068*M],0,0.035),
    Q(1,"s"+s,[0,-0.31, 0.054*M,0.044],0,0.03),
    Q(2,"s"+s,[0,-0.15,-0.024, 0.041*M,0.085,0.037*M],0,0.025),
    Q(2,"s"+s,[sd*0.004,-0.13,0.026, 0.043*M,0.095,0.036*M],0,0.025),
    Q(1,"e"+s,[0.01,-0.268, 0.045*M,0.031],0,0.03),
    Q(2,"e"+s,[sd*0.012,-0.06,-0.006, 0.043*M,0.085,0.036],0,0.025),
    Q(2,"e"+s,[-sd*0.008,-0.07,0.012, 0.036,0.08,0.032],0,0.025)
  ];
}
function legPrims(B,sd){
  const s=sd<0?"L":"R", L=B.L;
  return [
    Q(1,"h"+s,[0.02,-0.46, 0.088*L,0.052],0,0.045),
    Q(2,"h"+s,[0,-0.2,-0.034, 0.07*L,0.17,0.06*L],0,0.04),
    Q(2,"h"+s,[sd*0.04,-0.24,-0.008, 0.05*L,0.14,0.052],0,0.03),
    Q(2,"h"+s,[0,-0.21,0.038, 0.064*L,0.16,0.052],0,0.03),
    Q(2,"h"+s,[-sd*0.035,-0.1,0, 0.05,0.1,0.05],0,0.03),
    Q(5,"k"+s,[0,0,-0.036, 0.036],0,0.02),
    Q(1,"k"+s,[0,-0.44, 0.052,0.033],0,0.03),
    Q(2,"k"+s,[0,-0.12,0.03, 0.052*L,0.1,0.05*L],0,0.03),
    Q(2,"k"+s,[-sd*0.016,-0.14,0.022, 0.04*L,0.08,0.04],0,0.025),
    Q(5,"a"+s,[0,0,0, 0.034],0,0.02)
  ];
}
function bodyJob(A){
  const B=A.body;
  const prims=[...torsoPrims(B), Q(1,"neck",[-0.06,0.13, 0.062,0.055],0,0.045), ...armPrims(B,-1), ...armPrims(B,1), ...legPrims(B,-1), ...legPrims(B,1)];
  return finishJob({ prims, h:0.0105, segs:segsFor(["pelvis","torso","neck","sL","eL","wL","sR","eR","wR","hL","kL","aL","hR","kR","aR"],[],{ pelvis:[0.13,0.06], hL:[0.1,0.11], hR:[0.1,0.11] }) });
}
function jerseyJob(A){
  const B=A.body, sh=torsoPrims(B,0.004).slice(0,9).map(q=>Object.assign(q,{ k:Math.max(q.k,0.08) }));
  sh.push(Q(2,"pelvis",[0,0.03,0, 0.16,0.08,0.11],0,0.08));
  sh.push(Q(1,"torso",[0.4,-0.14, 0.152*B.W+0.01*B.belly,0.168+0.02*B.belly, 1,0.72+0.08*B.belly],0,0.1));
  const holeL=Q(5,"sL",[-0.03,-0.02,0, 0.1],1,0.015), holeR=Q(5,"sR",[0.03,-0.02,0, 0.1],1,0.015);
  const neckHole=Q(2,"torso",[0,0.57,-0.012, 0.086,0.075,0.082],1,0.02), scoop=Q(2,"torso",[0,0.535,-0.088, 0.048,0.05,0.045],1,0.015);
  const hem=Q(4,"torso",[0,-1,0, 0.05],2,0);
  return finishJob({ prims:[...sh,holeL,holeR,neckHole,scoop,hem], h:0.0085, off:0.016, aoK:0.8,
    trim:[{ prim:holeL, w:0.015 },{ prim:holeR, w:0.015 },{ prim:neckHole, w:0.011 },{ prim:scoop, w:0.011 }],
    segs:segsFor(["pelvis","torso","neck","sL","sR"]) });
}
function shortsJob(A){
  const B=A.body, L=B.L;
  const prims=[ Q(2,"pelvis",[0,0.01,0, 0.19+0.02*B.belly,0.125,0.135+0.02*B.belly]), Q(2,"pelvis",[-0.065,-0.05,0.05, 0.08,0.09,0.07],0,0.05), Q(2,"pelvis",[0.065,-0.05,0.05, 0.08,0.09,0.07],0,0.05),
    Q(1,"hL",[0.03,-0.38, 0.112*L,0.108],0,0.07), Q(1,"hR",[0.03,-0.38, 0.112*L,0.108],0,0.07) ];
  const top=Q(4,"pelvis",[0,1,0, 0.075],2,0), bottom=Q(4,"pelvis",[0,-1,0, 0.38],2,0);
  return finishJob({ prims:[...prims,top,bottom], h:0.0095, off:0.012, aoK:0.9,
    trim:[{ prim:Q(4,"pelvis",[0,1,0, 0.075]), w:0.03 },{ prim:Q(4,"pelvis",[0,-1,0, 0.38]), w:0.024 }],
    segs:segsFor(["pelvis","torso","hL","kL","hR","kR"],[],{ pelvis:[0.11,0.06], hL:[0.13,0.12], hR:[0.13,0.12] }) });
}
function handJob(sd){
  const s=sd<0?"L":"R", w="w"+s;
  const prims=[ Q(3,w,[0,-0.052,0, 0.042,0.05,0.016, 0.013]), Q(2,w,[sd*0.028,-0.035,-0.012, 0.022,0.032,0.017],0,0.015), Q(1,w,[0.02,-0.02, 0.031,0.034],0,0.015),
    Q(6,w,[sd*0.035,-0.09,0.002, -sd*0.035,-0.09,0.002, 0.014,0.013],0,0.01) ];
  for(let i=0;i<5;i++){ const f="f"+s+i, L=FINGER_LEN[i];
    prims.push(Q(1,f,[0.006,-L, i===0?0.0125:0.0108, i===0?0.0095:0.0086],0,0.008));
    if(i>0) prims.push(Q(5,f,[0,-L*0.42,0.002, 0.0112],0,0.006));
  }
  const extra=[]; for(let i=0;i<5;i++) extra.push(["f"+s+i,w,0.011,-1,[0,0,0],[0,-FINGER_LEN[i],0],0.014,0]);
  return finishJob({ prims, h:0.0032, aoD:[0.004,0.009,0.018,0.03], segs:segsFor([w],extra) });
}
function headJob(A){
  const F=A.face;
  const prims=[
    Q(2,null,[0,0.115,0.012, 0.077,0.093,0.097]),
    Q(2,null,[0,0.06,-0.03, 0.064*F.jaw,0.072,0.07],0,0.035),
    Q(2,null,[0,0.02,-0.04, 0.057*F.jaw,0.04,0.058],0,0.03),
    Q(2,null,[-0.05,0.02,-0.005, 0.02*F.jaw,0.028,0.032],0,0.025), Q(2,null,[0.05,0.02,-0.005, 0.02*F.jaw,0.028,0.032],0,0.025),
    Q(2,null,[0,-0.004,-0.075, 0.026*F.chin,0.022,0.021],0,0.02),
    Q(2,null,[-0.046,0.075,-0.063, 0.022*F.cheek,0.016,0.02],0,0.02), Q(2,null,[0.046,0.075,-0.063, 0.022*F.cheek,0.016,0.02],0,0.02),
    Q(6,null,[-0.042,0.117,-0.085, 0.042,0.117,-0.085, 0.013*F.brow,0.013*F.brow],0,0.02),
    Q(6,null,[0,0.108,-0.094, 0,0.066,-0.116, 0.0085,0.0125*F.nose],0,0.012),
    Q(5,null,[0,0.063,-0.116, 0.0135*F.nose],0,0.008),
    Q(5,null,[-0.0155*F.nose,0.059,-0.104, 0.0105*F.nose],0,0.008), Q(5,null,[0.0155*F.nose,0.059,-0.104, 0.0105*F.nose],0,0.008),
    Q(5,null,[-0.0085,0.0535,-0.111, 0.0042],1,0.003), Q(5,null,[0.0085,0.0535,-0.111, 0.0042],1,0.003),
    Q(2,null,[0,0.038,-0.098, 0.022*F.lips,0.0075*F.lips,0.011],0,0.008),
    Q(2,null,[0,0.026,-0.096, 0.02*F.lips,0.0088*F.lips,0.011],0,0.008),
    Q(2,null,[0,0.032,-0.106, 0.021*F.lips,0.0016,0.012],1,0.003),
    Q(2,null,[-0.032,0.093,-0.093, 0.019,0.012,0.013],1,0.012), Q(2,null,[0.032,0.093,-0.093, 0.019,0.012,0.013],1,0.012),
    Q(2,null,[-0.032,0.102,-0.091, 0.017,0.0055,0.01],0,0.006), Q(2,null,[0.032,0.102,-0.091, 0.017,0.0055,0.01],0,0.006),
    Q(2,null,[-0.079,0.088,0.012, 0.011,0.03,0.02],0,0.01), Q(2,null,[0.079,0.088,0.012, 0.011,0.03,0.02],0,0.01),
    Q(2,null,[-0.084,0.088,0.008, 0.006,0.019,0.012],1,0.004), Q(2,null,[0.084,0.088,0.008, 0.006,0.019,0.012],1,0.004),
    Q(6,null,[0,-0.145,0.008, 0,0.04,0.01, 0.056,0.054],0,0.03),
    Q(5,null,[0,-0.045,-0.043, 0.012],0,0.015)
  ];
  return finishJob({ prims, h:0.0042, aoD:[0.004,0.009,0.018,0.032], aoK:1.2 });
}
function hairline(shift=0){ const n=Math.hypot(1,0.55); return Q(4,null,[0,-1/n,-0.55/n, -(0.10325-shift)/n],2,0); }
function hairJob(A){
  const st=A.hair; if(st==="bald") return null;
  const ears=[Q(5,null,[-0.084,0.088,0.01, 0.03],1,0.01), Q(5,null,[0.084,0.088,0.01, 0.03],1,0.01)];
  let prims;
  if(st==="afro") prims=[Q(2,null,[0,0.165,0.02, 0.118,0.105,0.122],0,0,{ n:0.004, nf:170 }), hairline(0.012), ...ears];
  else {
    const off=st==="buzz"?0.0035:0.006;
    prims=[Q(2,null,[0,0.115,0.012, 0.077+off,0.093+off,0.097+off])];
    if(st==="curly") prims.push(Q(2,null,[0,0.185,-0.004, 0.08,0.05,0.09],0,0.03,{ n:0.005, nf:150 }));
    if(st==="bun") prims.push(Q(5,null,[0,0.205,0.06, 0.032],0,0.02,{ n:0.002, nf:200 }));
    if(st==="fade") prims.push(Q(2,null,[0,0.18,-0.01, 0.07,0.035,0.085],0,0.03,{ n:0.0015, nf:220 }));
    prims.push(hairline(st==="buzz"?-0.004:0), ...ears);
  }
  return finishJob({ prims, h:0.004, aoK:0.9 });
}
function beardJob(A){
  if(!A.beard) return null;
  const F=A.face, off=A.beard==="full"?0.007:0.0028;
  const prims=[ Q(2,null,[0,0.06,-0.03, 0.064*F.jaw+off,0.072+off,0.07+off]), Q(2,null,[0,0.02,-0.04, 0.057*F.jaw+off,0.04+off,0.058+off],0,0.03),
    Q(2,null,[0,-0.004,-0.075, 0.026*F.chin+off,0.022+off,0.021+off],0,0.02,A.beard==="full"?{ n:0.0015, nf:250 }:{}),
    Q(4,null,[0,1,0, 0.066],2,0.01), Q(4,null,[0,0,1, 0.03],2,0.01),
    Q(2,null,[0,0.032,-0.1, 0.024,0.012,0.03],1,0.004), Q(2,null,[0,0.08,-0.09, 0.03,0.02,0.04],1,0.01) ];
  return finishJob({ prims, h:0.0035, aoK:0.8 });
}
function shoeJob(){
  const prims=[ Q(2,null,[0,-0.042,0.035, 0.047,0.05,0.055]), Q(2,null,[0,-0.048,-0.05, 0.052,0.046,0.085],0,0.03), Q(2,null,[0,-0.058,-0.135, 0.046,0.032,0.058],0,0.03),
    Q(6,null,[0,-0.04,0.006, 0,0.07,0.01, 0.052,0.048],0,0.03), Q(4,null,[0,-1,0, 0.078],2,0) ];
  return finishJob({ prims, h:0.0045, aoK:0.8, trim:[{ prim:Q(4,null,[0,1,0, -0.03]), w:0.011 },{ prim:Q(4,null,[0,1,0, 0.06]), w:0.012 }] });
}
function soleJob(){ return finishJob({ prims:[ Q(3,null,[0,-0.085,-0.05, 0.055,0.013,0.15, 0.011]), Q(2,null,[0,-0.085,-0.05, 0.062,0.05,0.168],2,0.01) ], h:0.0045, aoK:0.5 }); }
function sockJob(){ return finishJob({ prims:[ Q(1,null,[-0.28,-0.43, 0.047,0.039]) ], h:0.005, aoK:0.6 }); }
function sleeveJobs(A){
  // the sleeve is the arm itself, grown by a few millimetres, so it hugs every muscle
  const sd=A.sleeve==="L"?-1:1, ap=armPrims(A.body,sd).map(q=>Object.assign({},q,{ bone:null }));
  return [ finishJob({ prims:[...ap.slice(0,4), Q(4,null,[0,1,0, -0.075],2,0.01)], h:0.0045, off:0.0035, aoK:0.6 }),
           finishJob({ prims:[...ap.slice(4,7), Q(4,null,[0,-1,0, 0.24],2,0.01)], h:0.0045, off:0.0035, aoK:0.6 }) ];
}

/* ----- background builders (Web Workers, with a main-thread fallback) ----- */
const MESH_SRC = sdfEval.toString()+"\n"+sdfSkin.toString()+"\n"+sdfMesh.toString()+"\nself.onmessage=e=>{ const out=sdfMesh(e.data.job); const tr=[out.pos.buffer,out.nrm.buffer,out.ao.buffer,out.idx.buffer]; if(out.trim) tr.push(out.trim.buffer); if(out.si){ tr.push(out.si.buffer,out.sw.buffer); } self.postMessage({ id:e.data.id, out }, tr); };";
const meshPool=(()=>{
  const n=Math.max(1,Math.min(4,(navigator.hardwareConcurrency||4)-1)); let workers=[];
  try{ const url=URL.createObjectURL(new Blob([MESH_SRC],{ type:"text/javascript" })); for(let i=0;i<n;i++) workers.push(new Worker(url)); }catch(e){ workers=[]; }
  const pending=new Map(), queue=[], idle=workers.slice(); let seq=0;
  const pump=()=>{ while(idle.length && queue.length){ const w=idle.pop(), j=queue.shift(); w._job=j; w.postMessage({ id:j.id, job:j.job }); } };
  workers.forEach(w=>{ w.onmessage=e=>{ const p=pending.get(e.data.id); pending.delete(e.data.id); idle.push(w); pump(); p&&p.res(e.data.out); };
    w.onerror=()=>{ const j=w._job; if(j){ try{ pending.get(j.id).res(sdfMesh(j.job)); }catch(err){ pending.get(j.id).rej(err); } pending.delete(j.id); } idle.push(w); pump(); }; });
  return { run(job){ return new Promise((res,rej)=>{ if(!workers.length){ setTimeout(()=>{ try{ res(sdfMesh(job)); }catch(err){ rej(err); } },0); return; } const id=++seq; pending.set(id,{ res,rej }); queue.push({ id, job }); pump(); }); } };
})();
function geoFrom(out, local){
  const g=new THREE.BufferGeometry();
  g.setAttribute("position",new THREE.BufferAttribute(out.pos,3));
  g.setAttribute("normal",new THREE.BufferAttribute(out.nrm,3));
  const c=new Float32Array(out.ao.length*3); for(let i=0;i<out.ao.length;i++){ c[i*3]=c[i*3+1]=c[i*3+2]=out.ao[i]; }
  g.setAttribute("color",new THREE.BufferAttribute(c,3));
  if(out.trim) g.setAttribute("aTrim",new THREE.BufferAttribute(out.trim,1));
  if(out.si){ g.setAttribute("skinIndex",new THREE.Uint16BufferAttribute(out.si,4)); g.setAttribute("skinWeight",new THREE.BufferAttribute(out.sw,4)); }
  g.setIndex(new THREE.BufferAttribute(out.idx,1));
  g.computeBoundingSphere();
  return g;
}
const buildCache=new Map();
function buildArch(id){
  if(buildCache.has(id)) return buildCache.get(id);
  const A=ARCH_BY_ID[id];
  const jobs={ body:bodyJob(A), jersey:jerseyJob(A), shorts:shortsJob(A), handL:handJob(-1), handR:handJob(1), head:headJob(A), hair:hairJob(A), beard:beardJob(A), shoe:shoeJob(), sole:soleJob(), sock:sockJob() };
  if(A.sleeve){ const [u,f]=sleeveJobs(A); jobs.sleeveU=u; jobs.sleeveF=f; }
  const keys=Object.keys(jobs).filter(k=>jobs[k]);
  const p=Promise.all(keys.map(k=>meshPool.run(jobs[k]))).then(outs=>{
    const geo={}; keys.forEach((k,i)=>geo[k]=geoFrom(outs[i]));
    // where to print the jersey numbers: the front and back of the jersey at chest height, in torso space
    const inv=BIND.inv.torso, v=new THREE.Vector3(), P=outs[keys.indexOf("jersey")].pos; let fz=-0.13, bz=0.13;
    for(let i=0;i<P.length;i+=3){ v.set(P[i],P[i+1],P[i+2]).applyMatrix4(inv); if(Math.abs(v.x)<0.03 && Math.abs(v.y-0.31)<0.03){ fz=Math.min(fz,v.z); bz=Math.max(bz,v.z); } }
    return { geo, fz, bz };
  });
  buildCache.set(id,p); return p;
}

/* ----- materials ----- */
function regionMaterial(base,trim,rough,skinning=false){
  const m=new THREE.MeshStandardMaterial({ color:0xffffff, roughness:rough, metalness:0, vertexColors:true, skinning });
  m.userData.base={ value:new THREE.Color(base) }; m.userData.trim={ value:new THREE.Color(trim) };
  m.onBeforeCompile=sh=>{
    sh.uniforms.uBase=m.userData.base; sh.uniforms.uTrim=m.userData.trim;
    sh.vertexShader=sh.vertexShader.replace("#include <common>","#include <common>\nattribute float aTrim;\nvarying float vTrim;").replace("#include <color_vertex>","#include <color_vertex>\nvTrim=aTrim;");
    sh.fragmentShader=sh.fragmentShader.replace("#include <common>","#include <common>\nuniform vec3 uBase;\nuniform vec3 uTrim;\nvarying float vTrim;").replace("#include <color_fragment>","diffuseColor.rgb=mix(uBase,uTrim,smoothstep(0.42,0.58,vTrim))*vColor;");
  };
  m.customProgramCacheKey=()=>"region"+(skinning?"S":"");
  return m;
}
function jerseyDecal(num,name,numC,trimC,back){
  const t=tex(256,256,(g,w,h)=>{ g.clearRect(0,0,w,h); g.textAlign="center"; g.textBaseline="middle";
    if(back && name){ g.font="700 32px 'Chakra Petch',sans-serif"; g.fillStyle=numC; g.fillText(name.toUpperCase().slice(0,12),w/2,34); }
    g.font=`700 ${back?150:160}px 'Chakra Petch',sans-serif`; g.lineWidth=10; g.strokeStyle=trimC; g.fillStyle=numC; const y=back?160:138; g.strokeText(String(num),w/2,y); g.fillText(String(num),w/2,y); });
  const geo=new THREE.PlaneGeometry(back?0.24:0.2,back?0.24:0.2,12,1), p=geo.attributes.position;
  for(let i=0;i<p.count;i++){ const x=p.getX(i); p.setZ(i,(back?-1:1)*0.9*x*x); }
  geo.computeVertexNormals();
  return new THREE.Mesh(geo,new THREE.MeshStandardMaterial({ map:t, transparent:true, roughness:0.6, polygonOffset:true, polygonOffsetFactor:-2 }));
}
function nameSprite(text,color){
  const c=document.createElement("canvas"); c.width=512; c.height=96; const g=c.getContext("2d");
  g.font="700 44px 'Chakra Petch',sans-serif"; const w=Math.min(500,g.measureText(text).width+60);
  g.fillStyle="rgba(10,14,20,.78)"; g.beginPath(); g.moveTo(256-w/2+20,14); g.arcTo(256+w/2,14,256+w/2,82,20); g.arcTo(256+w/2,82,256-w/2,82,20); g.arcTo(256-w/2,82,256-w/2,14,20); g.arcTo(256-w/2,14,256+w/2,14,20); g.fill();
  g.strokeStyle=color; g.lineWidth=6; g.stroke(); g.fillStyle="#ffffff"; g.textAlign="center"; g.textBaseline="middle"; g.fillText(text,256,50);
  const sp=new THREE.Sprite(new THREE.SpriteMaterial({ map:new THREE.CanvasTexture(c), transparent:true, depthWrite:false }));
  sp.scale.set(1.3,0.244,1); sp.position.y=2.32; return sp;
}
const eyeGeo=new THREE.SphereGeometry(0.0125,16,12), irisGeo=new THREE.SphereGeometry(0.0062,12,8), pupilGeo=new THREE.SphereGeometry(0.0032,8,6);
const eyeMatW=new THREE.MeshStandardMaterial({ color:0xf3efe9, roughness:0.2 }), irisMat=new THREE.MeshStandardMaterial({ color:0x3b2416, roughness:0.25 }), pupilMat=new THREE.MeshBasicMaterial({ color:0x050505 });
const bandGeo=new THREE.TorusGeometry(0.098,0.012,8,32);

/* ----- one player on the court ----- */
function makeAvatar(name,archId,opts={}){
  const A=ARCH_BY_ID[archId]||ARCH[0];
  const d=makeDriver(); setBindPose(d);
  d.root.scale.setScalar(A.scale);
  const bones=BONE_KEYS.map(k=>{ const b=new THREE.Bone(); d.bones[k].add(b); return b; });
  d.root.updateMatrixWorld(true);
  const skeleton=new THREE.Skeleton(bones);
  const mats=[];
  const keep=m=>{ mats.push(m); return m; };
  const skin=keep(new THREE.MeshStandardMaterial({ color:A.skin, roughness:0.52, metalness:0, vertexColors:true }));
  const skinS=keep(new THREE.MeshStandardMaterial({ color:A.skin, roughness:0.52, metalness:0, vertexColors:true, skinning:true }));
  const hairM=keep(new THREE.MeshStandardMaterial({ color:A.hairC, roughness:0.88, vertexColors:true }));
  const jerseyM=keep(regionMaterial(A.jersey,A.trim,0.66,true)), shortsM=keep(regionMaterial(A.jersey,A.trim,0.7,true)), shoeM=keep(regionMaterial(A.shoe,A.sole,0.45));
  const soleM=keep(new THREE.MeshStandardMaterial({ color:A.sole, roughness:0.6, vertexColors:true })), sockM=keep(new THREE.MeshStandardMaterial({ color:0xf7f7f5, roughness:0.85, vertexColors:true }));
  const sleeveM=keep(new THREE.MeshStandardMaterial({ color:A.sleeveC||"#111", roughness:0.5, vertexColors:true }));
  const av={ root:d.root, d, pelvis:d.pelvis, torso:d.torso, neck:d.neck, L:d.L, R:d.R, LL:d.LL, RL:d.RL, arch:A, phase:0, cur:{}, ready:false, meshes:[] };
  const label=opts.self||!name ? null : nameSprite(name,A.jersey); if(label){ label.position.y=2.32/A.scale; d.root.add(label); }
  const host=opts.scene||scene; host.add(d.root);
  d.root.visible=false;
  av.dispose=()=>{ av.gone=true; host.remove(d.root); mats.forEach(m=>{ if(m.map) m.map.dispose(); m.dispose(); }); if(label){ label.material.map.dispose(); label.material.dispose(); } };
  buildArch(A.id).then(({ geo, fz, bz })=>{
    if(av.gone) return;
    // skinned parts are bound in the bind pose, then the driver is free to move
    const keepPos=d.root.position.clone(), keepRot=d.root.rotation.clone(), keepPel=d.pelvis.position.y;
    d.root.position.set(0,0,0); d.root.rotation.set(0,0,0);
    setBindPose(d); d.root.updateMatrixWorld(true); skeleton.calculateInverses();
    const skinned=(g,m)=>{ const s=new THREE.SkinnedMesh(g,m); s.castShadow=true; s.frustumCulled=false; d.root.add(s); s.updateMatrixWorld(true); s.bind(skeleton); av.meshes.push(s); return s; };
    // geometry is in bind space at scale 1; the root carries the player's height
    skinned(geo.body,skinS); skinned(geo.jersey,jerseyM); skinned(geo.shorts,shortsM); skinned(geo.handL,skinS); skinned(geo.handR,skinS);
    const rigid=(g,m,parent,pos)=>{ const o=new THREE.Mesh(g,m); o.castShadow=true; if(pos) o.position.copy(pos); parent.add(o); av.meshes.push(o); return o; };
    rigid(geo.head,skin,d.head); if(geo.hair) rigid(geo.hair,hairM,d.head); if(geo.beard) rigid(geo.beard,hairM,d.head);
    [-1,1].forEach(sd=>{ const ew=rigid(eyeGeo,eyeMatW,d.head,new THREE.Vector3(sd*0.032,0.093,-0.083)); rigid(irisGeo,irisMat,d.head,new THREE.Vector3(sd*0.032,0.093,-0.0915)); rigid(pupilGeo,pupilMat,d.head,new THREE.Vector3(sd*0.032,0.093,-0.0952)); });
    [d.LL.a,d.RL.a].forEach(a=>{ rigid(geo.shoe,shoeM,a); rigid(geo.sole,soleM,a); });
    [d.LL.k,d.RL.k].forEach(k=>rigid(geo.sock,sockM,k));
    if(A.sleeve && geo.sleeveU){ const arm=A.sleeve==="L"?d.L:d.R; rigid(geo.sleeveU,sleeveM,arm.s); rigid(geo.sleeveF,sleeveM,arm.e); }
    if(A.band){ const bm=keep(new THREE.MeshStandardMaterial({ color:A.band, roughness:0.7 })); const b=rigid(bandGeo,bm,d.head,new THREE.Vector3(0,0.14,0.014)); b.rotation.x=Math.PI/2+0.22; b.scale.set(0.84,1.07,1); }
    const front=jerseyDecal(A.num,"",A.numC,A.trim,false); front.position.set(0,0.31,fz-0.004); front.rotation.y=Math.PI; d.torso.add(front); mats.push(front.material);
    const back=jerseyDecal(A.num,opts.label!==undefined?opts.label:name,A.numC,A.trim,true); back.position.set(0,0.3,bz+0.004); d.torso.add(back); mats.push(back.material);
    d.root.position.copy(keepPos); d.root.rotation.copy(keepRot); d.pelvis.position.y=keepPel;
    av.ready=true; d.root.visible=av.visible!==false;
  });
  return av;
}
const ext=(h,k)=>0.02+0.46*Math.cos(h)+0.44*Math.cos(h+k)+0.088;

/* ---------- poses: the driver skeleton is animated procedurally, the skinned body follows ---------- */
// two-bone reach for a dribbling hand: puts the palm on top of the ball (side "L" or "R")
function armIK(T,P,side,w){
  const sd=side==="R"?1:-1;
  const shY=(0.935+0.05*w)+0.04+DIM.SHY*Math.cos(T.lean), shF=DIM.SHY*Math.sin(T.lean);
  const tx=P.ballF-shF, ty=(P.ballY+P.br+0.02)-shY, u=DIM.UA, f=DIM.FA+0.06;
  const L=clamp(Math.hypot(tx,ty),0.12,u+f-0.002), a=Math.atan2(tx,-ty);
  const beta=Math.acos(clamp((u*u+L*L-f*f)/(2*u*L),-1,1)), e=Math.PI-Math.acos(clamp((u*u+f*f-L*L)/(2*u*f),-1,1));
  T["s"+side+"x"]=a-beta+T.lean; T["e"+side]=e; T["s"+side+"z"]=sd*clamp(0.08+(P.ballR*sd-DIM.SHX)*1.5,-0.4,0.75); T["w"+side]=-0.35; T["fin"+side]=0.2;
}
function poseTargets(av,mode,P){
  const T={ lean:0.06,neck:0,twist:0,roll:0, sLx:0.08,sLz:-0.1,eL:0.22,wL:0, sRx:0.08,sRz:0.1,eR:0.22,wR:0, hL:0.02,kL:-0.05,hR:0.02,kR:-0.05, hLz:-0.04,hRz:0.04, finL:0.45,finR:0.45,tri:0,air:0 };
  const sp=P.speed, w=Math.min(1,sp/1.4), s=Math.min(1,sp/6), ph=av.phase;
  const gait=(stH,stK,swing)=>{
    const gh=p=>0.08+(0.38+0.4*s)*Math.sin(p), gk=p=>-(0.12+(0.45+0.85*s)*Math.max(0,Math.sin(p+1.7)));
    T.hL=lerp(stH,gh(ph),w); T.kL=lerp(stK,gk(ph),w); T.hR=lerp(stH,gh(ph+Math.PI),w); T.kR=lerp(stK,gk(ph+Math.PI),w);
    if(swing){ T.sLx=0.08-(0.3+0.45*s)*w*Math.sin(ph); T.sRx=0.08+(0.3+0.45*s)*w*Math.sin(ph); T.eL=T.eR=0.22+1.0*w; }
  };
  const chest=()=>{ T.sLx=T.sRx=1.05; T.eL=T.eR=1.65; T.sLz=0.12; T.sRz=-0.12; T.finL=T.finR=0.6; };
  switch(mode){
    case "free": gait(0.03,-0.06,true); T.lean=0.04+0.22*s; T.hLz=-0.05; T.hRz=0.05; break;
    case "def": {
      // defensive slide: low, wide, arms out, small shuffle steps
      const sh=Math.min(1,sp/1.2), o=Math.sin(ph);
      T.lean=0.34; T.neck=-0.28; T.hL=T.hR=0.66; T.kL=T.kR=-1.15;
      T.hLz=-0.3-0.13*sh*o; T.hRz=0.3-0.13*sh*o;
      T.kL-=0.3*sh*Math.max(0,o); T.kR-=0.3*sh*Math.max(0,-o);
      T.sLx=T.sRx=0.5; T.sLz=-1.1-0.08*o*sh; T.sRz=1.1-0.08*o*sh; T.eL=T.eR=0.55; T.wL=T.wR=0.25; T.finL=T.finR=0.12; break; }
    case "dribble": case "prot": {
      const prot=mode==="prot";
      gait(prot?0.6:0.42, prot?-1.1:-0.8, false); T.lean=(prot?0.44:0.24)+0.12*s;
      if(prot){ T.hLz=-0.16; T.hRz=0.16; }
      const dh=P.ballR>=0?1:-1, act=dh>0?"R":"L", off=dh>0?"L":"R", os=-dh;
      T["s"+off+"x"]=prot?0.95:lerp(0.72,0.12+(0.35+0.4*s)*Math.sin(ph+(off==="L"?Math.PI:0)),w);
      T["s"+off+"z"]=os*(prot?0.28:lerp(0.42,0.12,w)); T["e"+off]=prot?1.45:lerp(0.95,1.1,w); T["fin"+off]=0.35;
      armIK(T,P,act,w);
      // signature moves change the legs and shoulders
      if(P.dm==="x"){ const lead=P.dl>0?"R":"L", trail=P.dl>0?"L":"R"; T["h"+lead]=0.62; T["k"+lead]=-0.8; T["h"+trail]=-0.28; T["k"+trail]=-0.55; T.lean+=0.1; }
      else if(P.dm==="c"){ T.kL-=0.18; T.kR-=0.18; T.hL+=0.1; T.hR+=0.1; T.roll=dh*0.08; }
      else if(P.dm==="i"){ T.roll=-dh*0.14; T.twist=-dh*0.18; }
      else if(P.dm==="b"){ T.twist=dh*0.28; T.lean+=0.05; }
      break; }
    case "shoot": {
      const t=P.t;
      if(t<0.2){ const k=t/0.2; T.hL=T.hR=0.25+0.4*k; T.kL=T.kR=-(0.4+0.75*k); T.lean=0.14; chest(); T.sLx=T.sRx=0.95+0.4*k; }
      else if(!P.released){ const k=Math.min(1,(t-0.2)/0.16); T.hL=T.hR=0.12; T.kL=T.kR=-0.22; T.lean=0.02; T.sRx=1.35+1.4*k; T.eR=1.75-0.2*k; T.sRz=-0.05; T.sLx=1.35+1.2*k; T.eL=1.6; T.sLz=0.22; T.finL=T.finR=0.4; T.wR=-0.4; }
      else { T.hL=T.hR=0.35; T.kL=T.kR=-0.6; T.lean=0; T.sRx=2.9; T.eR=0.08; T.wR=1.25; T.finR=1.0; T.sRz=0.02; T.sLx=2.5; T.eL=0.7; T.sLz=-0.1; }
      T.air=P.air?1:0; break; }
    case "layup":
      if(!P.air){ gait(0.3,-0.6,false); T.lean=0.2; chest(); }
      else { T.hL=1.5; T.kL=-1.8; T.hR=-0.08; T.kR=-0.25; T.lean=0.02; T.sRx=3.0; T.eR=P.released?0.05:0.3; T.wR=P.released?0.7:-0.2; T.sLx=1.2; T.eL=1.3; T.sLz=-0.2; T.air=1; }
      break;
    case "dunkRun": gait(0.3,-0.6,false); T.lean=0.25; chest(); break;
    case "dunk":
      T.hL=0.9; T.kL=-1.5; T.hR=0.5; T.kR=-1.1; T.lean=-0.04; T.air=1; T.finL=T.finR=0.6;
      if(!P.released){ T.sLx=T.sRx=3.05; T.eL=T.eR=0.95; T.sLz=0.12; T.sRz=-0.12; } else { T.sLx=T.sRx=2.7; T.eL=T.eR=0.1; }
      break;
    case "hang": { const sw=Math.sin(P.t*7)*0.3*Math.exp(-P.t*1.5);
      T.sLx=T.sRx=3.1; T.eL=T.eR=0.04; T.sLz=0.1; T.sRz=-0.1; T.hL=0.25+sw; T.hR=0.4+sw; T.kL=-0.5; T.kR=-0.75; T.lean=-0.06; T.finL=T.finR=1.2; T.air=1; break; }
    case "blk":
      T.sLx=T.sRx=3.1; T.sLz=-0.18; T.sRz=0.18; T.eL=T.eR=0.05; T.wL=T.wR=-0.2; T.finL=T.finR=0.1;
      T.hL=0.35; T.kL=-0.7; T.hR=0.2; T.kR=-0.45; T.lean=-0.02; T.air=P.air?1:0; break;
    case "dc": { const k=P.t/0.95;
      T.air=1; T.lean=-0.04; T.finL=T.finR=0.6; T.sLz=0.12; T.sRz=-0.12;
      if(P.released){ T.sLx=T.sRx=2.7; T.eL=T.eR=0.1; T.hL=0.9; T.kL=-1.5; T.hR=0.5; T.kR=-1.1; }
      else if(k<0.3){ T.sLx=T.sRx=3.05; T.eL=T.eR=0.95; T.hL=0.8; T.kL=-1.4; T.hR=0.4; T.kR=-1.0; }
      else if(k<0.56){ T.sLx=T.sRx=0.9; T.eL=T.eR=1.7; T.hL=1.25; T.kL=-1.95; T.hR=1.05; T.kR=-1.75; T.lean=0.25; }
      else { T.sLx=T.sRx=3.1; T.eL=T.eR=0.7; T.hL=0.7; T.kL=-1.3; T.hR=0.4; T.kR=-0.9; }
      break; }
    case "cel":
      T.sLx=T.sRx=2.75; T.sLz=-0.55; T.sRz=0.55; T.eL=T.eR=0.18; T.tri=1; T.wL=T.wR=-0.2;
      T.hL=T.hR=0.12; T.kL=T.kR=-0.25; T.lean=-0.12; T.neck=0.25; T.air=P.air?1:0; break;
    case "pose":
      // showcase stance on the select screen
      T.hL=0.06; T.kL=-0.1; T.hR=-0.02; T.kR=-0.04; T.hLz=-0.09; T.hRz=0.09; T.lean=0.02;
      T.sLx=0.1; T.sLz=-0.16; T.eL=0.35; T.sRx=0.05; T.sRz=0.14; T.eR=0.3; T.finL=T.finR=0.55; break;
  }
  return T;
}
const TRI=[1.3,0,0,0,1.7];
function applyPose(av,T,dt){
  const c=av.cur, k=1-Math.exp(-dt*16);
  for(const key in T){ c[key] = c[key]===undefined ? T[key] : c[key]+(T[key]-c[key])*k; }
  av.pelvis.position.y = c.air>0.5 ? 1.0 : Math.max(ext(c.hL,c.kL)*Math.cos(c.hLz), ext(c.hR,c.kR)*Math.cos(c.hRz));
  av.torso.rotation.set(-c.lean,c.twist,c.roll); av.neck.rotation.set(c.lean*0.6+c.neck,-c.twist*0.6,0);
  av.L.s.rotation.set(c.sLx,0,c.sLz); av.L.e.rotation.x=c.eL; av.L.w.rotation.x=c.wL;
  av.R.s.rotation.set(c.sRx,0,c.sRz); av.R.e.rotation.x=c.eR; av.R.w.rotation.x=c.wR;
  av.LL.h.rotation.set(c.hL,0,c.hLz); av.LL.k.rotation.x=c.kL; av.LL.a.rotation.set(-(c.hL+c.kL)*0.9,0,-c.hLz*0.8);
  av.RL.h.rotation.set(c.hR,0,c.hRz); av.RL.k.rotation.x=c.kR; av.RL.a.rotation.set(-(c.hR+c.kR)*0.9,0,-c.hRz*0.8);
  [[av.L.f,c.finL],[av.R.f,c.finR]].forEach(([fs,fin])=>fs.forEach((f,i)=>{ f.rotation.x=lerp(fin,TRI[i],c.tri); }));
}
function poseAvatar(av,mode,P,dt){
  const sc=av.arch.scale;
  const Q={ ...P, speed:(P.speed||0)/sc, ballY:(P.ballY||0)/sc, ballF:(P.ballF||0)/sc, ballR:(P.ballR||0)/sc, br:R/sc };
  av.phase += dt*(Q.speed>0.2 ? (mode==="def" ? 4+Q.speed*2.4 : 3+Q.speed*1.7) : 0);
  applyPose(av, poseTargets(av,mode,Q), dt);
}
const _a=new V3(), _b=new V3();
function palmWorld(av,side,out){ av.root.updateMatrixWorld(true); return av[side].palmPt.getWorldPosition(out); }

/* ---------- local player state ---------- */
let myArch="ace"; try{ const sv=localStorage.getItem("hoops.arch"); if(ARCH_BY_ID[sv]) myArch=sv; }catch(e){}
const look={ color:ARCH_BY_ID[myArch].jersey };
let myName="Player";
let me = makeAvatar(myName, myArch, { self:true, label:"" });
const handY=()=>0.92*me.arch.scale;
const player = { x:0, z:-5.6, y:0, vy:0, vx:0, vz:0, speed:0, yaw:0, state:"play", t:0, air:false };
const cam = { yaw:0, pitch:0, pos:new V3(0,2.4,-1), look:new V3(0,1.4,-9) };
const ball = { p:new V3(), v:new V3(), state:"dribble", type:"regular", spin:new V3(), hold:0, t:0, info:null, scored:false, scoredAt:0, passT:0 };
let score=0, attempts=0, makes=0, att3=0, made3=0, neighbor=0, paused=true, detailOpen=false, lastRimHit=0, reachUp=2.2, pendingCel=false, celCount=0;
let shot=null, lay=null, dunk=null, rimTilt=0, netT=1, meterHide=0;
const stats = { regular:{}, airless:{} };
const keys = new Set();
const fwdOf=yaw=>new V3(-Math.sin(yaw),0,-Math.cos(yaw));
const rightOf=yaw=>new V3(Math.cos(yaw),0,-Math.sin(yaw));
function distToRim(){ return Math.hypot(player.x-RIM.x, player.z-RIM.z); }
function yawToRim(){ return Math.atan2(-(RIM.x-player.x), -(RIM.z-player.z)); }

function setType(t){
  ball.type=t; ballMesh.material = t==="regular"?matRegular:matAirless;
  $("ballName").textContent = BALLS[t].name; $("ballDot").style.background = BALLS[t].color;
  $("ballChip").style.borderColor = BALLS[t].color;
  ring.material.color.set(t==="regular"?0xff5d5d:0x3fcf9f);
}
setType("regular");

/* ---------- audio ---------- */
let ac=null, noiseBuf=null;
function audioInit(){
  if(ac) { ac.resume?.(); return; }
  try{
    ac = new (window.AudioContext||window.webkitAudioContext)();
    noiseBuf = ac.createBuffer(1, ac.sampleRate*0.5, ac.sampleRate);
    const d=noiseBuf.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1;
    // ocean waves in the background
    const wb=ac.createBuffer(1, ac.sampleRate*4, ac.sampleRate), wd=wb.getChannelData(0); let last=0;
    for(let i=0;i<wd.length;i++){ last=(last+0.02*(Math.random()*2-1))/1.02; wd[i]=last*3.5; }
    const src=ac.createBufferSource(); src.buffer=wb; src.loop=true;
    const lp=ac.createBiquadFilter(); lp.type="lowpass"; lp.frequency.value=700;
    const gain=ac.createGain(); gain.gain.value=0.05;
    const lfo=ac.createOscillator(); lfo.frequency.value=0.11; const lg=ac.createGain(); lg.gain.value=0.035; lfo.connect(lg).connect(gain.gain);
    src.connect(lp).connect(gain).connect(ac.destination); src.start(); lfo.start();
  }catch(e){ ac=null; }
}
function env(g, t, peak, dur){ g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(Math.max(0.0002,peak),t+0.004); g.gain.exponentialRampToValueAtTime(0.0001,t+dur); }
function tone(freq, peak, dur, type="sine", f2){
  const t=ac.currentTime, o=ac.createOscillator(), g=ac.createGain();
  o.type=type; o.frequency.setValueAtTime(freq,t); if(f2) o.frequency.exponentialRampToValueAtTime(f2,t+dur);
  env(g,t,peak,dur); o.connect(g).connect(ac.destination); o.start(t); o.stop(t+dur+0.05);
}
function noise(peak, dur, ftype, freq, q=1){
  const t=ac.currentTime, s=ac.createBufferSource(), f=ac.createBiquadFilter(), g=ac.createGain();
  s.buffer=noiseBuf; f.type=ftype; f.frequency.value=freq; f.Q.value=q; env(g,t,peak,dur);
  s.connect(f).connect(g).connect(ac.destination); s.start(t); s.stop(t+dur+0.05);
}
function bounceSound(type, speed){
  if(!ac) return;
  const k = Math.min(1, speed/5.5);
  if(type==="regular"){
    tone(150, 0.5*k, 0.16, "sine", 70); tone(1020, 0.14*k, 0.45, "sine", 960); tone(2350, 0.05*k, 0.18, "sine");
    noise(0.25*k, 0.035, "bandpass", 3200, 1.2);
  } else { tone(95, 0.3*k, 0.09, "sine", 60); noise(0.15*k, 0.05, "lowpass", 420, 0.7); }
}
function rimSound(s){ if(!ac) return; const k=Math.min(1,s/6); tone(620,0.12*k,0.35,"triangle",560); tone(1480,0.05*k,0.25,"sine"); }
function swishSound(){ if(!ac) return; noise(0.14,0.3,"highpass",2500,0.6); }
function dunkSound(){ if(!ac) return; tone(70,0.6,0.25,"sine",40); rimSound(6); noise(0.3,0.08,"bandpass",900,1); }
function cheerSound(){ if(!ac) return; [523,659,784,1047].forEach((f,i)=>setTimeout(()=>tone(f,0.08,0.25,"triangle"),i*70)); noise(0.06,0.9,"bandpass",1800,0.4); }

/* ---------- impact model ---------- */
let myBounces=0;
function impact(speed){
  const t = ball.type, B = BALLS[t];
  const out = speed*B.e;
  const db = Math.max(30, Math.min(95, B.base + 20*Math.log10(Math.max(speed,0.4)/4)));
  bounceSound(t, speed); myBounces++;
  const st = stats[t]; st.v=speed; st.o=out; st.db=db;
  $("db").textContent = db.toFixed(0)+" dB";
  const bar=$("dbBar"); bar.style.width = ((db-30)/65*100)+"%"; bar.style.background = db>65?"var(--red)":db>55?"var(--amber)":"var(--teal)";
  $("keep").textContent = Math.round(B.e*B.e*100)+"%";
  neighbor = Math.min(100, neighbor + Math.max(0, db-56)*1.4);
  ring.position.x=ball.p.x; ring.position.z=ball.p.z; ringT=0; ringMax = Math.max(0.3,(db-40)/12);
  return out;
}
function dribblePush(t){
  const h = HAND_Y - R, up = Math.sqrt(2*G*h)*1.01, vin = up/BALLS[t||ball.type].e;
  return Math.sqrt(Math.max(0, vin*vin - 2*G*h));
}

/* ---------- shots, layups, dunks ---------- */
function launch(start,target,deg){
  const dx=target.x-start.x, dz=target.z-start.z, D=Math.hypot(dx,dz)||0.01, dy=target.y-start.y;
  let th=deg*Math.PI/180; while(D*Math.tan(th)-dy<0.15 && th<1.45) th+=0.03;
  const v=Math.sqrt(G*D*D/(2*Math.cos(th)**2*(D*Math.tan(th)-dy)));
  ball.p.copy(start); ball.v.set(dx/D*v*Math.cos(th), v*Math.sin(th), dz/D*v*Math.cos(th));
  ball.spin.set(dz/D,0,-dx/D).multiplyScalar(-9);
  ball.state="flying"; ball.t=0; ball.scored=false; ball.prev=ball.p.y;
  return D/(v*Math.cos(th));
}
function holdPos(useRight){
  if(useRight){ palmWorld(me,"R",_a); return _a.add(new V3(0,0.13,0)); }
  palmWorld(me,"L",_a); palmWorld(me,"R",_b);
  return _a.add(_b).multiplyScalar(0.5).add(new V3(0,0.06,0)).addScaledVector(fwdOf(player.yaw),0.07);
}
function needBall(){ toast(role==="player" ? "Your opponent has the ball. Press F to block!" : ball.state==="flying"||ball.state==="pass" ? "Wait for the ball to come back, or press R" : "Get the ball first"); }
function canAct(){ return onCourt && !paused && !detailOpen && role!=="spec" && player.state==="play" && !player.air && countdownT<=0 && !(TR && TR.st!=="play"); }
function startShot(){
  if(!canAct()) return;
  if(ball.state!=="dribble") return needBall();
  const dr=distToRim();
  if(dr<5.2 && (keys.has("ShiftLeft")||keys.has("ShiftRight"))) return startDunk("normal");
  if(dr<2.8) return startLayup();
  player.state="shoot"; player.t=0; player.air=false;
  shot={ m:null, released:false, three:isThree(player.x,player.z), dist:distToRim() };
  ball.state="hand"; $("meter").hidden=false; $("grade").textContent=""; $("meterFill").style.background="#fff";
  { const g1=grades()[1][0], z=document.querySelector("#meter .zone"); z.style.bottom=((0.91-g1)*100)+"%"; z.style.height=(Math.min(1,0.91+g1)-(0.91-g1))*100+"%"; }
}
function releaseShot(){ if(player.state==="shoot" && shot && shot.m===null) shot.m=meterVal(player.t); }
const meterVal=t=>(t-0.08)/0.48;
function grades(){ const s=me.arch.r.shoot/100; return [[0.022+0.03*s,"EXCELLENT","#3fcf9f"],[0.05+0.06*s,"GOOD","#3fcf9f"],[0.2,null,"#ffc04d"],[9,null,"#ff5d5d"]]; }
function releaseJumper(){
  const start=holdPos(false).clone();
  const q=shot.m-0.91, aq=Math.abs(q);
  const GR=grades(), gi=GR.findIndex(g=>aq<=g[0]); const g=GR[gi];
  const label = g[1] || (q<0 ? (aq>0.2?"VERY EARLY":"SLIGHTLY EARLY") : (aq>0.2?"VERY LATE":"SLIGHTLY LATE"));
  $("grade").textContent=label; $("grade").style.color=g[2]; $("meterFill").style.background=g[2];
  const dist=shot.dist, far=Math.max(0,dist-8)*0.04*(1.5-me.arch.r.shoot/100);
  let depth, lat;
  if(gi<=1){ depth=gauss()*(0.02+gi*0.025+far*0.5); lat=gauss()*(0.015+gi*0.015); }
  else { depth=q*1.05+gauss()*0.04; lat=gauss()*(0.05+aq*0.15); }
  depth+=gauss()*far; lat+=gauss()*far*0.5;
  const dir=new V3(RIM.x-start.x,0,RIM.z-start.z).normalize(), perp=new V3(-dir.z,0,dir.x);
  const target=new V3(RIM.x,RIM.y+0.02,RIM.z).addScaledVector(dir,depth).addScaledVector(perp,lat);
  launch(start,target,dist>8?50:53);
  ball.info={ kind:"jumper", three:shot.three, dist, grade:gi };
  shot.released=true; attempts++; if(shot.three) att3++; updateShots();
  meterHide=0.9;
}
function startLayup(){
  const d=new V3(player.x-RIM.x,0,player.z-RIM.z); if(d.length()<0.3) d.set(0,0,1); d.normalize();
  if(d.z<0.15){ d.z=0.15; d.normalize(); }
  player.state="layup"; player.t=0; player.air=false;
  lay={ fx:player.x, fz:player.z, tx:RIM.x+d.x*1.05, tz:RIM.z+d.z*1.05, released:false };
  ball.state="hand";
}
function startDunk(kind){
  if(!canAct()) return;
  if(ball.state!=="dribble") return needBall();
  const dist=distToRim(), maxD=kind==="dc"?5.5:5.2;
  if(dist>maxD){ toast(`Get within ${maxD} m of the rim to dunk`); return; }
  const d=new V3(player.x-RIM.x,0,player.z-RIM.z); if(d.length()<0.3) d.set(0,0,1); d.normalize();
  if(d.z<0.15){ d.z=0.15; d.normalize(); }
  const tk={ x:RIM.x+d.x*Math.min(1.7,Math.max(1.2,dist)), z:RIM.z+d.z*Math.min(1.7,Math.max(1.2,dist)) };
  const runD=Math.hypot(tk.x-player.x,tk.z-player.z);
  dunk={ sx:player.x, sz:player.z, tx:tk.x, tz:tk.z, qx:RIM.x+d.x*0.6, qz:RIM.z+d.z*0.6, runT:Math.max(0.18,runD/6.5), flyT:kind==="dc"?0.95:0.5, slammed:false, made:false, kind };
  player.state="dunk"; player.t=0; ball.state="hand";
}
function startBlock(){
  if(!onCourt||paused||detailOpen||role==="spec"||countdownT>0||player.state!=="play"||player.air||(TR&&TR.st!=="play")) return;
  if(ball.state==="dribble"){ if(role==="player"){ toast("You can't block while you have the ball"); return; } ball.state="hand"; }
  else if(ball.state!=="none" && role!=="player") return;
  player.state="block"; player.t=0; player.vy=3.3+0.8*me.arch.r.def/100; player.air=true;
}
function slam(D){
  D.slammed=true; attempts++; updateShots();
  const d=new V3(player.x-RIM.x,0,player.z-RIM.z); if(d.length()<0.1) d.set(0,0,1); d.normalize();
  ball.state="flying"; ball.t=0; ball.scored=false; ball.blocked=false;
  ball.info={ kind:D.kind==="dc"?"dunk2":"dunk", three:false };
  const blocker=findBlocker(new V3(RIM.x,RIM.y,RIM.z),1.5,0.25);
  if(blocker){ ball.p.set(RIM.x+d.x*0.5,RIM.y+0.35,RIM.z+d.z*0.5); ball.prev=ball.p.y; blockBall(blocker); D.made=false; return; }
  // not every dunk goes down: a double clutch is harder to finish
  const dk=me.arch.r.dunk/100;
  if(Math.random() < (D.kind==="dc" ? 0.33+0.42*dk : 0.62+0.32*dk)){
    ball.p.set(RIM.x,RIM.y+0.3,RIM.z); ball.v.set(0,-6.5,0); D.made=true; dunkSound(); rimTilt=0.2;
  } else {
    ball.p.set(RIM.x+d.x*0.45,RIM.y+0.2,RIM.z+d.z*0.45); ball.v.set(d.x*2.6+(Math.random()-0.5)*1.5,3.4,d.z*2.6+(Math.random()-0.5)*1.5);
    D.made=false; ball.info=null; rimSound(6); rimTilt=0.12; flash("RIMMED OUT!");
  }
  ball.prev=ball.p.y;
}
function findBlocker(pos,radius,minY=0.15){
  if(role!=="player"||!TR) return null;
  const r=remotes.get(oppPeer()); if(!r||r.mode!=="blk") return null;
  const rp=r.av.root.position; if(rp.y<minY) return null;
  const reach=radius*(0.85+0.3*r.av.arch.r.def/100)*r.av.arch.scale;
  if(Math.hypot(pos.x-rp.x,pos.z-rp.z)>reach || pos.y>rp.y+2.8*r.av.arch.scale) return null;
  return r;
}
function blockSound(){ if(!ac) return; tone(160,0.45,0.14,"square",80); noise(0.3,0.1,"bandpass",700,1); }
function blockBall(r){
  const rp=r.av.root.position, d=new V3(ball.p.x-rp.x,0,ball.p.z-rp.z); if(d.length()<0.05) d.set(0,0,1); d.normalize();
  ball.v.set(d.x*4+(Math.random()-0.5)*1.5, 1.2+Math.random(), d.z*4+(Math.random()-0.5)*1.5);
  ball.info=null; ball.blocked=true; ball.state="flying"; gotBlocked++; blockSound(); flash("BLOCKED!");
}
function updateShots(){ $("shots").textContent=`FG ${makes}/${attempts} · 3PT ${made3}/${att3}`; }
let threeTimer;
function showThree(dist){
  const el=$("three"); $("threeDist").textContent=dist? dist.toFixed(1)+" m from the rim":"";
  el.classList.remove("on"); void el.offsetWidth; el.classList.add("on"); clearTimeout(threeTimer); threeTimer=setTimeout(()=>el.classList.remove("on"),1800);
}
function onScore(){
  const info=ball.info||{ kind:"jumper", three:false };
  const pts=info.three?3:2; score+=pts; makes++; if(info.three) made3++;
  if(role==="player" && TR && TR.st==="play") myMS++;
  $("score").textContent=score; updateShots(); rosterDirty=true; swishSound(); netT=0;
  if(info.three){ showThree(info.dist); pendingCel=true; cheerSound(); }
  else flash(info.kind==="dunk2"?"DOUBLE CLUTCH SLAM!":info.kind==="dunk"?"SLAM DUNK!":info.kind==="layup"?"LAYUP +2":info.grade===0?"SPLASH! +2":"BUCKET +2");
}
function startPass(){
  const chest=new V3(player.x,1.15,player.z).addScaledVector(fwdOf(player.yaw),0.45);
  const T=launch(ball.p.clone(),chest,ball.p.distanceTo(chest)<3?20:35);
  ball.state="pass"; ball.info=null; ball.passT=T;
}
function catchBall(){
  ball.state="dribble"; ball.v.set(0,0,0); ball.info=null;
  const r=rightOf(player.yaw); drib.hand=((ball.p.x-player.x)*r.x+(ball.p.z-player.z)*r.z)<0 ? -1 : 1;
  drib.ph="hold"; drib.t=0; drib.hold=0.12; drib.move="n";
}
/* ----- dribbling: every bounce is planned between the hands, with crossovers, between the legs, behind the back and in-and-outs ----- */
const drib={ ph:"hold", t:0, hold:0.12, hand:1, toSide:1, move:"n", lastMove:"n", lead:1, from:new V3(), to:new V3(), fl:new V3(), tDown:0.2, tUp:0.27, nextHold:0.14 };
let spaceHeld=false;
function dribLocal(side,prot){ const sc=me.arch.scale, sp=Math.min(1,player.speed/4); return new V3(side*0.31*sc,(prot?0.6:0.92)*sc,(0.27+0.12*sp)*sc); }
function toWorld(l,out){ const f=fwdOf(player.yaw), r=rightOf(player.yaw); return out.set(player.x+r.x*l.x+f.x*l.z, l.y, player.z+r.z*l.x+f.z*l.z); }
function chooseMove(prot){
  if(prot) return "n";
  if(drib.lastMove!=="n" && Math.random()<0.7) return "n";
  const rnd=Math.random();
  if(player.speed>1.2){ if(rnd<0.4) return "n"; if(rnd<0.6) return "c"; if(rnd<0.76) return "x"; if(rnd<0.9) return "i"; return player.speed>3 ? "b" : "c"; }
  if(rnd<0.58) return "n"; if(rnd<0.8) return "x"; if(rnd<0.95) return "c"; return "i";
}
function planBounce(){
  const prot=spaceHeld, sd=drib.hand, sc=me.arch.scale, sp=Math.min(1,player.speed/4), mv=chooseMove(prot);
  drib.move=mv; drib.lastMove=mv; drib.from.copy(dribLocal(sd,prot));
  let to=sd, fx=sd*0.36, fz=0.42+0.18*sp, td=0.2, tu=0.27, hold=0.14;
  if(mv==="c"){ fx=sd*0.04; fz=0.45+0.1*sp; to=-sd; td=0.15; tu=0.2; hold=0.1; }
  else if(mv==="x"){ fx=0; fz=0.04+0.12*sp; to=-sd; td=0.16; tu=0.22; hold=0.1; drib.lead=-sd; }
  else if(mv==="b"){ fx=0; fz=-0.26; to=-sd; td=0.17; tu=0.24; hold=0.1; }
  else if(mv==="i"){ fx=sd*0.42; fz=0.46+0.12*sp; td=0.19; tu=0.24; hold=0.1; }
  if(prot){ fx=sd*0.3; fz=0.32; td=0.12; tu=0.15; hold=0.07; }
  drib.fl.set(fx*sc,R,fz*sc); drib.toSide=to; drib.to.copy(dribLocal(to,prot)); drib.tDown=td; drib.tUp=tu; drib.nextHold=hold; drib.ph="down"; drib.t=0;
}
function updateDribble(dt){
  drib.t+=dt; const L=new V3(), sc=me.arch.scale;
  if(drib.ph==="hold"){
    L.copy(dribLocal(drib.hand,spaceHeld));
    if(drib.t>=drib.hold){ planBounce(); L.copy(drib.from); }
  }
  if(drib.ph==="down"){
    const s=Math.min(1,drib.t/drib.tDown);
    L.lerpVectors(drib.from,drib.fl,s); L.y=drib.from.y-(drib.from.y-R)*(0.35*s+0.65*s*s);
    if(drib.move==="i") L.x-=drib.hand*0.26*sc*Math.sin(Math.PI*Math.min(1,s*1.15));
    if(drib.move==="b") L.z-=0.06*sc*Math.sin(Math.PI*s);
    if(s>=1){ L.y=R; toWorld(L,ball.p); impact((drib.from.y-R)*1.65/drib.tDown*0.62); drib.ph="up"; drib.t=0; }
  } else if(drib.ph==="up"){
    const s=Math.min(1,drib.t/drib.tUp);
    L.lerpVectors(drib.fl,drib.to,s); L.y=R+(drib.to.y-R)*(1-(1-s)*(1-s));
    if(s>=1){ drib.ph="hold"; drib.t=0; drib.hand=drib.toSide; drib.hold=drib.nextHold; drib.move="n"; }
  }
  toWorld(L,ball.p);
  ballMesh.rotation.x += dt*(drib.ph==="down"?-10:drib.ph==="up"?8:0);
}

/* ---------- input ---------- */
let onCourt=false;
function readName(){
  myName=($("nick").value.trim().replace(/\s+/g," ")||"Player").slice(0,16);
  try{ localStorage.setItem("hoops.nick",myName); }catch(e){}
  me.dispose(); me=makeAvatar(myName,myArch,{ self:true, label:myName });
}
try{ $("nick").value=localStorage.getItem("hoops.nick")||""; }catch(e){}
/* ----- player select: cards with portraits rendered from the real 3D players ----- */
const portrait=(()=>{
  let pr=null, ps=null, pc=null, chain=Promise.resolve();
  const shot=async id=>{
    if(!pr){ pr=new THREE.WebGLRenderer({ antialias:true, alpha:true, preserveDrawingBuffer:true }); pr.setPixelRatio(1); pr.setSize(240,300);
      ps=new THREE.Scene(); ps.add(new THREE.HemisphereLight(0xdfe9ff,0x6a5a48,0.75));
      const l=new THREE.DirectionalLight(0xffe2c0,1.05); l.position.set(-1.6,2.6,-2.4); ps.add(l);
      const l2=new THREE.DirectionalLight(0x8fbcff,0.55); l2.position.set(2.2,1.6,1.2); ps.add(l2);
      pc=new THREE.PerspectiveCamera(24,240/300,0.05,20); }
    const A=ARCH_BY_ID[id], av=makeAvatar("",id,{ self:true, scene:ps, label:"" });
    await buildArch(id); await new Promise(r=>setTimeout(r,0));
    for(let i=0;i<5;i++) poseAvatar(av,"pose",{ speed:0 },1);
    av.root.rotation.y=-0.3; av.root.visible=true; av.root.updateMatrixWorld(true);
    const s=A.scale; pc.position.set(0.1*s,1.74*s,-1.45*s); pc.lookAt(0,1.6*s,0);
    pr.render(ps,pc); const url=pr.domElement.toDataURL("image/png"); av.dispose(); return url;
  };
  return id=>{ const p=chain.then(()=>shot(id)); chain=p.catch(()=>{}); return p; };
})();
function renderCards(){
  const box=$("cards"); box.replaceChildren();
  ARCH.forEach(A=>{
    const b=document.createElement("button"); b.type="button"; b.className="pcard"+(A.id===myArch?" on":""); b.style.setProperty("--cc",A.jersey); b.dataset.id=A.id;
    const ph=document.createElement("div"); ph.className="ph"; const wait=document.createElement("span"); wait.textContent="Building…"; ph.append(wait);
    const o=document.createElement("div"); o.className="ovr"; o.innerHTML=""; o.append(String(ovr(A))); const sm=document.createElement("small"); sm.textContent="OVR"; o.append(sm);
    const n=document.createElement("div"); n.className="num"; n.textContent="#"+A.num+" "+A.pos;
    const nm=document.createElement("div"); nm.className="nm"; nm.textContent=A.name;
    const rl=document.createElement("div"); rl.className="rl"; rl.textContent=A.role+" · "+A.height;
    const bars=document.createElement("div"); bars.className="bars";
    [["SHT",A.r.shoot],["SPD",A.r.speed],["DNK",A.r.dunk],["DEF",A.r.def]].forEach(([k,v])=>{ const a=document.createElement("span"); a.textContent=k; const i=document.createElement("i"), bb=document.createElement("b"); bb.style.width=v+"%"; i.append(bb); const c=document.createElement("span"); c.textContent=v; bars.append(a,i,c); });
    b.append(ph,o,n,nm,rl,bars);
    b.addEventListener("click",()=>pickArch(A.id));
    box.append(b);
  });
}
function pickArch(id){
  if(!ARCH_BY_ID[id]) return;
  myArch=id; look.color=ARCH_BY_ID[id].jersey; try{ localStorage.setItem("hoops.arch",id); }catch(e){}
  document.querySelectorAll(".pcard").forEach(c=>c.classList.toggle("on",c.dataset.id===id));
  me.dispose(); me=makeAvatar(myName,myArch,{ self:true, label:myName==="Player"?"":myName });
}
renderCards(); document.body.classList.add("start");
(async()=>{
  // build your player first, then everyone else in the background; each card gets a portrait as soon as its player exists
  const order=[myArch,...ARCH.map(a=>a.id).filter(i=>i!==myArch)]; let done=0;
  order.forEach(id=>buildArch(id).then(()=>portrait(id)).then(url=>{
    const ph=document.querySelector(`.pcard[data-id="${id}"] .ph`); if(ph){ const img=new Image(); img.alt=ARCH_BY_ID[id].name; img.src=url; ph.replaceChildren(img); }
  }).catch(()=>{}).finally(()=>{ done++; $("buildNote").textContent = done<order.length ? `Building players… ${done}/${order.length}` : "Click a card to switch players"; }));
})();
function startErr(msg){ const e=$("startErr"); e.textContent=msg; e.hidden=!msg; }
$("hostBtn").addEventListener("click", ()=>{ audioInit(); readName(); enterGame(String(Math.floor(100000+Math.random()*900000)), true); });
$("soloBtn").addEventListener("click", ()=>{ audioInit(); readName(); leaveNet(); goCourt(); });
$("joinForm").addEventListener("submit", e=>{
  e.preventDefault(); audioInit();
  const p=$("pinInput").value.replace(/\D/g,"");
  if(p.length!==6){ startErr("Game PINs have 6 digits. Check the number on the host's screen."); return; }
  readName(); enterGame(p,false);
});
$("goCourt").addEventListener("click", ()=>{ if(isHost && hostT){ hostT.st="off"; pushTR(); } goCourt(); });
$("startTour").addEventListener("click", ()=>{ if(hostStart()) goCourt(); });
$("presentChk").addEventListener("change", e=>{ presenting=e.target.checked; if(net) net.presence({ pr:presenting?1:0 }).catch(()=>{}); lobbyDirty=true; });
$("againBtn").addEventListener("click", ()=>{ if(!hostStart()) toast("You need at least 2 players for a tournament"); });
$("freeBtn").addEventListener("click", ()=>{ if(hostT){ hostT.st="off"; pushTR(); } });
$("fsBtn").addEventListener("click", ()=>{
  try{ if(document.fullscreenElement) document.exitFullscreen(); else { const r=document.documentElement.requestFullscreen(); r&&r.catch&&r.catch(()=>toast("Full screen isn't available here. Use your browser's full-screen mode instead.")); } }
  catch(e){ toast("Full screen isn't available here. Use your browser's full-screen mode instead."); }
});
$("leaveLobby").addEventListener("click", ()=>{ leaveNet(); $("lobby").hidden=true; $("start").hidden=false; document.body.classList.add("start"); });
let helpT=0;
function goCourt(){ helpT=0; document.body.classList.remove("start"); $("start").hidden=true; $("lobby").hidden=true; onCourt=true; paused=false; rosterDirty=true; if(!presenting) lock(); canvas.focus(); }
function lock(){ try{ const r=canvas.requestPointerLock?.(); r?.catch?.(()=>{}); }catch(e){} }
canvas.addEventListener("click", ()=>{ if(onCourt && !detailOpen && document.pointerLockElement!==canvas) lock(); });
document.addEventListener("mousemove", e=>{
  if(document.pointerLockElement===canvas && Math.abs(e.movementX)<250 && Math.abs(e.movementY)<250){ cam.yaw -= e.movementX*0.0024; cam.pitch -= e.movementY*0.0018; clampPitch(); }
});
let drag=null;
canvas.addEventListener("pointerdown", e=>{ if(document.pointerLockElement!==canvas) drag={x:e.clientX,y:e.clientY}; });
addEventListener("pointermove", e=>{ if(drag){ cam.yaw -= (e.clientX-drag.x)*0.005; cam.pitch -= (e.clientY-drag.y)*0.003; drag={x:e.clientX,y:e.clientY}; clampPitch(); }});
addEventListener("pointerup", ()=>drag=null);
function clampPitch(){ cam.pitch=clamp(cam.pitch,-0.45,0.4); }

function keyDown(code){
  if(!onCourt) return;
  if(code==="KeyP") return toggleDetail();
  if(paused || detailOpen) return;
  if(code==="KeyB"){ bracketOpen=!bracketOpen; }
  if(code==="KeyH"){ helpT = $("helpCard").classList.contains("faded") ? 9999 : 10.5; }
  if(code==="KeyE") startShot();
  if(code==="KeyG") startDunk("normal");
  if(code==="KeyT") startDunk("dc");
  if(code==="KeyF") startBlock();
  if(code==="KeyQ"){ setType(ball.type==="regular"?"airless":"regular"); toast(BALLS[ball.type].name); }
  if(code==="KeyR" && player.state==="play" && role!=="spec"){ if(role==="player") toast("No ball resets during a match"); else catchBall(); }
  keys.add(code);
}
function keyUp(code){ keys.delete(code); if(code==="KeyE") releaseShot(); }
addEventListener("keydown", e=>{
  if(e.target && (e.target.tagName==="INPUT" || e.target.tagName==="BUTTON")) return;
  if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(e.code)) e.preventDefault();
  if(e.repeat) return;
  keyDown(e.code);
});
addEventListener("keyup", e=>keyUp(e.code));
addEventListener("blur", ()=>{ keys.clear(); releaseShot(); });
document.querySelectorAll("#touch button").forEach(b=>{
  const k=b.dataset.k;
  b.addEventListener("pointerdown", e=>{ e.preventDefault(); audioInit(); keyDown(k); });
  ["pointerup","pointerleave","pointercancel"].forEach(ev=>b.addEventListener(ev, ()=>keyUp(k)));
});
$("closeDetail").addEventListener("click", toggleDetail);

let toastTimer;
function toast(msg){ const t=$("toast"); t.textContent=msg; t.classList.add("on"); clearTimeout(toastTimer); toastTimer=setTimeout(()=>t.classList.remove("on"),1800); }
let flashTimer;
function flash(msg){ const f=$("flash"); f.textContent=msg; f.classList.add("on"); clearTimeout(flashTimer); flashTimer=setTimeout(()=>f.classList.remove("on"),1200); }

/* ---------- detail view ---------- */
function toggleDetail(){
  if(!onCourt) return;
  detailOpen=!detailOpen; $("detail").hidden=!detailOpen;
  if(detailOpen){ try{ document.exitPointerLock?.(); }catch(e){} keys.clear(); fillStats(); }
  else { lock(); canvas.focus(); }
}
function fillStats(){
  for(const [t,c] of [["regular","R"],["airless","A"]]){
    const s=stats[t];
    $("s"+c+"v").textContent = s.v? s.v.toFixed(1)+" m/s":"--";
    $("s"+c+"o").textContent = s.o? s.o.toFixed(1)+" m/s":"--";
    $("s"+c+"d").textContent = s.db? s.db.toFixed(0)+" dB":"--";
    $("s"+c+"p").textContent = dribblePush(t).toFixed(1)+" m/s";
  }
}
const cut = $("cut"), cg = cut.getContext("2d");
const air = Array.from({length:46},()=>({a:Math.random()*Math.PI*2, r:Math.sqrt(Math.random())*0.85, s:Math.random()*Math.PI*2}));
function drawCut(time){
  const W=cut.width,H=cut.height; cg.clearRect(0,0,W,H);
  const floorY=H-80, Rp=78, cyc=(time/2600)%1;
  cg.fillStyle="#6b4a2e"; cg.fillRect(0,floorY,W,26);
  cg.fillStyle="#4b3320"; cg.fillRect(0,floorY+26,W,54);
  [["regular",W*0.27],["airless",W*0.73]].forEach(([t,cx])=>{
    const B=BALLS[t], reg=t==="regular", active=ball.type===t;
    const drop=floorY-Rp-250, rise=B.e*B.e;
    let y, sq=0;
    if(cyc<0.38){ const k=cyc/0.38; y=drop+(floorY-Rp-drop)*k*k; }
    else if(cyc<0.52){ const k=(cyc-0.38)/0.14; sq=Math.sin(k*Math.PI)*(reg?0.2:0.28); y=floorY-Rp*(1-sq); }
    else { const k=(cyc-0.52)/0.48; const top=floorY-Rp-(floorY-Rp-drop)*rise; y=floorY-Rp-(floorY-Rp-top)*(1-(1-k)**2); }
    const rx=Rp*(1+sq*0.75), ry=Rp*(1-sq);
    // drop-height guides
    cg.setLineDash([5,7]); cg.strokeStyle="#3a4558"; cg.lineWidth=1.5;
    cg.beginPath(); cg.moveTo(cx-150,drop+Rp); cg.lineTo(cx+150,drop+Rp); cg.stroke();
    const topY=floorY-Rp-(floorY-Rp-drop)*rise;
    cg.strokeStyle=B.color; cg.beginPath(); cg.moveTo(cx-150,topY+Rp); cg.lineTo(cx+150,topY+Rp); cg.stroke(); cg.setLineDash([]);
    cg.fillStyle="#93a0b4"; cg.font="600 15px 'Chakra Petch',sans-serif"; cg.textAlign="left";
    cg.fillText("drop height", cx+156, drop+Rp+5);
    cg.fillStyle=B.color; cg.fillText("bounce "+Math.round(rise*100)+"%", cx+156, topY+Rp+5);
    // ball body
    cg.save(); cg.beginPath(); cg.ellipse(cx,y,rx,ry,0,0,Math.PI*2); cg.clip();
    if(reg){
      cg.fillStyle="#3a2416"; cg.fillRect(cx-rx,y-ry,rx*2,ry*2);
      const heat = sq*5;
      air.forEach(m=>{ m.s+=0.05+heat*0.25; const jx=Math.cos(m.s)*4, jy=Math.sin(m.s*1.3)*4;
        cg.fillStyle=`rgba(255,${200-heat*120},${150-heat*100},.9)`; cg.beginPath(); cg.arc(cx+Math.cos(m.a)*m.r*rx+jx, y+Math.sin(m.a)*m.r*ry+jy, 3.2,0,7); cg.fill(); });
    } else {
      cg.fillStyle="#0e3a2e"; cg.fillRect(cx-rx,y-ry,rx*2,ry*2);
      const s=17, hh=s*Math.sqrt(3), syy=1-sq*1.1, sxx=1+sq*0.6;
      cg.strokeStyle="#bdf3df"; cg.lineWidth=3;
      for(let r=-6;r<=6;r++) for(let c=-5;c<=5;c++){
        const px=cx+(c*s*3+(r%2?s*1.5:0))*sxx*0.55, py=y+r*hh/2*syy*0.55;
        cg.beginPath(); for(let a=0;a<6;a++){ const tt=Math.PI/3*a; cg.lineTo(px+s*0.5*Math.cos(tt)*sxx, py+s*0.5*Math.sin(tt)*syy); } cg.closePath(); cg.stroke();
      }
    }
    cg.restore();
    cg.lineWidth=7; cg.strokeStyle=reg?"#d4652a":"#3fcf9f"; cg.beginPath(); cg.ellipse(cx,y,rx,ry,0,0,Math.PI*2); cg.stroke();
    // pressure / spring-back arrows during contact
    if(sq>0.05){
      cg.strokeStyle=cg.fillStyle="#fff"; cg.lineWidth=3;
      const n=reg?8:4;
      for(let i=0;i<n;i++){ const a=reg? (i/n)*Math.PI*2 : Math.PI*1.5+(i-1.5)*0.35;
        const x0=cx+Math.cos(a)*rx*0.35, y0=y+Math.sin(a)*ry*0.35, x1=cx+Math.cos(a)*rx*(0.35+sq*2.4), y1=y+Math.sin(a)*ry*(0.35+sq*2.4);
        cg.beginPath(); cg.moveTo(x0,y0); cg.lineTo(x1,y1); cg.stroke(); }
    }
    // sound + floor vibration after impact
    if(cyc>0.38 && cyc<0.95){
      const k=(cyc-0.38)/0.57, amp=reg?1:0.35;
      for(let i=0;i<(reg?4:2);i++){ const rr=Rp+20+k*170+i*28; const al=(1-k)*amp*(1-i*0.2);
        cg.strokeStyle=reg?`rgba(255,93,93,${al})`:`rgba(63,207,159,${al})`; cg.lineWidth=3;
        cg.beginPath(); cg.arc(cx,floorY-Rp,rr,-Math.PI*0.95,-Math.PI*0.05); cg.stroke(); }
      cg.strokeStyle=reg?`rgba(255,93,93,${1-k})`:`rgba(63,207,159,${1-k})`; cg.lineWidth=3; cg.beginPath();
      for(let x=-170;x<=170;x+=4){ const yy=floorY+52+Math.sin(x*0.12+time*0.03)*(reg?11:3)*(1-k)*Math.exp(-Math.abs(x)/220); x===-170?cg.moveTo(cx+x,yy):cg.lineTo(cx+x,yy); }
      cg.stroke();
    }
    // labels
    cg.textAlign="center"; cg.fillStyle=active?B.color:"#eef2f7"; cg.font="700 24px 'Chakra Petch',sans-serif";
    cg.fillText(reg?"REGULAR · air spring":"AIRLESS · lattice spring", cx, 40);
    cg.fillStyle="#93a0b4"; cg.font="500 16px 'Barlow',sans-serif";
    cg.fillText(reg?"Squeezed air pushes the shell back. The hollow shell rings.":"Bending cells spring back. The open lattice damps the ring.", cx, 66);
    cg.fillStyle="#cdd5e1"; cg.font="600 14px 'Chakra Petch',sans-serif";
    cg.fillText(reg?"floor vibration: strong":"floor vibration: weak", cx, floorY+74);
    if(active){ cg.fillStyle=B.color; cg.font="700 12px 'Chakra Petch',sans-serif"; cg.fillText("IN YOUR HAND", cx, 90); }
  });
  cg.fillStyle="#5d6a7e"; cg.font="500 13px 'Barlow',sans-serif"; cg.textAlign="right";
  cg.fillText("slow motion, squash exaggerated", W-16, H-10);
}

/* ---------- playing together: a 6-digit game PIN opens a private court ---------- */
let net=null, netState="solo", pin="", isHost=false, rosterDirty=true, rosterTimer=0, lastSend=0, lobbyDirty=false, lobbyTimer=0, lobbySig="";
const remotes=new Map();
const roomReady = (async()=>{ try{ return window.claude?.use ? await window.claude.use("room") : null; }catch(e){ return null; } })();
function fmtPin(p){ return p.slice(0,3)+" "+p.slice(3); }
function num(v,d=0){ return typeof v==="number" && isFinite(v) ? v : d; }
function safeColor(c){ return /^#[0-9a-f]{6}$/i.test(String(c))?c:"#9aa3b0"; }
function leaveNet(){ if(net && net.leave) net.leave().catch(()=>{}); net=null; pin=""; netState="solo"; rosterDirty=true; hostT=null; TR=null; myPeer=null; myTok=null; presenting=false; }
function lobbyUnavailable(){
  net=null; netState="solo";
  $("lobbyHint").textContent="Couldn't connect to the online game. Check the internet connection (some school networks block it), or practice alone for now.";
  $("goCourt").textContent="Practice alone";
}
async function enterGame(p,host){
  startErr(""); leaveNet(); pin=p; isHost=host; netState="connecting"; presenting = host && $("presentChk").checked;
  $("start").hidden=true; $("lobby").hidden=false;
  $("lobbyRole").textContent = host ? "Your game PIN" : "Joining game PIN";
  $("lobbyPin").textContent=fmtPin(p);
  $("lobbyHint").textContent="Connecting…"; $("goCourt").textContent="Go to the court";
  lobbyDirty=true;
  const rm=await roomReady;
  if(pin!==p) return;
  if(!rm){ lobbyUnavailable(); return; }
  try{
    const room=await rm.join("pin-"+p);
    if(pin!==p){ room.leave().catch(()=>{}); return; }
    net=room; netState="on";
    net.presence({ n:myName, c:look.color, h:host?1:0, pr:presenting?1:0 }).catch(()=>{});
    net.onPeers(()=>{ rosterDirty=true; lobbyDirty=true; if(!myPeer){ const me2=net&&net.peers().find(q=>q.sameTab); if(me2) myPeer=me2.peer; } }, ()=>{ net=null; netState="solo"; rosterDirty=true; lobbyDirty=true; });
    $("lobbyHint").textContent = host
      ? "Send classmates this game file or its link. They type their name and this PIN, then press Join. Start the tournament when everyone is here."
      : "You're in. When the host starts the tournament, you'll be taken to the court.";
    lobbyDirty=true;
    if(!host) setTimeout(()=>{ if(net && pin===p && otherPeers().length===0) $("lobbyHint").textContent="Nobody is in this game yet. Check the PIN with your host, or wait here."; }, 3500);
  }catch(e){ if(pin===p) lobbyUnavailable(); }
}
function otherPeers(){ return net ? net.peers().filter(pe=>!pe.sameTab && pe.presence && typeof pe.presence.n==="string") : []; }
function renderLobby(){
  if($("lobby").hidden) return;
  const list=[{ name:myName, color:look.color, me:true, host:isHost, pr:presenting }].concat(otherPeers().map(pe=>({ name:String(pe.presence.n).slice(0,16)||"Player", color:safeColor(pe.presence.c), host:pe.presence.h===1, pr:pe.presence.pr===1 })));
  $("startTour").hidden=!isHost; $("presentWrap").hidden=!isHost;
  const players=list.filter(pl=>!pl.pr).length;
  $("tourHint").textContent = isHost ? (players<2 ? "A tournament needs at least 2 players. "+players+" so far." : players+" players will be put in a random bracket. Winner stays on, first to 3 baskets.") : "";
  $("startTour").disabled = !net || players<2;
  const sig=JSON.stringify(list); if(sig===lobbySig) return; lobbySig=sig;
  $("lobbyPlayers").replaceChildren(...list.map(pl=>{
    const sp=document.createElement("span"), i=document.createElement("i"); sp.className="pchip"; i.style.background=pl.color;
    sp.append(i, document.createTextNode(pl.name+(pl.me?" (you)":"")+(pl.host?" · host":"")+(pl.pr?" · presenting":""))); return sp;
  }));
  $("lobbyCount").textContent = list.length+(list.length===1?" player":" players");
}
const MODE_CODE={ free:"f", dribble:"d", shoot:"s", layup:"l", dunkRun:"r", dunk:"k", hang:"h", cel:"c", blk:"B", dc:"D", def:"V", prot:"W" };
const CODE_MODE=Object.fromEntries(Object.entries(MODE_CODE).map(([k,v])=>[v,k]));
let localMode="dribble", localReleased=false, localPoseT=0, localDm="n";
function sendPresence(now){
  if(!net || now-lastSend<66) return; lastSend=now;
  const base={ n:myName, c:look.color, pl:myArch, h:isHost?1:0, pr:presenting?1:0, s:score };
  if(role==="spec"){ net.presence({ ...base, x:null, z:null, mm:null, pt:null }).catch(()=>{}); return; }
  net.presence({ ...base,
    x:+player.x.toFixed(2), z:+player.z.toFixed(2), y:+player.y.toFixed(2), yaw:+player.yaw.toFixed(2),
    a:MODE_CODE[localMode]||"f", at:+localPoseT.toFixed(2), rl:localReleased?1:0, dm:localDm, dl:drib.lead,
    b:[+ball.p.x.toFixed(2),+ball.p.y.toFixed(2),+ball.p.z.toFixed(2)], t:ball.type==="regular"?0:1, k:attempts, bc:myBounces, ce:celCount,
    bs: ball.state==="flying"||ball.state==="pass" ? "f" : ball.state==="none" ? "n" : "d",
    mm: role==="player"&&TR ? TR.m : null, ms:myMS, pt:myTok, bkd:gotBlocked }).catch(()=>{});
}
function createRemote(name,archId){
  const av=makeAvatar(name,archId,{ label:name }), b=new THREE.Mesh(ballGeo, matRegular); b.castShadow=true; scene.add(b);
  return { av, ball:b, name, archId, dm:"n", dl:1, type:"regular", tx:0, tz:0, ty:0, tyaw:0, tb:new V3(), bc:null, s:null, at:0, lastAt:-1, mode:"free", rl:0, speed:0, fresh:true,
    dispose(){ av.dispose(); scene.remove(b); } };
}
function remoteBounce(r){
  const d=Math.hypot(r.ball.position.x-player.x, r.ball.position.z-player.z);
  bounceSound(r.type, 4.5/(1+d/2.5));
}
function updateRemotes(dt){
  if(!net){ for(const r of remotes.values()) r.dispose(); remotes.clear(); return; }
  const seen=new Set();
  for(const pe of net.peers()){
    if(pe.sameTab) continue;
    const pr=pe.presence||{};
    if(typeof pr.x!=="number"||typeof pr.z!=="number") continue;
    seen.add(pe.peer);
    const name=String(pr.n||"Player").slice(0,16)||"Player";
    const archId=ARCH_BY_ID[pr.pl] ? pr.pl : "ace";
    let r=remotes.get(pe.peer);
    if(!r || r.name!==name || r.archId!==archId){ if(r) r.dispose(); r=createRemote(name,archId); remotes.set(pe.peer,r); rosterDirty=true; }
    r.dm=["n","c","x","b","i"].includes(pr.dm)?pr.dm:"n"; r.dl=pr.dl===-1?-1:1;
    r.tx=clamp(pr.x,-FENCE.x,FENCE.x); r.tz=clamp(pr.z,FENCE.zMin,FENCE.zMax); r.ty=clamp(num(pr.y),0,2); r.tyaw=num(pr.yaw);
    if(Array.isArray(pr.b)&&pr.b.length===3) r.tb.set(num(pr.b[0]),Math.max(R,num(pr.b[1],1)),num(pr.b[2]));
    const t=pr.t===1?"airless":"regular"; if(r.type!==t){ r.type=t; r.ball.material = t==="regular"?matRegular:matAirless; }
    const bc=num(pr.bc,-1); if(r.bc!==null && bc>r.bc && bc-r.bc<6) remoteBounce(r); r.bc=bc;
    const bk=num(pr.bkd,0); if(r.bkd!==undefined && bk>r.bkd){ flash("BLOCKED!"); blockSound(); } r.bkd=bk;
    const sc=num(pr.s,0); if(!TR && r.s!==null && sc>r.s){ toast(sc-r.s===3 ? name+" hit a three!" : name+" scored +"+(sc-r.s)); if(sc-r.s===3) cheerSound(); } r.s=sc;
    const m=CODE_MODE[pr.a]||"free"; r.mode=m; r.rl=pr.rl===1;
    const at=num(pr.at); if(at!==r.lastAt){ r.lastAt=at; r.at=at; }
  }
  for(const [key,r] of remotes) if(!seen.has(key)){ r.dispose(); remotes.delete(key); rosterDirty=true; }
  // in a tournament there is one game ball: only the player holding possession shows it
  const tok = TR ? curToken() : null;
  for(const [key,r] of remotes) r.ball.visible = !TR || (tok && tok.h===key);
  const a=Math.min(1,dt*10);
  for(const r of remotes.values()){
    const g=r.av.root; r.at+=dt;
    if(r.fresh){ g.position.set(r.tx,r.ty,r.tz); r.ball.position.copy(r.tb); g.rotation.y=r.tyaw; r.fresh=false; }
    const ox=g.position.x, oz=g.position.z;
    g.position.x+=(r.tx-ox)*a; g.position.z+=(r.tz-oz)*a; g.position.y+=(r.ty-g.position.y)*Math.min(1,dt*14);
    const v=dt>0?Math.hypot(g.position.x-ox,g.position.z-oz)/dt:0; r.speed+=(v-r.speed)*Math.min(1,dt*6);
    g.rotation.y+=angleTo(g.rotation.y,r.tyaw)*a;
    r.ball.position.lerp(r.tb, Math.min(1,dt*18));
    const f=fwdOf(g.rotation.y), rr=rightOf(g.rotation.y);
    const P={ speed:r.speed>0.4?r.speed:0, t:r.at, released:r.rl, air:g.position.y>0.03, dm:r.dm, dl:r.dl,
      ballY:r.ball.position.y-g.position.y, ballF:(r.ball.position.x-g.position.x)*f.x+(r.ball.position.z-g.position.z)*f.z, ballR:(r.ball.position.x-g.position.x)*rr.x+(r.ball.position.z-g.position.z)*rr.z };
    poseAvatar(r.av, r.mode, P, dt);
  }
}
function renderRoster(){
  const dot=$("netDot"), txt=$("netText"), box=$("roster");
  if(net && TR){ box.hidden=true; dot.style.background="var(--amber)"; txt.textContent="Tournament · PIN "+fmtPin(pin); return; }
  if(!net){
    box.hidden=true; dot.style.background="var(--muted)";
    txt.textContent = netState==="connecting" ? "Connecting…" : "Solo practice";
    return;
  }
  const rows=[{ name:myName, color:look.color, s:score, me:true }];
  for(const pe of otherPeers()) rows.push({ name:String(pe.presence.n).slice(0,16)||"Player", color:safeColor(pe.presence.c), s:Math.max(0,Math.floor(num(pe.presence.s))) });
  rows.sort((a,b)=>b.s-a.s);
  dot.style.background="var(--teal)";
  txt.textContent="PIN "+fmtPin(pin)+" · "+rows.length+(rows.length===1?" player":" players");
  box.hidden=false; $("rosterTitle").textContent="Game "+fmtPin(pin);
  $("rosterList").replaceChildren(...rows.slice(0,10).map(rw=>{
    const li=document.createElement("li"), n=document.createElement("span"), i=document.createElement("i"), b=document.createElement("b");
    i.style.background=rw.color; n.append(i, document.createTextNode(rw.name+(rw.me?" (you)":""))); b.textContent=rw.s+" pts";
    li.append(n,b); return li;
  }));
}

/* ---------- tournament: winner stays on, first to 3 baskets ---------- */
const WIN=3;
let myPeer=null, presenting=false, role="free", TR=null, hostT=null, seenM=0, countdownT=0, myTok=null, myMS=0, gotBlocked=0, gapUntil=0, missing={}, bracketOpen=true, bracketSig="", hostTimer=0;
function validTR(t){ return t && typeof t==="object" && typeof t.m==="number" && ["play","gap","done","off"].includes(t.st) && Array.isArray(t.q) && Array.isArray(t.h) && t.nm && typeof t.nm==="object"; }
function getTR(){
  if(isHost) return hostT && hostT.st!=="off" ? hostT : null;
  if(!net) return null;
  for(const pe of net.peers()){ if(pe.sameTab) continue; const pr=pe.presence||{}; if(pr.h===1 && validTR(pr.tr)) return pr.tr.st==="off" ? null : pr.tr; }
  return null;
}
function presOf(id){ if(!net||!id) return null; const pe=net.peers().find(q=>q.peer===id); return pe ? (pe.presence||{}) : null; }
function nameOf(id){
  if(id && id===myPeer) return myName;
  if(TR && TR.nm && typeof TR.nm[id]==="string") return TR.nm[id].slice(0,16)||"Player";
  const p=presOf(id); return p && typeof p.n==="string" ? p.n.slice(0,16)||"Player" : "Player";
}
function colorOf(id){ if(id===myPeer) return look.color; const p=presOf(id); return p ? safeColor(p.c) : "#9aa3b0"; }
function matchScore(id){
  if(!TR) return 0;
  if(id===myPeer) return role==="player" ? myMS : 0;
  const p=presOf(id); return p && p.mm===TR.m ? clamp(Math.floor(num(p.ms)),0,WIN) : 0;
}
function oppPeer(){ return TR ? (TR.a===myPeer ? TR.b : TR.a) : null; }
// whoever holds the highest possession token owns the game ball and simulates it
function curToken(){
  let best={ v:0, h:TR?TR.a:null };
  if(!TR) return best;
  const consider=pt=>{ if(Array.isArray(pt) && pt[0]===TR.m && typeof pt[1]==="number" && (pt[2]===TR.a||pt[2]===TR.b)){ if(pt[1]>best.v || (pt[1]===best.v && pt[2]>best.h)) best={ v:pt[1], h:pt[2] }; } };
  [TR.a,TR.b].forEach(id=>{ if(id===myPeer) consider(myTok); else { const p=presOf(id); if(p) consider(p.pt); } });
  return best;
}
function handOff(){ const c=curToken(); myTok=[TR.m,c.v+1,oppPeer()]; ball.state="none"; }
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function entrants(){
  const list=[]; if(!presenting && myPeer) list.push([myPeer,myName]);
  for(const pe of otherPeers()){ if(pe.presence.pr===1) continue; list.push([pe.peer,String(pe.presence.n).slice(0,16)||"Player"]); }
  return list.slice(0,24);
}
function pushTR(){ if(net && hostT) net.presence({ tr:hostT }).catch(()=>{}); }
function hostStart(){
  if(!net||!myPeer){ toast("Still connecting. Try again in a moment."); return false; }
  const e=shuffle(entrants());
  if(e.length<2) return false;
  hostT={ id:Math.floor(Math.random()*1e6), st:"play", m:1, a:e[0][0], b:e[1][0], q:e.slice(2).map(x=>x[0]), h:[], lw:null, ch:null, nm:Object.fromEntries(e) };
  missing={}; pushTR(); return true;
}
function hostTick(){
  if(!isHost||!hostT||!net||hostT.st==="off"||hostT.st==="done") return;
  const now=performance.now(); let changed=false;
  const alive=id=> id===myPeer ? !presenting : !!otherPeers().find(pe=>pe.peer===id);
  const out=new Set(hostT.h.map(x=>x[1]));
  // people who join late go to the back of the line
  for(const [id,nm] of entrants()){
    if(id!==hostT.a && id!==hostT.b && !hostT.q.includes(id) && !out.has(id) && hostT.q.length<22){ hostT.q.push(id); hostT.nm[id]=nm; changed=true; }
  }
  const q2=hostT.q.filter(alive); if(q2.length!==hostT.q.length){ hostT.q=q2; changed=true; }
  if(hostT.st==="play"){
    const sc=id=> id===myPeer ? myMS : (()=>{ const p=presOf(id); return p && p.mm===hostT.m ? num(p.ms) : 0; })();
    const sa=sc(hostT.a), sb=sc(hostT.b);
    [hostT.a,hostT.b].forEach(id=>{ if(alive(id)) delete missing[id]; else if(!missing[id]) missing[id]=now; });
    const gone=id=>missing[id] && now-missing[id]>4000;
    if(sa>=WIN || sb>=WIN || gone(hostT.a) || gone(hostT.b)){
      let w,l;
      if(gone(hostT.a) && !gone(hostT.b)){ w=hostT.b; l=hostT.a; } else if(gone(hostT.b) && !gone(hostT.a)){ w=hostT.a; l=hostT.b; }
      else if(sa>=sb){ w=hostT.a; l=hostT.b; } else { w=hostT.b; l=hostT.a; }
      hostT.h.push([w,l,Math.max(sa,sb),Math.min(sa,sb)]); hostT.lw=w; hostT.st="gap"; gapUntil=now+4000; changed=true;
    }
  } else if(hostT.st==="gap" && now>gapUntil){
    let a=hostT.lw; if(!alive(a)) a=hostT.q.shift();
    const b=hostT.q.shift();
    if(a && b){ hostT.m++; hostT.a=a; hostT.b=b; hostT.st="play"; missing={}; }
    else { hostT.st="done"; hostT.ch=a||hostT.lw; }
    changed=true;
  }
  if(changed) pushTR();
}
function resetForMatch(){
  const isA=myPeer===TR.a;
  Object.assign(player,{ x:isA?-1.8:1.8, z:-4.4, y:0, vy:0, vx:0, vz:0, air:false, state:"play", t:0 });
  player.yaw=yawToRim(); cam.yaw=player.yaw; cam.pitch=0; ball.state="none"; ball.info=null; pendingCel=false; $("meter").hidden=true;
}
function updateTournament(dt){
  if(net && !myPeer){ const s=net.peers().find(q=>q.sameTab); if(s) myPeer=s.peer; }
  TR = net ? getTR() : null;
  const prev=role;
  if(presenting && onCourt) role="spec";
  else if(TR) role = (TR.st==="play"||TR.st==="gap") && (myPeer===TR.a||myPeer===TR.b) ? "player" : "spec";
  else role="free";
  if(prev!==role) rosterDirty=true;
  // anyone waiting in the lobby is brought in when the tournament starts
  if(TR && !onCourt && !$("lobby").hidden) goCourt();
  if(TR && TR.st==="play" && TR.m!==seenM){
    seenM=TR.m; countdownT=3.4;
    if(role==="player"){ myMS=0; myTok=null; resetForMatch(); }
  }
  if(role!=="player" && prev==="player"){ ball.state="none"; player.state="play"; player.y=0; player.air=false; }
  if(role==="spec") ball.state="none";
  if(role==="free" && prev!=="free"){ catchBall(); ball.p.set(player.x+0.3,handY(),player.z-0.3); myTok=null; }
  if(role==="player" && TR.st==="play"){
    const tok=curToken();
    if(tok.h===myPeer && ball.state==="none"){ catchBall(); ball.p.set(player.x+0.3,handY(),player.z-0.3); }
    if(tok.h!==myPeer && ball.state!=="none"){
      ball.state="none";
      if(["shoot","layup","dunk"].includes(player.state)){ player.state=player.air?"drop":"play"; $("meter").hidden=true; }
    }
    // grab the ball when your opponent's shot or block leaves it loose near you
    if(tok.h!==myPeer && player.state==="play" && countdownT<=0){
      const r=remotes.get(tok.h), p=presOf(tok.h);
      if(r && p && p.bs==="f"){ const bp=r.ball.position;
        if(Math.hypot(bp.x-player.x,bp.z-player.z)<0.85 && bp.y<1.9){ myTok=[TR.m,tok.v+1,myPeer]; catchBall(); ball.p.set(bp.x,handY(),bp.z); } }
    }
  }
  if(countdownT>0) countdownT-=dt;
  document.body.classList.toggle("spec", role==="spec");
  me.visible = role!=="spec"; if(me.ready) me.root.visible=me.visible;
  if(isHost){ hostTimer+=dt; if(hostTimer>0.25){ hostTimer=0; hostTick(); } }
  renderTourUI();
}
function setText(id,v){ const e=$(id); if(e.textContent!==v) e.textContent=v; }
function setHidden(id,h){ const e=$(id); if(e.hidden!==h) e.hidden=h; }
function renderTourUI(){
  const live = TR && (TR.st==="play"||TR.st==="gap");
  setHidden("matchBar", !live);
  if(live){
    setText("mbA",nameOf(TR.a)); setText("mbB",nameOf(TR.b)); setText("mbAs",String(matchScore(TR.a))); setText("mbBs",String(matchScore(TR.b))); setText("mbM","Match "+TR.m);
    $("mbAc").style.background=colorOf(TR.a); $("mbBc").style.background=colorOf(TR.b);
  }
  setHidden("bracket", !(TR && (bracketOpen || role==="spec")));
  if(TR) renderBracket();
  const showCount = TR && TR.st==="play" && countdownT>0;
  setHidden("count", !showCount);
  if(showCount){ const n=Math.ceil(countdownT-0.4); setText("count", n>0 ? String(n) : "GO!"); }
  const gap = TR && TR.st==="gap" && TR.h.length;
  setHidden("result", !gap);
  if(gap){ const x=TR.h[TR.h.length-1];
    setText("resultText", nameOf(x[0])+" wins "+x[2]+"–"+x[3]);
    setText("resultNext", TR.q.length ? "Next: "+nameOf(TR.lw)+" vs "+nameOf(TR.q[0]) : "That was the final match"); }
  const done = TR && TR.st==="done";
  setHidden("champ", !done);
  if(done){ setText("champName", nameOf(TR.ch)); setText("champLine", "Won "+TR.h.filter(x=>x[0]===TR.ch).length+" match"+(TR.h.filter(x=>x[0]===TR.ch).length===1?"":"es")+" on the beach court"); setHidden("champHost", !isHost); }
  setHidden("pinBanner", !(net && pin && (presenting || role==="spec")));
  if(pin) setText("pinBig", fmtPin(pin));
  setHidden("fsBtn", !isHost);
}
function renderBracket(){
  const items=[];
  TR.h.forEach((x,i)=>items.push({ no:"Match "+(i+1), parts:[[nameOf(x[0])+" "+x[2],"w"],[" – ",""],[x[3]+" "+nameOf(x[1]),"l"]] }));
  if(TR.st==="play") items.push({ no:"Match "+TR.m+" · live", cls:"live", parts:[[nameOf(TR.a)+" "+matchScore(TR.a),""],[" – ",""],[matchScore(TR.b)+" "+nameOf(TR.b),""]] });
  let n=TR.h.length+(TR.st==="play"?2:1);
  TR.q.forEach((id,i)=>items.push({ no:"Match "+(n+i), parts:[[TR.st==="gap"&&i===0 ? nameOf(TR.lw) : "Winner",""],[" vs ",""],[nameOf(id),""]] }));
  if(TR.st==="done") items.push({ no:"Champion", cls:"champ", parts:[[nameOf(TR.ch),"w"]] });
  const sig=JSON.stringify(items); if(sig===bracketSig) return; bracketSig=sig;
  $("bracketList").replaceChildren(...items.map(it=>{
    const li=document.createElement("li"); if(it.cls) li.className=it.cls;
    const no=document.createElement("span"); no.className="no"; no.textContent=it.no;
    const line=document.createElement("span"); line.className="line";
    it.parts.forEach(([t,c])=>{ const sp=document.createElement("span"); if(c) sp.className=c; sp.textContent=t; line.append(sp); });
    li.append(no,line); return li;
  }));
}
// presenter / spectator camera: a TV-style view from the sideline that follows the action
function broadcastCamera(dt,now){
  const pts=[];
  for(const r of remotes.values()) pts.push(r.av.root.position);
  if(role!=="spec") pts.push(new V3(player.x,0,player.z));
  const t=new V3(0,0,-7.5);
  if(pts.length){ t.set(0,0,0); pts.forEach(p=>{ t.x+=p.x; t.z+=p.z; }); t.x/=pts.length; t.z/=pts.length; }
  t.x=clamp(t.x,-5,5); t.z=clamp(t.z,-10.5,-3);
  const sway=Math.sin(now*0.00012)*1.6;
  const pos=new V3(t.x*0.35+5.6+sway, 4.4, t.z+6.4), look=new V3(t.x*0.8, 1.3, t.z-1.7);
  const k=1-Math.exp(-dt*1.8);
  cam.pos.lerp(pos,k); cam.look.lerp(look,k);
  camera.position.copy(cam.pos); camera.lookAt(cam.look); sky.position.copy(camera.position);
}

/* ---------- game loop ---------- */
let last=performance.now();
const tmp=new V3();
function airPhysics(dt){
  if(!player.air) return false;
  player.vy-=G*dt; player.y+=player.vy*dt;
  if(player.y<=0){ player.y=0; player.vy=0; player.air=false; return true; }
  return false;
}
function updateStates(dt){
  const st=player.state; player.t+=dt; const t=player.t;
  if(st==="shoot"){
    if(t>=0.2 && !player.air && !shot.jumped){ player.vy=3.1; player.air=true; shot.jumped=true; }
    if(!shot.released){
      const m=meterVal(t); $("meterFill").style.height=clamp(m,0,1)*100+"%";
      if(shot.m===null && m>=1.15) shot.m=1.15;
      if(shot.m!==null && shot.jumped) releaseJumper();
    }
    if(airPhysics(dt) && shot.released){ player.state="play"; player.t=0; }
  } else if(st==="layup"){
    if(t<0.32){ const k=1-(1-t/0.32)**2; player.x=lerp(lay.fx,lay.tx,k); player.z=lerp(lay.fz,lay.tz,k); }
    else if(!player.air && !lay.jumped){ player.vy=3.5; player.air=true; lay.jumped=true; }
    if(t>=0.52 && !lay.released){
      const ln=0.02+0.03*(1-me.arch.r.dunk/100), start=holdPos(true).clone(), target=new V3(RIM.x+gauss()*ln,RIM.y+0.02,RIM.z+gauss()*ln);
      launch(start,target,64); ball.info={ kind:"layup", three:false, dist:distToRim() }; lay.released=true; attempts++; updateShots();
    }
    if(airPhysics(dt) && lay.released){ player.state="play"; player.t=0; }
  } else if(st==="dunk"){
    const D=dunk, ft=t-D.runT;
    if(t<D.runT){ const k=t/D.runT; player.x=lerp(D.sx,D.tx,k); player.z=lerp(D.sz,D.tz,k); player.y=0; }
    else if(ft<D.flyT){ const k=ft/D.flyT; player.x=lerp(D.tx,D.qx,k); player.z=lerp(D.tz,D.qz,k);
      // a double clutch floats: the player gets up early and hangs while pumping the ball down and back up
      player.y = D.kind==="dc" ? Math.max(0,3.4-2.15*me.arch.scale)*(1-(1-Math.min(1,k/0.45))**2) : Math.max(0,(3.42-reachUp))*(1-(1-k)*(1-k));
      if(k>(D.kind==="dc"?0.88:0.84) && !D.slammed) slam(D); }
    else if(D.made && ft<D.flyT+0.6){ player.x=D.qx; player.z=D.qz; player.y=Math.max(0,3.1-reachUp); }
    else { player.state="drop"; player.t=0; player.air=true; player.vy=0; }
  } else if(st==="block"){
    if(airPhysics(dt)){ player.state="play"; player.t=0; if(ball.state==="hand") catchBall(); }
  } else if(st==="drop"){
    if(airPhysics(dt)){ player.state="play"; player.t=0; }
  } else if(st==="celebrate"){
    player.y = t<0.45 ? 0.32*Math.sin(Math.PI*t/0.45) : 0;
    if(t>2.0){ player.state="play"; player.t=0; player.y=0; }
  } else if(st==="play"){
    if(pendingCel && !player.air){ pendingCel=false; player.state="celebrate"; player.t=0; celCount++; }
  }
}
function step(dt){
  // movement relative to the camera
  let mx=0,mz=0;
  if(keys.has("KeyW")) mz-=1; if(keys.has("KeyS")) mz+=1; if(keys.has("KeyA")) mx-=1; if(keys.has("KeyD")) mx+=1;
  if(keys.has("ArrowLeft")) cam.yaw+=1.8*dt; if(keys.has("ArrowRight")) cam.yaw-=1.8*dt;
  if(keys.has("ArrowUp")) cam.pitch+=1*dt; if(keys.has("ArrowDown")) cam.pitch-=1*dt; clampPitch();
  spaceHeld=keys.has("Space") && player.state==="play";
  const RT=me.arch.r, stanceDef=spaceHeld && ball.state!=="dribble", stanceProt=spaceHeld && ball.state==="dribble";
  const canMove=player.state==="play" && countdownT<=0 && !(TR && TR.st!=="play"), sprint=keys.has("ShiftLeft")||keys.has("ShiftRight");
  const sp = stanceDef ? 2.3+0.9*RT.def/100 : stanceProt ? 2.5+0.6*RT.speed/100 : sprint ? 4.9+1.7*RT.speed/100 : 2.9+1.2*RT.speed/100;
  let tvx=0,tvz=0;
  if(canMove && (mx||mz)){ const l=Math.hypot(mx,mz); mx/=l; mz/=l; const f=fwdOf(cam.yaw), r=rightOf(cam.yaw); tvx=(r.x*mx-f.x*mz)*sp; tvz=(r.z*mx-f.z*mz)*sp; }
  const acc=1-Math.exp(-dt*9); player.vx+=(tvx-player.vx)*acc; player.vz+=(tvz-player.vz)*acc;
  if(canMove){ player.x+=player.vx*dt; player.z+=player.vz*dt; } else { player.vx=player.vz=0; }
  player.x=clamp(player.x,-PB.x,PB.x); player.z=clamp(player.z,PB.zMin,PB.zMax);
  // keep out of the hoop stanchion
  if(Math.abs(player.x)<0.9 && player.z<-14.9) player.z=-14.9;
  // don't walk through your opponent
  if(role==="player"){ const r=remotes.get(oppPeer()); if(r){ const op=r.av.root.position, dx=player.x-op.x, dz=player.z-op.z, d=Math.hypot(dx,dz); if(d<0.62 && d>0.001){ player.x=op.x+dx/d*0.62; player.z=op.z+dz/d*0.62; } } }
  player.speed=Math.hypot(player.vx,player.vz);
  let want = player.speed>0.35 ? Math.atan2(-player.vx,-player.vz) : (ball.state==="dribble" ? cam.yaw : player.yaw);
  if(stanceDef){ want=cam.yaw; const r=role==="player" && remotes.get(oppPeer()); if(r){ const op=r.av.root.position; want=Math.atan2(-(op.x-player.x),-(op.z-player.z)); } }
  if(["shoot","layup","dunk","drop"].includes(player.state)) want=yawToRim();
  if(player.state==="block") want=player.yaw;
  if(player.state==="celebrate") want=player.yaw;
  player.yaw+=angleTo(player.yaw,want)*Math.min(1,dt*10);

  updateStates(dt);
  if(meterHide>0){ meterHide-=dt; if(meterHide<=0 && player.state!=="shoot") $("meter").hidden=true; }

  // pose the player
  const f=fwdOf(player.yaw);
  let mode="free", released=false, poseT=player.t;
  switch(player.state){
    case "play": mode = ball.state==="dribble" ? (stanceProt?"prot":"dribble") : (stanceDef?"def":"free"); break;
    case "shoot": mode="shoot"; released=shot.released; break;
    case "layup": mode="layup"; released=lay.released; break;
    case "dunk": { const ft=player.t-dunk.runT; mode = ft<0 ? "dunkRun" : ft<dunk.flyT ? (dunk.kind==="dc"?"dc":"dunk") : "hang"; released=dunk.slammed; poseT = mode==="dc" ? ft : mode==="hang" ? ft-dunk.flyT : player.t; break; }
    case "drop": mode="hang"; break;
    case "block": mode="blk"; break;
    case "celebrate": mode="cel"; break;
  }
  localMode=mode; localReleased=released; localPoseT=poseT;
  const movingSpeed = player.state==="play" ? player.speed : (["layup","dunk"].includes(player.state) && !player.air && player.y<0.01 ? 5.5 : 0);
  me.root.position.set(player.x,player.y,player.z); me.root.rotation.y=player.yaw;
  const rgt=rightOf(player.yaw);
  localDm = ball.state==="dribble" && drib.ph!=="hold" ? drib.move : "n";
  poseAvatar(me, mode, { speed:movingSpeed, t:poseT, released, air:player.y>0.02, dm:localDm, dl:drib.lead,
    ballY:ball.p.y-player.y, ballF:(ball.p.x-player.x)*f.x+(ball.p.z-player.z)*f.z, ballR:(ball.p.x-player.x)*rgt.x+(ball.p.z-player.z)*rgt.z }, dt);
  palmWorld(me,"R",_a); reachUp = lerp(reachUp, _a.y-player.y, 0.3);

  updateBall(dt);

  if(ringT<1){ ringT+=dt*2.2; const s=0.2+ringT*ringMax; ring.scale.set(s,s,s); ring.material.opacity=(1-ringT)*0.7; } else ring.material.opacity=0;
  neighbor=Math.max(0,neighbor-dt*5);
  const nb=$("nbBar"); nb.style.width=neighbor+"%"; nb.style.background = neighbor>66?"var(--red)":neighbor>33?"var(--amber)":"var(--teal)";
  $("nbText").textContent = neighbor>80?"Banging on the ceiling":neighbor>55?"Annoyed":neighbor>25?"Noticing":"Calm";
  const three=isThree(player.x,player.z), dr=distToRim(), label=(three?"3PT range":dr<2.8?"Layup range":dr<5.2?"Dunk range":"Mid-range")+" · "+dr.toFixed(1)+" m";
  if($("rangeText").textContent!==label){ $("rangeText").textContent=label; $("rangeChip").classList.toggle("three",three); }
}
function updateBall(dt){
  ballMesh.visible = ball.state!=="none" && role!=="spec";
  if(ball.state==="none") return;
  if(ball.state==="dribble"){
    // the ball never stops: it keeps bouncing whether you're walking or standing still
    updateDribble(dt);
  } else if(ball.state==="hand"){
    const useRight = player.state==="layup" && player.air;
    if(player.state==="block"){ palmWorld(me,"L",_a); palmWorld(me,"R",_b); ball.p.copy(_a.add(_b).multiplyScalar(0.5)).y+=0.1; }
    else
    ball.p.copy(holdPos(useRight)); if(player.state==="dunk" && player.t>=dunk.runT) ball.p.y+=0.04;
  } else {
    flyBall(dt);
  }
  ballMesh.position.copy(ball.p);
  const squash = ball.p.y<R+0.02 ? (ball.type==="regular"?0.86:0.8) : 1;
  ballMesh.scale.set(1/Math.sqrt(squash), squash, 1/Math.sqrt(squash));
}
function flyBall(dt){
  const sub=4, h=dt/sub;
  for(let i=0;i<sub;i++){
    ball.prev=ball.p.y;
    ball.v.y-=G*h; ball.p.addScaledVector(ball.v,h);
    if(ball.p.y<R){ ball.p.y=R; if(ball.v.y<-0.6) ball.v.y=impact(-ball.v.y); else { ball.v.y=0; ball.v.x*=1-2.5*h; ball.v.z*=1-2.5*h; } }
    if(ball.p.x<-FENCE.x+R){ ball.p.x=-FENCE.x+R; ball.v.x=Math.abs(ball.v.x)*0.4; }
    if(ball.p.x> FENCE.x-R){ ball.p.x= FENCE.x-R; ball.v.x=-Math.abs(ball.v.x)*0.4; }
    if(ball.p.z<FENCE.zMin+R){ ball.p.z=FENCE.zMin+R; ball.v.z=Math.abs(ball.v.z)*0.4; }
    if(ball.p.z>FENCE.zMax-R){ ball.p.z=FENCE.zMax-R; ball.v.z=-Math.abs(ball.v.z)*0.4; }
    if(Math.abs(ball.p.x)<0.915+R*0.5 && ball.p.y>2.9 && ball.p.y<3.97 && ball.p.z-R<BOARD_Z && ball.p.z>BOARD_Z-0.15 && ball.v.z<0){
      ball.p.z=BOARD_Z+R; ball.v.z=-ball.v.z*0.6; rimSound(2);
    }
    for(const q of rimPts){
      tmp.subVectors(ball.p,q); const d=tmp.length();
      if(d<R+0.019){ tmp.divideScalar(d); const vn=ball.v.dot(tmp);
        if(vn<0){ ball.v.addScaledVector(tmp,-(1+0.55)*vn); const now=performance.now(); if(now-lastRimHit>120){ rimSound(-vn); lastRimHit=now; } }
        ball.p.addScaledVector(tmp,R+0.019-d); }
    }
    if(ball.info && !ball.blocked && ball.t<0.5){ const r=findBlocker(ball.p,0.85); if(r && ball.p.y>r.av.root.position.y+1.3) blockBall(r); }
    if(ball.state==="flying" && ball.info && !ball.scored && ball.prev>RIM.y && ball.p.y<=RIM.y && ball.v.y<0 && Math.hypot(ball.p.x-RIM.x,ball.p.z-RIM.z)<RIM.r-0.02){
      ball.scored=true; ball.scoredAt=ball.t; onScore(); ball.v.x*=0.3; ball.v.z*=0.3;
    }
  }
  ball.t+=dt;
  ballMesh.rotation.x += ball.spin.x*dt; ballMesh.rotation.z += ball.spin.z*dt; ball.spin.multiplyScalar(1-dt*0.6);
  const chest=new V3(player.x,1.15+player.y,player.z).addScaledVector(fwdOf(player.yaw),0.4);
  const free = player.state==="play";
  if(ball.state==="pass"){
    if(free && (ball.p.distanceTo(chest)<0.6 || ball.t>ball.passT+0.5)) catchBall();
    return;
  }
  const match = role==="player";
  // grab a loose ball you run into
  if(free && ball.t>0.6 && !(match && ball.scored) && Math.hypot(ball.p.x-player.x,ball.p.z-player.z)<0.8 && ball.p.y<1.8){ catchBall(); return; }
  // in a match: after a basket the ball goes to the other player; misses stay loose for a rebound
  if(match){ if(ball.scored && ball.t-ball.scoredAt>0.7) handOff(); return; }
  // rebound comes back to you automatically, like a practice partner passing it out
  const settled = ball.p.y<=R+0.01 && ball.v.length()<0.7 && ball.t>1;
  if(free && ((ball.scored && ball.t-ball.scoredAt>0.8) || ball.t>3.2 || settled)) startPass();
}
let celBlend=0;
function showcaseCamera(dt,now){
  // the select screen frames your player from the front, off to the right of the menu
  const f=fwdOf(player.yaw), r=rightOf(player.yaw), wide=innerWidth>820, ang=Math.sin(now*0.00022)*0.35;
  const side = wide ? 0.95 : 0;
  const pos=new V3(player.x,0,player.z).addScaledVector(f,3.3*Math.cos(ang)).addScaledVector(r,3.3*Math.sin(ang)+side); pos.y=1.42;
  const look=new V3(player.x,1.08,player.z).addScaledVector(r,side);
  const k=1-Math.exp(-dt*4); cam.pos.lerp(pos,k); cam.look.lerp(look,k);
  camera.position.copy(cam.pos); camera.lookAt(cam.look); sky.position.copy(camera.position);
}
function updateCamera(dt,instant){
  // during a three-point celebration the camera swings around to face the shooter
  const want = player.state==="celebrate" && player.t<1.7 ? 1 : 0;
  celBlend += (want-celBlend)*(instant?1:1-Math.exp(-dt*3.5));
  const e = celBlend*celBlend*(3-2*celBlend);
  const behindA = cam.yaw+Math.PI, frontA = player.yaw+0.35;
  const ang = behindA + angleTo(behindA,frontA)*e;
  const dist = lerp(4.6,2.7,e);
  const f=fwdOf(cam.yaw);
  const pos=new V3(player.x-Math.sin(ang)*dist, 0, player.z-Math.cos(ang)*dist);
  pos.y = lerp(Math.max(0.6,2.3-cam.pitch*2.6+player.y*0.45), 1.55, e);
  const lookBack=new V3(player.x,0,player.z).addScaledVector(f,3.2); lookBack.y=1.4+cam.pitch*3.2+player.y*0.55;
  const lookFront=new V3(player.x,1.5+player.y*0.6,player.z);
  const look=lookBack.lerp(lookFront,e);
  const k=instant?1:1-Math.exp(-dt*10);
  cam.pos.lerp(pos,k); cam.look.lerp(look,k);
  camera.position.copy(cam.pos); camera.lookAt(cam.look); sky.position.copy(camera.position);
}
function idle(dt){
  const f=fwdOf(player.yaw), r=rightOf(player.yaw);
  spaceHeld=false; player.speed=0;
  me.root.position.set(player.x,player.y,player.z); me.root.rotation.y=player.yaw;
  if(ball.state==="dribble") updateBall(dt);
  const dm = ball.state==="dribble" && drib.ph!=="hold" ? drib.move : "n";
  poseAvatar(me, ball.state==="dribble"?"dribble":"free", { speed:0, t:0, released:false, air:false, dm, dl:drib.lead, ballY:ball.p.y, ballF:(ball.p.x-player.x)*f.x+(ball.p.z-player.z)*f.z, ballR:(ball.p.x-player.x)*r.x+(ball.p.z-player.z)*r.z }, dt);
}
function frame(now){
  const dt=Math.min(1/30,(now-last)/1000); last=now;
  updateTournament(dt);
  if(onCourt){ helpT+=dt; const show=helpT<10||helpT>9000; $("helpCard").classList.toggle("faded",!show); $("helpTip").style.opacity=show?0:1; }
  if(role!=="spec"){ if(!paused && !detailOpen) step(dt); else idle(dt); }
  if(role==="spec"){ ballMesh.visible=false; broadcastCamera(dt,now); } else if(!onCourt) showcaseCamera(dt,now); else updateCamera(dt,false);
  if(onCourt) sendPresence(now);
  updateRemotes(dt);
  rosterTimer+=dt; if(rosterDirty && rosterTimer>0.3){ rosterTimer=0; rosterDirty=false; renderRoster(); }
  lobbyTimer+=dt; if(lobbyDirty && lobbyTimer>0.3){ lobbyTimer=0; lobbyDirty=false; renderLobby(); }
  // water, net, rim
  waterNormal.offset.x+=dt*0.004; waterNormal.offset.y+=dt*0.009;
  foamTex.offset.x+=dt*0.01; foam.material.opacity=0.55+0.25*Math.sin(now*0.0011);
  if(netT<1){ netT+=dt*2; const s=Math.sin(netT*Math.PI); hoopNet.scale.set(1-s*0.15,1+s*0.25,1-s*0.15); }
  rimTilt*=Math.exp(-dt*6); hoop.rotation.x=rimTilt;
  if(window.__camOverride){ const o=window.__camOverride(); camera.position.copy(o[0]); camera.lookAt(o[1]); }
  renderer.render(scene,camera);
  if(detailOpen) drawCut(now);
  requestAnimationFrame(frame);
}
ball.p.set(player.x+0.3,handY(),player.z-0.3);
updateCamera(0,true);
if(window.__HOOPS_TEST){ window.__drib=drib; } requestAnimationFrame(frame);
})();
</script>

</body>
</html>
