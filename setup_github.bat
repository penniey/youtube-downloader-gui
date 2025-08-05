@echo off
echo Setting up GitHub repository for YouTube Downloader GUI...
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed or not in PATH!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

REM Initialize git repository if not already done
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

REM Add all files
echo Adding files to Git...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: YouTube Downloader GUI with dark theme"

echo.
echo Repository setup complete!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run the following commands:
echo.
echo    git remote add origin https://github.com/yourusername/youtube-downloader-gui.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Don't forget to create a release with the executable file!
pause
