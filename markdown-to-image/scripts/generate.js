#!/usr/bin/env node

/**
 * Markdown to Image Generator
 * Converts Markdown files to images using theme-based styling
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { generateSinglePageHTML } from './markdownRenderer.js';
import { chromium } from 'playwright';
import { execSync } from 'child_process';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Size presets for different platforms
 */
const SIZE_PRESETS = {
  default: { width: 1440, height: 2400 },
  'instagram-story': { width: 1080, height: 1920 },
  twitter: { width: 1200, height: 675 },
  wechat: { width: 900, height: 1600 }
};

/**
 * Check if Playwright browsers are installed by trying to launch
 */
async function checkPlaywrightInstalled() {
  try {
    // Try to launch browser to check if it's installed
    const browser = await chromium.launch({ headless: true });
    await browser.close();
    return true;
  } catch (error) {
    // If error message contains "Executable doesn't exist", browser is not installed
    if (error.message && error.message.includes("Executable doesn't exist")) {
      return false;
    }
    // For other errors, assume browser is installed but something else went wrong
    return true;
  }
}

/**
 * Install Playwright browsers if not already installed
 */
async function ensurePlaywrightInstalled() {
  const isInstalled = await checkPlaywrightInstalled();
  
  if (isInstalled) {
    return true;
  }
  
  console.log('📦 Playwright 浏览器未安装，正在安装...');
  console.log('   这只需要执行一次，请稍候...\n');
  
  try {
    execSync('npx playwright install chromium', {
      cwd: __dirname,
      stdio: 'inherit'
    });
    console.log('\n✓ Playwright 浏览器安装完成\n');
    return true;
  } catch (error) {
    console.error('✗ Playwright 浏览器安装失败:', error.message);
    console.error('   请手动运行: cd scripts && npx playwright install chromium');
    return false;
  }
}

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    input: null,
    output: null,  // Will be dynamically set based on input file location
    size: 'default',
    width: null,
    height: null,
    padding: null,  // Will use theme defaults if not specified
    showFrontmatter: false,  // Default: don't show frontmatter
    themeName: 'blue'  // Default theme
  };
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--input':
      case '-i':
        options.input = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--size':
      case '-s':
        options.size = args[++i];
        break;
      case '--width':
      case '-w':
        options.width = parseInt(args[++i], 10);
        break;
      case '--height':
      case '-h':
        options.height = parseInt(args[++i], 10);
        break;
      case '--padding':
      case '-p':
        const paddingValue = args[++i];
        if (paddingValue.includes(',')) {
          // Format: top,right,bottom,left
          const parts = paddingValue.split(',').map(p => parseInt(p.trim(), 10));
          options.padding = {
            top: parts[0] || 200,
            right: parts[1] || 100,
            bottom: parts[2] || 200,
            left: parts[3] || 100
          };
        } else {
          // Single value for all sides
          const p = parseInt(paddingValue, 10);
          options.padding = { top: p, right: p, bottom: p, left: p };
        }
        break;
      case '--show-frontmatter':
        options.showFrontmatter = true;
        break;
      case '--theme':
      case '-t':
        options.themeName = args[++i];
        break;
      case '--help':
        printHelp();
        process.exit(0);
        break;
    }
  }
  
  // Apply size preset if no custom dimensions
  if (!options.width || !options.height) {
    const preset = SIZE_PRESETS[options.size] || SIZE_PRESETS.default;
    options.width = options.width || preset.width;
    options.height = options.height || preset.height;
  }
  
  return options;
}

/**
 * Print help message
 */
function printHelp() {
  console.log(`
Markdown to Image Generator

Usage:
  node generate.js --input <file> [options]

Options:
  -i, --input <file>       Input Markdown file (required)
  -o, --output <dir>       Output directory (default: same as input file directory/converted_images)
  -s, --size <preset>      Size preset: default, instagram-story, twitter, wechat
  -w, --width <px>         Custom width in pixels
  -h, --height <px>        Height (max height per image) in pixels
  -p, --padding <value>    Padding in pixels (single value or top,right,bottom,left)
                            If not specified, uses theme default padding
  -t, --theme <name>       Theme name (default: blue)
      --show-frontmatter   Show YAML frontmatter in the first image (default: hidden)
      --help               Show this help message

Size Presets:
  default          1440 x 2400px  (General social media)
  instagram-story  1080 x 1920px  (Instagram stories)
  twitter          1200 x 675px   (Twitter images)
  wechat           900 x 1600px   (WeChat long images)

Examples:
  # Basic usage (creates converted_images/ in same directory as input)
  node generate.js --input note.md

  # Custom size
  node generate.js --input note.md --width 1200 --height 1600

  # Instagram story size
  node generate.js --input note.md --size instagram-story
  
  # Custom padding (all sides)
  node generate.js --input note.md --padding 100
  
  # Custom padding (top,right,bottom,left)
  node generate.js --input note.md --padding 100,80,100,80
  
  # Custom output directory (overrides default behavior)
  node generate.js --input note.md --output ./custom-output
`);
}

