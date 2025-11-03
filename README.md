# 🤖 AI Market Analyst

A production-ready **RAG (Retrieval-Augmented Generation)** application built with FastAPI, React, and Google Gemini API. This system enables intelligent document analysis, question-answering, text summarization, and structured data extraction using advanced AI techniques.

## 🎯 Features

- **📚 Document Q&A**: Ask questions about your documents using RAG pipeline
- **📝 Text Summarization**: Generate concise summaries from long documents
- **🔍 Structured Data Extraction**: Extract JSON data from unstructured text using AI
- **🧠 Local Embeddings**: Uses `sentence-transformers` for offline document processing
- **💾 Chroma Vector Store**: Persistent vector database for efficient retrieval
- **🛡️ Security**: Built-in prompt injection guardrails
- **🎨 Modern UI**: Beautiful, responsive React frontend with Tailwind CSS

## 🏗️ System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React UI  │────▶│   FastAPI    │────▶│   Gemini    │
│  (Frontend) │     │   (Backend)  │     │    API      │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │    Chroma    │
                    │ Vector Store │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Local       │
                    │  Embeddings  │
                    └──────────────┘
```

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** (for frontend)
- **Google Gemini API Key** ([Get it here](https://aistudio.google.com/app/apikey))
- **pip** and **npm** package managers

## 🚀 Quick Start

### Step 1: Clone & Setup

```bash
# Navigate to project directory
cd ai-market-analyst

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
nano .env  # or use your preferred editor
```

**Required `.env` configuration:**

```env
GEMINI_API_KEY=your_actual_gemini_key_here
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_STORE_TYPE=chroma
ENABLE_GUARDRAILS=True
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

**Important:** Replace `your_actual_gemini_key_here` with your actual Gemini API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Step 3: Add Documents (Optional)

Place your documents (`.txt`, `.pdf`, `.docx`, `.md`) in `data/documents/` directory. The vector store will be built automatically on first server start.

### Step 4: Start Backend Server

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Start the backend server
python main.py

# OR use the run script
chmod +x run.sh
./run.sh
```

**Backend will be available at:** `http://localhost:8000`

**Test the backend:**
```bash
curl http://localhost:8000/api/v1/health
```

### Step 5: Start Frontend (New Terminal)

```bash
# Navigate to UI directory
cd ui

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

## 📡 API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Question Answering
```bash
POST /api/v1/qa
Content-Type: application/json

{
  "question": "What is the company name?"
}
```

**Response:**
```json
{
  "answer": "The company name is Innovate Inc.",
  "source_documents": [
    {
      "page_content": "Innovate Inc. is a leading provider..."
    }
  ]
}
```

### Text Summarization
```bash
POST /api/v1/summary
Content-Type: application/json

{
  "text": "Long text here...",
  "max_length": 500
}
```

**Response:**
```json
{
  "summary": "Concise summary of the text..."
}
```

### Structured Data Extraction
```bash
POST /api/v1/extract
Content-Type: application/json

