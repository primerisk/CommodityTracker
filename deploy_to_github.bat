@echo off
echo ==========================================
echo Precious Metal Tracker - GitHub Deployment
echo ==========================================
echo.

echo Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads
    echo and allow it to add to your PATH during installation.
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
git commit -m "Initial commit of Precious Metal Tracker"

echo.
echo ==========================================
echo Please create a NEW repository on GitHub.
echo Copy the HTTPS URL (e.g., https://github.com/username/repo.git)
echo ==========================================
echo.
set /p repo_url="Enter GitHub Repository URL: "

echo.
echo Adding remote origin...
git remote add origin %repo_url%

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo Deployment Complete!
pause