/**
 * Generate images using markdown renderer
 */
async function generateMarkdownImages(markdownContent, options) {
  const { width, height, padding, output, basename, themeName = 'blue' } = options;
  
  const { parseTheme } = await import('./themeParser.js');
  const theme = parseTheme(themeName);

  // Get padding from theme if not provided
  let finalPadding = padding;
  if (!finalPadding) {
    finalPadding = {
      top: theme.layout.paddingTop,
      right: theme.layout.paddingRight,
      bottom: theme.layout.paddingBottom,
      left: theme.layout.paddingLeft
    };
  }
  
  // Create output directory if it doesn't exist
  if (!fs.existsSync(output)) {
    fs.mkdirSync(output, { recursive: true });
  }
  
  // Generate single HTML page with all content
  const htmlContent = generateSinglePageHTML(markdownContent, {
    width,
    padding: finalPadding,
    showFrontmatter: options.showFrontmatter,
    themeName: themeName,
    baseUrl: options.baseUrl
  });
  
  // Launch browser - trust Playwright to find the executable
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 2 // High DPI for better quality
  });
  
  const files = [];
  
  try {
    const page = await context.newPage();
    
    // Set content
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    
    // Wait a bit for fonts to load
    await page.waitForTimeout(500);
    
    // Calculate split points in the browser context
    const { splitPoints, totalHeight } = await page.evaluate(({ height, padding }) => {
      const totalHeight = document.body.scrollHeight;
      console.log('Total Height:', totalHeight);
      
      const points = [0];
      let currentY = 0;
      
      // Get all text line rects and image rects
      const range = document.createRange();
      const treeWalker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const rects = [];
      let currentNode;
      
      while (currentNode = treeWalker.nextNode()) {
        if (currentNode.nodeValue.trim()) {
          range.selectNodeContents(currentNode);
          const rectsList = range.getClientRects();
          for (const r of rectsList) {
            rects.push({ top: r.top + window.scrollY, bottom: r.bottom + window.scrollY });
          }
        }
      }
      
      document.querySelectorAll('img').forEach(img => {
        const r = img.getBoundingClientRect();
        rects.push({ top: r.top + window.scrollY, bottom: r.bottom + window.scrollY });
      });
      
      // Sort rects by top
      rects.sort((a, b) => a.top - b.top);
      
      while (currentY < totalHeight) {
        let availableHeight;
        const remainingHeight = totalHeight - currentY;
        const pTop = padding && padding.top ? padding.top : 0;
        const pBottom = padding && padding.bottom ? padding.bottom : 0;
        
        const extraTop = (currentY > 0) ? pTop : 0;
        
        if (remainingHeight <= (height - extraTop)) {
            availableHeight = remainingHeight;
        } else {
            availableHeight = height - extraTop - pBottom;
        }
        
        if (availableHeight <= 0) {
            availableHeight = 100;
        }

        const idealCut = currentY + availableHeight;
        
        if (idealCut >= totalHeight) {
            points.push(totalHeight);
            break;
        }

        const searchStart = idealCut;
        const searchEnd = Math.max(currentY + 100, idealCut - 400); // 400px search window
        
        let bestCut = -1;
        
        // Identify rects that might be in the cutting zone
        const relevantRects = rects.filter(r => r.bottom > searchEnd && r.top < searchStart);
        
        // Scan for a safe cut point
        for (let y = searchStart; y >= searchEnd; y -= 2) {
          const hits = relevantRects.some(r => y >= r.top && y <= r.bottom);
          if (!hits) {
            bestCut = y;
            break;
          }
        }
        
        if (bestCut === -1) {
          bestCut = idealCut;
        }
        
        points.push(bestCut);
        currentY = bestCut;
      }
      
      return { splitPoints: points, totalHeight };
    }, { height, padding: finalPadding });
    
    console.log(`  ℹ️  Content height: ${totalHeight}px`);
    console.log(`  ℹ️  Split content into ${splitPoints.length - 1} pages based on content analysis`);
    
    // Generate screenshots for each segment
    for (let i = 0; i < splitPoints.length - 1; i++) {
      const start = splitPoints[i];
      const end = splitPoints[i+1];
      const segmentHeight = end - start;
      
      if (segmentHeight < 1) continue;
      
      const suffix = (splitPoints.length - 1) > 1 ? `-${i + 1}` : '';
      const outputPath = path.join(output, `${basename}${suffix}.png`);
      
      // Determine padding for this page
      const isFirstPage = (i === 0);
      const isLastPage = (i === splitPoints.length - 2);
      const addTop = (!isFirstPage && finalPadding) ? finalPadding.top : 0;
      const addBottom = (!isLastPage && finalPadding) ? finalPadding.bottom : 0;
      
      // Method: Resize viewport to match segment height, then translate content
      // This is more robust than scrolling + clipping for very long pages
      await page.setViewportSize({ width, height: Math.ceil(segmentHeight) });
      
      // Move content up so the desired segment starts at the top of the viewport
      await page.evaluate((y) => {
        document.body.style.transform = `translateY(-${y}px)`;
        // Force layout update
        document.body.offsetHeight;
      }, start);
      
      // Wait for any lazy loading or rendering catchup
      await page.waitForTimeout(50);
      
      // Capture the visible viewport
      const segmentHeightCeil = Math.ceil(segmentHeight);
      const contentBuffer = await page.screenshot({
        type: 'png',
        fullPage: false
      });
      
      // Post-process with Sharp: Add padding AND ensure fixed height
      // Initialize Sharp with the screenshot
      let image = sharp(contentBuffer);
      
      // Calculate total dimensions needed
      // 1. Current raw image height
      const currentHeight = segmentHeightCeil;
      
      // 2. Padding that MUST be added
      const pTop = (addTop > 0 && finalPadding) ? finalPadding.top : 0;
      const pBottom = (addBottom > 0 && finalPadding) ? finalPadding.bottom : 0;
      
      // 3. Calculate filler needed to reach target fixed height
      // Total height we have so far (content + padding)
      const contentWithPadding = currentHeight + pTop + pBottom;
      
      // How much more to add to bottom to reach target height?
      // If content is already larger than target (unlikely but possible), don't force crop, just keep it.
      let fillerHeight = 0;
      if (height && contentWithPadding < height) {
        fillerHeight = height - contentWithPadding;
      }
      
      // 4. Single extend operation
      if (pTop > 0 || pBottom > 0 || fillerHeight > 0) {
        image = image.extend({
            top: pTop,
            bottom: pBottom + fillerHeight, // Add padding AND filler together
            left: 0,
            right: 0,
            background: theme.colors.background || '#ffffff'
        });
      }
      
      // Save the final image
      await image.toFile(outputPath);
      
      files.push(outputPath);
    }
    
  } finally {
    await browser.close();
  }
  
  return files;
}

