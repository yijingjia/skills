#!/usr/bin/env node

/**
 * Markdown HTML Renderer
 * Renders Markdown with theme-based styling
 */

import { marked } from 'marked';
import { parseTheme } from './themeParser.js';
import path from 'path';
import fs from 'fs';

/**
 * Default theme name
 */
const DEFAULT_THEME = 'blue';

/**
 * Get padding from theme or use provided padding
 */
function getPadding(theme, providedPadding) {
  if (providedPadding) return providedPadding;
  
  return {
    top: theme.layout.paddingTop,
    right: theme.layout.paddingRight,
    bottom: theme.layout.paddingBottom,
    left: theme.layout.paddingLeft
  };
}

/**
 * Get default title for callout type
 */
function getDefaultCalloutTitle(type) {
  const titles = {
    note: 'Note',
    abstract: 'Abstract',
    summary: 'Summary',
    tldr: 'TL;DR',
    info: 'Info',
    todo: 'Todo',
    tip: 'Tip',
    hint: 'Hint',
    important: 'Important',
    success: 'Success',
    check: 'Check',
    done: 'Done',
    question: 'Question',
    help: 'Help',
    faq: 'FAQ',
    warning: 'Warning',
    caution: 'Caution',
    attention: 'Attention',
    failure: 'Failure',
    fail: 'Fail',
    missing: 'Missing',
    danger: 'Danger',
    error: 'Error',
    bug: 'Bug',
    example: 'Example',
    quote: 'Quote',
    cite: 'Cite'
  };
  return titles[type] || type.charAt(0).toUpperCase() + type.slice(1);
}

/**
 * Get icon for callout type
 */
function getCalloutIcon(type) {
  const icons = {
    note: '📝',
    abstract: '📋',
    summary: '📋',
    tldr: '📋',
    info: 'ℹ️',
    todo: '☑️',
    tip: '💡',
    hint: '💡',
    important: '🔥',
    success: '✅',
    check: '✅',
    done: '✅',
    question: '❓',
    help: '❓',
    faq: '❓',
    warning: '⚠️',
    caution: '⚠️',
    attention: '⚠️',
    failure: '❌',
    fail: '❌',
    missing: '❌',
    danger: '⚡',
    error: '⚡',
    bug: '🐛',
    example: '📖',
    quote: '💬',
    cite: '💬'
  };
  return icons[type] || '📌';
}

/**
 * Configure custom renderer for theme
 */
