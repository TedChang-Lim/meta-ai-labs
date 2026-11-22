#!/usr/bin/env python3
"""다모아(knot) 위키 링크 그래프 생성기.

wiki/*.md 를 읽어 [[링크]] 관계를 뽑고, 자기완결형 HTML(graph-knot.html)을 만든다.
정본은 .md 이고 이 HTML 은 사본이다 — 언제든 다시 만들면 된다.

사용:
    python3 scripts/build_graph.py            # 생성 + 통계
    python3 scripts/build_graph.py --check    # 통계만(파일 안 씀)
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

KNOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(KNOT, "wiki")
OUT = os.path.join(KNOT, "graph-knot.html")

LINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|([^\]]*))?\]\]")


def parse(path: str) -> dict:
    txt = open(path, encoding="utf-8", errors="replace").read()
    slug = os.path.splitext(os.path.basename(path))[0]

    typ = "note"
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    body = txt
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("type:"):
                typ = line.split(":", 1)[1].strip() or "note"
        body = txt[m.end():]

    title = slug
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    links = []
    for tgt, _label in LINK_RE.findall(body):
        tgt = tgt.strip()
        if tgt and tgt not in links and tgt != slug:
            links.append(tgt)
    return {"slug": slug, "title": title, "type": typ, "links": links}


def main() -> int:
    check_only = "--check" in sys.argv
    if not os.path.isdir(WIKI):
        print("wiki 폴더가 없습니다:", WIKI)
        return 1

    pages = [parse(os.path.join(WIKI, f)) for f in sorted(os.listdir(WIKI)) if f.endswith(".md")]
    known = {p["slug"] for p in pages}
    title_of = {p["slug"]: p["title"] for p in pages}

    edges, dangling = [], {}
    for p in pages:
        for tgt in p["links"]:
            if tgt in known:
                edges.append({"source": p["slug"], "target": tgt})
            else:
                dangling.setdefault(tgt, []).append(p["slug"])

    deg = {p["slug"]: 0 for p in pages}
    for e in edges:
        deg[e["source"]] = deg.get(e["source"], 0) + 1
        deg[e["target"]] = deg.get(e["target"], 0) + 1

    nodes = [{
        "id": p["slug"],
        "label": title_of[p["slug"]],
        "type": p["type"],
        "deg": deg.get(p["slug"], 0),
    } for p in pages]

    types: dict[str, int] = {}
    for p in pages:
        types[p["type"]] = types.get(p["type"], 0) + 1

    print(f"페이지 {len(pages)} · 연결 {len(edges)} · 끊어진 링크 {len(dangling)}")
    print("타입:", ", ".join(f"{k} {v}" for k, v in sorted(types.items(), key=lambda x: -x[1])))
    if dangling:
        for tgt, srcs in list(dangling.items())[:10]:
            print(f"  끊김: [[{tgt}]] ← {', '.join(srcs[:3])}")

    if check_only:
        return 0

    kst = timezone(timedelta(hours=9))
    payload = {
        "generated": datetime.now(kst).strftime("%Y-%m-%d %H:%M"),
        "nodes": nodes,
        "links": edges,
    }
    html = TEMPLATE.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("생성:", OUT, f"({os.path.getsize(OUT):,}B)")
    return 0


TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>다모아 — 지식 그래프</title>
<style>
  :root{
    --bg:#0b0d0c; --panel:#121614; --line:#252d28; --text:#eef2ef;
    --muted:#a9b2ac; --faint:#78827c; --gold:#c79a51;
    --c-source:#5b9dd9; --c-entity:#c79a51; --c-concept:#7fc8a9;
    --c-note:#ad8fe0; --c-domain:#e0765a;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;background:var(--bg);color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Pretendard",sans-serif;
    -webkit-font-smoothing:antialiased}
  #wrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;height:100%}
  @media (max-width:640px){#wrap{grid-template-columns:1fr;grid-template-rows:minmax(0,1fr) 240px}}
  #stage{position:relative;overflow:hidden}
  canvas{display:block;width:100%;height:100%;cursor:grab;touch-action:none}
  canvas.dragging{cursor:grabbing}
  .hud{position:absolute;left:0;top:0;padding:16px 20px;pointer-events:none}
  .hud h1{margin:0;font-size:13px;letter-spacing:.18em;color:var(--gold);font-weight:600}
  .hud p{margin:6px 0 0;font-size:11.5px;color:var(--faint)}
  .legend{position:absolute;left:20px;bottom:16px;display:flex;gap:16px;flex-wrap:wrap;
    font-size:11px;color:var(--muted);pointer-events:none}
  .legend i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;vertical-align:middle}
  .hint{position:absolute;right:20px;bottom:16px;font-size:10.5px;color:var(--faint);pointer-events:none}
  #side{border-left:1px solid var(--line);background:var(--panel);display:flex;flex-direction:column;min-height:0}
  #side h2{margin:0;padding:16px 18px 12px;font-size:10.5px;letter-spacing:.18em;
    color:var(--faint);border-bottom:1px solid var(--line);font-weight:600}
  #info{padding:16px 18px;font-size:12.5px;line-height:1.7;color:var(--muted);overflow:auto;flex:1}
  #info b{color:var(--text);font-weight:600;font-size:14px}
  #info .none{color:var(--faint);font-size:12px;line-height:1.7}
  #info ul{margin:10px 0 0;padding:0;list-style:none}
  #info li{padding:7px 9px;border:1px solid var(--line);border-radius:4px;margin-bottom:6px;
    font-size:12px;cursor:pointer;color:var(--muted)}
  #info li:hover{border-color:var(--gold);color:var(--gold)}
  #info .tag{display:inline-block;font-size:10px;letter-spacing:.12em;padding:2px 7px;
    border-radius:3px;background:#1c231e;color:var(--faint);margin-bottom:10px}
  #info .slug{margin-top:6px;font-size:10.5px;color:var(--faint);word-break:break-all}
  #foot{padding:10px 18px;border-top:1px solid var(--line);font-size:10px;color:var(--faint)}
  #search{width:100%;margin:12px 0 0;padding:8px 10px;background:#0e1210;border:1px solid var(--line);
    border-radius:4px;color:var(--text);font-size:12px;outline:none}
  #search:focus{border-color:var(--gold)}
  #tip{position:fixed;pointer-events:none;padding:5px 9px;background:#171d19;border:1px solid var(--line);
    border-radius:4px;font-size:11.5px;color:var(--text);opacity:0;transition:opacity .1s;max-width:280px;z-index:9}
</style>
</head>
<body>
<div id="wrap">
  <div id="stage">
    <canvas id="c"></canvas>
    <div class="hud">
      <h1>다모아 — 지식 그래프</h1>
      <p id="sub"></p>
    </div>
    <div class="legend" id="legend"></div>
    <div class="hint">휠 확대 · 끌어서 이동 · 점을 누르면 이웃</div>
  </div>
  <aside id="side">
    <h2>페이지</h2>
    <div id="info"></div>
    <div id="foot">knot/wiki 정본에서 자동 생성 · scripts/build_graph.py</div>
  </aside>
</div>
<div id="tip"></div>
<script>
const D = /*__DATA__*/;
const COLORS = {source:'#5b9dd9', entity:'#c79a51', concept:'#7fc8a9', note:'#ad8fe0', domain:'#e0765a'};
const NAMES  = {source:'자료', entity:'대상', concept:'개념', note:'기록', domain:'영역'};
const colorOf = t => COLORS[t] || '#8a8f8b';

const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const tip = document.getElementById('tip');
let W=0, H=0, DPR=Math.min(devicePixelRatio||1, 2);
const view = {x:0, y:0, k:1};

const nodes = D.nodes.map((n,i)=>{
  const a = (i / Math.max(1,D.nodes.length)) * Math.PI * 2;
  const rad = 300 * (0.55 + 0.45*Math.random());
  return {...n, x:Math.cos(a)*rad, y:Math.sin(a)*rad, vx:0, vy:0,
          r: 4.5 + Math.min(11, Math.sqrt(n.deg)*2.8)};
});
const byId = Object.fromEntries(nodes.map(n=>[n.id,n]));
const links = D.links.filter(l=>byId[l.source]&&byId[l.target]);
const nbr = Object.fromEntries(nodes.map(n=>[n.id,new Set()]));
links.forEach(l=>{ nbr[l.source].add(l.target); nbr[l.target].add(l.source); });

document.getElementById('sub').textContent =
  `페이지 ${D.nodes.length} · 연결 ${links.length} · ${D.generated} 생성`;
document.getElementById('legend').innerHTML =
  Object.keys(COLORS).filter(k=>D.nodes.some(n=>n.type===k))
    .map(k=>`<span><i style="background:${COLORS[k]}"></i>${NAMES[k]} <span style="color:var(--faint)">${k}</span></span>`)
    .join('') + '<span style="color:var(--faint)">점 크기 = 연결 수</span>';

function resize(){
  const r = cv.parentElement.getBoundingClientRect();
  W = r.width; H = r.height;
  cv.width = W*DPR; cv.height = H*DPR;
  ctx.setTransform(DPR,0,0,DPR,0,0);
}
addEventListener('resize', resize); resize();

let hover=null, picked=null, drag=null, panning=null;
let alpha = 1;

function tick(){
  for(let i=0;i<nodes.length;i++){
    const a=nodes[i];
    for(let j=i+1;j<nodes.length;j++){
      const b=nodes[j];
      const dx=b.x-a.x, dy=b.y-a.y, d2=dx*dx+dy*dy+0.01;
      if(d2>250000) continue;
      const d=Math.sqrt(d2), f=(2200*alpha)/d2;
      const fx=dx/d*f, fy=dy/d*f;
      a.vx-=fx; a.vy-=fy; b.vx+=fx; b.vy+=fy;
    }
  }
  links.forEach(l=>{
    const a=byId[l.source], b=byId[l.target];
    const dx=b.x-a.x, dy=b.y-a.y, d=Math.hypot(dx,dy)||0.01;
    const f=(d-165)*0.006*alpha;
    const fx=dx/d*f, fy=dy/d*f;
    a.vx+=fx; a.vy+=fy; b.vx-=fx; b.vy-=fy;
  });
  nodes.forEach(n=>{
    n.vx -= n.x*0.0009*alpha; n.vy -= n.y*0.0009*alpha;
    n.vx *= 0.87; n.vy *= 0.87;
    if(n!==drag){ n.x += n.vx; n.y += n.vy; }
  });
  alpha = Math.max(0.03, alpha*0.996);
}

ctx.font = '11.5px -apple-system, "Apple SD Gothic Neo", sans-serif';
function labelOf(n){
  return n.label.length>16 ? n.label.slice(0,15)+'…' : n.label;
}
function overlaps(a,b){
  return !(a.x+a.w < b.x || b.x+b.w < a.x || a.y+a.h < b.y || b.y+b.h < a.y);
}

function draw(){
  ctx.clearRect(0,0,W,H);
  ctx.save();
  ctx.translate(W/2 + view.x, H/2 + view.y);
  ctx.scale(view.k, view.k);

  const focus = picked || hover;
  const dim = focus ? new Set([focus, ...nbr[focus]]) : null;

  links.forEach(l=>{
    const a=byId[l.source], b=byId[l.target];
    const lit = !dim || (dim.has(l.source) && dim.has(l.target));
    ctx.strokeStyle = lit ? 'rgba(199,154,81,0.34)' : 'rgba(150,160,155,0.08)';
    ctx.lineWidth = (lit ? 1.15 : 0.6) / view.k;
    ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
  });

  nodes.forEach(n=>{
    const lit = !dim || dim.has(n.id);
    const isPick = n.id===picked, isHov = n.id===hover;
    const r = n.r * (isPick?1.5:isHov?1.28:1);
    ctx.beginPath(); ctx.arc(n.x,n.y,r,0,Math.PI*2);
    ctx.globalAlpha = lit ? 1 : 0.22;
    ctx.fillStyle = colorOf(n.type);
    ctx.fill();
    ctx.globalAlpha = 1;
    if(isPick){ ctx.strokeStyle='#fff'; ctx.lineWidth=1.6/view.k; ctx.stroke(); }
    else if(n.deg===0){ ctx.strokeStyle='rgba(255,255,255,0.22)'; ctx.lineWidth=1/view.k; ctx.stroke(); }
  });

  // 라벨 — 상위 + 선택/호버/이웃. 겹치면 건너뛴다.
  const TOPN = 14;
  const topSet = new Set([...nodes].sort((a,b)=>b.deg-a.deg).slice(0,TOPN).map(n=>n.id));
  const want = nodes
    .filter(n=> topSet.has(n.id) || n.id===picked || n.id===hover || (dim && dim.has(n.id)))
    .sort((a,b)=>(b.id===picked)-(a.id===picked) || b.deg-a.deg);
  const placed = [];
  ctx.textAlign='center'; ctx.textBaseline='top';
  want.forEach(n=>{
    const t = labelOf(n);
    const w = ctx.measureText(t).width;
    const rc = {t, x:n.x-w/2-3, y:n.y+n.r+3, w:w+6, h:15};
    if(placed.some(p=>overlaps(p,rc))) return;
    placed.push(rc);
    const lit = !dim || dim.has(n.id);
    ctx.lineWidth = 3.5/view.k; ctx.strokeStyle = 'rgba(11,13,12,0.9)';
    ctx.strokeText(t, n.x, rc.y);
    ctx.fillStyle = lit ? 'rgba(238,242,239,0.95)' : 'rgba(170,180,175,0.3)';
    ctx.fillText(t, n.x, rc.y);
  });
  ctx.restore();
}

let frames = 0, fitted = false;
function fitView(){
  if(!nodes.length) return;
  let minX=1e9,maxX=-1e9,minY=1e9,maxY=-1e9;
  nodes.forEach(n=>{
    minX=Math.min(minX,n.x); maxX=Math.max(maxX,n.x);
    minY=Math.min(minY,n.y); maxY=Math.max(maxY,n.y);
  });
  const pad = 70;
  const k = Math.min((W-pad*2)/Math.max(1,maxX-minX), (H-pad*2)/Math.max(1,maxY-minY), 1.7);
  view.k = Math.max(0.35, Math.min(3.5, k));
  view.x = -((minX+maxX)/2) * view.k;
  view.y = -((minY+maxY)/2) * view.k;
}
function loop(){
  tick(); draw();
  frames++;
  if(!fitted && frames>150){ fitView(); fitted=true; }
  requestAnimationFrame(loop);
}
loop();

// ---- 좌표·상호작용 ----
function toWorld(ev){
  const r = cv.getBoundingClientRect();
  const sx = ev.clientX - r.left, sy = ev.clientY - r.top;
  return { x:(sx - W/2 - view.x)/view.k, y:(sy - H/2 - view.y)/view.k };
}
function hit(p){
  let best=null, bd=1e9;
  nodes.forEach(n=>{
    const d = Math.hypot(n.x-p.x, n.y-p.y);
    if(d < Math.max(13, n.r+6) && d < bd){ bd=d; best=n; }
  });
  return best;
}
function renderInfo(){
  const box=document.getElementById('info');
  if(!picked){
    box.innerHTML='<div class="none">점을 누르면 이 페이지와 이어진 페이지가 나옵니다.</div>'
      + '<input id="search" placeholder="제목으로 찾기">';
    bindSearch(); return;
  }
  const n=byId[picked];
  const nb=[...nbr[picked]].map(id=>byId[id]).filter(Boolean).sort((a,b)=>b.deg-a.deg);
  box.innerHTML = `<span class="tag">${NAMES[n.type]||n.type} · ${n.type}</span><br><b>${n.label}</b>`
    + `<div class="slug">${n.id} · 이웃 ${nb.length}개</div>`
    + `<div style="margin-top:12px;font-size:12px">이어진 페이지 ${nb.length}개</div>`
    + (nb.length? '<ul>'+nb.map(x=>`<li data-id="${x.id}">${x.label}</li>`).join('')+'</ul>'
                : '<div class="none" style="margin-top:8px">아직 이어진 페이지가 없습니다(외톨이).</div>');
  box.querySelectorAll('li').forEach(li=>{
    li.onclick = ()=>{ picked=li.dataset.id; renderInfo(); };
  });
}
function bindSearch(){
  const inp=document.getElementById('search');
  if(!inp) return;
  inp.oninput = ()=>{
    const q = inp.value.trim().toLowerCase();
    if(!q) return;
    const f = nodes.find(n=>n.label.toLowerCase().includes(q) || n.id.includes(q));
    if(f){ picked=f.id; renderInfo(); }
  };
}

cv.addEventListener('wheel', ev=>{
  ev.preventDefault();
  const r = cv.getBoundingClientRect();
  const sx = ev.clientX - r.left - W/2, sy = ev.clientY - r.top - H/2;
  const k2 = Math.min(3.5, Math.max(0.35, view.k * (ev.deltaY<0?1.12:0.89)));
  view.x = sx - (sx - view.x) * (k2/view.k);
  view.y = sy - (sy - view.y) * (k2/view.k);
  view.k = k2;
}, {passive:false});

cv.addEventListener('mousemove', ev=>{
  if(panning){ view.x += ev.movementX; view.y += ev.movementY; return; }
  const p=toWorld(ev);
  if(drag){ drag.x=p.x; drag.y=p.y; drag.vx=0; drag.vy=0; alpha=Math.max(alpha,0.2); return; }
  const h=hit(p);
  hover = h?h.id:null;
  cv.style.cursor = h?'pointer':'grab';
  if(h){
    tip.textContent = `${h.label} · 이웃 ${nbr[h.id].size}개`;
    tip.style.opacity=1;
    tip.style.left=(ev.clientX+14)+'px'; tip.style.top=(ev.clientY+14)+'px';
  } else tip.style.opacity=0;
});
cv.addEventListener('mousedown', ev=>{
  if(ev.button!==0) return;
  const h=hit(toWorld(ev));
  if(h){ drag=h; }
  else { panning={x:ev.clientX,y:ev.clientY}; }
  cv.classList.add('dragging');
});
addEventListener('mouseup', ()=>{ drag=null; panning=null; cv.classList.remove('dragging'); });
cv.addEventListener('mouseleave', ()=>{ tip.style.opacity=0; });
cv.addEventListener('click', ev=>{
  const h=hit(toWorld(ev));
  picked = h && h.id!==picked ? h.id : null;
  renderInfo();
});

// 시작 시 연결이 가장 많은 페이지를 골라 둔다 — 빈 패널 방지
const top0 = [...nodes].sort((a,b)=>b.deg-a.deg)[0];
if(top0) picked = top0.id;
renderInfo();
bindSearch();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    raise SystemExit(main())
