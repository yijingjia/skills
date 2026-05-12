#!/usr/bin/env python3
"""
markdown-to-image renderer — Markdown -> XHS card PNGs via Playwright
Usage: python render.py <file.md> [--theme light|dark|warm|forest]
"""
import sys, re, json, argparse, tempfile, os
from pathlib import Path

THEMES = {
    "light":  {"bg":"#ffffff","text":"#1a1a1a","hl":"#1e6fe8","codeBg":"#f5f5f5","codeText":"#333333","icBg":"#f0f0f0","icText":"#c44444"},
    "dark":   {"bg":"#1a1a2e","text":"#e8e8f0","hl":"#7eb8ff","codeBg":"#0d0d1e","codeText":"#a8d8a8","icBg":"#0d0d1e","icText":"#ff9e9e"},
    "warm":   {"bg":"#fdf8f0","text":"#2d2016","hl":"#c44a1e","codeBg":"#ede8df","codeText":"#3d2e1a","icBg":"#ede8df","icText":"#8b3a1a"},
    "forest": {"bg":"#ffffff","text":"#1a1a1a","hl":"#2a7a50","codeBg":"#f2f7f4","codeText":"#1a3d2a","icBg":"#eaf4ee","icText":"#1a6640"},
}
CARD_W, CARD_H = 270, 360
PAD_V, PAD_H_CARD, PAD_BOT = 22, 20, 16
MAX_BODY_H = CARD_H - PAD_V - PAD_BOT - 8
COVER_IMG_MAX_H = 150  # 封面图最大高度，留出正文空间
BODY_IMG_MAX_H  = 200  # 正文页图片最大高度，防止高图撑爆卡片
COVER_IMG_STYLE = f'max-width:100%;max-height:{COVER_IMG_MAX_H}px;width:auto;height:auto;border-radius:6px;margin:0 auto 9px;display:block'
BODY_IMG_STYLE  = f'max-width:100%;max-height:{BODY_IMG_MAX_H}px;width:auto;height:auto;border-radius:4px;margin-bottom:10px;display:block'
FONTS = {
    "sans": {
        "stack":        '-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif',
        "szTitle":"20px","szH1":"14px","szH2":"12px","szH3":"11px","szBody":"8px","szCode":"8.5px",
        "wTitle":400,"wH1":400,"wH2":400,"wH3":400,"wBody":300,"wHl":300,"wCode":200,"wTh":400,
    },
    "serif": {
        "stack":        '"Source Han Serif SC","思源宋体","Noto Serif CJK SC","STSong","SimSun",serif',
        "szTitle":"22px","szH1":"14px","szH2":"12px","szH3":"8.5px","szBody":"8.5px","szCode":"8.5px",
        "wTitle":600,"wH1":600,"wH2":600,"wH3":700,"wBody":400,"wHl":400,"wCode":300,"wTh":500,
    },
}

