---
name: design-extractor
description: 从参考网站提取完整设计系统，生成 design tokens、color palette、设计系统文档和可交互 HTML playground，并保存为可复用文件供后续页面开发使用。当用户想复刻、参考或提取某个网站的设计风格、配色、动效、排版、组件结构时触发。也适用于"我想参考 X 网站的风格来做我的网站"、"帮我提取这个网站的设计规范"、"复刻这个网站的导航/卡片/组件"等场景。
---

# Design Extractor Skill

从目标网站提取完整设计系统（tokens + 组件结构），保存为可复用文件，供后续页面生成时作为设计上下文使用。

---

## 模式选择

启动后先询问用户使用哪种模式：

- **自动模式（推荐）**：只需提供 URL，Playwright 自动完成所有提取，包括截图和录屏
- **手动模式**：用户自己在 DevTools 运行脚本，适合无法安装 Playwright 的场景

---

## 自动模式（Playwright）

### 步骤 1：环境检测与安装

在项目根目录运行：

```bash
node design-extractor/scripts/setup.js
```

脚本会自动：

- 检测 Node.js 版本（需要 16+）
- 检测包管理器（npm / pnpm / yarn）
- 安装 Playwright
- 下载 Chromium（约 150MB，仅首次需要）

### 步骤 2：运行提取脚本

```bash
node design-extractor/scripts/extract.js <目标网站URL>
```

示例：

```bash
node design-extractor/scripts/extract.js https://aptosnetwork.com
```

脚本自动完成：

- 打开页面，等待完整渲染（含 SPA）
- 提取所有 CSS 变量和设计相关 CSS 规则
- 检测 JS 动效库（GSAP / Lottie / Framer Motion 等）
- 扫描并提取组件 HTML 骨架
- 截图：首屏 / 中段 / 底部 / hover 状态 / 全页
- 录屏整个会话（捕获动效）
- 输出 `site.css` 和 `raw.json`

### 步骤 3：查看提取结果

提取完成后，`design-extractor/` 目录结构：

```
design-extractor/
├── site.css              ← CSS 变量 + 设计规则
├── raw.json              ← 组件结构 + 动效库检测结果
└── screenshots/
    ├── 01-hero.png
    ├── 02-mid.png
    ├── 03-lower.png
    ├── 04-hover-*.png
    ├── 05-fullpage.png
    └── *.webm            ← 录屏（动效参考）
```

告知用户：

- 查看截图确认提取效果
- 如有动效库被检测为 `true`，建议提供额外的动效录屏补充

### 步骤 4：生成设计系统

读取 `site.css`、`raw.json` 和所有截图，进入**第三阶段**生成设计系统文件。

---

## 手动模式

按以下顺序逐步引导，每步等用户完成后再进入下一步。

### 步骤 1：检测 JS 动效库

运行**脚本三**（见 `references/devtools-scripts.md`）：

- 全部 `false` → 动效为纯 CSS，后续可完整提取
- 有 `true` → 提示用户额外提供动效截图或录屏

### 步骤 2：提取 CSS

依次运行**脚本一**（CSS 规则）和**脚本二**（CSS 变量），分别复制结果。

### 步骤 3：扫描页面组件

运行**脚本四**，查看页面上存在哪些组件（✅/❌）。

让用户确认：

- 哪些组件需要提取？
- 有无动态组件（modal、toast）需要先手动触发？

### 步骤 4：提取组件 HTML

根据步骤 3 的确认结果，让用户修改**脚本五**中的 `targets` 列表，删掉不需要的组件后运行，复制结果。

**提醒用户**：动态组件（modal、dropdown、toast）需先在页面上触发显示，再运行脚本五。

### 步骤 5：收集截图（布局参考）

请用户提供以下截图：

- 首页 hero 区域
- 含卡片或列表的内容区域
- 任何需要复刻的关键页面区域
- 如有动效，提供录屏或 GIF

---

## 写入文件（仅手动模式需要）

自动模式跳过此步骤，文件已由脚本自动生成。

手动模式下，用户提供所有内容后，写入以下文件：

```
design-extractor/
├── site.css          ← 脚本一 + 脚本二内容合并
└── components.json   ← 脚本五输出的组件 HTML 结构
```

```bash
mkdir -p design-extractor
```

---

## 第三阶段：分析并生成设计系统文件