function configureRenderer(theme, baseUrl) {
  const renderer = new marked.Renderer();
  const h2Style = (theme && theme.layout && theme.layout.h2Style) || 'background';
  
  // Override image rendering to handle local paths
  renderer.image = function(href, title, text) {
    let finalHref = href;
    
    // Check if it's a relative local path (not starting with http/https/data)
    if (baseUrl && href && !href.startsWith('http') && !href.startsWith('data:') && !href.startsWith('file:')) {
      try {
        // Resolve absolute path
        const cleanBase = baseUrl.replace(/^file:\/\//, '');
        const absPath = path.resolve(cleanBase, href);
        
        // Read file and convert to base64
        if (fs.existsSync(absPath)) {
          const fileBuffer = fs.readFileSync(absPath);
          const ext = path.extname(absPath).toLowerCase().replace('.', '');
          const mimeType = ext === 'svg' ? 'image/svg+xml' : `image/${ext}`;
          const base64 = fileBuffer.toString('base64');
          finalHref = `data:${mimeType};base64,${base64}`;
        } else {
          console.warn(`Warning: Image file not found: ${absPath}`);
        }
      } catch (err) {
        console.warn(`Warning: Failed to load image ${href}: ${err.message}`);
      }
    }
    
    return `<img src="${finalHref}" alt="${text}" title="${title || ''}" />`;
  };

  // Override heading rendering to match theme style
  renderer.heading = function(text, level) {
    if (level === 1) {
      // H1: centered with special styling
      return `<h1>${text}</h1>\n`;
    } else if (level === 2) {
      // H2: configurable style
      if (h2Style === 'background') {
        return `<h2><span class="h2-bg">${text}</span></h2>\n`;
      } else {
        // Border-left style (or others) don't need the span wrapper for bg
        return `<h2>${text}</h2>\n`;
      }
    } else {
      return `<h${level}>${text}</h${level}>\n`;
    }
  };
  
  // Override blockquote rendering to support Obsidian callouts
  renderer.blockquote = function(quote) {
    // Check if this is an Obsidian callout
    // Two patterns:
    // 1. <p>[!type] title</p> followed by other content (lists, etc.)
    // 2. <p>[!type] title\ncontent in same paragraph</p>
    
    // Try pattern 1 first: separate title paragraph
    let calloutMatch = quote.match(/<p>\[!(\w+)\]\s*([^\n<]*?)<\/p>([\s\S]*)/);
    
    if (calloutMatch) {
      const [, type, title, restContent] = calloutMatch;
      const calloutType = type.toLowerCase();
      const calloutTitle = title.trim() || getDefaultCalloutTitle(calloutType);
      const calloutIcon = getCalloutIcon(calloutType);
      
      let cleanContent = restContent.trim();
      
      return `<div class="callout callout-${calloutType}">
  <div class="callout-title">
    <span class="callout-icon">${calloutIcon}</span>
    <span class="callout-title-text">${calloutTitle}</span>
  </div>
  <div class="callout-content">
${cleanContent}
  </div>
</div>\n`;
    }
    
    // Try pattern 2: title and content in same <p> tag
    calloutMatch = quote.match(/<p>\[!(\w+)\]\s*([^\n]*?)\n([\s\S]*?)<\/p>/);
    
    if (calloutMatch) {
      const [, type, title, content] = calloutMatch;
      const calloutType = type.toLowerCase();
      const calloutTitle = title.trim() || getDefaultCalloutTitle(calloutType);
      const calloutIcon = getCalloutIcon(calloutType);
      
      let cleanContent = content.trim();
      if (cleanContent && !cleanContent.startsWith('<')) {
        cleanContent = `<p>${cleanContent}</p>`;
      }
      
      return `<div class="callout callout-${calloutType}">
  <div class="callout-title">
    <span class="callout-icon">${calloutIcon}</span>
    <span class="callout-title-text">${calloutTitle}</span>
  </div>
  <div class="callout-content">
${cleanContent}
  </div>
</div>\n`;
    }
    
    // Regular blockquote
    return `<blockquote>\n${quote}</blockquote>\n`;
  };
  
  // Override code rendering
  renderer.code = function(code, language) {
    return `<pre><code class="language-${language || ''}">${code}</code></pre>\n`;
  };
  
  // Override list rendering
  renderer.list = function(body, ordered, start) {
    const type = ordered ? 'ol' : 'ul';
    const startAttr = (ordered && start !== 1) ? ` start="${start}"` : '';
    return `<${type}${startAttr}>\n${body}</${type}>\n`;
  };
  
  return renderer;
}

/**
 * Extract and format YAML front matter
 */
function extractFrontMatter(markdown) {
  const frontMatterMatch = markdown.match(/^---\n([\s\S]*?)\n---\n/);
  if (!frontMatterMatch) {
    return { frontMatter: null, content: markdown };
  }
  
  const frontMatterText = frontMatterMatch[1];
  const content = markdown.slice(frontMatterMatch[0].length);
  
  return { frontMatter: frontMatterText, content };
}

/**
 * Generate HTML from Markdown with theme styling
 */
export function generateMarkdownHTML(markdownContent, options = {}) {
  const { 
    width = 1440, 
    height = 2400, 
    padding, 
    showFrontmatter = false,
    themeName = DEFAULT_THEME 
  } = options;
  
  // Load theme configuration
  const theme = parseTheme(themeName);
  const finalPadding = getPadding(theme, padding);
  
  // Extract YAML front matter if present
  const { frontMatter, content } = extractFrontMatter(markdownContent);
  
  // Configure custom renderer
  const renderer = configureRenderer(theme, options.baseUrl);
  marked.setOptions({ renderer });
  
  // Convert Markdown to HTML
  const contentHTML = marked.parse(content);
  
  // Format front matter as styled block if present and showFrontmatter is true
  let frontMatterHTML = '';
  if (frontMatter && showFrontmatter) {
    frontMatterHTML = `<pre class="md-meta-block">${frontMatter}</pre>\n`;
  }
  
  // Build CSS for theme
  const css = buildThemeCSS({ width, height, padding: finalPadding, theme });
  
  // Build complete HTML document
  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Markdown to Image - ${theme.name}</title>
  <style>
${css}
  </style>
</head>
<body>
  <div class="container">
    <div class="content" id="write">
${frontMatterHTML}${contentHTML}
    </div>
  </div>
</body>
</html>`;
  
  return html;
}

/**
 * Build CSS for theme
 * Generates theme-based CSS from configuration
 */
function buildThemeCSS(options) {
  let { width, height, padding, theme } = options;
  
  // Extract theme values
  const colors = theme.colors;
  const fonts = theme.fonts;
  const layout = theme.layout;
  const callouts = theme.callouts;
  
  // Handle padding
  const paddingTop = typeof padding === 'object' ? padding.top : padding;
  const paddingRight = typeof padding === 'object' ? padding.right : padding;
  const paddingBottom = typeof padding === 'object' ? padding.bottom : padding;
  const paddingLeft = typeof padding === 'object' ? padding.left : padding;
  
  // Get layout values from theme
  const baseFontSize = layout.baseFontSize;
  const lineHeight = layout.lineHeight;
  const scale = layout.scaleFactor;
  const h1Scale = layout.h1Scale || 2.0;
  const headingAlign = layout.headingAlign || 'center';
  const h2Style = layout.h2Style || 'background';
  
  return `
/* Reset and base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --text-color: ${colors.textcolor || '#40464f'};
  --primary-color: ${colors.primarycolor || '#4870ac'};
  --bg-color: ${colors.background || '#ffffff'};
  --marker-color: ${colors.markercolor || '#a2b6d4'};
  --source-color: ${colors.sourcecolor || '#a8a8a9'};
  --highlight-color: ${colors.highlightcolor || '#ffffb5'}c2;
  --header-span-color: var(--primary-color);
  --block-bg-color: ${colors.blockbackground || '#f6f8fa'};
  --img-shadow-color: ${colors.imageshadow || '#e3e8f0'};
}

body {
  margin: 0;
  padding: 0;
  background: var(--bg-color);
  color: var(--text-color);
  font-family: '${fonts.body}', sans-serif;
  font-size: ${baseFontSize}px;
  line-height: ${lineHeight};
  word-spacing: 0px;
  letter-spacing: 0px;
  word-break: break-word;
  word-wrap: break-word;
  text-align: justify;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.container {
  width: ${width}px;
  min-height: ${height}px;
  background: var(--bg-color);
  padding: ${paddingTop}px ${paddingRight}px ${paddingBottom}px ${paddingLeft}px;
}

.content {
  width: 100%;
}

#write {
  max-width: 100%;
  color: var(--text-color);
  line-height: 1.6;
}

/* Strong - Primary color */
#write strong {
  color: var(--primary-color);
  font-weight: 600;
}

/* Links */
#write a {
  color: var(--primary-color);
  word-wrap: break-word;
  text-decoration: underline solid;
  text-underline-offset: ${4 * scale}px;
  text-decoration-thickness: ${1 * scale}px;
}