{
  "text": "Innovate Inc. reported $12 million in revenue for Q3 2025.",
  "schema": {
    "company": "string",
    "revenue": "number",
    "period": "string"
  }
}
```

**Response:**
```json
{
  "data": {
    "company": "Innovate Inc.",
    "revenue": 12000000,
    "period": "Q3 2025"
  }
}
```

## 🔍 Structured Data Extraction

The extraction tool uses advanced prompt engineering to reliably extract structured JSON from unstructured text.

### How It Works

1. **Schema Definition**: Define your desired output structure as a JSON schema
2. **AI Processing**: Gemini API processes the text using structured prompts
3. **JSON Parsing**: Automatic parsing with fallback error handling
4. **Validation**: Ensures all schema fields are present (uses `null` for missing values)

### Example Request

```json
{
  "text": "Innovate Inc. reported $12 million in revenue for Q3 2025. Competitors include FutureFlow and Synergy Systems.",
  "schema": {
    "company": "string",
    "revenue": "number",
    "period": "string",
    "competitors": "array"
  }
}
```

### Example Response

```json
{
  "data": {
    "company": "Innovate Inc.",
    "revenue": 12000000,
    "period": "Q3 2025",
    "competitors": ["FutureFlow", "Synergy Systems"]
  }
}
```

### Prompt Design Strategy

The extraction prompt is designed for **reliability**:

- **Explicit JSON Schema**: Provides clear structure expectations
- **Strict Formatting Rules**: Instructs model to output only valid JSON
- **Null Handling**: Explicit instructions for missing data
- **Validation**: Multiple parsing attempts with error recovery

## ⚙️ Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | - | **Yes** |
| `LLM_PROVIDER` | LLM provider (currently gemini) | `gemini` | No |
| `LLM_MODEL` | Chat model for Q&A and summarization | `gemini-2.5-flash` | No |
| `EMBEDDING_MODEL` | Local embedding model (offline) | `all-MiniLM-L6-v2` | No |
| `VECTOR_STORE_TYPE` | Vector store backend | `chroma` | No |
| `ENABLE_GUARDRAILS` | Enable prompt injection protection | `True` | No |
| `CHUNK_SIZE` | Text chunk size for processing | `1000` | No |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` | No |

## 🧪 Testing

### Backend Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/

# Run specific test
pytest tests/test_guardrails.py -v
```

### Manual API Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Q&A test
curl -X POST http://localhost:8000/api/v1/qa \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the company name?"}'

# Extract test
curl -X POST http://localhost:8000/api/v1/extract \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Innovate Inc. reported $12 million in revenue for Q3 2025.",
    "schema": {"company": "string", "revenue": "number", "period": "string"}
  }'
```

## 🎨 Frontend Components

- **QATool**: Interactive Q&A interface with source document display
- **SummaryTool**: Text summarization with file upload support
- **ExtractTool**: JSON schema-based extraction with example templates

## 🔒 Security Features

- **Prompt Injection Detection**: Regex-based patterns to detect malicious inputs
- **Input Validation**: Length limits and format checking
- **CORS Configuration**: Configurable for production deployment
- **Environment Variables**: Secure API key management

## 📝 Key Features

- **Uses Google Gemini API** (free student API available) - No OpenAI credits required!
- **Local Embeddings**: Uses `sentence-transformers` with `all-MiniLM-L6-v2` (runs completely offline for embeddings)
- **Chroma Vector Store**: Persistent, local vector database (no cloud dependencies)
- **Model**: `gemini-2.5-flash` (fast and efficient, default) or `gemini-2.5-pro` (more powerful)
- **Automatic Model Selection**: System automatically finds best available Gemini model
- **Vector store is built automatically** on first run
- **Documents are chunked** with configurable size (default: 1000 chars, 200 overlap)
- **Guardrails can be disabled** by setting `ENABLE_GUARDRAILS=False` in `.env`
- **Easy model switching**: Change `LLM_MODEL` in `.env` to switch between flash/pro
- **Offline Operation**: Only Gemini API calls require internet; embeddings and vector store work offline

## 🐛 Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not configured" error**
   - Ensure `.env` file exists in the root directory
   - Check that `GEMINI_API_KEY` is set (not `your_actual_gemini_key_here`)
   - Verify `.env` file is in the same directory as `config.py`
   - Get your API key from: https://aistudio.google.com/app/apikey
   - Restart the server after updating `.env`

2. **Import errors / Module not found**
   - Ensure virtual environment is activated: `source venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Verify `python-dotenv` is installed: `pip list | grep python-dotenv`

3. **Vector store not found or empty**
   - Place documents in `data/documents/` directory
   - Supported formats: `.txt`, `.pdf`, `.docx`, `.md`
   - Restart the server to rebuild vector store
   - Check console logs for vector store creation messages

4. **Frontend not connecting to backend**
   - Verify backend is running on port 8000: `curl http://localhost:8000/api/v1/health`
   - Check browser console for CORS errors
   - Ensure `vite.config.js` proxy is configured correctly

