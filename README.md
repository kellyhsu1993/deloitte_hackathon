
# Deloitte Hackathon – AI-Enabled Institutional Insight Engine

This project builds a prototype knowledge graph and semantic search engine by extracting structured insights from public documents across 10 BC post-secondary institutions. It supports strategic planning, benchmarking, and consultant-facing intelligence.

---

## Project Pipeline Overview

### Phase 1: Ingest + Tag Top 40 Documents
- Focused on 4 core PDFs per institution (40 total):
  - Strategic Plan
  - Financial Statement
  - Government Mandate Letter
  - Courses List
- PDFs processed page-by-page using LangChain
- Output:
  - `documents.json` – full page content + metadata
  - `pdf_metadata.json` – metadata only

---

### Phase 2: Build Knowledge Graph (In Progress)
- Extract structured (subject–predicate–object) triples using LLMs
- Each page of text is analyzed using GPT-3.5 via OpenAI API
- Output:
  - `triples.jsonl` – one JSON triple per line

---

## Repository Contents

| File / Folder           | Purpose |
|-------------------------|---------|
| `ingest.py`             | Loads PDFs and exports text/metadata as LangChain `Document` objects |
| `extract_triples.py`    | Extracts triples from `documents.json` using GPT-3.5 and saves to `triples.jsonl` |
| `.env`                  | (ignored) Store your OpenAI API key locally as `OPENAI_API_KEY=sk-...` |
| `documents.json`        | Extracted content + metadata per page |
| `pdf_metadata.json`     | Summary metadata for each page |
| `triples.jsonl`         | Triple output ready for graph import or semantic indexing |
| `requirements.txt`      | Python dependencies |

---

## API Setup

Create a `.env` file (not tracked in Git) and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-key-here
```

---

## Running the Pipeline

### 1. Ingest PDF Documents
```bash
python ingest.py --root . --export
```

### 2. Extract Triples
```bash
python extract_triples.py --input documents.json --output triples.jsonl
```

Progress bar + logging included. Skips empty/short pages automatically.

---

## Sample Triple Output

```json
{
  "subject": "Selkirk College",
  "predicate": "offers",
  "object": "Renewable Energy Diploma",
  "institution": "Selkirk College",
  "source": "Selkirk Strategic Plan.pdf"
}
```

---

## Next Steps

- Chunk + embed text for semantic search (Phase 3)
- Streamlit QA interface for consultant queries (Phase 4)
- Optional: Load triples into Neo4j for graph visualizations

---

## Notes

- LLM-powered extraction optimized to run on a $62 OpenAI/OpenRouter token budget
- Modular codebase — easy to swap in Claude or local LLMs
- Clean JSON formats ready for use in knowledge graphs or search tools

---

## Team

This prototype was developed by Team 2 for the Deloitte Vancouver hackathon in March 2025.
