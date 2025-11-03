#!/bin/bash

echo "Setting up AI Market Analyst..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create directories
mkdir -p data/documents data/vectorstore

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created from .env.example"
    else
        cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
VECTOR_STORE_TYPE=faiss
ENABLE_GUARDRAILS=True
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EOF
        echo "✅ .env file created with default values"
    fi
    echo "⚠️  IMPORTANT: Please update .env with your GEMINI_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Verify python-dotenv installation
echo "Verifying python-dotenv installation..."
pip show python-dotenv > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ python-dotenv is installed"
else
    echo "⚠️  Installing python-dotenv..."
    pip install python-dotenv
fi

echo ""
echo "Setup complete ✅"
echo ""
echo "Next steps:"
echo "1. Update .env with your GEMINI_API_KEY (get it from: https://aistudio.google.com/app/apikey)"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Place documents in data/documents/ (optional)"
echo "4. Start backend: ./run.sh"
echo "5. In another terminal, start frontend: cd ui && npm install && npm run dev"