/* Mark/Highlight */
mark {
  background: var(--highlight-color);
  padding: ${1 * scale}px ${0.15 * 38}px;
  border-radius: ${1 * scale}px;
  color: inherit;
}

/* Paragraphs */
#write p {
  font-size: ${baseFontSize}px;
  padding-top: ${0.2 * baseFontSize}px;
  padding-bottom: ${0.2 * baseFontSize}px;
  margin: 0;
  margin-bottom: ${20 * scale}px;
  line-height: ${1.8 * baseFontSize}px;
  color: var(--text-color);
}

/* Headings */
#write h1,
#write h2,
#write h3,
#write h4,
#write h5,
#write h6 {
  font-family: '${fonts.header}', sans-serif;
  padding: 0px;
  color: var(--primary-color);
  line-height: 1.3;
}

#write h4,
#write h5,
#write h6 {
  font-weight: normal;
}

/* H1 - Styled */
#write h1 {
  text-align: ${headingAlign};
  font-size: ${h1Scale * baseFontSize}px;
  padding-top: ${0.9 * baseFontSize}px;
  margin-bottom: ${2.3 * baseFontSize}px;
  font-weight: 600;
}

/* H2 - Configurable Style */
#write h2 {
  font-size: ${1.5 * baseFontSize}px;
  margin: ${1.2 * baseFontSize}px 0 ${0.6 * baseFontSize}px 0;
  display: block;
  font-weight: 600;
  ${h2Style === 'border-left' ? `
    padding-left: ${0.5 * baseFontSize}px;
    border-left: ${0.2 * baseFontSize}px solid var(--primary-color);
    line-height: 1.3;
  ` : ''}
}

