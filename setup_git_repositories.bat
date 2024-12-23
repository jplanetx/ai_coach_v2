@echo off
REM Navigate to the project directory
cd /d "C:\Projects\ai_coach_v2"

REM Initialize Git repository
git init

REM Add README
copy NUL README.md
type README.md

REM Add all files
git add .

REM Create initial commit
git commit -m "Initial commit for AI Coach V2"

REM Prompt for GitHub username
set /p github_username="Enter your GitHub username: "

REM Create GitHub repository
gh repo create ai_coach_v2 --public --source=. --remote=origin

REM Create GitLab repository
glab project create --name ai_coach_v2 --public

REM Add GitLab remote
git remote add gitlab https://gitlab.com/%github_username%/ai_coach_v2.git

REM Push to both GitHub and GitLab
git push -u origin main
git push -u gitlab main

echo Repositories created and pushed successfully!
pause