读取 `site.css` 和 `components.json`，结合截图，生成以下文件：

| 文件                                | 内容                   |
| ----------------------------------- | ---------------------- |
| `design-extractor/tokens.json`      | Design tokens          |
| `design-extractor/palette.md`       | Color palette          |
| `design-extractor/design-system.md` | 设计系统规范（含组件） |
| `design-extractor/components.md`    | 组件结构文档           |
| `design-extractor/playground.html`  | 可交互 HTML playground |

---

### tokens.json 格式

```json
{
  "color": {
    "brand": { "primary": "", "secondary": "", "accent": "" },
    "surface": { "background": "", "card": "", "elevated": "" },
    "text": { "primary": "", "secondary": "", "muted": "", "inverse": "" },
    "border": { "default": "", "subtle": "", "strong": "" },
    "state": { "success": "", "warning": "", "error": "" }
  },
  "typography": {
    "fontFamily": { "base": "", "heading": "", "mono": "" },
    "fontSize": { "xs": "", "sm": "", "md": "", "lg": "", "xl": "", "2xl": "" },
    "fontWeight": { "regular": "", "medium": "", "semibold": "", "bold": "" },
    "lineHeight": { "tight": "", "normal": "", "relaxed": "" }
  },
  "spacing": { "xs": "", "sm": "", "md": "", "lg": "", "xl": "", "2xl": "" },
  "radius": { "sm": "", "md": "", "lg": "", "xl": "" },
  "shadow": { "sm": "", "md": "", "lg": "" },
  "motion": {
    "duration": { "fast": "", "normal": "", "slow": "" },
    "easing": { "standard": "", "enter": "", "exit": "" }
  },
  "opacity": { "disabled": "", "hover": "" }
}
```

规则：

- spacing 基于 4px 或 8px 体系（或原网站实际体系）
- 颜色语义化命名
- shadow 用标准 CSS box-shadow 格式
- motion 从 CSS 提取；如检测到 JS 动效库，标注 `"source": "js-animation-library"` 并基于风格推断

---

### components.md 格式

基于 `components.json` 的 HTML 结构，为每个提取到的组件生成文档：

```markdown
# Components

## Header / 导航

- 结构说明
- sticky/fixed 行为
- 移动端折叠方式
- 关键 class 名
- 示例 HTML（简化版）

## [其他组件同上]
```

每个组件必须包含：

- 语义化 HTML 骨架（去除业务内容，保留结构）
- 状态说明（hover / active / open / disabled）
- 与 tokens 的对应关系（使用哪些 color / spacing / radius）

---

### design-system.md 格式

必须涵盖以下所有章节，每章节要有具体数值和用法说明，不允许模糊描述：

```markdown
# Design System Guide

## 0. Overview

- 设计系统整体定位与风格描述
- 核心设计语言（极简/高密度/editorial 等）
- 主要使用场景

## 1. Design Principles

- 3–5 条设计哲学，每条附具体体现方式

## 2. Color Palette

- 完整原始色板（所有色值，含 HEX + 用途）
- 语义化颜色映射（brand / surface / text / border / state）
- Light / Dark 模式对照表
- 颜色使用规则（✅ 推荐 / ❌ 禁止）
- 颜色组合示例（哪些颜色可以叠加使用）

## 3. Typography

- 字体家族说明（每种字体的性格与适用场景）
- 字体组合规则（heading 与 body 如何搭配使用）
- 完整字阶表（size / weight / line-height / letter-spacing / 用途）
- 可变字重说明（如使用 variable font，列出实际使用的 weight 值）
- 响应式字号变化规则
- 特殊排版规则（uppercase / mono 的使用场景）

## 4. Spacing System

- 基础单位说明（如 5px base unit）
- 完整间距表（token 名 / 数值 / 典型用途）
- 组件内间距 vs 布局间距的使用区别
- 内容 gutter 和容器宽度规则

## 5. Component Styles

- 每个提取到的组件，包含：
  - 视觉规格（尺寸、内边距、颜色、圆角、阴影）
  - 所有交互状态（default / hover / active / focus / disabled）
  - 使用的 token 引用
  - HTML 骨架示例

## 6. Shadows & Elevation

- 完整阴影层级（sm / md / lg / xl）
- 每级阴影的 CSS box-shadow 值
- 何时使用何种层级（卡片 / 弹窗 / tooltip 等）
- 暗色模式下阴影的处理方式

## 7. Animations & Transitions

- 所有 duration 值及使用场景
- 所有 easing 函数（含 cubic-bezier 值）及适用场景
- 具体动效清单（@keyframes 名称 / 效果描述 / 触发时机）
- prefers-reduced-motion 处理方式

## 8. Border Radius

- 完整圆角层级（sm / md / lg / xl / full）
- 每级对应的像素值
- 各组件使用的圆角级别

## 9. Opacity & Transparency

- 所有透明度值（disabled / hover / overlay 等）
- 半透明颜色的使用规则（rgba border、overlay 背景）
- 透明度与颜色叠加的典型场景

## 10. Responsive Design

- 断点定义（名称 / rem 值 / 目标设备）
- 响应式布局规则
- 字号在各断点的变化

## 11. Common Usage Patterns（如项目使用 Tailwind）

- 项目中高频出现的 class 组合
- 每种模式对应的视觉效果和使用场景
- 示例代码片段
```

