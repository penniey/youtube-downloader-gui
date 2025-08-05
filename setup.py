#!/usr/bin/env python3
"""
Setup script for YouTube Downloader GUI
This script will install required dependencies and check if everything is working.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version OK: {sys.version}")
    return True

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print("✓ tkinter is available")
        return True
    except ImportError:
        print("✗ tkinter is not available")
        print("Please install tkinter:")
        print("  - On Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  - On CentOS/RHEL: sudo yum install tkinter")
        print("  - On Windows: tkinter should be included with Python")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    # Install yt-dlp
    print("Installing yt-dlp...")
    if install_package("yt-dlp"):
        print("✓ yt-dlp installed successfully")
    else:
        print("✗ Failed to install yt-dlp")
        print("Trying to install youtube-dl as fallback...")
        if install_package("youtube-dl"):
            print("✓ youtube-dl installed successfully")
        else:
            print("✗ Failed to install youtube-dl")
            return False
    
    return True

def test_installation():
    """Test if everything is working"""
    print("\nTesting installation...")
    
    # Test yt-dlp
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✓ yt-dlp is working: {result.stdout.strip()}")
        downloader_ok = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try youtube-dl
        try:
            result = subprocess.run(['youtube-dl', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✓ youtube-dl is working: {result.stdout.strip()}")
            downloader_ok = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Neither yt-dlp nor youtube-dl is working")
            downloader_ok = False
    
    # Test FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        ffmpeg_version = result.stdout.split('\n')[0]
        print(f"✓ FFmpeg is working: {ffmpeg_version}")
        ffmpeg_ok = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg not found (required for audio conversion)")
        print("  Install FFmpeg for MP3 conversion support:")
        print("  • Chocolatey: choco install ffmpeg")
        print("  • Winget: winget install FFmpeg")
        print("  • Manual: https://ffmpeg.org/download.html")
        ffmpeg_ok = False
    
    return downloader_ok, ffmpeg_ok

def main():
    """Main setup function"""
    print("YouTube Downloader GUI - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check tkinter
    if not check_tkinter():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed! Please install dependencies manually:")
        print("pip install yt-dlp")
        sys.exit(1)
    
    # Test installation
    downloader_ok, ffmpeg_ok = test_installation()
    
    if not downloader_ok:
        print("\nSetup failed! Please install dependencies manually:")
        print("pip install yt-dlp")
        sys.exit(1)
    elif not ffmpeg_ok:
        print("\n⚠ Setup completed with warnings!")
        print("FFmpeg is not installed - audio conversion will not work.")
        print("Video downloads will work normally.")
        print("\nTo enable audio conversion (MP3), install FFmpeg:")
        print("• Chocolatey: choco install ffmpeg")
        print("• Winget: winget install FFmpeg") 
        print("• Manual: https://ffmpeg.org/download.html")
    else:
        print("\n✓ Setup completed successfully!")
        print("All features including audio conversion are available!")
    
    print("\nYou can now run the GUI with:")
    print("  python youtube_gui.py")
    print("or double-click run_gui.bat on Windows")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