# ── Parser ───────────────────────────────────────────────────────────────────
def parse_md(text):
    lines = text.split("\n"); nodes = []; i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m: nodes.append({"type":f"h{len(m.group(1))}","text":m.group(2)}); i+=1; continue
        if line.startswith("```"):
            code=[]; i+=1
            while i<len(lines) and not lines[i].startswith("```"): code.append(lines[i]); i+=1
            nodes.append({"type":"code","text":"\n".join(code)}); i+=1; continue
        if "|" in line and i+1<len(lines) and re.match(r'^[\s|:-]+$',lines[i+1]):
            headers=[c.strip() for c in line.split("|") if c.strip()]; i+=2; rows=[]
            while i<len(lines) and "|" in lines[i]: rows.append([c.strip() for c in lines[i].split("|") if c.strip()]); i+=1
            nodes.append({"type":"table","headers":headers,"rows":rows}); continue
        if line.startswith("> "):
            bq=line[2:]
            while i+1<len(lines) and lines[i+1].startswith("> "): i+=1; bq+=" "+lines[i][2:]
            nodes.append({"type":"bq","text":bq}); i+=1; continue
        if re.match(r'^[-*]{3,}$',line.strip()): nodes.append({"type":"hr"}); i+=1; continue
        if re.match(r'^[-*+]\s',line):
            items=[]
            while i<len(lines):
                mm=re.match(r'^[-*+]\s+(.*)',lines[i])
                ms=re.match(r'^[ \t]+[-*+]\s+(.*)',lines[i])
                if mm: items.append({"text":mm.group(1),"sub":[]}); i+=1
                elif ms and items: items[-1]["sub"].append(ms.group(1)); i+=1
                else: break
            nodes.append({"type":"ul","items":items}); continue
        if re.match(r'^\d+\.\s',line):
            items=[]
            while i<len(lines):
                if re.match(r'^\d+\.\s',lines[i]):
                    items.append(re.sub(r'^\d+\.\s','',lines[i]).strip()); i+=1
                    while i<len(lines) and re.match(r'^[ \t]+\S',lines[i]): items[-1]+=" "+lines[i].strip(); i+=1
                else: break
            nodes.append({"type":"ol","items":items}); continue
        m=re.match(r'^!\[\[([^\]]+)\]\]',line)
        if m: nodes.append({"type":"img","alt":m.group(1),"src":m.group(1)}); i+=1; continue
        m=re.match(r'^!\[([^\]]*)\]\(([^)]+)\)',line)
        if m: nodes.append({"type":"img","alt":m.group(1),"src":m.group(2)}); i+=1; continue
        if line.strip(): nodes.append({"type":"p","text":line.strip()})
        i+=1
    return nodes

