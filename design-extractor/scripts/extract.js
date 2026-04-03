/**
 * Design Extractor — Playwright 自动化脚本
 * 用法: node extract.js <URL> [输出目录]
 * 示例: node extract.js https://example.com ./design-extractor
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const url = process.argv[2];
const outputDir = process.argv[3] || './design-extractor';

if (!url) {
  console.error('请提供目标网站 URL\n用法: node extract.js <URL> [输出目录]');
  process.exit(1);
}

async function extract() {
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(outputDir, 'screenshots'), { recursive: true });

  console.log(`\n🚀 启动浏览器，目标: ${url}\n`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
  });
  const page = await context.newPage();

  // ── 1. 加载页面 ────────────────────────────────────────
  console.log('📄 加载页面...');
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  // ── 2. 截图：首屏（导航初始/透明状态） ────────────────
  console.log('📸 截图：首屏');
  await page.screenshot({
    path: path.join(outputDir, 'screenshots', '01-hero.png'),
    fullPage: false
  });

  // 导航单独截图（初始状态）
  const navEl = await page.$('header, nav, [class*="header"], [class*="navbar"]');
  if (navEl) {
    await navEl.screenshot({
      path: path.join(outputDir, 'screenshots', '02-nav-initial.png')
    });
  }

  // ── 3. 滚动触发 sticky 导航 ────────────────────────────
  console.log('📸 截图：sticky 导航');
  await page.evaluate(() => window.scrollTo(0, 300));
  await page.waitForTimeout(600);
  await page.screenshot({
    path: path.join(outputDir, 'screenshots', '03-nav-sticky.png'),
    fullPage: false
  });
  const navSticky = await page.$('header, nav, [class*="header"], [class*="navbar"]');
  if (navSticky) {
    await navSticky.screenshot({
      path: path.join(outputDir, 'screenshots', '04-nav-sticky-close.png')
    });
  }

  // ── 4. 截图：中段 / 底部 ───────────────────────────────
  console.log('📸 截图：中段 / 底部');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outputDir, 'screenshots', '05-mid.png'), fullPage: false });

  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(outputDir, 'screenshots', '06-footer.png'), fullPage: false });

  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);

  // ── 5. 截图：hover 状态 ────────────────────────────────
  console.log('📸 截图：hover 状态');
  try {
    for (const sel of ['nav a', 'button', '[class*="btn"]', '[class*="card"]', 'a']) {
      const el = await page.$(sel);
      if (el) {
        const isVisible = await el.isVisible();
        if (isVisible) {
          await el.hover();
          await page.waitForTimeout(300);
          await page.screenshot({ path: path.join(outputDir, 'screenshots', '07-hover.png'), fullPage: false });
          break;
        }
      }
    }
  } catch (err) {
    console.log('⚠️  Hover 截图跳过（元素不可见或超时）');
  }

  // ── 6. 全页截图 ────────────────────────────────────────
  await page.screenshot({ path: path.join(outputDir, 'screenshots', '08-fullpage.png'), fullPage: true });

  // ── 7. CSS 变量 ────────────────────────────────────────
  console.log('🎨 提取 CSS 变量...');
  const cssVars = await page.evaluate(() => {
    const vars = {};
    const root = getComputedStyle(document.documentElement);
    [...document.styleSheets]
      .flatMap(s => { try { return [...s.cssRules] } catch { return [] } })
      .flatMap(r => r.cssText.match(/--[\w-]+/g) || [])
      .forEach(v => { vars[v] = root.getPropertyValue(v).trim(); });
    return vars;
  });

  // ── 8. 设计相关 CSS 规则 ───────────────────────────────
  console.log('📋 提取 CSS 规则...');
  const cssRules = await page.evaluate(() => {
    return [...document.styleSheets]
      .flatMap(s => { try { return [...s.cssRules] } catch { return [] } })
      .map(r => r.cssText)
      .filter(text =>
        text.includes('--') ||
        /color|font|spacing|radius|shadow|transition|animation|@keyframes|transform|opacity|backdrop/i.test(text)
      )
      .join('\n');
  });

  // ── 9. @keyframes ─────────────────────────────────────
  console.log('🎬 提取 @keyframes...');
  const keyframes = await page.evaluate(() => {
    return [...document.styleSheets]
      .flatMap(s => { try { return [...s.cssRules] } catch { return [] } })
      .filter(r => r.type === CSSRule.KEYFRAMES_RULE || r.cssText?.startsWith('@keyframes'))
      .map(r => r.cssText)
      .join('\n\n');
  });

  // ── 10. Transition 汇总 ────────────────────────────────
  const transitions = await page.evaluate(() => {
    const result = [];
    [...document.styleSheets]
      .flatMap(s => { try { return [...s.cssRules] } catch { return [] } })
      .forEach(r => {
        if (r.cssText && /transition|animation/.test(r.cssText)) {
          const match = r.cssText.match(/(transition|animation)[^;{]+/g);
          if (match) result.push(...match);
        }
      });
    return [...new Set(result)];
  });

  // ── 11. 字体检测 ──────────────────────────────────────
  console.log('🔤 检测字体...');
  const fonts = await page.evaluate(() => {
    const fontFaces = [];
    [...document.styleSheets].forEach(s => {
      try {
        [...s.cssRules].forEach(r => {
          if (r.type === CSSRule.FONT_FACE_RULE) {
            fontFaces.push({
              family: r.style.getPropertyValue('font-family').replace(/['"]/g, '').trim(),
              src: r.style.getPropertyValue('src'),
              weight: r.style.getPropertyValue('font-weight'),
              style: r.style.getPropertyValue('font-style'),
            });
          }
        });
      } catch {}
    });

    // 收集页面实际用到的 font-family
    const usedFamilies = new Set();
    document.querySelectorAll('*').forEach(el => {
      const ff = getComputedStyle(el).fontFamily;
      if (ff) usedFamilies.add(ff);
    });

    return { fontFaces, usedFamilies: [...usedFamilies].slice(0, 20) };
  });

  const googleFontsUrls = await page.evaluate(() =>
    [...document.querySelectorAll('link[href*="fonts.googleapis.com"]')].map(el => el.href)
  );

  // ── 12. 检测动效库（修复 $.Velocity bug） ─────────────
  console.log('🔍 检测动效库...');
  const animLibs = await page.evaluate(() => ({
    gsap:         typeof window.gsap !== 'undefined' || typeof window.GSAP !== 'undefined',
    lottie:       typeof window.lottie !== 'undefined' || document.querySelector('[data-lottie]') !== null,
    framerMotion: typeof window.Motion !== 'undefined' || typeof window.framerMotion !== 'undefined',
    animejs:      typeof window.anime !== 'undefined',
    velocity:     typeof window.Velocity !== 'undefined' || (typeof window.$ !== 'undefined' && typeof window.$.Velocity !== 'undefined'),
    threejs:      typeof window.THREE !== 'undefined',
    particles:    typeof window.particlesJS !== 'undefined' || typeof window.tsParticles !== 'undefined',
  }));

  // ── 13. 组件提取（含 sticky/fixed 专项扫描） ──────────
  console.log('🧩 提取组件...');
  const components = await page.evaluate(() => {
    const targets = {
      header:    ['header', 'nav', '[class*="header"]', '[class*="navbar"]', '[class*="nav-"]'],
      footer:    ['footer', '[class*="footer"]'],
      hero:      ['[class*="hero"]', '[class*="banner"]', 'main > section:first-child'],
      card:      ['[class*="card"]', '[class*="tile"]'],
      modal:     ['[class*="modal"]', '[class*="dialog"]', '[role="dialog"]'],
      dropdown:  ['[class*="dropdown"]', '[class*="popover"]'],
      tabs:      ['[class*="tab"]', '[role="tablist"]'],
      accordion: ['details', '[class*="accordion"]'],
      form:      ['form'],
      button:    ['button', '[class*="btn"]', '[class*="button"]'],
      badge:     ['[class*="badge"]', '[class*="tag"]', '[class*="chip"]'],
      toast:     ['[class*="toast"]', '[class*="notification"]', '[class*="alert"]'],
    };

    // 专项：sticky / fixed 元素（捕获悬浮导航等）
    const stickyElements = [...document.querySelectorAll('*')]
      .filter(el => ['sticky', 'fixed'].includes(getComputedStyle(el).position))
      .map(el => ({
        tag: el.tagName.toLowerCase(),
        className: el.className,
        position: getComputedStyle(el).position,
        html: el.outerHTML.slice(0, 2000),
      }));

    const result = { stickyElements };

    Object.entries(targets).forEach(([name, sels]) => {
      for (const sel of sels) {
        const el = document.querySelector(sel);
        if (el) {
          const clone = el.cloneNode(true);
          clone.querySelectorAll('img').forEach(img => {
            img.removeAttribute('src');
            img.removeAttribute('srcset');
          });
          clone.querySelectorAll('script, style').forEach(e => e.remove());
          result[name] = {
            selector: sel,
            position: getComputedStyle(el).position,
            html: clone.outerHTML.slice(0, 4000),
          };
          break;
        }
      }
    });

    return result;
  });

  await browser.close();

  // ── 14. 写入文件 ──────────────────────────────────────
  console.log('\n💾 写入文件...');

  // site.css
  const siteCss = [
    `/* ===== CSS Variables ===== */\n:root {\n`,
    Object.entries(cssVars).map(([k, v]) => `  ${k}: ${v};`).join('\n'),
    `\n}\n\n`,
    `/* ===== Design CSS Rules ===== */\n`,
    cssRules,
    `\n\n/* ===== @keyframes ===== */\n`,
    keyframes,
  ].join('');

  fs.writeFileSync(path.join(outputDir, 'site.css'), siteCss, 'utf-8');

  // raw.json
  fs.writeFileSync(path.join(outputDir, 'raw.json'), JSON.stringify({
    url,
    extractedAt: new Date().toISOString(),
    cssVars,
    transitions,
    keyframesCount: (keyframes.match(/@keyframes/g) || []).length,
    fonts: { ...fonts, googleFontsUrls },
    animLibs,
    components,
  }, null, 2), 'utf-8');

  // fonts-report.md
  const fontFamilyNames = [...new Set(
    fonts.fontFaces.map(f => f.family.replace(/ fallback:.*$/, '').trim())
  )];

  const fontsReport = [
    `# Fonts Report\n`,
    `## 检测到的自定义字体\n`,
    fontFamilyNames.length
      ? fontFamilyNames.map(f => `- **${f}**`).join('\n')
      : '- 未检测到自定义字体（使用系统字体）',
    `\n\n## Google Fonts\n`,
    googleFontsUrls.length
      ? googleFontsUrls.map(u => `- ${u}`).join('\n')
      : '- 未使用 Google Fonts',
    `\n\n## 字体替代建议\n`,
    `自定义字体文件无法直接复用（私有 CDN），以下是替代方向：\n`,
    fontFamilyNames.map(f => `- **${f}** → 搜索：https://fonts.google.com/?query=${encodeURIComponent(f.split('-')[0])}`).join('\n'),
    `\n\n## @font-face 详情\n`,
    fonts.fontFaces.map(f =>
      `### ${f.family}\n- weight: ${f.weight || 'normal'}\n- style: ${f.style || 'normal'}`
    ).join('\n\n'),
  ].join('\n');

  fs.writeFileSync(path.join(outputDir, 'fonts-report.md'), fontsReport, 'utf-8');

  // ── 15. 摘要输出 ──────────────────────────────────────
  const screenshotCount = fs.readdirSync(path.join(outputDir, 'screenshots')).length;
  const jsLibsDetected = Object.entries(animLibs).filter(([, v]) => v).map(([k]) => k);
  const componentList = Object.keys(components).filter(k => k !== 'stickyElements');

  console.log('\n✅ 提取完成！\n');
  console.log(`📁 ${outputDir}/`);
  console.log(`   ├── site.css          CSS 变量 + 规则 + @keyframes`);
  console.log(`   ├── raw.json          组件 + 动效 + 字体数据`);
  console.log(`   ├── fonts-report.md   字体分析 + 替代建议`);
  console.log(`   └── screenshots/      ${screenshotCount} 张截图`);
  console.log(`\n📊 摘要:`);
  console.log(`   CSS 变量       ${Object.keys(cssVars).length} 个`);
  console.log(`   @keyframes     ${(keyframes.match(/@keyframes/g) || []).length} 个`);
  console.log(`   Transition     ${transitions.length} 条`);
  console.log(`   自定义字体     ${fontFamilyNames.join(', ') || '无'}`);
  console.log(`   检测到组件     ${componentList.join(', ')}`);
  console.log(`   Sticky/Fixed   ${components.stickyElements?.length || 0} 个元素`);

  if (jsLibsDetected.length) {
    console.log(`\n⚠️  JS 动效库: ${jsLibsDetected.join(', ')} (动效参数需参考截图推断)`);
  }

  console.log(`\n下一步：告诉 Claude "基于 design-extractor/ 生成设计系统"\n`);
}

extract().catch(err => {
  console.error('\n❌ 提取失败：', err.message);
  process.exit(1);
});