#write h2 .h2-bg {
  ${h2Style === 'background' ? `
    padding: ${1 * scale}px ${12.5 * scale}px;
    border-radius: ${4 * scale}px;
    background-color: var(--header-span-color);
    color: var(--bg-color);
    display: inline-block;
  ` : `
    background-color: transparent;
    color: var(--primary-color);
    padding: 0;
    display: inline;
  `}
}

#write h2 a {
  ${h2Style === 'background' ? `color: var(--bg-color);` : `color: var(--primary-color);`}
  text-decoration: underline;
  text-underline-offset: ${3 * scale}px;
  text-decoration-thickness: ${1.2 * scale}px;
}

/* H3 */
#write h3 {
  font-size: ${1.4 * baseFontSize}px;
  margin: ${1 * baseFontSize}px 0 ${1 * baseFontSize}px;
  font-weight: 500;
}

/* H4 */
#write h4 {
  font-size: ${1.2 * baseFontSize}px;
  margin: ${0.8 * baseFontSize}px 0 ${0.8 * baseFontSize}px;
}

/* H5 */
#write h5 {
  font-size: ${1.1 * baseFontSize}px;
  margin: ${0.6 * baseFontSize}px 0 ${0.6 * baseFontSize}px;
}

/* H6 */
#write h6 {
  font-size: ${1.1 * baseFontSize}px;
  margin: ${0.4 * baseFontSize}px 0 ${0.4 * baseFontSize}px;
}

/* Lists */
#write ul,
#write ol {
  margin-top: ${8 * scale}px;
  margin-bottom: ${8 * scale}px;
  padding-left: ${20 * scale}px;
}

#write ul {
  list-style-type: disc;
}

#write ol {
  list-style-type: decimal;
}

#write li {
  margin: ${0.4 * baseFontSize}px 0;
  line-height: ${1.7 * baseFontSize}px;
  color: var(--text-color);
}

#write ul li::marker {
  color: var(--marker-color);
  font-weight: bold;
}

#write ol li::marker {
  color: var(--marker-color);
  font-weight: bold;
}

#write ul ul {
  list-style-type: square;
}

/* Blockquotes */
#write blockquote {
  display: block;
  font-size: ${0.9 * baseFontSize}px;
  overflow: visible;
  border-left: ${3 * scale}px solid var(--primary-color);
  padding: ${15 * scale}px ${30 * scale}px ${15 * scale}px ${20 * scale}px;
  margin-bottom: ${20 * scale}px;
  margin-top: ${20 * scale}px;
  background: var(--block-bg-color);
}

/* Obsidian Callouts */
.callout {
  border-radius: ${8 * scale}px;
  padding: ${20 * scale}px;
  margin: ${20 * scale}px 0;
  background: var(--block-bg-color);
  border-left: ${4 * scale}px solid var(--primary-color);
  overflow: visible;
}

.callout-title {
  display: flex;
  align-items: center;
  gap: ${10 * scale}px;
  font-weight: 600;
  margin-bottom: ${10 * scale}px;
  color: var(--primary-color);
  font-size: ${1.05 * baseFontSize}px;
}

.callout-icon {
  font-size: ${1.2 * baseFontSize}px;
  line-height: 1;
}

.callout-title-text {
  flex: 1;
}

.callout-content {
  color: var(--text-color);
  font-size: ${0.95 * baseFontSize}px;
  line-height: 1.6;
}

.callout-content > *:last-child {
  margin-bottom: 0;
}

.callout-content p {
  margin-bottom: ${10 * scale}px;
}

/* Callout type colors - from theme configuration */
.callout-note {
  background: ${callouts.note ? `${callouts.note}1a` : 'rgba(72, 112, 172, 0.1)'};
  border-left-color: ${callouts.note || '#4870ac'};
}

.callout-note .callout-title {
  color: ${callouts.note || '#4870ac'};
}

.callout-abstract, .callout-summary, .callout-tldr {
  background: ${callouts.note ? `${callouts.note}1a` : 'rgba(72, 112, 172, 0.1)'};
  border-left-color: ${callouts.note || '#4870ac'};
}

.callout-abstract .callout-title,
.callout-summary .callout-title,
.callout-tldr .callout-title {
  color: ${callouts.note || '#4870ac'};
}

.callout-info {
  background: ${callouts.info ? `${callouts.info}1a` : 'rgba(72, 112, 172, 0.1)'};
  border-left-color: ${callouts.info || '#527da8'};
}

.callout-info .callout-title {
  color: ${callouts.info || '#527da8'};
}

