---
name: markdown-to-image
description: Convert Markdown files to themed images with HTML and Playwright rendering. Supports automatic content splitting, Obsidian callouts, YAML frontmatter (optional), customizable padding (default top=50px, bottom=120px), and default size of 1440x2400px. Use when user wants to render Markdown as images, visualize Markdown content, or create social media graphics from Markdown files.
---

# Markdown to Image

Convert Markdown files into beautifully themed images. This skill uses HTML-based rendering with Playwright for high-quality screenshots, featuring automatic content splitting, optimized padding, and full support for Obsidian callouts.

## Technical Implementation

**Version 2.0** uses a modern HTML-first approach:

1. **Markdown → HTML**: Markdown content is converted to styled HTML using `marked`
2. **Theme CSS**: Theme colors and fonts are applied via CSS stylesheets
3. **Playwright Screenshots**: HTML pages are rendered and captured as PNG images using Chromium
4. **Automatic Splitting**: Content is intelligently split into multiple pages when exceeding height limits

### Advantages of HTML Rendering

- **Superior Typography**: Browser rendering engine provides better text layout and font rendering
- **CSS Power**: Full CSS capabilities for styling (gradients, shadows, complex layouts)
- **Easier Maintenance**: Styles defined in CSS rather than manual Canvas calculations
- **More Markdown Features**: Better support for tables, nested lists, and complex formatting
- **Consistent Results**: Chromium ensures consistent rendering across platforms

## Quick Start

When a user requests Markdown to image conversion, follow this workflow:

### Step 1: Gather Requirements

**If user didn't specify**, ask these questions:

1. **Input file**: "Which Markdown file would you like to convert?"
   - If user says "this file" or "current file", use the currently open file
   - Otherwise, ask for the file path

2. **Image size**: "What size should the images be?"
   - Show preset options:
     - `default` (1440x2400px) - General use ⭐ **Recommended**
     - `instagram-story` (1080x1920px) - Instagram stories
     - `twitter` (1200x675px) - Twitter images
     - `wechat` (900x1600px) - WeChat long images
     - `custom` - User specifies width and height
   - Default to `default` if user doesn't have preference

3. **Frontmatter**: "Do you want to show YAML frontmatter in the first image?"
   - Default: No (hidden)
   - Use `--show-frontmatter` flag to show

### Step 2: Execute Generation

4. **Check dependencies** (first time only): Verify `npm install` has been run
5. **Run generation**: Execute `node scripts/generate.js` with collected parameters
6. **Monitor progress**: Show generation progress to user
7. **Return results**: Display generated image paths and confirm success (images are saved in `converted_images` folder next to input file)

### Example Interaction Flow

**User**: "Convert note.md to an image"

**Assistant response**:
```
I'll convert note.md to an image using the blue theme!

Default settings:
- Size: 1440x2400px (optimized for general use)
- Padding: top=200px, bottom=200px, sides=100px
- Frontmatter: hidden (use --show-frontmatter to display)

Generating...
```

Then proceed with generation.

## Theme

This skill uses the blue theme - a clean, elegant theme with soft blue tones, optimized for Chinese and English content.

**Theme features:**
- Elegant blue color scheme
- Optimized typography for mixed CJK/English text
- Professional appearance for documentation and notes
- Enhanced callout styles matching code block styling

## Size Presets

| Preset | Width | Height | Use Case |
|--------|-------|--------|----------|
| default | 1440px | 2400px | General use (recommended) |
| instagram-story | 1080px | 1920px | Instagram stories |
| twitter | 1200px | 675px | Twitter images |
| wechat | 900px | 1600px | WeChat long images |

**Default padding:** top=200px, right=100px, bottom=200px, left=100px

Custom dimensions can be specified with `--width` and `--height` parameters.

## Usage Examples

### Basic Usage

```bash
cd scripts
node generate.js --input /path/to/file.md
```

### Show Frontmatter

```bash
node generate.js --input /path/to/file.md --show-frontmatter
```

### Custom Size

```bash
node generate.js --input note.md --width 1200 --height 1600
```

### Custom Padding

```bash
# Same padding on all sides
node generate.js --input note.md --padding 100

# Different padding for each side (top,right,bottom,left)
node generate.js --input note.md --padding 50,80,120,80
```

### Size Presets

```bash
# Instagram story format
node generate.js --input note.md --size instagram-story

# Twitter format
node generate.js --input note.md --size twitter
```

## Command Line Parameters

