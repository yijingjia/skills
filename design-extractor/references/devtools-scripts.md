# DevTools 提取脚本

## 脚本一：提取过滤后的 CSS 规则

在目标网站的 DevTools Console 中运行：

```javascript
const styles = [...document.styleSheets]
  .flatMap((s) => {
    try {
      return [...s.cssRules];
    } catch {
      return [];
    }
  })
  .map((r) => r.cssText)
  .filter(
    (text) =>
      text.includes("--") ||
      /color|font|spacing|radius|shadow|transition|animation|@keyframes|transform/i.test(
        text,
      ),
  )
  .join("\n");

copy(styles);
```

运行后显示 `undefined` 是正常的，内容已复制到剪贴板。

---

## 脚本二：提取 CSS 变量

```javascript
const vars = {};
const root = getComputedStyle(document.documentElement);
[...document.styleSheets]
  .flatMap((s) => {
    try {
      return [...s.cssRules];
    } catch {
      return [];
    }
  })
  .flatMap((r) => r.cssText.match(/--[\w-]+/g) || [])
  .forEach((v) => (vars[v] = root.getPropertyValue(v).trim()));

copy(JSON.stringify(vars, null, 2));
```

---

## 脚本三：检测 JS 动效库

```javascript
["gsap", "GSAP", "Lottie", "Motion", "anime", "framer"]
  .map((lib) => `${lib}: ${!!window[lib]}`)
  .join("\n");
```

如果有库返回 `true`，说明该网站使用 JS 驱动动效，CSS 中无法提取，需要截图/录屏辅助。

---

## 脚本四：扫描页面现有组件

运行后查看哪些组件存在（✅），再决定提取哪些：

```javascript
const selectors = {
  "header / 导航": [
    "header",
    "nav",
    '[class*="header"]',
    '[class*="navbar"]',
    '[class*="nav-"]',
  ],
  footer: ["footer", '[class*="footer"]'],
  sidebar: ["aside", '[class*="sidebar"]', '[class*="side-bar"]'],
  "hero section": [
    '[class*="hero"]',
    '[class*="banner"]',
    '[class*="jumbotron"]',
  ],
  card: ['[class*="card"]', '[class*="tile"]', '[class*="item"]'],
  "grid / 列表": ['[class*="grid"]', '[class*="list"]', '[class*="feed"]'],
  "modal / 弹窗": [
    '[class*="modal"]',
    '[class*="dialog"]',
    '[class*="overlay"]',
  ],
  dropdown: ['[class*="dropdown"]', '[class*="menu"]', '[class*="popover"]'],
  tabs: ['[class*="tab"]', '[role="tablist"]'],
  accordion: ['[class*="accordion"]', '[class*="collapse"]', "details"],
  tooltip: ['[class*="tooltip"]', '[role="tooltip"]'],
  "form / input": ["form", "input", "textarea", "select"],
  button: ["button", '[class*="btn"]', '[class*="button"]'],
  "toast / 通知": [
    '[class*="toast"]',
    '[class*="notification"]',
    '[class*="alert"]',
  ],
  "badge / tag": ['[class*="badge"]', '[class*="tag"]', '[class*="chip"]'],
  pagination: [
    '[class*="pagination"]',
    '[class*="pager"]',
    'nav[aria-label*="page"]',
  ],
};

Object.entries(selectors).forEach(([name, sels]) => {
  const found = sels.find((s) => document.querySelector(s));
  console.log(found ? `✅ ${name}` : `❌ ${name}`);
});
```

---

## 脚本五：批量提取组件 HTML 结构

根据脚本四的结果，删掉不需要的组件，然后运行。

**注意**：modal、toast 等动态组件需要先手动触发显示，再运行此脚本。

```javascript
// 按需修改这个列表，保留你想提取的组件
const targets = {
  header: ["header", "nav", '[class*="header"]', '[class*="navbar"]'],
  footer: ["footer", '[class*="footer"]'],
  hero: ['[class*="hero"]', '[class*="banner"]'],
  card: ['[class*="card"]'],
  modal: ['[class*="modal"]', '[class*="dialog"]'],
  dropdown: ['[class*="dropdown"]', '[class*="menu"]'],
  tabs: ['[class*="tab"]', '[role="tablist"]'],
  accordion: ["details", '[class*="accordion"]'],
  form: ["form"],
  toast: ['[class*="toast"]', '[class*="notification"]'],
};

const result = {};

Object.entries(targets).forEach(([name, sels]) => {
  for (const sel of sels) {
    const el = document.querySelector(sel);
    if (el) {
      const clone = el.cloneNode(true);
      clone.querySelectorAll("img").forEach((img) => {
        img.removeAttribute("src");
        img.removeAttribute("srcset");
      });
      clone.querySelectorAll("script, style").forEach((e) => e.remove());
      result[name] = {
        selector: sel,
        html: clone.outerHTML.slice(0, 3000),
      };
      break;
    }
  }
});

copy(JSON.stringify(result, null, 2));
```

---

## 注意事项

- 跨域 CSS 文件可能无法读取（CORS 限制），脚本会自动跳过
- 脚本五每个组件限制 3000 字符，复杂组件建议截图补充
- 动态渲染的组件（modal、toast）需先触发显示再提取
- 脚本三全为 `false` 说明动效均为纯 CSS，可完整提取