.callout-todo {
  background: ${callouts.note ? `${callouts.note}1a` : 'rgba(72, 112, 172, 0.1)'};
  border-left-color: ${callouts.note || '#4870ac'};
}

.callout-todo .callout-title {
  color: ${callouts.note || '#4870ac'};
}

.callout-tip, .callout-hint, .callout-important {
  background: ${callouts.tip ? `${callouts.tip}1a` : 'rgba(66, 132, 133, 0.1)'};
  border-left-color: ${callouts.tip || '#428485'};
}

.callout-tip .callout-title,
.callout-hint .callout-title,
.callout-important .callout-title {
  color: ${callouts.tip || '#428485'};
}

.callout-success, .callout-check, .callout-done {
  background: ${callouts.success ? `${callouts.success}1a` : 'rgba(66, 132, 133, 0.1)'};
  border-left-color: ${callouts.success || '#428485'};
}

.callout-success .callout-title,
.callout-check .callout-title,
.callout-done .callout-title {
  color: ${callouts.success || '#428485'};
}

.callout-question, .callout-help, .callout-faq {
  background: ${callouts.question ? `${callouts.question}1a` : 'rgba(168, 134, 82, 0.1)'};
  border-left-color: ${callouts.question || '#a88652'};
}

.callout-question .callout-title,
.callout-help .callout-title,
.callout-faq .callout-title {
  color: ${callouts.question || '#a88652'};
}

.callout-warning, .callout-caution, .callout-attention {
  background: ${callouts.warning ? `${callouts.warning}1a` : 'rgba(168, 134, 82, 0.1)'};
  border-left-color: ${callouts.warning || '#a88652'};
}

.callout-warning .callout-title,
.callout-caution .callout-title,
.callout-attention .callout-title {
  color: ${callouts.warning || '#a88652'};
}

.callout-failure, .callout-fail, .callout-missing {
  background: ${callouts.failure ? `${callouts.failure}1a` : 'rgba(163, 79, 85, 0.1)'};
  border-left-color: ${callouts.failure || '#a34f55'};
}

.callout-failure .callout-title,
.callout-fail .callout-title,
.callout-missing .callout-title {
  color: ${callouts.failure || '#a34f55'};
}

.callout-danger, .callout-error {
  background: ${callouts.danger ? `${callouts.danger}1a` : 'rgba(163, 79, 85, 0.1)'};
  border-left-color: ${callouts.danger || '#a34f55'};
}

.callout-danger .callout-title,
.callout-error .callout-title {
  color: ${callouts.danger || '#a34f55'};
}

.callout-bug {
  background: ${callouts.bug ? `${callouts.bug}1a` : 'rgba(163, 79, 85, 0.1)'};
  border-left-color: ${callouts.bug || '#a34f55'};
}

.callout-bug .callout-title {
  color: ${callouts.bug || '#a34f55'};
}

.callout-example {
  background: ${callouts.example ? `${callouts.example}1a` : 'rgba(97, 79, 156, 0.1)'};
  border-left-color: ${callouts.example || '#614f9c'};
}

.callout-example .callout-title {
  color: ${callouts.example || '#614f9c'};
}

.callout-quote, .callout-cite {
  background: ${callouts.quote ? `${callouts.quote}1a` : 'rgba(168, 168, 169, 0.1)'};
  border-left-color: ${callouts.quote || '#a8a8a9'};
}

.callout-quote .callout-title,
.callout-cite .callout-title {
  color: ${callouts.quote || '#a8a8a9'};
}

/* Inline code */
#write code {
  color: var(--primary-color);
  font-size: ${0.94 * baseFontSize}px;
  font-weight: normal;
  word-wrap: break-word;
  padding: ${2 * scale}px ${4 * scale}px ${2 * scale}px;
  border-radius: ${3 * scale}px;
  margin: ${2 * scale}px;
  background-color: var(--block-bg-color);
  font-family: '${fonts.code}', monospace;
  word-break: break-all;
}

/* Code blocks */
#write pre {
  margin: ${1.5 * baseFontSize}px 0;
  background: rgba(72, 112, 172, 0.08);
  border-left: 4px solid var(--primary-color);
  border-radius: ${8 * scale}px;
  padding: ${1.5 * baseFontSize}px ${1.2 * baseFontSize}px;
  overflow-x: auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

#write pre code {
  color: #4f5467;
  font-family: '${fonts.code}', monospace;
  font-size: ${0.95 * baseFontSize}px;
  line-height: 1.6;
  background-color: transparent;
  padding: 0;
  margin: 0;
  border-radius: 0;
  display: block;
}

