# Installation & Setup Guide

## ✅ Fixed Issues & Solutions

### Issue 1: Command Error
**Error:** `pip installrequirements.txt` (missing space)
**Solution:** Use `pip install -r requirements.txt`

### Issue 2: faiss-cpu Version
**Error:** `ERROR: Could not find a version that satisfies the requirement faiss-cpu==1.7.4`
**Solution:** Updated to `faiss-cpu>=1.8.0` (version 1.7.4 doesn't exist)

### Issue 3: OpenAI Version Conflict
**Error:** `langchain-openai 0.0.2 depends on openai>=1.6.1,<2.0.0` but had `openai==1.3.0`
**Solution:** Updated to `openai>=1.6.1,<2.0.0`

### Issue 4: LangChain Deprecation Warnings
**Warning:** Importing from `langchain.chat_models` is deprecated
**Solution:** Updated imports to use `langchain_community.chat_models`

## 📦 Installation Steps

### 1. Ensure Virtual Environment is Active
```bash
cd ai-market-analyst
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
pip list | grep -E "fastapi|uvicorn|openai|langchain|faiss"
```

Should show:
- fastapi (0.104.1)
- uvicorn (0.24.0)
- openai (>=1.6.1,<2.0.0)
- langchain (0.1.0)
- faiss-cpu (>=1.8.0)

### 4. Test Imports
```bash
python3 -c "from main import app; print('✅ All imports successful')"
```

## 🚀 Running the Application

### Backend
```bash
source venv/bin/activate
./run.sh
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (in another terminal)
```bash
cd ui
npm install
npm run dev
```

## 🔍 Troubleshooting

If you see deprecation warnings, they're harmless but you can verify everything works:
- All warnings are just deprecation notices, not errors
- The application will still work correctly
- Future versions may require updates