```
-i, --input <file>         Input Markdown file (required)
-s, --size <preset>        Size preset (default/instagram-story/twitter/wechat)
-w, --width <px>           Custom width in pixels
-h, --height <px>          Custom max height per image in pixels
-p, --padding <value>      Padding in pixels (single value or top,right,bottom,left)
                           Default: top=200, right=100, bottom=200, left=100
-t, --theme <name>         Theme name (default: blue)
    --show-frontmatter     Show YAML frontmatter in the first image (default: hidden)
    --help                 Show help message

### Padding Options

You can customize the padding (margins) around the content in two ways:

1. **Single value** - applies to all sides:
   ```bash
   node generate.js --input note.md --padding 100
   ```
   This sets 100px padding on all sides (top, right, bottom, left).

2. **Four values** - specify each side individually:
   ```bash
   node generate.js --input note.md --padding 50,80,120,80
   ```
   Format: `top,right,bottom,left` (in pixels)

Default padding: top=200px, right=100px, bottom=200px, left=100px

## Supported Markdown Features

The renderer supports:

- **Headings** (H1-H6) - Styled with elegant theme fonts
- **Paragraphs** - Automatic text wrapping with CJK support
- **Lists** - Ordered and unordered with proper indentation
- **Code blocks** - Styled with callout-like background, border, and matching font size
- **Blockquotes** - Styled with left border
- **Obsidian Callouts** - Fully styled callouts with icons and colors (note, warning, success, tip, etc.)
- **YAML Frontmatter** - Optional display in first image (use `--show-frontmatter`)
- **Line breaks** - Preserved spacing
- **Chinese/Japanese/Korean** - Full CJK character support
- **Mixed language** - Seamless rendering of English + CJK text

### Obsidian Callout Support

The renderer fully supports Obsidian callouts with proper styling and icons:

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

Supported callout types:
- `note`, `abstract`, `summary`, `tldr`
- `info`, `todo`
- `tip`, `hint`, `important`
- `success`, `check`, `done`
- `question`, `help`, `faq`
- `warning`, `caution`, `attention`
- `failure`, `fail`, `missing`
- `danger`, `error`
- `bug`
- `example`
- `quote`, `cite`

Each callout type has its own color scheme and icon for visual distinction.

## Content Splitting

When Markdown content exceeds the specified height:

- The renderer automatically creates multiple images
- Each image is dynamically sized to fit its content (up to max height)
- Images are numbered sequentially (e.g., `output-1.png`, `output-2.png`)
- Splitting happens at natural content boundaries when possible
- No unnecessary white space at the bottom of images

## Installation and Dependencies

Before first use, install Node.js dependencies:

```bash
cd scripts
npm install
npx playwright install chromium
```

Required packages:
- `marked` - Markdown parsing to HTML
- `playwright` - Browser automation for screenshots

**Note**: The first time you run `npx playwright install chromium`, it will download the Chromium browser (~160MB). This is a one-time setup.

## Workflow

1. **User requests conversion**: "Convert note.md to an image"
2. **Check dependencies**: Ensure npm packages are installed (auto-checks on first run)
3. **Prepare parameters**: 
   - Input file path
   - Size preferences (default: 1440x2400px)
   - Whether to show frontmatter (default: no)
4. **Execute script**: Run generate.js with parameters
5. **Verify output**: Check that images were created successfully
6. **Return paths**: Provide user with file locations

## Example Conversation Flow

**User**: "Convert my note.md to an image"

**Assistant actions**:
1. Verify note.md exists
2. Run: `cd scripts && node generate.js --input ../note.md`
3. Check output directory (`../converted_images`) for generated images
4. Report: "Generated 3 images: converted_images/output-1.png, ..."

## Troubleshooting

**Playwright not installed**: The script will automatically install Chromium on first run. If manual installation is needed, run `npx playwright install chromium` in the scripts directory.

**Browser download fails**: Check your internet connection. Playwright needs to download Chromium (~160MB) on first setup.

**Text rendering issues**: Playwright uses system fonts automatically. On macOS, it will use PingFang SC, Heiti SC for Chinese.

**Slow generation**: The first page takes longer as Playwright launches the browser. Subsequent pages in the same run are faster.

**Memory issues with large files**: Consider splitting the Markdown file or using smaller height values to create more, smaller images.

**Content truncated**: If content appears cut off, this usually indicates the pagination algorithm needs adjustment. The current version is optimized to prevent overflow.

## Performance Notes

- **First run**: Slower due to browser launch (~2-3 seconds overhead)
- **Subsequent pages**: Fast (~200-500ms per page)
- **Auto Playwright install**: First run automatically installs Chromium if needed

## Key Features

- **Optimized padding**: Top 200px, Bottom 200px for better visual balance
- **Dynamic height**: Images sized to actual content, no excess whitespace
- **Obsidian callouts**: Full support with icons and styling
- **Code blocks**: Styled to match callouts with consistent font sizes
- **Frontmatter control**: Show or hide YAML frontmatter (default: hidden)
- **Smart pagination**: Prevents content overflow and truncation
