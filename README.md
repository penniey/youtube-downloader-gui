# YouTube Downloader GUI

A simple, user-friendly GUI wrapper for yt-dlp (youtube-dl) built with Python's tkinter.

## 🚀 Quick Start (No Installation Required)

**Download the ready-to-use executable:**

📥 **[Download YouTube Downloader.exe](../../releases/latest)** (Windows)

Simply download and run - no Python installation required!

## ✨ Features

- **🎨 Modern Dark Theme**: Beautiful purple-themed interface
- **📱 Easy-to-use interface**: No command line knowledge required
- **📹 Multiple format options**: Download in various video qualities or audio-only
- **⏱️ Real-time progress**: See download progress and output in real-time
- **ℹ️ Video information**: Get video details before downloading
- **📁 Custom download location**: Choose where to save your downloads
- **🔧 Automatic dependency installation**: The app can install yt-dlp if missing
- **🎵 Audio formats**: MP3, M4A, WebM support

## 🌐 Supported Sites

This GUI supports all sites that yt-dlp supports, including but not limited to:
- YouTube
- Vimeo
- Facebook
- Twitter
- Instagram
- TikTok
- And more!

## 📦 Building Your Own Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Use the provided build script:
   ```bash
   # Windows
   build_exe.bat
   
   # Or manually:
   pyinstaller --windowed --onefile --name "YouTube Downloader" --icon=icon.ico youtube_gui.py
   ```

The executable will be created in the `dist` folder.

## 📄 License

This project is open source. Please respect YouTube's terms of service and only download content you have permission to download.