# ── Shared JS (injected into every page via <script>) ────────────────────────
NODE_HTML_JS = """
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function inline(text,th){
  text=esc(text);
  text=text.replace(/\\*\\*(.+?)\\*\\*/g,'<span style="color:'+th.hl+';font-weight:'+th.wHl+'">$1</span>');
  text=text.replace(/\\*(.+?)\\*/g,'<em style="font-style:italic">$1</em>');
  text=text.replace(/`([^`]+)`/g,'<code style="font-family:inherit;font-size:'+th.szCode+';font-weight:'+th.wCode+';padding:1px 4px;border-radius:3px;background:'+th.icBg+';color:'+th.text+'">$1</code>');
  text=text.replace(/\\[([^\\]]+)\\]\\([^)]+\\)/g,'<span style="color:'+th.hl+'">$1</span>');
  return text;
}
function codeFont(t){var l=t.split('\\n'),mx=0;for(var i=0;i<l.length;i++)if(l[i].length>mx)mx=l[i].length;if(mx>50||l.length>12)return'6.5px';if(mx>35||l.length>8)return'7px';return'8px';}
function tableFont(h,r){var c=h.length,all=h.concat([].concat.apply([],r)),mx=0;for(var i=0;i<all.length;i++)if(all[i].length>mx)mx=all[i].length;if(c>=4||mx>20)return'6.5px';if(c>=3||mx>14)return'7px';return'8px';}
var LH='1.55';var LH_LIST='1.55';
function nodeHtml(node,th){
  var t=node.type;
  if(t==='h1')return'<div style="font-size:'+th.szH1+';font-weight:'+th.wH1+';line-height:1.3;margin-bottom:2px;margin-top:14px;color:'+th.hl+'">'+inline(node.text,th)+'</div>';
  if(t==='h2')return'<div style="font-size:'+th.szH2+';font-weight:'+th.wH2+';line-height:1.3;margin-bottom:2px;margin-top:14px;color:'+th.text+'">'+inline(node.text,th)+'</div>';
  if(t==='h3')return'<div style="font-size:'+th.szH3+';font-weight:'+th.wH3+';line-height:1.3;margin-bottom:2px;margin-top:14px;color:'+th.text+'">'+inline(node.text,th)+'</div>';
  if(t==='p')return'<div style="font-size:'+th.szBody+';font-weight:'+th.wBody+';line-height:'+LH+';margin-bottom:10px;color:'+th.text+'">'+inline(node.text,th)+'</div>';
  if(t==='bq')return'<div style="border-left:3px solid '+th.hl+';padding:4px 8px;margin-bottom:10px;font-size:'+th.szBody+';font-weight:'+th.wBody+';line-height:'+LH+';font-style:italic;color:'+th.text+';opacity:.8">'+inline(node.text,th)+'</div>';
  if(t==='hr')return'<div style="border-top:0.5px solid '+th.text+';opacity:.2;margin:8px 0"></div>';
  if(t==='code'){var fs=codeFont(node.text);return'<pre style="font-family:monospace;font-size:'+fs+';line-height:1.55;padding:7px 9px;border-radius:4px;margin-bottom:10px;background:'+th.codeBg+';color:'+th.codeText+';white-space:pre-wrap;word-break:break-all">'+esc(node.text)+'</pre>';}
  if(t==='img'){var mh=node.maxH||th.bodyImgMaxH;return'<img src="'+node.src+'" alt="'+(node.alt||'')+'" style="max-width:100%;max-height:'+mh+'px;width:auto;height:auto;border-radius:4px;margin:0 auto 10px;display:block">';}
  if(t==='ul'){var s='<div style="margin-bottom:10px">';for(var i=0;i<node.items.length;i++){var item=node.items[i];var txt=typeof item==='string'?item:item.text;var sub=typeof item==='object'&&item.sub?item.sub:[];var inner='<div>'+inline(txt,th);if(sub.length>0){inner+='<div style="margin-top:2px">';for(var j=0;j<sub.length;j++)inner+='<div style="font-size:'+th.szBody+';font-weight:'+th.wBody+';line-height:'+LH_LIST+';display:flex;gap:4px;align-items:flex-start;color:'+th.text+'"><div style="flex-shrink:0;margin-top:5px;width:2px;height:2px;border-radius:50%;background:'+th.hl+';opacity:.7"></div><div>'+inline(sub[j],th)+'</div></div>';inner+='</div>';}inner+='</div>';s+='<div style="font-size:'+th.szBody+';font-weight:'+th.wBody+';line-height:'+LH_LIST+';display:flex;gap:5px;align-items:flex-start;color:'+th.text+'"><div style="flex-shrink:0;margin-top:6px;width:3px;height:3px;border-radius:50%;background:'+th.hl+'"></div>'+inner+'</div>';}return s+'</div>';}
  if(t==='ol'){var s='<div style="margin-bottom:10px">';for(var i=0;i<node.items.length;i++)s+='<div style="font-size:'+th.szBody+';font-weight:'+th.wBody+';line-height:'+LH_LIST+';display:flex;gap:3px;color:'+th.text+'"><div style="flex-shrink:0;font-size:'+th.szBody+';color:'+th.hl+';white-space:nowrap">'+(i+1)+'.</div><div>'+inline(node.items[i],th)+'</div></div>';return s+'</div>';}
  if(t==='table'){var fs=tableFont(node.headers,node.rows),pv=fs==='6.5px'?'3px':'4px',ph=fs==='6.5px'?'4px':'5px';var ths='';for(var i=0;i<node.headers.length;i++)ths+='<th style="font-weight:'+th.wTh+';padding:'+pv+' '+ph+';border-bottom:1.5px solid '+th.hl+';text-align:left;color:'+th.text+';word-break:break-all;line-height:1.4">'+inline(node.headers[i],th)+'</th>';var trs='';for(var i=0;i<node.rows.length;i++){trs+='<tr>';for(var j=0;j<node.rows[i].length;j++)trs+='<td style="padding:'+pv+' '+ph+';border-bottom:0.5px solid '+th.text+';opacity:.8;line-height:1.4;color:'+th.text+';word-break:break-all">'+inline(node.rows[i][j],th)+'</td>';trs+='</tr>';}return'<table style="width:100%;border-collapse:collapse;font-size:'+fs+';margin-bottom:10px;table-layout:fixed"><thead><tr>'+ths+'</tr></thead><tbody>'+trs+'</tbody></table>';}
  return'';
}
function measureNodes(nodes,th){var box=document.createElement('div');box.style.cssText='position:absolute;left:-9999px;top:0;width:230px;display:flex;flex-direction:column';document.body.appendChild(box);var r=[];for(var i=0;i<nodes.length;i++){var ph=box.scrollHeight;var w=document.createElement('div');w.innerHTML=nodeHtml(nodes[i],th);var child=w.firstElementChild||w;box.appendChild(child);box.offsetHeight;r.push(box.scrollHeight-ph);}box.remove();return r;}
function measureText(html){var d=document.createElement('div');d.style.cssText='position:absolute;left:-9999px;width:230px';d.innerHTML=html;document.body.appendChild(d);var h=d.offsetHeight;d.remove();return h;}
async function measureTextAsync(html){var d=document.createElement('div');d.style.cssText='position:absolute;left:-9999px;width:230px';d.innerHTML=html;document.body.appendChild(d);var imgs=d.querySelectorAll('img');await Promise.all(Array.from(imgs).map(function(img){if(img.complete)return Promise.resolve();return new Promise(function(res){img.onload=res;img.onerror=res;});}));var h=d.offsetHeight;d.remove();return h;}
"""