/* Images */
#write img {
  margin: 0 auto;
  max-width: 100%;
  display: block;
  filter: drop-shadow(var(--img-shadow-color) 0px ${6 * scale}px ${6 * scale}px);
  padding: ${1 * baseFontSize}px;
}

/* Tables */
#write table {
  display: table;
  text-align: justify;
  overflow-x: auto;
  border-collapse: collapse;
  border-spacing: 0px;
  font-size: ${1 * baseFontSize}px;
  margin: 0px 0px ${20 * scale}px;
  width: 100%;
}

#write table tr {
  border: 0;
  border-top: ${1 * scale}px solid #ccc;
}

#write table tr th,
#write table tr td {
  font-size: ${1 * baseFontSize}px;
  border: ${1 * scale}px solid #d9dfe4;
  padding: ${5 * scale}px ${10 * scale}px;
  text-align: justify;
}

#write table tr th {
  font-family: '${fonts.header}', sans-serif;
  text-align: center;
  font-weight: bold;
  color: var(--primary-color);
}

/* Horizontal rules */
hr {
  margin-top: ${20 * scale}px;
  margin-bottom: ${20 * scale}px;
  border: 0;
  border-top: ${2 * scale}px solid #eef2f5;
  border-radius: ${2 * scale}px;
}

/* Emphasis */
#write em {
  font-style: italic;
  padding: 0 ${3 * scale}px 0 0;
}

/* YAML Front Matter / Meta Block */
pre.md-meta-block {
  font-family: '${fonts.code}', monospace;
  color: var(--primary-color);
  background: #f6f8fa;
  padding: ${1.5 * baseFontSize}px;
  margin: ${-37 * scale}px 0 ${3.8 * baseFontSize}px;
  filter: drop-shadow(var(--img-shadow-color) 0px ${3 * scale}px ${3 * scale}px);
  font-size: ${0.9 * baseFontSize}px;
  line-height: ${1.4 * baseFontSize}px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* Task lists / Checkboxes */
#write .task-list-item {
  list-style-type: none;
}

#write .task-list-item input[type="checkbox"] {
  margin-right: ${0.5 * baseFontSize}px;
  width: ${1.0125 * baseFontSize}px;
  height: ${1.0125 * baseFontSize}px;
  vertical-align: middle;
  border: ${1 * scale}px solid var(--marker-color);
  border-radius: ${1.2 * baseFontSize}px;
  background-color: #fdfdfd;
  appearance: none;
  -webkit-appearance: none;
  position: relative;
}

#write .task-list-item input[type="checkbox"]:checked::before {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: bold;
  color: var(--primary-color);
  font-size: ${0.75 * baseFontSize}px;
  line-height: 1;
}
`;
}

/**
 * Generate HTML for single page (no fixed height)
 * Returns HTML string for one page with auto height
 */
export function generateSinglePageHTML(markdownContent, options = {}) {
  const { 
    width = 1440, 
    padding, 
    showFrontmatter = false,
    themeName = DEFAULT_THEME 
  } = options;
  
  // Load theme configuration
  const theme = parseTheme(themeName);
  const finalPadding = getPadding(theme, padding);
  
  // Extract YAML front matter if present
  const { frontMatter, content } = extractFrontMatter(markdownContent);
  
  // Configure custom renderer
  const renderer = configureRenderer(theme, options.baseUrl);
  marked.setOptions({ renderer });
  
  // Convert Markdown to HTML
  const contentHTML = marked.parse(content);
  
  // Format front matter as styled block if present and showFrontmatter is true
  let frontMatterHTML = '';
  if (frontMatter && showFrontmatter) {
    frontMatterHTML = `<pre class="md-meta-block">${frontMatter}</pre>\n`;
  }
  
  // Build CSS for theme
  const css = buildThemeCSS({ width, height: 0, padding: finalPadding, theme }); // Height 0 or ignored for single page
  
  // Use absolute path for base URL to ensure local images load correctly
  const baseUrlStr = options.baseUrl ? `<base href="file://${options.baseUrl}/">` : '';

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  ${baseUrlStr}
  <title>Markdown to Image - ${theme.name}</title>
  <style>
${css}
    /* Override container height for single page mode */
    .container {
      min-height: auto;
      height: auto;
      overflow: visible;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="content" id="write">
${frontMatterHTML}${contentHTML}
    </div>
  </div>
</body>
</html>`;
}
