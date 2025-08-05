#!/usr/bin/env python3
"""
Test script to debug FFmpeg issues with yt-dlp
"""

import subprocess
import sys

def test_ffmpeg():
    """Test FFmpeg detection"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        print("✅ FFmpeg is available")
        print(f"Version: {result.stdout.split('\\n')[0]}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found")
        return False

def test_yt_dlp():
    """Test yt-dlp detection"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, check=True)
        print("✅ yt-dlp is available")
        print(f"Version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp not found")
        return False

def test_conversion_command():
    """Test the exact command we're using"""
    if not test_ffmpeg() or not test_yt_dlp():
        return
    
    print("\\n🔧 Testing MP3 conversion command...")
    
    # Test URL (a short video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (short and reliable)
    
    # The command our GUI would use
    cmd = [
        'yt-dlp',
        '--format', 'best[acodec!=mp3]/bestaudio',
        '-x', '--audio-format', 'mp3', '--audio-quality', '0',
        '--no-playlist',
        '-o', 'test_output.%(ext)s',
        '--simulate',  # Don't actually download, just simulate
        test_url
    ]
    
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Command would work!")
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("❌ Command failed!")
        print(f"Error: {e.stderr}")

if __name__ == "__main__":
    print("YouTube Downloader - FFmpeg Test")
    print("=" * 40)
    test_conversion_command()
