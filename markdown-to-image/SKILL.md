---
name: markdown-to-image
description: 将 Markdown 文件渲染为小红书卡片图片（3:4 竖版 PNG）。支持文本、代码块、表格、列表、引用、图片等内容块，自动分页，支持四种视觉主题。当用户提到"生成小红书图片"、"把文章做成卡片"、"导出图片"、"/md2img"时触发此 skill。
---

# markdown-to-image Skill

将 Markdown 文章渲染为小红书风格卡片图片（270×360px，3:4 比例，3× 高清输出）。

---

## 快速开始

### 第一次使用：安装环境

```bash
python markdown-to-image/setup.py
```

自动完成：检测 Python 3.8+、安装 `playwright`、下载 Chromium（约 150MB，仅需一次）。

### 生成卡片图片

```bash
# 默认 light 主题
python markdown-to-image/scripts/render.py article.md

# 指定主题
python markdown-to-image/scripts/render.py article.md --theme dark
```

PNG 输出到 `.md` 文件所在目录，命名：`<文件名>_01_<主题>.png`、`<文件名>_02_<主题>.png`...

---

## 主题

| 主题 | 描述 |
|------|------|
| `light` | 白底黑字，蓝色高亮（默认） |
| `dark` | 深蓝底色，浅蓝高亮 |
| `warm` | 暖米底色，橙红高亮 |
| `forest` | 白底黑字，绿色高亮 |

自定义主色调：修改 `scripts/render.py` 顶部 `THEMES` 字典中对应主题的 `hl` 字段。

---

## 支持的 Markdown 语法

| 语法 | 渲染效果 |
|------|---------|
| `# h1` / `## h2` / `### h3` | 三级标题 |
| 正文段落 | 10px，行高 1.75 |
| `**文字**` | 主色调高亮（不加粗字重） |
| `*文字*` | 斜体 |
| `` `code` `` | 内联代码块 |
| ` ```...``` ` | 代码块，字号自动缩放 |
| `> 引用` | 左侧主色竖线 |
| `---` | 分割线（不触发分页） |
| `- item` / `1. item` | 无序 / 有序列表 |
| `![alt](url)` | 图片（封面图自动识别） |
| 标准 Markdown 表格 | 字号自动缩放适应列数 |

---

## 分页逻辑

**封面页**：`# 标题` + 第一段副标题 + 第一张图片（可选）组成封面顶部，图片下方继续贪心填充正文，直到塞满为止。

**正文页**：用 Playwright 真实渲染测量每个节点的 offsetHeight，按实际高度分页，不会截断内容。

`---` 渲染为视觉分割线，不触发分页。

---

## 在 Claude Code 中注册为命令

在项目或全局 `CLAUDE.md` 中添加：

```markdown
## 自定义命令

### /md2img
将 Markdown 文件生成为小红书卡片图片。
用法: /md2img <file.md> [--theme light|dark|warm|forest]
执行: python markdown-to-image/scripts/render.py $ARGUMENTS
```

之后在 Claude Code 中直接输入：
```
/md2img article.md
/md2img article.md --theme dark
```

---

## 目录结构

```
markdown-to-image/
├── SKILL.md            本文件
├── setup.py            环境检测与安装
└── scripts/
    └── render.py       核心渲染脚本（Markdown 解析 + Playwright 截图）
```

---

## 常见问题

**中文字体显示异常？**
Chromium 使用系统字体。macOS 自带苹方，Windows 自带微软雅黑，Linux 需手动安装：
```bash
sudo apt install fonts-noto-cjk
```

**网络图片加载失败？**
脚本使用 `wait_for_load_state("networkidle")` 等待图片加载。若图片需要认证或跨域限制，建议换用公开 CDN URL。

**如何添加新主题？**
在 `render.py` 顶部 `THEMES` 字典中新增一条，包含 `bg`、`text`、`hl`、`codeBg`、`codeText`、`icBg`、`icText` 七个字段即可。
