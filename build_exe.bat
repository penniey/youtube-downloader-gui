@echo off
echo Building YouTube Downloader GUI executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller.
        pause
        exit /b 1
    )
)

echo Building executable...
pyinstaller --windowed --onefile --name "YouTube Downloader" --distpath "./dist" --workpath "./build" youtube_gui.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable created in: dist\YouTube Downloader.exe
echo.
pause