/**
 * Generate images from Markdown
 */
async function generate(options) {
  // Validate input file
  if (!options.input) {
    console.error('Error: Input file is required. Use --input <file>');
    process.exit(1);
  }
  
  if (!fs.existsSync(options.input)) {
    console.error(`Error: Input file not found: ${options.input}`);
    process.exit(1);
  }
  
  // Read Markdown content
  const markdownContent = fs.readFileSync(options.input, 'utf-8');
  const inputBasename = path.basename(options.input, path.extname(options.input));
  
  // Set output directory to be in the same directory as input file
  const inputDir = path.dirname(options.input);
  const outputDir = path.join(inputDir, 'converted_images');
  
  // Override options.output with the new path
  options.output = outputDir;
  
  console.log(`📄 Input: ${options.input}`);
  console.log(`📐 Size: ${options.width} x ${options.height}px`);
  console.log(`🎨 Theme: ${options.themeName || 'default'}`);
  console.log(`📁 Output: ${outputDir}`);
  console.log('');
  
  try {
    console.log('Processing...');
    
    const files = await generateMarkdownImages(markdownContent, {
      width: options.width,
      height: options.height,
      padding: options.padding,
      output: options.output,
      basename: inputBasename,
      showFrontmatter: options.showFrontmatter,
      themeName: options.themeName,
      baseUrl: path.dirname(path.resolve(options.input))
    });
    
    console.log(`  ✓ Generated ${files.length} image(s)`);
    files.forEach(file => console.log(`    - ${file}`));
    
    console.log('');
    console.log(`✨ Done! Generated ${files.length} image(s) in ${options.output}`);
    
  } catch (error) {
    console.error(`  ✗ Error: ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

/**
 * Main entry point
 */
async function main() {
  try {
    // Ensure Playwright is installed before proceeding
    const isInstalled = await ensurePlaywrightInstalled();
    if (!isInstalled) {
      process.exit(1);
    }
    
    const options = parseArgs();
    await generate(options);
  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { generate, parseArgs };
