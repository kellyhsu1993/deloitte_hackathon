import os
import json
import logging
from typing import List
from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def ingest_pdfs_from_directory(root_path: str) -> List[Document]:
    """
    Ingest all PDF files from institution-specific subdirectories and enrich them with metadata.

    Parameters:
        root_path (str): Path to the root directory containing one subdirectory per institution.

    Returns:
        List[Document]: A list of LangChain Document objects with attached metadata.
    """
    all_documents = []

    if not os.path.isdir(root_path):
        raise ValueError(f"Provided root path does not exist or is not a directory: {root_path}")

    for institution_name in os.listdir(root_path):
        if institution_name.startswith(".") or institution_name == "venv":
            continue
        
        institution_path = os.path.join(root_path, institution_name)

        if not os.path.isdir(institution_path):
            logger.debug(f"Skipping non-directory item: {institution_path}")
            continue

        logger.info(f"Processing institution: {institution_name}")

        for filename in os.listdir(institution_path):
            if not filename.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(institution_path, filename)
            if not os.path.isfile(file_path):
                logger.warning(f"Skipping non-file: {file_path}")
                continue

            try:
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                doc_type = classify_document_type(filename)

                for page in pages:
                    page.metadata.update({
                        "institution": institution_name,
                        "source_file": filename,
                        "doc_type": doc_type,
                        "content_type": "PDF"
                    })

                all_documents.extend(pages)
                logger.info(f"Ingested {len(pages)} pages from {filename}")

            except Exception as e:
                logger.error(f"Failed to process file {file_path}: {e}")

    return all_documents


def classify_document_type(filename: str) -> str:
    """
    Infer the document type based on keywords in the filename.

    Parameters:
        filename (str): Name of the file to classify.

    Returns:
        str: Standardized document type label.
    """
    name = filename.lower()
    if "strategic" in name:
        return "Strategic Plan"
    elif "financial" in name:
        return "Financial Statement"
    elif "mandate" in name:
        return "Government Mandate Letter"
    elif "course" in name:
        return "Courses List"
    else:
        return "Unknown"


def export_metadata_to_json(documents: List[Document], output_path: str = "pdf_metadata.json"):
    """
    Export metadata from the document list to a JSON file.

    Parameters:
        documents (List[Document]): List of LangChain documents.
        output_path (str): Path to save the metadata JSON.
    """
    metadata = [doc.metadata for doc in documents]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Exported metadata to {output_path}")


def export_documents(documents: List[Document], filename="documents.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in documents
        ], f, indent=2)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest PDF documents from institution folders.")
    parser.add_argument("--root", required=True, help="Path to root folder containing institution subfolders.")
    parser.add_argument("--export", action="store_true", help="Export metadata to a JSON file.")

    args = parser.parse_args()

    docs = ingest_pdfs_from_directory(args.root)
    export_documents(docs)

    if args.export:
        export_metadata_to_json(docs)
    else:
        logger.info("Metadata export was skipped (use --export to enable it).")
