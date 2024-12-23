@echo off
echo Installing NVM for Windows...
winget install CoreyButler.NVMForWindows

echo Installing Node.js 18.x LTS...
nvm install 18.20.2
nvm use 18.20.2

echo Node.js version:
node --version

echo NPM version:
npm --version

pause