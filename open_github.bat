@echo off
echo Opening GitHub setup pages...
echo.

echo Opening GitHub to create new repository...
start https://github.com/new

echo.
echo Instructions:
echo 1. Create a new repository named: youtube-downloader-gui
echo 2. Make it public
echo 3. Don't initialize with README (we already have one)
echo 4. Copy the repository URL when created
echo.
echo Then run these commands in this folder:
echo.
echo git remote add origin https://github.com/YOURUSERNAME/youtube-downloader-gui.git
echo git branch -M main  
echo git push -u origin main
echo.
echo After pushing, create a release at:
echo https://github.com/YOURUSERNAME/youtube-downloader-gui/releases/new
echo.
pause
