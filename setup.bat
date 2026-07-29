@echo off
REM Family Tree Application Setup Script for Windows
REM This script sets up the development environment for the Family Tree application

echo.
echo 🌳 Family Tree Application Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python installed: 
python --version
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ℹ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo ✓ Pip upgraded
echo.

REM Install requirements
echo 📚 Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✓ Dependencies installed
) else (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Create .env file if it doesn't exist
echo ⚙️ Setting up environment configuration...
if not exist ".env" (
    (
        echo FLASK_APP=app.py
        echo FLASK_ENV=development
        echo SECRET_KEY=dev-secret-key-change-in-production
        echo DATABASE_URL=sqlite:///family.db
    ) > .env
    echo ✓ .env file created
) else (
    echo ℹ .env file already exists
)
echo.

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "static\uploads" mkdir static\uploads
if not exist "logs" mkdir logs
echo ✓ Directories created
echo.

REM Initialize database
echo 🗄️ Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✓ Database initialized')"
echo.

REM Display completion message
echo ==================================================
echo ✅ Setup Complete!
echo ==================================================
echo.
echo 🎯 Next steps:
echo 1. Virtual environment is activated
echo.
echo 2. Run the application:
echo    python app.py
echo.
echo 3. Open your browser and go to:
echo    http://localhost:5000
echo.
echo 4. Create a test account to get started!
echo.
echo 📖 For more information, see README.md
echo.

pause