5. **Port already in use**
   - Backend: Change port in `run.sh` or use: `uvicorn main:app --port 8001`
   - Frontend: Change port in `ui/vite.config.js` or use: `npm run dev -- --port 3001`

6. **Permission denied errors**
   - Make scripts executable: `chmod +x setup.sh run.sh`
   - On Windows, use Git Bash or WSL

7. **npm install fails**
   - Ensure Node.js 16+ is installed: `node --version`
   - Try clearing cache: `npm cache clean --force`
   - Delete `node_modules` and `package-lock.json`, then reinstall

8. **pip install errors / dependency conflicts**
   - **chromadb errors**: Ensure Python 3.8+ and updated pip: `pip install --upgrade pip`
   - **sentence-transformers**: May take time to download model on first run (offline after first download)
   - **Wrong command**: Use `pip install -r requirements.txt` (note the space and `-r`)
   - If issues persist: `pip install --upgrade pip` then retry

9. **"404 models/gemini-1.5-flash is not found" error**
   - **Cause**: Old model names (`gemini-1.5-flash`) are deprecated
   - **Solution**: Update `.env` with `LLM_MODEL=gemini-2.5-flash`
   - The system automatically tries to find the best available model
   - Check available models by looking at server startup logs

10. **Extraction returns error or invalid JSON**
    - Ensure schema is valid JSON object (not array)
    - Check that text contains extractable information
    - Verify API key is valid and has quota
    - Check server logs for detailed error messages

### Debug Mode

Enable detailed logging by checking console output:
- Backend logs show vector store initialization
- Frontend console shows API request/response details
- Check browser Network tab for API errors

## 📄 Project Structure

```
ai-market-analyst/
├── chains/
│   ├── extraction_chain.py    # Structured data extraction
│   ├── gemini_helper.py       # Gemini API integration
│   ├── qa_chain.py            # Question answering chain
│   └── summary_chain.py       # Text summarization chain
├── data/
│   ├── documents/             # Place your documents here
│   └── vectorstore/           # Chroma vector store (auto-created)
├── ingestion/
│   ├── document_loader.py      # Document loading utilities
│   ├── text_processor.py      # Text chunking
│   └── vector_store.py        # Chroma vector store management
├── router/
│   └── routes.py              # FastAPI routes
├── utils/
│   └── guardrails.py          # Security guardrails
├── ui/
│   └── src/
│       ├── components/         # React components
│       └── App.jsx             # Main app component
├── tests/                      # Test files
├── .env.example                # Environment template
├── config.py                   # Configuration
├── main.py                     # FastAPI application
└── requirements.txt            # Python dependencies
```

## ✅ Submission Ready Checklist

- [x] **Backend Implementation**
  - [x] FastAPI server with all endpoints functional
  - [x] Gemini API integration working
  - [x] Chroma vector store with local embeddings
  - [x] Structured data extraction chain validated
  - [x] Error handling and validation implemented

- [x] **Frontend Implementation**
  - [x] React UI with all three tools
  - [x] Professional styling with Tailwind CSS
  - [x] Error handling and loading states
  - [x] Responsive design

- [x] **Integration**
  - [x] All API endpoints connected
  - [x] Frontend-backend communication working
  - [x] Vector store initialization validated
  - [x] Document ingestion pipeline tested

- [x] **Documentation**
  - [x] Comprehensive README.md
  - [x] API documentation
  - [x] Configuration guide
  - [x] Troubleshooting section
  - [x] Case study document

- [x] **Testing**
  - [x] Extraction endpoint tested with sample data
  - [x] Q&A endpoint validated
  - [x] Summary endpoint verified
  - [x] Health check working

## 📚 Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ for the Agentic AI Residency Project**
