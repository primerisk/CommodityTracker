@echo off
setlocal
echo ==========================================
echo Precious Metal Tracker - GitHub Deployment
echo ==========================================
echo.

echo Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads
    pause
    exit /b
)

echo Initializing Repository...
if not exist .git (
    git init
    echo Repository initialized.
) else (
    echo Repository already initialized.
)

echo.
echo Adding files...
git add .

echo.
echo Committing files...
git commit -m "Automated update of Precious Metal Tracker" || echo Nothing to commit or working tree clean.

echo.
echo ==========================================
set "default_url=https://github.com/primerisk/CommodityTracker.git"
echo Default Repository: %default_url%
echo (Note: Using the root .git URL derived from your request)
echo ==========================================
echo.
set /p "repo_url=Enter GitHub Repository URL (Press Enter for default): "
if "%repo_url%"=="" set "repo_url=%default_url%"

echo.
echo Setting remote origin to %repo_url%...
git remote remove origin >nul 2>&1
git remote add origin %repo_url%

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
echo NOTE: If this is a new repository, this will succeed.
echo If the remote has unrelated history, you might need to force push or pull first.
git push -u origin main

echo.
echo Deployment Script Finished.
pause
