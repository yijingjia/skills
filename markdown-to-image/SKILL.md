---
name: markdown-to-image
description: 将 Markdown 文件渲染为小红书卡片图片（270×360px，3:4 竖版 PNG，默认 4× 高清输出）。支持文本、代码块、表格、列表、引用、Obsidian wikilink 图片等内容块；自动分页与段落跨页切分；提供 light/dark/warm/forest 四种主题与 sans/serif 两种字体可选。当用户提到"生成小红书图片"、"把文章做成卡片"、"Markdown 转图片"、"导出文章为卡片图"时触发此 skill。
---

# markdown-to-image Skill

将 Markdown 文章渲染为小红书风格卡片图片（270×360px，3:4 比例，默认 4× 高清输出）。

---

## 快速开始

> 以下所有命令均假设你**已 `cd` 进入 skill 自身目录**。
> 把这个 skill 放在任意位置都可以——脚本通过相对路径调用，不依赖具体安装路径。

### 第一次使用：安装环境

```bash
cd <SKILL_DIR>                          # 进入 skill 所在目录
python3 -m venv .venv                   # 创建虚拟环境
.venv/bin/pip install playwright        # 安装依赖
.venv/bin/playwright install chromium   # 下载 Chromium（约 150MB，仅需一次）
```

或一键运行：

```bash
cd <SKILL_DIR>
python3 setup.py
```

### 生成卡片图片

在 skill 目录下运行：

```bash
# 默认 light 主题 + sans 字体
.venv/bin/python scripts/render.py /path/to/article.md

# 指定主题
.venv/bin/python scripts/render.py /path/to/article.md --theme dark

# 指定字体
.venv/bin/python scripts/render.py /path/to/article.md --font serif

# 指定缩放
.venv/bin/python scripts/render.py /path/to/article.md --scale 6
```

PNG 输出到 `.md` 文件所在目录，命名：`<文件名>_01_<主题>_<字体>.png`、`<文件名>_02_<主题>_<字体>.png`...

> **可选：注册全局命令** —— 把 skill 路径写入 shell alias，避免每次输入完整路径：
> ```bash
> # 加到 ~/.zshrc 或 ~/.bashrc
> alias md2img='<SKILL_DIR>/.venv/bin/python <SKILL_DIR>/scripts/render.py'
> ```
> 之后任意位置可直接 `md2img article.md --theme warm`。

---

## 主题（`--theme`）

| 主题 | 描述 |
|------|------|
| `light` | 白底黑字，蓝色高亮（默认） |
| `dark` | 深蓝底色，浅蓝高亮 |
| `warm` | 暖米底色，橙红高亮 |
| `forest` | 白底黑字，绿色高亮 |

自定义主色调：修改 `scripts/render.py` 顶部 `THEMES` 字典中对应主题的 `hl` 字段。

---

## 字体（`--font`）

| 字体 | 描述 |
|------|------|
| `sans` | 苹方 / 微软雅黑等无衬线（默认） |
| `serif` | 思源宋体 / 宋体等衬线字体 |

添加新字体：在 `scripts/render.py` 顶部 `FONTS` 字典新增一条，配置 `stack`、字号、字重。

---

## 缩放倍率（`--scale`）

| 参数 | 输出像素 | 说明 |
|------|---------|------|
| `--scale 4` | 1080×1440px | 默认，小红书推荐 |
| `--scale 2` | 540×720px | 体积小、加载快 |
| `--scale 6` | 1620×2160px | 更高清，文件更大 |

---

## 支持的 Markdown 语法

| 语法 | 渲染效果 |
|------|---------|
| `# h1` / `## h2` / `### h3` | 三级标题 |
| 正文段落 | 8px，行高 1.55 |
| `**文字**` | 主色调高亮（不加粗字重） |
| `*文字*` | 斜体 |
| `` `code` `` | 内联代码块 |
| ` ```...``` ` | 代码块，字号自动缩放 |
| `> 引用` | 左侧主色竖线 |
| `---` | 分割线（不触发分页） |
| `- item` / `1. item` | 无序 / 有序列表 |
| `![alt](url)` | 图片（封面图自动识别） |
| `![[file.png]]` | Obsidian wikilink 图片 |
| 标准 Markdown 表格 | 字号自动缩放适应列数 |

---

## 分页逻辑

**封面页**：`# 标题` + 第一张图片（限高由 `COVER_IMG_MAX_H` 控制，默认 150px，等比缩放保持比例）+ 贪心填充正文段落。

**正文页**：用 Playwright 真实渲染测量每个节点的 `offsetHeight`，按实际高度分页。

**段落跨页切分**：当一段正文塞不下时，自动按字符二分查找能填满剩余空间的最大长度，优先在中文标点（。！？；，：、）处切分。前半段留在当前页，后半段进入下一页。内容不丢失，最后一行完整显示，不会出现半行截断。

`---` 渲染为视觉分割线，不触发分页。

---

## 目录结构

```
markdown-to-image/
├── SKILL.md            本文件
├── setup.py            环境检测与自动安装
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
在 `scripts/render.py` 顶部 `THEMES` 字典中新增一条，包含 `bg`、`text`、`hl`、`codeBg`、`codeText`、`icBg`、`icText` 七个字段即可。

**封面正文太少 / 想多放几段？**
封面图默认限高 150px。修改 `scripts/render.py` 顶部 `COVER_IMG_MAX_H` 常量（减小数值留更多正文空间，增大数值让图片更显眼）。
