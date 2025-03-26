# Deloitte Hackathon – AI-Enabled Institutional Intelligence Platform

## 📊 Project Overview

This repository supports a prototype AI tool designed for the Deloitte Higher Education Practice Hackathon. Our goal is to build an intelligent data pipeline and semantic interface to analyze public information about British Columbia post-secondary institutions and surface strategic insights for consulting teams.

The initial MVP will focus on rapidly answering one question:
- Which institutions share overlapping programs and are suitable for collaboration?

The final product will enable rapid answers to key questions such as:
- Which institutions are well-suited for a merger?
- Who offers trades programs or AI curriculum?
- Which colleges are aligned in goals and could collaborate?
- What programs have launched since 2022?
- What trends in student housing exist in BC?

---

## 🧩 What This Repository Contains

### 1. `deloitte_hackathon/` (Main App Code)
Contains scripts and logic to:
- Ingest and tag documents (PDFs and Excel files)
- Parse metadata (institution, document type, publication date)
- Extract structured knowledge (entities and relationships)
- Embed documents into a vector database
- Serve a semantic Q&A interface using LangChain

### 2. `venv/`
Local Python virtual environment (excluded from Git via `.gitignore`)

---

## 🗂️ Data Sources

### 🔹 Per-Institution Documents (PDF)
For each of the 10 institutions in BC, we include PDF copies of:
- Strategic Plan
- Financial Statement (2023–2024)
- Government Mandate Letter
- Course List

### 🔹 Province-Wide Datasets (Excel)
10 `.xlsx` datasets from the BC Data Catalogue include:
- FTE Enrolments – institutional capacity
- Operating Grants – funding per student insights
- Graduate Unemployment Rates – outcome effectiveness
- Student Headcount – regional reach
- Student Satisfaction – program quality proxy
- Student Housing Beds – infrastructure equity
- Capital Allowance – investment benchmarking
- Credentials Awarded – program output
- Institution Locations – mapping and clustering
- Tuition Fees – cost accessibility by region

---

## ⚙️ Ingestion Pipeline Steps

1. **Document Ingestion**  
   - Parse PDFs using `LangChain` with `PyMuPDF`
   - Read Excel files using `pandas`

2. **Metadata Extraction & Tagging**  
   - Automatically tag documents by type and content keywords

3. **Entity & Relationship Extraction**  
   - Use `spaCy` for Named Entity Recognition (NER)
   - Generate subject–predicate–object triples for knowledge graph

4. **Vector Embedding & Indexing**  
   - Split documents into semantic chunks
   - Embed and store in `FAISS` or `Pinecone` for fast retrieval

5. **Semantic Search Interface**  
   - Ask consultant-style questions and retrieve answers with citations

---

## 🚀 Getting Started

Clone this repo and activate the virtual environment:

```bash
git clone https://github.com/pidoko/deloitte_hackathon.git
cd deloitte_hackathon
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