---

### palette.md 格式

必须包含：

- 原始色板：所有颜色（色块名 / HEX / RGB / 用途描述）
- 语义映射表：每个语义 token 对应的原始色值
- Light/Dark 模式颜色对照
- 颜色使用场景举例（至少每类 2 个实际使用示例）

---

### playground.html 要求

纯 HTML + CSS + 少量 JS，无外部依赖，必须包含以下所有板块：

**页面结构**

- 顶部固定导航：各板块快速跳转锚点
- 左侧侧边栏（sticky）：主色 color picker + Light/Dark 模式切换
- 右侧主内容区：按以下顺序排列所有板块

**必须包含的板块（缺一不可）**

1. **Overview** — 设计系统名称、风格描述、设计语言关键词标签

2. **Color Palette**
   - 原始色板（所有颜色，色块 + 名称 + HEX，点击复制 HEX）
   - 语义颜色分组展示（brand / surface / text / border / state）
   - Light/Dark 模式颜色对比

3. **Typography**
   - 完整字阶展示（每行显示：token 名 / size / weight / line-height / 实际文字渲染）
   - 字体组合示例（Serif heading + Sans body 的实际搭配效果）
   - 特殊样式展示（mono uppercase、可变字重对比）

4. **Spacing System**
   - 可视化间距条（每个 token：名称 + 数值 + 对应宽度色块）

5. **Shadows & Elevation**
   - 每级阴影的卡片展示（sm / md / lg / xl）
   - 显示对应 CSS 值

6. **Border Radius**
   - 每级圆角的方块展示（sm / md / lg / xl / full）
   - 显示对应数值

7. **Opacity & Transparency**
   - 每个透明度值的视觉展示
   - 半透明边框和 overlay 效果示例

8. **Animations & Transitions**
   - 每个 @keyframes 的可触发动效演示（点击/hover 触发）
   - duration × easing 组合对比（相同动效，不同参数的视觉差异）
   - 显示对应 CSS 代码

9. **Component Styles**
   - 基于提取到的组件还原，每个组件展示所有状态（default / hover / active / disabled）
   - 显示组件使用的 token 引用

10. **Common Patterns**（如适用）
    - 高频 class 组合的视觉示例
    - 每个 pattern 附代码片段（可复制）

**交互要求**

- 主色 color picker 修改后，所有使用该颜色的元素实时更新
- Light/Dark 切换影响全局语义颜色
- 点击色块复制 HEX 值，显示复制成功提示
- 点击代码片段复制代码
- 动效演示可重复触发

---

## 第四阶段：后续使用说明

生成完成后告知用户：

```
设计系统文件已保存至 design-extractor/ 目录：

- tokens.json        → 开发时引用设计变量
- palette.md         → 颜色参考
- components.md      → 组件结构参考
- design-system.md   → 完整设计规范
- playground.html    → 在浏览器中预览

后续让我帮你生成页面时，说"参考 design-extractor/ 的设计风格"，
我会自动读取这些文件作为设计上下文。
```

---

## 注意事项

- CSS 为空时，说明网站使用 CSS-in-JS 或内联样式，提示用户改用截图方式
- 颜色不完整时，基于视觉风格推断，在 tokens.json 中标注 `"inferred": true`
- 组件 HTML 超过 3000 字符时，AI 基于截图补充还原
- 不输出分析过程，直接输出结果文件
