# AI--Research-Knowledge_Assistant

## What this project does
- Upload PDF files
- Extract text and chunk it
- Store chunks in ChromaDB
- Search semantically
- Ask questions with Groq LLM
- Summarize documents
- Compare documents
- Classify documents with TensorFlow
- Show basic analytics

## Setup
1. Create a virtual environment
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`
4. Add your Groq API key
5. Run:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Docs
Open:
- http://127.0.0.1:8000/docs

## Notes
- This is a simple version for understanding.
- The TensorFlow classifier here is a demo model. For a final submission, replace it with a real labeled dataset.
