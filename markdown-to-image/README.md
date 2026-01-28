# Markdown to Image Skill

An AI skill that converts Markdown files into beautifully styled images using the elegant blue theme.

## What This Skill Does

This skill enables your AI assistant to transform any Markdown document into publication-ready images with just a simple request. Perfect for:
- Creating social media graphics from your notes
- Generating shareable images for Twitter, Instagram, WeChat
- Visualizing documentation for presentations
- Converting Obsidian notes into image formats

## Features

- 📱 **Multiple Sizes**: Supports various image sizes for social media platforms
- 📄 **Automatic Pagination**: Long documents are intelligently split into multiple images
- 🔧 **Highly Customizable**: Custom dimensions, padding, and frontmatter display
- ✨ **Full Markdown Support**: Headings, lists, code blocks, tables, blockquotes, and Obsidian callouts

## Installation

To enable this skill for your AI assistant:

1. **Navigate to the scripts directory:**
   ```bash
   cd markdown-to-image/scripts
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

**Note**: The skill will automatically install Playwright browsers on the first use.

## How to Use

Simply ask your AI assistant to convert a Markdown file to an image. The skill handles everything automatically.

### Basic Example

```
User: Convert my note.md to an image

Assistant: I'll convert note.md to an image using the blue theme!

Default settings:
- Size: 1440x2400px (optimized for general use)
- Padding: top=200px, bottom=200px, sides=100px
- Frontmatter: hidden

Generating...
✓ Generated 1 image: ./converted_images/note.png
```

### With Custom Options

```
User: Convert chapter1.md to Instagram story size

Assistant: Converting chapter1.md to Instagram story format (1080x1920px)...

✓ Generated 3 images: ./converted_images/chapter1-1.png, chapter1-2.png, chapter1-3.png
```

### Show Frontmatter

```
User: Convert my article.md to an image, show the frontmatter too

Assistant: Converting article.md with frontmatter visible...

✓ Generated image: ./converted_images/article.png
```

## Available Size Presets

| Preset | Dimensions | Use Case |
|--------|-----------|----------|
| `default` | 1440 x 2400px | General use (Recommended) |
| `instagram-story` | 1080 x 1920px | Instagram Stories |
| `twitter` | 1200 x 675px | Twitter images |
| `wechat` | 900 x 1600px | WeChat long images |

## Supported Markdown Features

- ✅ **Headings** (H1-H6)
- ✅ **Text Formatting** (Bold, Italic, Links)
- ✅ **Code** (Inline code and syntax-highlighted code blocks)
- ✅ **Lists** (Ordered, Unordered, and Nested)
- ✅ **Blockquotes**
- ✅ **Obsidian Callouts** (All 14 types)
- ✅ **Tables**
- ✅ **YAML Frontmatter** (Optional)

## Obsidian Callouts

The skill fully supports Obsidian callouts:

```markdown
> [!note]
> This is a note callout.

> [!warning] Custom Title
> This is a warning with a custom title.

> [!success]
> Task completed successfully!

> [!tip]
> Here's a helpful tip.
```

Supported types: `note`, `warning`, `success`, `tip`, `info`, `todo`, `question`, `danger`, `bug`, `example`, and more.

## Project Structure

```
markdown-to-image/
├── scripts/
│   ├── generate.js        # Main generation script (used by AI)
│   ├── markdownRenderer.js  # Markdown to HTML renderer
│   ├── package.json       # Dependencies
│   └── ...
├── themes/
│   └── blue.md    # Theme definitions
├── README.md              # This file
└── SKILL.md               # Skill definition for AI agents
```

## Technical Details

- **Version**: 2.0
- **Rendering**: HTML-based with Playwright (Chromium)
- **Markdown Parser**: marked.js
- **Default Padding**: top=200px, right=100px, bottom=200px, left=100px
- **Output Format**: PNG

## License

MIT License

## Acknowledgments

- Original theme: [Typora Theme - Lapis](https://github.com/YiNNx/typora-theme-lapis) by YiNNx
- Markdown parser: [marked.js](https://marked.js.org/)
- Browser automation: [Playwright](https://playwright.dev/)

---

Built with Claude AI
