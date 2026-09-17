#!/usr/bin/env python3
"""Generate the Cainz x imgix AI Image Edit demo mockup."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(HERE, "..", "manifest.json")))

# ---- the one thing to swap if the source domain changes -------------------
DOMAIN = os.environ.get("IMGIX_DOMAIN", "jpblogtzk.imgix.net")
FOLDER = "tkanemoto"
# --------------------------------------------------------------------------

CATS = [
    ("packaging", "パッケージ商材", "袋・パウチ・ボトル・箱。<code>ai-image-edit=packaging</code> が最も効くカテゴリです。"),
    ("home", "収納・インテリア", "家具・収納用品。"),
    ("appliance", "家電・工具", "生活家電と電動工具。"),
    ("outdoor", "アウトドア・エクステリア", "キャンプ・園芸・DIY。"),
    ("living", "寝具・ルームウェア", "毛布・スリッパ・敷パッド。"),
    ("pet", "ペット用品", "ペット服・キャットグッズ。"),
]

# hero products for the before/after sliders — packaged goods where the edit shows
SLIDERS = [
    ("4549509981787_01.jpg", "カインズ 酸素系漂白剤 2kg", "紙袋のシワ・折れを平滑化し、露出を補正"),
    ("4550596262499_01.jpg", "花と野菜の培養土 25L", "大型ポリ袋のたるみと影を整える"),
    ("4549509274551_01.jpg", "薬用泡ハンドソープ 詰替 220ml", "パウチのシワを除去（バーコードは保護）"),
    ("4550596176352_01.jpg", "スマイリア 猫用 1.2kg", "フード袋のヨレと硬い影を補正"),
    ("4550596105543_01.jpg", "おうちカレー 170g×4袋", "レトルト外装の反射とシワを軽減"),
    ("4904998126871_01.jpg", "都ほまれ 原酒 2000ml", "瓶ラベルの歪みとハイライトを整える"),
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def render():
    cat_js = {}
    for key, _, _ in CATS:
        cat_js[key] = [{"f": r[0], "n": r[1], "p": r[2],
                        "t": (r[3] if len(r) > 3 else "")} for r in MANIFEST[key]]
    data = {
        "domain": DOMAIN,
        "folder": FOLDER,
        "cats": cat_js,
        "banners": [{"f": r[0], "n": r[1]} for r in MANIFEST["banners"]],
        "strips": [{"f": r[0], "n": r[1]} for r in MANIFEST["strips"]],
        "features": [{"f": r[0], "n": r[1]} for r in MANIFEST["features"]],
        "sliders": [{"f": a, "n": b, "d": c} for a, b, c in SLIDERS],
        "catmeta": [{"k": k, "t": t, "d": d} for k, t, d in CATS],
    }
    return TEMPLATE.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Packaging Retouch Demo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --green:#0f8a3d; --green-dk:#0a6e30; --green-lt:#e8f5ec;
  --ink:#16181d; --ink-2:#4a5058; --ink-3:#7c848e;
  --line:#e2e5ea; --bg:#ffffff; --bg-2:#f6f7f9; --card:#ffffff;
  --accent:#c8102e; --amber:#b26a00;
  --imgix:#c2185b; --imgix-2:#6a1b9a;
  --radius:10px;
  --shadow:0 1px 2px rgba(16,24,40,.06),0 4px 12px rgba(16,24,40,.06);
}
:root:not([data-theme="light"]){
  @media (prefers-color-scheme: dark){
    --ink:#e9ecf1; --ink-2:#aab2bd; --ink-3:#818a95;
    --line:#2b3039; --bg:#111419; --bg-2:#171b21; --card:#1a1f26;
    --green-lt:#12301f;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 4px 14px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"]{
  --ink:#e9ecf1; --ink-2:#aab2bd; --ink-3:#818a95;
  --line:#2b3039; --bg:#111419; --bg-2:#171b21; --card:#1a1f26;
  --green-lt:#12301f;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 4px 14px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--bg); color:var(--ink);
  font-family:"Noto Sans JP",Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:15px; line-height:1.6; -webkit-font-smoothing:antialiased;
}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}

/* ---------- demo bar ---------- */
.demobar{
  position:sticky; top:0; z-index:60;
  background:linear-gradient(90deg,var(--imgix-2),var(--imgix));
  color:#fff; box-shadow:0 2px 10px rgba(0,0,0,.18);
}
.demobar .wrap{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.db-brand{display:flex;align-items:center;gap:9px;font-weight:700;letter-spacing:.2px;font-size:14px}
.db-dot{width:9px;height:9px;border-radius:50%;background:#7ef3b0;box-shadow:0 0 0 3px rgba(126,243,176,.25)}
.db-note{font-size:12.5px;opacity:.92;flex:1;min-width:200px;line-height:1.45}
.db-note b{font-weight:700}
.switch{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.14);border-radius:999px;padding:4px}
.switch button{
  appearance:none;border:0;cursor:pointer;border-radius:999px;
  padding:7px 15px;font:600 12.5px/1 "Noto Sans JP",Inter,sans-serif;
  color:#fff;background:transparent;transition:.15s;white-space:nowrap;
}
.switch button.on{background:#fff;color:var(--imgix-2)}
.db-params{
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;
  background:rgba(0,0,0,.24);padding:5px 10px;border-radius:6px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;
}
.db-stats{font-size:12px;opacity:.9;font-variant-numeric:tabular-nums;white-space:nowrap}

/* ---------- cainz-ish header ---------- */
.mockflag{
  background:#fff3cd;color:#664d03;border-bottom:1px solid #ffe69c;
  font-size:12px;text-align:center;padding:6px 16px;
}
:root[data-theme="dark"] .mockflag,
:root:not([data-theme="light"]) .mockflag{@media (prefers-color-scheme:dark){background:#3a2f06;color:#ffe08a;border-color:#5a4a0a}}
header.site{background:var(--green);color:#fff}
header.site .wrap{display:flex;align-items:center;gap:18px;padding-top:12px;padding-bottom:12px}
.logo{height:34px;width:auto;filter:brightness(0) invert(1)}
.searchbox{flex:1;display:flex;background:#fff;border-radius:6px;overflow:hidden;min-width:0}
.searchbox input{flex:1;border:0;padding:9px 12px;font:400 14px/1.4 "Noto Sans JP",sans-serif;min-width:0;color:#16181d;background:#fff}
.searchbox input:focus{outline:2px solid #ffd54f;outline-offset:-2px}
.searchbox button{border:0;background:var(--green-dk);color:#fff;padding:0 16px;cursor:pointer;font-size:14px}
.hdr-ico{display:flex;gap:16px;font-size:11.5px;text-align:center;opacity:.97}
.hdr-ico span{display:block;font-size:19px;line-height:1.2}
nav.cats{background:var(--green-dk);color:#fff}
nav.cats .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:0;padding-bottom:0;scrollbar-width:none}
nav.cats .wrap::-webkit-scrollbar{display:none}
nav.cats a{padding:11px 14px;font-size:13px;text-decoration:none;white-space:nowrap;opacity:.94}
nav.cats a:hover{background:rgba(255,255,255,.12)}

/* ---------- hero ---------- */
.hero{margin:22px 0 10px}
.hero-main{border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);background:var(--bg-2);aspect-ratio:4/1}
.hero-main img{width:100%;height:100%;object-fit:cover;display:block}
.hero-thumbs{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:10px}
.hero-thumbs button{
  padding:0;border:2px solid transparent;border-radius:7px;overflow:hidden;
  cursor:pointer;background:var(--bg-2);aspect-ratio:4/1;
}
.hero-thumbs button.on{border-color:var(--green)}
.hero-thumbs img{width:100%;height:100%;object-fit:cover;display:block}

/* ---------- sections ---------- */
section{margin:44px 0}
.sec-head{display:flex;align-items:flex-end;gap:14px;margin-bottom:16px;flex-wrap:wrap}
.sec-head h2{margin:0;font-size:20px;font-weight:700;letter-spacing:.01em}
.sec-head p{margin:0;font-size:13px;color:var(--ink-2);flex:1;min-width:220px}
.pill{
  display:inline-block;background:var(--green-lt);color:var(--green-dk);
  font-size:11.5px;font-weight:700;padding:3px 9px;border-radius:999px;
}
:root[data-theme="dark"] .pill,
:root:not([data-theme="light"]) .pill{@media (prefers-color-scheme:dark){color:#6fe39b}}
.pill.hot{background:#fdeaef;color:#a3114a}
:root[data-theme="dark"] .pill.hot,
:root:not([data-theme="light"]) .pill.hot{@media (prefers-color-scheme:dark){background:#3a0f22;color:#ff8fb8}}

.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
@media(max-width:1000px){.grid{grid-template-columns:repeat(4,1fr)}.hero-thumbs{grid-template-columns:repeat(5,1fr)}}
@media(max-width:640px){.grid{grid-template-columns:repeat(2,1fr)}}

.card{
  background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden;display:flex;flex-direction:column;transition:.16s;
}
.card:hover{box-shadow:var(--shadow);transform:translateY(-2px)}
.ph{position:relative;aspect-ratio:1;background:#fff;overflow:hidden}
:root[data-theme="dark"] .ph,
:root:not([data-theme="light"]) .ph{@media (prefers-color-scheme:dark){background:#f2f2f2}}
.ph img{width:100%;height:100%;object-fit:contain;display:block}
.ph.loading::after{
  content:"";position:absolute;inset:0;background:
    linear-gradient(100deg,transparent 30%,rgba(194,24,91,.14) 50%,transparent 70%);
  background-size:220% 100%;animation:sh 1.1s linear infinite;
}
@keyframes sh{from{background-position:180% 0}to{background-position:-80% 0}}
.badge-ai{
  position:absolute;top:7px;left:7px;z-index:2;
  background:linear-gradient(90deg,var(--imgix-2),var(--imgix));color:#fff;
  font-size:10px;font-weight:700;padding:3px 7px;border-radius:5px;letter-spacing:.3px;
}
.badge-skip{
  position:absolute;top:7px;left:7px;z-index:2;
  background:rgba(20,22,26,.72);color:#fff;
  font-size:10px;font-weight:600;padding:3px 7px;border-radius:5px;
}
.tag{position:absolute;top:7px;right:7px;z-index:2;background:rgba(255,255,255,.94);color:var(--ink-2);font-size:10px;font-weight:600;padding:3px 7px;border-radius:5px;border:1px solid var(--line)}
.card-b{padding:10px 11px 12px;display:flex;flex-direction:column;gap:5px;flex:1}
.card-b .nm{font-size:12.5px;line-height:1.45;color:var(--ink);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.9em}
.card-b .pr{font-size:16px;font-weight:700;color:var(--accent);font-variant-numeric:tabular-nums;margin-top:auto}
.card-b .pr small{font-size:10.5px;font-weight:500;color:var(--ink-3);margin-left:2px}
.stars{font-size:10.5px;color:var(--amber)}
.stars span{color:var(--ink-3);margin-left:4px}

/* ---------- comparison sliders ---------- */
.cmp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
@media(max-width:960px){.cmp-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.cmp-grid{grid-template-columns:1fr}}
.cmp{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.cmp-stage{position:relative;aspect-ratio:1;background:#fff;overflow:hidden;cursor:ew-resize;touch-action:none;user-select:none}
.cmp-stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block;pointer-events:none}
.cmp-after{clip-path:inset(0 0 0 50%)}
.cmp-line{position:absolute;top:0;bottom:0;left:50%;width:2px;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.28);pointer-events:none}
.cmp-knob{
  position:absolute;top:50%;left:50%;translate:-50% -50%;
  width:34px;height:34px;border-radius:50%;background:#fff;
  box-shadow:0 2px 8px rgba(0,0,0,.3);display:grid;place-items:center;
  font-size:13px;color:#333;pointer-events:none;
}
.cmp-tag{position:absolute;bottom:9px;font-size:10.5px;font-weight:700;padding:3px 8px;border-radius:5px;color:#fff;pointer-events:none;z-index:3}
.cmp-tag.l{left:9px;background:rgba(20,22,26,.78)}
.cmp-tag.r{right:9px;background:linear-gradient(90deg,var(--imgix-2),var(--imgix))}
.cmp-b{padding:11px 13px 13px}
.cmp-b h4{margin:0 0 3px;font-size:13.5px;font-weight:700}
.cmp-b p{margin:0;font-size:12px;color:var(--ink-2);line-height:1.5}

/* ---------- strips / features ---------- */
.strips{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
@media(max-width:700px){.strips{grid-template-columns:1fr}}
.strips img{width:100%;aspect-ratio:4/1;object-fit:cover;border-radius:var(--radius);display:block;box-shadow:var(--shadow);background:var(--bg-2)}
.feats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:860px){.feats{grid-template-columns:repeat(2,1fr)}}
.feats figure{margin:0}
.feats img{width:100%;aspect-ratio:2/1;object-fit:cover;border-radius:var(--radius);display:block;box-shadow:var(--shadow);background:var(--bg-2)}
.feats figcaption{font-size:12px;color:var(--ink-2);margin-top:7px;line-height:1.45}

/* ---------- explainer ---------- */
.explain{background:var(--bg-2);border:1px solid var(--line);border-radius:14px;padding:26px}
.explain h3{margin:0 0 6px;font-size:17px}
.explain>p{margin:0 0 20px;font-size:13.5px;color:var(--ink-2);max-width:80ch}
.ex-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:820px){.ex-grid{grid-template-columns:1fr}}
.ex-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
.ex-card h4{margin:0 0 7px;font-size:13.5px;display:flex;align-items:center;gap:7px}
.ex-card h4 em{font-style:normal;background:var(--imgix);color:#fff;width:20px;height:20px;border-radius:5px;display:grid;place-items:center;font-size:11px;font-weight:700;flex:none}
.ex-card p{margin:0;font-size:12.5px;color:var(--ink-2);line-height:1.6}
.ex-card code{background:var(--bg-2);padding:1px 5px;border-radius:4px;border:1px solid var(--line)}
.urlbox{
  margin-top:20px;background:#0f1218;color:#d7dbe2;border-radius:10px;padding:14px 16px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;line-height:1.75;
  overflow-x:auto;white-space:pre;
}
.urlbox .k{color:#ff8fb8}.urlbox .v{color:#7ee3a8}.urlbox .c{color:#6b7480}

footer.site{background:var(--bg-2);border-top:1px solid var(--line);margin-top:54px;padding:26px 0;font-size:12px;color:var(--ink-3)}
footer.site .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
</style>
</head>
<body>

<div class="demobar">
  <div class="wrap">
    <div class="db-brand"><span class="db-dot"></span>imgix AI Image Edit デモ</div>
    <div class="switch" role="group" aria-label="画像モード切替">
      <button id="btnOff" class="on" type="button">通常配信</button>
      <button id="btnOn" type="button">AI補正 ON</button>
    </div>
    <div class="db-params" id="paramView"></div>
    <div class="db-note">上のトグルで、<b>同じ画像 URL にパラメータを足すだけ</b>でサイト全体がどう変わるかを切り替えられます。</div>
    <div class="db-stats" id="stats"></div>
  </div>
</div>

<div class="mockflag">
  これは imgix の機能説明用モックアップです。カインズ様の実サイトではありません。画像はデモ目的で www.cainz.com から取得しています。
</div>

<header class="site">
  <div class="wrap">
    <img class="logo" id="logo" alt="CAINZ">
    <div class="searchbox">
      <input type="text" placeholder="なにをお探しですか？" aria-label="検索">
      <button type="button">検索</button>
    </div>
    <div class="hdr-ico">
      <div><span>♡</span>お気に入り</div>
      <div><span>☰</span>マイページ</div>
      <div><span>🛒</span>カート</div>
    </div>
  </div>
</header>
<nav class="cats">
  <div class="wrap" id="navcats"></div>
</nav>

<main class="wrap">

  <div class="hero">
    <div class="hero-main"><img id="heroImg" alt=""></div>
    <div class="hero-thumbs" id="heroThumbs"></div>
  </div>

  <section id="sec-compare">
    <div class="sec-head">
      <h2>Before / After</h2>
      <span class="pill hot">ai-image-edit=packaging</span>
      <p>スライダーを左右に動かすと、同じ原本画像に対する AI 補正の効果を確認できます。撮り直しも Photoshop 作業もありません。</p>
    </div>
    <div class="cmp-grid" id="cmpGrid"></div>
  </section>

  <section>
    <div class="strips" id="strips"></div>
  </section>

  <div id="catSections"></div>

  <section>
    <div class="sec-head"><h2>特集・ランキング</h2></div>
    <div class="feats" id="feats"></div>
  </section>

  <section>
    <div class="explain">
      <h3>このデモで起きていること</h3>
      <p>商品画像は 1 枚も差し替えていません。カインズ様のサイトから取得した原本 89 点をそのまま imgix Asset Manager にアップロードし、配信 URL に 2 つのパラメータを足しているだけです。</p>
      <div class="ex-grid">
        <div class="ex-card">
          <h4><em>1</em>ai-image-edit=packaging</h4>
          <p>袋・パウチのシワや折れ、箱・缶・瓶のへこみを均し、強すぎる影と露出を補正します。<b>バーコード・成分表示・ロゴなどの重要要素は保護</b>されるため、法令表示が崩れません。</p>
        </div>
        <div class="ex-card">
          <h4><em>2</em>ai-image-edit-analysis=true</h4>
          <p>本処理の前に軽量な解析が走り、<b>補正が必要な画像かどうかを自動判定</b>します。不要と判定された画像（家具・家電・バナーなど）は原本のまま配信され、フルクレジットを消費しません。全点に同じ URL を当てて良いのはこのためです。</p>
        </div>
        <div class="ex-card">
          <h4><em>3</em>運用上のインパクト</h4>
          <p>撮影・レタッチの外注工数をかけずに、既存カタログ全点の品質を底上げできます。原本は保持されるため、いつでもパラメータを外して元に戻せます。</p>
        </div>
      </div>
      <div class="urlbox" id="urlbox"></div>
    </div>
  </section>

</main>

<footer class="site">
  <div class="wrap">
    <div>imgix AI Image Edit — 検証用モックアップ</div>
    <div id="footdomain"></div>
  </div>
</footer>

<script>
const DATA = /*__DATA__*/null;
const BASE = "https://" + DATA.domain + "/" + DATA.folder + "/";
const AI = "ai-image-edit=packaging&ai-image-edit-analysis=true";

let aiOn = false;
const tracked = [];   // {el, kind}

function url(file, params, withAI){
  let q = params.slice();
  if (withAI) q.push(AI);
  return BASE + encodeURIComponent(file) + "?" + q.join("&");
}

/* imgix returns HTTP 423 while an AI render is in flight. The <img> fires
   `error`; retry the same URL with backoff until the render lands. */
function load(el, file, params, withAI, tries){
  tries = tries || 0;
  const box = el.closest(".ph");
  if (withAI && box) box.classList.add("loading");
  el.onerror = () => {
    /* Cold renders can take minutes. imgix answers 423 meanwhile, and the
       browser caches that error — so a plain retry just replays the cached
       failure. Revalidate the cache entry with fetch() before retrying. */
    if (tries < 40){
      setTimeout(() => {
        const u = url(file, params, withAI);
        fetch(u, {cache: "reload"})
          .catch(() => {})
          .then(() => load(el, file, params, withAI, tries + 1));
      }, Math.min(2000 + tries * 1200, 15000));
    } else if (box){
      box.classList.remove("loading");
    }
  };
  el.onload = () => { if (box) box.classList.remove("loading"); bump(el); };
  el.src = url(file, params, withAI);
}

/* count distinct elements, not load events — the hero carousel re-fires onload */
let loadedEls = new Set();
function bump(el){
  loadedEls.add(el);
  document.getElementById("stats").textContent =
    aiOn ? loadedEls.size + " / " + tracked.length + " 枚 配信済み"
         : tracked.length + " 枚";
}

function track(el, file, params){
  tracked.push({el, file, params});
}

function applyMode(){
  loadedEls = new Set();
  tracked.forEach(t => load(t.el, t.file, t.params, aiOn));
  document.getElementById("paramView").textContent = aiOn ? "?" + AI : "?（パラメータなし）";
  document.getElementById("btnOn").classList.toggle("on", aiOn);
  document.getElementById("btnOff").classList.toggle("on", !aiOn);
  document.querySelectorAll(".badge-ai").forEach(b => b.style.display = aiOn ? "" : "none");
  document.getElementById("stats").textContent =
    aiOn ? "0 / " + tracked.length + " 枚 配信済み" : tracked.length + " 枚";
}

/* ---------- build ---------- */
const P_CARD   = ["w=440","h=440","fit=fill","fill=solid","fill-color=white","auto=compress,format"];
const P_HERO   = ["w=1400","ar=4:1","fit=crop","auto=compress,format"];
const P_THUMB  = ["w=300","ar=4:1","fit=crop","auto=compress,format"];
const P_STRIP  = ["w=760","ar=4:1","fit=crop","auto=compress,format"];
const P_FEAT   = ["w=560","ar=2:1","fit=crop","auto=compress,format"];
const P_CMP    = ["w=700","h=700","fit=fill","fill=solid","fill-color=white","auto=compress,format"];

document.getElementById("logo").src = BASE + "cainz-logo.svg";
document.getElementById("footdomain").textContent = DATA.domain + "/" + DATA.folder + "/";

/* nav */
document.getElementById("navcats").innerHTML =
  DATA.catmeta.map(c => '<a href="#cat-' + c.k + '">' + c.t + "</a>").join("") +
  '<a href="#sec-compare">Before / After</a>';

/* hero */
const heroImg = document.getElementById("heroImg");
let heroIdx = 0;
document.getElementById("heroThumbs").innerHTML = DATA.banners.map((b, i) =>
  '<button type="button" data-i="' + i + '" class="' + (i ? "" : "on") + '"><img alt=""></button>').join("");
const thumbBtns = [...document.querySelectorAll(".hero-thumbs button")];
thumbBtns.forEach((btn, i) => {
  track(btn.querySelector("img"), DATA.banners[i].f, P_THUMB);
  btn.onclick = () => setHero(i);
});
function setHero(i){
  heroIdx = i;
  thumbBtns.forEach((b, j) => b.classList.toggle("on", i === j));
  heroImg.alt = DATA.banners[i].n;
  load(heroImg, DATA.banners[i].f, P_HERO, aiOn);
}
heroImg.alt = DATA.banners[0].n;
track(heroImg, DATA.banners[0].f, P_HERO);
setInterval(() => setHero((heroIdx + 1) % DATA.banners.length), 6000);

/* before/after sliders */
document.getElementById("cmpGrid").innerHTML = DATA.sliders.map((s, i) => `
  <div class="cmp">
    <div class="cmp-stage" data-i="${i}">
      <img class="cmp-before" alt="">
      <img class="cmp-after" alt="">
      <span class="cmp-tag l">原本</span>
      <span class="cmp-tag r">AI 補正</span>
      <div class="cmp-line"></div><div class="cmp-knob">⇄</div>
    </div>
    <div class="cmp-b"><h4>${s.n}</h4><p>${s.d}</p></div>
  </div>`).join("");

document.querySelectorAll(".cmp-stage").forEach(stage => {
  const s = DATA.sliders[+stage.dataset.i];
  const before = stage.querySelector(".cmp-before");
  const after  = stage.querySelector(".cmp-after");
  before.src = url(s.f, P_CMP, false);
  load(after, s.f, P_CMP, true);           // always AI, independent of the toggle
  const line = stage.querySelector(".cmp-line");
  const knob = stage.querySelector(".cmp-knob");
  const set = pct => {
    pct = Math.max(0, Math.min(100, pct));
    after.style.clipPath = "inset(0 0 0 " + pct + "%)";
    line.style.left = pct + "%"; knob.style.left = pct + "%";
  };
  const move = e => {
    const r = stage.getBoundingClientRect();
    const x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
    set(x / r.width * 100);
  };
  let down = false;
  stage.addEventListener("pointerdown", e => { down = true; stage.setPointerCapture(e.pointerId); move(e); });
  stage.addEventListener("pointermove", e => { if (down) move(e); });
  stage.addEventListener("pointerup",  () => { down = false; });
  stage.addEventListener("pointercancel", () => { down = false; });
});

/* strips */
document.getElementById("strips").innerHTML =
  DATA.strips.map(() => "<img alt=''>").join("");
document.querySelectorAll("#strips img").forEach((img, i) => {
  img.alt = DATA.strips[i].n; track(img, DATA.strips[i].f, P_STRIP);
});

/* category sections */
document.getElementById("catSections").innerHTML = DATA.catmeta.map(c => {
  const items = DATA.cats[c.k];
  const hot = c.k === "packaging";
  return `<section id="cat-${c.k}">
    <div class="sec-head">
      <h2>${c.t}</h2>
      ${hot ? '<span class="pill hot">効果が見えやすい</span>' : '<span class="pill">解析で自動判定</span>'}
      <p>${c.d}</p>
    </div>
    <div class="grid">
      ${items.map((it, i) => `
        <article class="card">
          <div class="ph" data-cat="${c.k}" data-i="${i}">
            <span class="badge-ai" style="display:none">AI 補正</span>
            ${it.t ? '<span class="tag">' + it.t + "</span>" : ""}
            <img alt="">
          </div>
          <div class="card-b">
            <div class="nm">${it.n}</div>
            <div class="stars">★★★★☆ <span>(${12 + ((i * 37) % 180)})</span></div>
            <div class="pr">${it.p}<small>税込</small></div>
          </div>
        </article>`).join("")}
    </div>
  </section>`;
}).join("");

document.querySelectorAll(".ph[data-cat]").forEach(ph => {
  const it = DATA.cats[ph.dataset.cat][+ph.dataset.i];
  const img = ph.querySelector("img");
  img.alt = it.n; track(img, it.f, P_CARD);
});

/* features */
document.getElementById("feats").innerHTML = DATA.features.map(f =>
  "<figure><img alt=''><figcaption>" + f.n + "</figcaption></figure>").join("");
document.querySelectorAll("#feats img").forEach((img, i) => {
  img.alt = DATA.features[i].n; track(img, DATA.features[i].f, P_FEAT);
});

/* url example */
document.getElementById("urlbox").innerHTML =
  '<span class="c">// 通常配信</span>\n' +
  "https://" + DATA.domain + "/" + DATA.folder + "/4549509981787_01.jpg" +
  '<span class="v">?w=440&amp;h=440&amp;fit=fill&amp;fill=solid&amp;fill-color=white&amp;auto=compress,format</span>\n\n' +
  '<span class="c">// AI 補正 ON（同じ原本・同じパス、末尾に 2 パラメータを追加するだけ）</span>\n' +
  "https://" + DATA.domain + "/" + DATA.folder + "/4549509981787_01.jpg" +
  '<span class="v">?w=440&amp;h=440&amp;fit=fill&amp;fill=solid&amp;fill-color=white&amp;auto=compress,format</span>' +
  '<span class="k">&amp;ai-image-edit=packaging&amp;ai-image-edit-analysis=true</span>';

/* toggle */
document.getElementById("btnOn").onclick  = () => { aiOn = true;  applyMode(); };
document.getElementById("btnOff").onclick = () => { aiOn = false; applyMode(); };

applyMode();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    out = os.path.join(HERE, "index.html")
    open(out, "w").write(render())
    print("wrote", out, os.path.getsize(out), "bytes ·", DOMAIN)
