<div align="center">
  
# CoreProtect Generator

**A lightweight, cross-platform UI generator for Minecraft CoreProtect Commands.**  
**一款轻量级、跨平台的 Minecraft CoreProtect 指令生成器。**

[![Build PC](https://github.com/bentianjia/coreprotect_command_auto/actions/workflows/build-pc.yml/badge.svg)](https://github.com/bentianjia/coreprotect_command_auto/actions)
[![Build Android](https://github.com/bentianjia/coreprotect_command_auto/actions/workflows/build-android.yml/badge.svg)](https://github.com/bentianjia/coreprotect_command_auto/actions)

[**👇 立即下载 (Download Now) 👇**](https://github.com/bentianjia/coreprotect_command_auto/actions)  
*(自动跳转到最新打包的下载页面)*

#### ⚠Warning / 警告
此项目由AI辅助完成

</div>

---

## 🌟 Features / 特性

- 🖥️ **Cross-Platform / 跨平台支持**: Available on Windows (Electron) and Android (Capacitor). 支持 Windows 和 Android 双端运行。
- ⚡ **Code Synchronization / 代码同步**: The core logic is purely HTML/JS driven, ensuring seamless feature parity across PC and Mobile. 核心逻辑采用纯 HTML/JS，确保 PC 和移动端功能完美同步。
- 📦 **Cloud Build / 云端打包**: Fully automated GitHub Actions pipeline. Push the code, and GitHub will compile both `.exe` and `.apk` files for you! 全自动 GitHub Actions 流水线，只需推送代码，云端即会自动为您生成 `.exe` 和 `.apk` 文件！

---

## 🚀 Quick Start / 快速开始

### Download Pre-built Versions / 下载预编译版本
Navigate to the **[Actions / Releases](https://github.com/bentianjia/coreprotect_command_auto/actions)** tab in this repository to download the latest `.exe` or `.apk` artifacts from the cloud build.  
请前往本仓库的 **[Actions / Releases](https://github.com/bentianjia/coreprotect_command_auto/actions)** 页面，下载由云端自动生成的最新 `.exe` 或 `.apk` 文件。

### Run Locally (PC) / 本地运行（电脑端）
```bash
# Install dependencies / 安装依赖
npm install

# Start the application / 启动应用
npm start

# Build the portable exe / 打包便携版 exe
npm run build
```

### Build Locally (Android) / 本地打包（安卓端）
To build the Android APK on your local machine, you need **Android Studio** installed.  
在本地打包 APK 需要安装 **Android Studio**。

```bash
# Sync HTML assets to Android project / 同步网页代码到安卓工程
npm run sync:android

# Open Android Studio to build / 打开 Android Studio 进行打包
npx cap open android
```

---

## 🛠️ Tech Stack / 技术栈
- UI & Logic: HTML5, CSS3, JavaScript
- PC Wrapper: Electron, Electron-builder
- Mobile Wrapper: Capacitor

## 📄 License / 开源协议
ISC License



