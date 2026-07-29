#!/bin/bash

# Family Tree Application Setup Script
# This script sets up the development environment for the Family Tree application

echo "🌳 Family Tree Application Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python installed: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "ℹ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "✓ Pip upgraded"
echo ""

# Install requirements
echo "📚 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
echo "⚙️ Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///family.db
EOF
    echo "✓ .env file created"
else
    echo "ℹ .env file already exists"
fi
echo ""

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p static/uploads
mkdir -p logs
echo "✓ Directories created"
echo ""

# Initialize database
echo "🗄️ Initializing database..."
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✓ Database initialized")
EOF
echo ""

# Display completion message
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "🎯 Next steps:"
echo "1. Activate virtual environment (if not already):"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the application:"
echo "   python app.py"
echo ""
echo "3. Open your browser and go to:"
echo "   http://localhost:5000"
echo ""
echo "4. Create a test account to get started!"
echo ""
echo "📖 For more information, see README.md"
echo ""
