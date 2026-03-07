# ESG Investment Research Assistant
A RAG-based AI agent that answers questions about Australian ESG documents using LLMs and Vector Databases.

## 🌐 Live Demo
https://esg-investment-agent.streamlit.app/

## 🛠 Tech Stack
- **LLM**: OpenAI GPT-4o-mini + text-embedding-3-small
- **Vector DB**: Pinecone
- **Frontend**: Streamlit
- **Deployment**: Streamlit Cloud
- **Planned**: FastAPI, Redis cache, reranking
## 🏗 Architecture

**Offline Pipeline** (`parse_pdf.py` + `ingest.py`)
```
PDF → Text Extraction → Chunking → OpenAI Embedding → Pinecone (vector + metadata)
```

**Online Pipeline** (`query.py` + `app.py`)
```
User Query → OpenAI Embedding → Pinecone Top-K Search → GPT-4o-mini → Answer
```

## 🚀 Run Locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your API keys:
```
   OPENAI_API_KEY=XXXXX
   PINECONE_API_KEY=XXXXX
```
4. Run the app: `streamlit run app.py`

## 📄 Data Sources
- **BHP** - GHG Emissions Calculation Methodology 2025
- **Woodside Energy** - Climate and Sustainability Summary 2025
- **Commonwealth Bank (CBA)** - Climate Report 2024
- **Rio Tinto** - Sustainability Glossary 2025