#!/usr/bin/env node

/**
 * Theme Parser - Extract colors and fonts from theme-factory theme files
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Parse a theme file from local themes folder
 * @param {string} themeName - Name of the theme (e.g., 'blue')
 * @returns {Object} Theme configuration with colors, fonts, layout, and callouts
 */
export function parseTheme(themeName) {
  // Find theme file in local themes folder
  const themesPath = path.join(__dirname, '..', 'themes');
  
  // Try JSON first
  const jsonPath = path.join(themesPath, `${themeName}.json`);
  if (fs.existsSync(jsonPath)) {
    try {
      const content = fs.readFileSync(jsonPath, 'utf-8');
      const theme = JSON.parse(content);
      
      // Ensure required structure exists with defaults
      return validateAndFillDefaults(theme, themeName);
    } catch (error) {
      throw new Error(`Failed to parse theme JSON '${themeName}': ${error.message}`);
    }
  }

  // Fallback to legacy MD format if JSON doesn't exist
  const mdPath = path.join(themesPath, `${themeName}.md`);
  if (fs.existsSync(mdPath)) {
    return parseLegacyMdTheme(mdPath, themeName);
  }

  throw new Error(`Theme '${themeName}' not found (checked .json and .md in ${themesPath})`);
}

/**
 * Validate theme object and fill missing values with defaults
 */
function validateAndFillDefaults(theme, themeName) {
  const defaults = {
    name: themeName,
    colors: {},
    fonts: {
      header: 'Arial Bold',
      body: 'Arial',
      code: 'JetBrains Mono, Courier New, Monaco, Menlo'
    },
    layout: {
      baseFontSize: 38,
      lineHeight: 1.6,
      scaleFactor: 2.16,
      paddingTop: 200,
      paddingRight: 100,
      paddingBottom: 200,
      paddingLeft: 100,
      h1Scale: 2.0,
      headingAlign: 'center',
      h2Style: 'background' // 'background' or 'border-left'
    },
    callouts: {},
    description: ''
  };

  // Deep merge would be better, but simple spread is enough for this flat structure
  return {
    ...defaults,
    ...theme,
    colors: { ...defaults.colors, ...theme.colors },
    fonts: { ...defaults.fonts, ...theme.fonts },
    layout: { ...defaults.layout, ...theme.layout },
    callouts: { ...defaults.callouts, ...theme.callouts }
  };
}

/**
 * Legacy Markdown Theme Parser
 * @deprecated
 */
