#!/usr/bin/env node
/**
 * 环境检测 + 自动安装 Playwright
 * 运行: node setup.js
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');

console.log('\n🔍 检测环境...\n');

// 检测 Node.js 版本
const nodeVersion = process.versions.node;
const [major] = nodeVersion.split('.').map(Number);
if (major < 16) {
  console.error(`❌ Node.js 版本过低 (${nodeVersion})，需要 16+`);
  console.error('   请升级 Node.js: https://nodejs.org');
  process.exit(1);
}
console.log(`✅ Node.js ${nodeVersion}`);

// 检测包管理器
let pkgManager = 'npm';
try {
  execSync('pnpm --version', { stdio: 'ignore' });
  pkgManager = 'pnpm';
} catch {
  try {
    execSync('yarn --version', { stdio: 'ignore' });
    pkgManager = 'yarn';
  } catch {}
}
console.log(`✅ 包管理器: ${pkgManager}`);

// 检测操作系统
const platform = process.platform;
const platformName = { darwin: 'macOS', win32: 'Windows', linux: 'Linux' }[platform] || platform;
console.log(`✅ 操作系统: ${platformName}`);

// 检测 Playwright 是否已安装
let playwrightInstalled = false;
try {
  require.resolve('playwright');
  playwrightInstalled = true;
  console.log('✅ Playwright 已安装');
} catch {
  console.log('⚠️  Playwright 未安装');
}

// 安装 Playwright
if (!playwrightInstalled) {
  console.log('\n📦 安装 Playwright...');
  const installCmd = pkgManager === 'pnpm'
    ? 'pnpm add playwright'
    : pkgManager === 'yarn'
    ? 'yarn add playwright'
    : 'npm install playwright';

  try {
    execSync(installCmd, { stdio: 'inherit' });
    console.log('✅ Playwright 安装完成');
  } catch (err) {
    console.error('❌ Playwright 安装失败');
    process.exit(1);
  }
}

// 检测 Chromium 是否已下载
let chromiumInstalled = false;
try {
  const { chromium } = require('playwright');
  // 尝试找到 chromium 可执行文件
  const executablePath = chromium.executablePath?.();
  if (executablePath && fs.existsSync(executablePath)) {
    chromiumInstalled = true;
  }
} catch {}

if (!chromiumInstalled) {
  console.log('\n🌐 下载 Chromium 浏览器（约 150MB，仅需一次）...');
  try {
    execSync('npx playwright install chromium', { stdio: 'inherit' });
    console.log('✅ Chromium 下载完成');
  } catch (err) {
    console.error('❌ Chromium 下载失败');
    console.error('   请手动运行: npx playwright install chromium');
    process.exit(1);
  }
} else {
  console.log('✅ Chromium 已就绪');
}

console.log('\n🎉 环境准备完成！\n');
console.log('运行提取脚本：');
console.log('  node scripts/extract.js <目标网站URL>\n');
console.log('示例：');
console.log('  node scripts/extract.js https://aptosnetwork.com\n');