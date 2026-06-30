@echo off
echo ============================================
echo   Alpha Bot — Setup
echo ============================================
echo.

:: Create virtual environment
echo [1/4] Creating virtual environment...
python -m venv venv
echo Done.

:: Activate and install dependencies
echo [2/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo Done.

:: Create data directories
echo [3/4] Creating directories...
if not exist data mkdir data
if not exist data\stock mkdir data\stock
if not exist data\backups mkdir data\backups
if not exist logs mkdir logs
echo Done.

:: Copy env example if .env doesn't exist
echo [4/4] Setting up config...
if not exist .env (
    copy .env.example .env
    echo Created .env — please fill in your values before starting the bot.
) else (
    echo .env already exists, skipping.
)

echo.
echo ============================================
echo   Setup complete!
echo   1. Edit .env with your credentials
echo   2. Run: start_bot.bat
echo ============================================
pause