def load_js_on_page(page):
    """Inject NODE_HTML_JS into the page via addScriptTag."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(NODE_HTML_JS)
        tmp = f.name
    page.add_script_tag(path=tmp)
    os.unlink(tmp)

# ── Measure & paginate ───────────────────────────────────────────────────────
def measure_nodes(nodes, th, page):
    if not nodes: return []
    return page.evaluate("([nodes,th]) => measureNodes(nodes,th)", [nodes, th])

def measure_text_h(html, page):
    return page.evaluate("(html) => measureText(html)", html)

SPLIT_PUNCT = "。！？；，：、.!?;,:"

def measure_p_h(text, th, page):
    """Measure a paragraph node's rendered height."""
    return page.evaluate("([nodes,th]) => measureNodes(nodes,th)", [[{"type":"p","text":text}], th])[0]

def split_paragraph(text, avail_h, th, page):
    """
    Split a paragraph so its rendered height ≤ avail_h.
    Returns (head, tail) where head fits, tail is the rest.
    If even 1 char overflows, returns ("", text) — caller should push entire paragraph forward.
    Prefers to split at Chinese/Western punctuation.
    """
    if not text: return ("", "")
    full_h = measure_p_h(text, th, page)
    if full_h <= avail_h: return (text, "")
    lo, hi = 0, len(text)
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid == 0: lo = mid + 1; continue
        h = measure_p_h(text[:mid], th, page)
        if h <= avail_h:
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    if best == 0: return ("", text)
    # Try to back up to nearest punctuation for cleaner split
    cut = best
    for j in range(best - 1, max(best - 30, 0) - 1, -1):
        if text[j] in SPLIT_PUNCT:
            cut = j + 1; break
    return (text[:cut], text[cut:])

