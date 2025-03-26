import os
import json
import logging
from typing import List, Dict
import spacy
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Setup logging
log_filename = f"llm_extraction_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_filename, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"LLM input/output logs will be saved to: {log_filename}")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Setup LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt for extracting triples
triplet_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Extract all subject–predicate–object relationships from the following text.

Return a list of JSON objects in this exact format:
[
  {{ "subject": "...", "predicate": "...", "object": "..." }},
  ...
]

Text:
{text}

Triples:
"""
)
triplet_chain = LLMChain(llm=llm, prompt=triplet_prompt)

# Text splitter
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

def extract_triples(text: str) -> List[Dict[str, str]]:
    try:
        response = triplet_chain.run(text=text).strip()
        logger.info("\n=== CHUNK START ===\n%s\n--- LLM Response ---\n%s\n=== CHUNK END ===\n", text, response)

        parsed = json.loads(response)

        # Handle case where LLM returns a single dict instead of list
        if isinstance(parsed, dict):
            parsed = [parsed]

        if isinstance(parsed, list) and all(
            isinstance(t, dict) and "subject" in t and "predicate" in t and "object" in t for t in parsed
        ):
            return parsed
        else:
            logger.warning("Parsed response missing expected triple structure.")
    except Exception as e:
        logger.warning(f"LLM extraction failed: {e}")

    return []

def process_documents(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        logger.error(f"Input file does not exist: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    documents = [Document(page_content=item["content"], metadata=item["metadata"]) for item in raw_data]
    all_triples = []

    for i, doc in enumerate(tqdm(documents, desc="Extracting Triples")):
        text = doc.page_content.strip()
        if not text or len(text) < 100:
            continue

        chunks = text_splitter.split_text(text)
        logger.info(f"Processing page {i + 1}/{len(documents)} with {len(chunks)} chunks")

        for chunk in chunks:
            triples = extract_triples(chunk)
            for triple in triples:
                triple["institution"] = doc.metadata.get("institution", "Unknown")
                triple["source"] = doc.metadata.get("source_file", "Unknown")
                all_triples.append(triple)

    # Deduplicate triples
    unique_triples = [dict(t) for t in {tuple(sorted(d.items())) for d in all_triples}]

    with open(output_path, "w", encoding="utf-8") as f:
        for triple in unique_triples:
            f.write(json.dumps(triple) + "\n")

    logger.info(f"Extracted {len(unique_triples)} unique triples and saved to {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract relationship triples from documents.json")
    parser.add_argument("--input", default="documents.json", help="Path to the input documents.json")
    parser.add_argument("--output", default="triples.jsonl", help="Path to output triples file (.jsonl)")

    args = parser.parse_args()
    process_documents(args.input, args.output)
