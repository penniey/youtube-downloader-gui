@echo off
echo Preparing GitHub Release for YouTube Downloader GUI...
echo.

REM Check if executable exists
if not exist "dist\YouTube Downloader.exe" (
    echo Executable not found! Please run build_exe.bat first.
    pause
    exit /b 1
)

REM Create release folder
if not exist "release" mkdir release

REM Copy executable to release folder
echo Copying executable to release folder...
copy "dist\YouTube Downloader.exe" "release\YouTube-Downloader-GUI.exe"

REM Create release notes
echo Creating release notes...
echo YouTube Downloader GUI - v1.0.0 > release\RELEASE_NOTES.txt
echo. >> release\RELEASE_NOTES.txt
echo ## What's New >> release\RELEASE_NOTES.txt
echo - Beautiful dark theme with purple accents >> release\RELEASE_NOTES.txt
echo - Easy-to-use GUI for yt-dlp >> release\RELEASE_NOTES.txt
echo - Support for multiple video qualities >> release\RELEASE_NOTES.txt
echo - Audio-only downloads in multiple formats >> release\RELEASE_NOTES.txt
echo - Real-time download progress >> release\RELEASE_NOTES.txt
echo - Video information preview >> release\RELEASE_NOTES.txt
echo - Automatic dependency management >> release\RELEASE_NOTES.txt
echo. >> release\RELEASE_NOTES.txt
echo ## Installation >> release\RELEASE_NOTES.txt
echo 1. Download YouTube-Downloader-GUI.exe >> release\RELEASE_NOTES.txt
echo 2. Run the executable - no installation required! >> release\RELEASE_NOTES.txt
echo. >> release\RELEASE_NOTES.txt
echo ## System Requirements >> release\RELEASE_NOTES.txt
echo - Windows 10/11 >> release\RELEASE_NOTES.txt
echo - Internet connection for downloading videos >> release\RELEASE_NOTES.txt
echo. >> release\RELEASE_NOTES.txt
echo ## Note >> release\RELEASE_NOTES.txt
echo This is a portable executable - no installation required! >> release\RELEASE_NOTES.txt

echo.
echo Release preparation complete!
echo.
echo Files in release folder:
echo - YouTube-Downloader-GUI.exe (Main executable)
echo - RELEASE_NOTES.txt (Release notes)
echo.
echo To create a GitHub release:
echo 1. Go to your GitHub repository
echo 2. Click "Releases" -> "Create a new release"
echo 3. Tag: v1.0.0
echo 4. Title: YouTube Downloader GUI v1.0.0
echo 5. Upload the files from the 'release' folder
echo 6. Use the content from RELEASE_NOTES.txt as description
echo.
pause