def paginate(nodes, th, page):
    remaining = list(nodes)
    title_node = img_node = None
    for i,n in enumerate(remaining):
        if not title_node and n["type"]=="h1": title_node=n; remaining.pop(i); break
    # 只有图片紧跟在标题后（中间没有正文段落/标题）才提升为封面图
    for i,n in enumerate(remaining):
        if n["type"] in ("p", "h2", "h3"): break
        if n["type"] == "img": img_node=n; remaining.pop(i); break

    fixed_h = PAD_V + PAD_BOT + 5
    if title_node:
        fixed_h += measure_text_h(f'<div style="font-size:{th["szTitle"]};font-weight:{th["wTitle"]};line-height:1.25;margin-bottom:10px">{title_node["text"]}</div>', page)
    if img_node:
        img_h = page.evaluate("(html) => measureTextAsync(html)", f'<img src="{img_node["src"]}" style="{COVER_IMG_STYLE}">')
        fixed_h += img_h

    heights = measure_nodes(remaining, th, page)
    cover_body=[]; used_h=fixed_h; overflow_start=len(remaining)
    for i,(n,nh) in enumerate(zip(remaining,heights)):
        if n["type"] == "img":
            avail = MAX_BODY_H - used_h
            img_max = min(BODY_IMG_MAX_H, int(avail) - 10) if avail >= 30 else BODY_IMG_MAX_H
            # 用 maxH 直接作为图片占高（不依赖 measure_nodes，因为临时 html 已被删除）
            estimated_h = img_max + 10  # +10 for margin-bottom
            if used_h + estimated_h <= MAX_BODY_H:
                cover_body.append(dict(n, maxH=img_max)); used_h += estimated_h
            else:
                overflow_start = i
                break
            continue
        if used_h+nh<=MAX_BODY_H:
            cover_body.append(n); used_h+=nh
        else:
            # Try to split a paragraph
            if n["type"]=="p":
                avail = MAX_BODY_H - used_h
                head, tail = split_paragraph(n["text"], avail, th, page)
                if head:
                    cover_body.append({"type":"p","text":head})
                    remaining[i] = {"type":"p","text":tail}
                    overflow_start = i
                else:
                    overflow_start = i
            else:
                overflow_start = i
            break

    overflow = remaining[overflow_start:]
    pages=[{"type":"cover","titleNode":title_node,"imgNode":img_node,"bodyNodes":cover_body}]
    # Content pages with paragraph splitting
    idx = 0
    while idx < len(overflow):
        cur, h = [], 0
        while idx < len(overflow):
            n = overflow[idx]
            if n["type"] == "img":
                # 用 maxH 直接估算图片占高，不依赖 measure_nodes
                avail = MAX_BODY_H - h
                img_max = min(BODY_IMG_MAX_H, int(avail) - 10) if avail >= 30 else BODY_IMG_MAX_H
                estimated_h = img_max + 10
                capped = dict(n, maxH=img_max)
                if h + estimated_h <= MAX_BODY_H:
                    cur.append(capped); h += estimated_h; idx += 1
                elif not cur:
                    cur.append(capped); idx += 1
                break
            nh = measure_nodes([n], th, page)[0]
            if h + nh <= MAX_BODY_H:
                cur.append(n); h += nh; idx += 1
            elif n["type"] == "p" and cur:
                avail = MAX_BODY_H - h
                head, tail = split_paragraph(n["text"], avail, th, page)
                if head:
                    cur.append({"type":"p","text":head})
                    overflow[idx] = {"type":"p","text":tail}
                break
            elif not cur:
                # Single node taller than page, force-include it
                cur.append(n); idx += 1; break
            else:
                break
        if cur: pages.append({"type":"content","nodes":cur})
    return pages

# ── Card HTML builder ─────────────────────────────────────────────────────────
def build_card_html(pg, idx, total, th, base_style):
    pg_num = f'<div style="position:absolute;bottom:12px;right:16px;font-size:9px;opacity:.35;color:{th["text"]}">{idx+1} / {total}</div>'
    deco   = f'<div style="position:absolute;right:-20px;bottom:-20px;width:90px;height:90px;border-radius:50%;background:{th["hl"]};opacity:.07"></div>'
    nodes_for_render = []

    if pg["type"] == "cover":
        tn=pg.get("titleNode"); img=pg.get("imgNode"); body=pg.get("bodyNodes",[])
        static=""
        if tn: static+=f'<div style="font-size:{th["szTitle"]};font-weight:{th["wTitle"]};line-height:1.25;margin-bottom:10px;color:{th["text"]}">{tn["text"]}</div>'
        if img: static+=f'<img src="{img["src"]}" style="{COVER_IMG_STYLE}">'
        nodes_for_render = body
        cstyle=f'box-sizing:border-box;width:100%;height:100%;display:flex;flex-direction:column;padding:{PAD_V}px {PAD_H_CARD}px {PAD_BOT}px;position:relative;background:{th["bg"]};overflow:hidden'
    else:
        static=""; nodes_for_render=pg["nodes"]
        cstyle=f'box-sizing:border-box;width:100%;height:100%;padding:{PAD_V}px {PAD_H_CARD}px {PAD_BOT}px;display:flex;flex-direction:column;overflow:hidden;position:relative;background:{th["bg"]}'

    nodes_json=json.dumps(nodes_for_render,ensure_ascii=False)
    th_json=json.dumps(th,ensure_ascii=False)

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{base_style} html,body{{width:{CARD_W}px;height:{CARD_H}px;overflow:hidden;}}</style>
</head><body>
<div style="width:{CARD_W}px;height:{CARD_H}px;border-radius:8px;overflow:hidden;background:{th['bg']}">
  <div style="{cstyle}">
    {static}<div id="body"></div>{deco}{pg_num}
  </div>