function parseLegacyMdTheme(themePath, themeName) {
  const content = fs.readFileSync(themePath, 'utf-8');
  
  // Parse theme content
  const theme = {
    name: themeName,
    colors: {},
    fonts: {},
    layout: {},
    callouts: {},
    description: ''
  };
  
  // Extract description (first paragraph after title)
  const descMatch = content.match(/^# .+\n\n(.+)/m);
  if (descMatch) {
    theme.description = descMatch[1].trim();
  }
  
  // Extract colors - look for hex codes with labels
  const colorSection = content.match(/## Color Palette([\s\S]*?)(?=##|$)/);
  if (colorSection) {
    const colorLines = colorSection[1].split('\n');
    colorLines.forEach(line => {
      // Match patterns like "- **Deep Navy**: `#1a2332` - Primary background color"
      const match = line.match(/\*\*([^*]+)\*\*:\s*`(#[0-9a-fA-F]{6})`/);
      if (match) {
        const [, label, hex] = match;
        // Normalize label to camelCase key
        const key = label.toLowerCase().replace(/\s+/g, '');
        theme.colors[key] = hex;
      }
    });
  }
  
  // Extract fonts
  const fontSection = content.match(/## Typography([\s\S]*?)(?=##|$)/);
  if (fontSection) {
    const fontLines = fontSection[1].split('\n');
    fontLines.forEach(line => {
      const headerMatch = line.match(/\*\*Headers\*\*:\s*(.+)/);
      const bodyMatch = line.match(/\*\*Body Text\*\*:\s*(.+)/);
      const codeMatch = line.match(/\*\*Code Font\*\*:\s*(.+)/);
      
      if (headerMatch) {
        theme.fonts.header = headerMatch[1].trim();
      }
      if (bodyMatch) {
        theme.fonts.body = bodyMatch[1].trim();
      }
      if (codeMatch) {
        theme.fonts.code = codeMatch[1].trim();
      }
    });
  }
  
  // Extract layout settings
  const layoutSection = content.match(/## Layout([\s\S]*?)(?=##|$)/);
  if (layoutSection) {
    const layoutLines = layoutSection[1].split('\n');
    layoutLines.forEach(line => {
      const baseFontMatch = line.match(/\*\*Base Font Size\*\*:\s*`(\d+)`/);
      const lineHeightMatch = line.match(/\*\*Line Height\*\*:\s*`([\d.]+)`/);
      const scaleMatch = line.match(/\*\*Scale Factor\*\*:\s*`([\d.]+)`/);
      const paddingTopMatch = line.match(/\*\*Default Padding Top\*\*:\s*`(\d+)`/);
      const paddingRightMatch = line.match(/\*\*Default Padding Right\*\*:\s*`(\d+)`/);
      const paddingBottomMatch = line.match(/\*\*Default Padding Bottom\*\*:\s*`(\d+)`/);
      const paddingLeftMatch = line.match(/\*\*Default Padding Left\*\*:\s*`(\d+)`/);
      
      if (baseFontMatch) theme.layout.baseFontSize = parseInt(baseFontMatch[1]);
      if (lineHeightMatch) theme.layout.lineHeight = parseFloat(lineHeightMatch[1]);
      if (scaleMatch) theme.layout.scaleFactor = parseFloat(scaleMatch[1]);
      if (paddingTopMatch) theme.layout.paddingTop = parseInt(paddingTopMatch[1]);
      if (paddingRightMatch) theme.layout.paddingRight = parseInt(paddingRightMatch[1]);
      if (paddingBottomMatch) theme.layout.paddingBottom = parseInt(paddingBottomMatch[1]);
      if (paddingLeftMatch) theme.layout.paddingLeft = parseInt(paddingLeftMatch[1]);
    });
  }
  
  // Extract callout colors
  const calloutSection = content.match(/## Callout Colors([\s\S]*?)(?=##|$)/);
  if (calloutSection) {
    const calloutLines = calloutSection[1].split('\n');
    calloutLines.forEach(line => {
      const match = line.match(/\*\*([^*]+)\*\*:\s*`(#[0-9a-fA-F]{6})`/);
      if (match) {
        const [, label, hex] = match;
        const key = label.toLowerCase().replace(/\s+/g, '');
        theme.callouts[key] = hex;
      }
    });
  }
  
  return validateAndFillDefaults(theme, themeName);
}

/**
 * Get list of available themes from local themes folder
 * @returns {string[]} Array of theme names
 */
export function listThemes() {
  const themesPath = path.join(__dirname, '..', 'themes');
  
  if (!fs.existsSync(themesPath)) {
    return [];
  }
  
  const files = fs.readdirSync(themesPath);
  const themes = new Set();
  
  files.forEach(file => {
    if (file.endsWith('.json')) {
      themes.add(file.replace('.json', ''));
    } else if (file.endsWith('.md')) {
      themes.add(file.replace('.md', ''));
    }
  });
  
  return Array.from(themes).sort();
}


/**
 * Map theme colors to rendering roles
 * @param {Object} colors - Color object from theme
 * @returns {Object} Mapped colors for rendering
 */
export function mapColorsForRendering(colors) {
  const colorKeys = Object.keys(colors);
  
  return {
    background: colors[colorKeys[0]] || '#ffffff',
    primary: colors[colorKeys[1]] || '#333333',
    secondary: colors[colorKeys[2]] || '#666666',
    accent: colors[colorKeys[3]] || '#999999',
    text: colors[colorKeys[3]] || '#000000',
  };
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const themeName = process.argv[2];
  
  if (!themeName) {
    console.log('Available themes:');
    listThemes().forEach(theme => console.log(`  - ${theme}`));
    process.exit(0);
  }
  
  try {
    const theme = parseTheme(themeName);
    console.log(JSON.stringify(theme, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}
