# YouTube Downloader GUI

A simple, user-friendly GUI wrapper for yt-dlp (youtube-dl) built with Python's tkinter.

![YouTube Downloader GUI](https://via.placeholder.com/800x600/1e1e1e/ffffff?text=YouTube+Downloader+GUI)

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

## 💻 For Developers

### Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- yt-dlp (will be installed automatically if missing)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/youtube-downloader-gui.git
   cd youtube-downloader-gui
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the application:
   ```bash
   python youtube_gui.py
   ```

2. Enter a YouTube URL in the URL field
3. Choose your download options:
   - **Quality**: Select video quality (best, 720p, 480p, etc.)
   - **Audio only**: Check this to download audio in various formats
4. Select download location (defaults to Downloads folder)
5. Click "Download" to start downloading

## 🔧 Features Explained

### URL Input
- Paste YouTube URLs directly or use the "Paste" button to get URL from clipboard
- Supports individual videos

### Download Options
- **Quality Selection**: Choose from various video qualities or "best" for highest available
- **Audio Only**: Downloads audio in multiple formats (MP3, M4A, WebM)

### Video Information
- Click "Get Info" to see video details before downloading:
  - Title, uploader, duration, view count, upload date

### Progress Tracking
- Real-time output log shows download progress
- Progress bar indicates when operations are running
- Status messages keep you informed

## 🌐 Supported Sites

This GUI supports all sites that yt-dlp supports, including but not limited to:
- YouTube
- Vimeo
- Facebook
- Twitter
- Instagram
- TikTok
- And many more!

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

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## 📄 License

This project is open source. Please respect YouTube's terms of service and only download content you have permission to download.

## ⭐ Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x600/1e1e1e/ffffff?text=Dark+Theme+Interface)

### Download in Progress
![Download Progress](https://via.placeholder.com/800x600/1e1e1e/ffffff?text=Download+Progress)

## 🔗 Links

- [Download Latest Release](../../releases/latest)
- [Report Issues](../../issues)
- [View Source Code](../../)