</div>
<script>{NODE_HTML_JS}
(function(){{var nodes={nodes_json};var th={th_json};var c=document.getElementById('body');
for(var i=0;i<nodes.length;i++){{var w=document.createElement('div');w.innerHTML=nodeHtml(nodes[i],th);while(w.firstChild)c.appendChild(w.firstChild);}}}})();
</script>
</body></html>"""

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--theme",default="light",choices=list(THEMES.keys()))
    parser.add_argument("--font",default="sans",choices=list(FONTS.keys()))
    parser.add_argument("--scale",default=4,type=int,help="device scale factor, default 4 (1080x1440px)")
    args=parser.parse_args()
    md_path=Path(args.file)
    if not md_path.exists(): print(f"❌ 文件不存在: {md_path}"); sys.exit(1)

    font_cfg=FONTS[args.font]
    font_stack=font_cfg["stack"]
    th={**THEMES[args.theme], **{k:v for k,v in font_cfg.items() if k!="stack"}, "fontStack":font_stack, "bodyImgMaxH":BODY_IMG_MAX_H}
    base_style=f'*{{box-sizing:border-box;margin:0;padding:0;}}body{{font-family:{font_stack};}}'
    nodes=parse_md(md_path.read_text(encoding="utf-8"))
    print(f"📄 {md_path.name}  ({len(nodes)} 节点)  主题: {args.theme}  字体: {args.font}  缩放: {args.scale}x")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 请先运行: python markdown-to-image/setup.py"); sys.exit(1)

    with sync_playwright() as pw:
        browser=pw.chromium.launch()

        # measure page — use file:// so relative images load correctly
        content_w = CARD_W - 2 * PAD_H_CARD
        measure_html=f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{base_style} body{{width:{content_w}px}}</style></head><body></body></html>'
        tmp_measure=md_path.parent/f"._tmp_measure.html"
        tmp_measure.write_text(measure_html,encoding="utf-8")
        mp=browser.new_page(viewport={"width":content_w,"height":600})
        mp.goto(f"file://{tmp_measure.resolve()}")
        mp.wait_for_load_state("networkidle")
        load_js_on_page(mp)
        tmp_measure.unlink()
        print("📐 测量节点高度...")
        pages=paginate(nodes,th,mp)
        mp.close()
        print(f"📦 共 {len(pages)} 张卡片，开始渲染...")

        # render page
        rp=browser.new_page(viewport={"width":CARD_W,"height":CARD_H},device_scale_factor=args.scale)
        for i,pg in enumerate(pages):
            html=build_card_html(pg,i,len(pages),th,base_style)
            tmp_html=md_path.parent/f"._tmp_card_{i}.html"
            tmp_html.write_text(html,encoding="utf-8")
            rp.goto(f"file://{tmp_html.resolve()}")
            rp.wait_for_load_state("networkidle")
            out=md_path.parent/f"{md_path.stem}_{i+1:02d}_{args.theme}_{args.font}.png"
            rp.screenshot(path=str(out),full_page=False)
            tmp_html.unlink()
            print(f"  ✅ {i+1}/{len(pages)} → {out.name}")

        rp.close(); browser.close()
    print(f"\n🎉 完成！已保存到 {md_path.parent}/")

if __name__=="__main__":
    main()
