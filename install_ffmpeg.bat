@echo off
echo Installing FFmpeg for audio conversion support...
echo.

REM Check if Chocolatey is available
where choco >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Chocolatey to install FFmpeg...
    choco install ffmpeg -y
    if %ERRORLEVEL% == 0 (
        echo ✓ FFmpeg installed successfully via Chocolatey!
        goto :success
    )
)

REM Check if Winget is available
where winget >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Winget to install FFmpeg...
    winget install FFmpeg
    if %ERRORLEVEL% == 0 (
        echo ✓ FFmpeg installed successfully via Winget!
        goto :success
    )
)

REM Check if Scoop is available
where scoop >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Scoop to install FFmpeg...
    scoop install ffmpeg
    if %ERRORLEVEL% == 0 (
        echo ✓ FFmpeg installed successfully via Scoop!
        goto :success
    )
)

echo No package manager found. Please install FFmpeg manually:
echo 1. Go to https://ffmpeg.org/download.html
echo 2. Download the Windows build
echo 3. Extract and add to your PATH
echo.
echo Or install a package manager first:
echo • Chocolatey: https://chocolatey.org/install
echo • Winget: Included with Windows 10/11
echo • Scoop: https://scoop.sh/
goto :end

:success
echo.
echo FFmpeg is now installed! You can now use audio conversion features.
echo Restart the YouTube Downloader GUI to use the new functionality.

:end
echo.
pause
