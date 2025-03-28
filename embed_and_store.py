import os
import json
import uuid
from tqdm import tqdm
from dotenv import load_dotenv
import openai
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = os.getenv("PINECONE_INDEX_NAME")
env = os.getenv("PINECONE_ENV") 

# Create index if it doesn't exist
if index_name not in [index.name for index in pc.list_indexes()]:
    print("Index Name:", index_name)
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=env)  # Adjust cloud & region as needed
    )

index = pc.Index(index_name)

def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return response.data[0].embedding

def build_text_from_triple(triple: dict) -> str:
    return f"{triple['subject']} {triple['predicate']} {triple['object']}"

def load_triples(filepath: str) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def store_to_pinecone(vectors: list[dict]):
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors[i:i + batch_size])

def main():
    triples = load_triples("triples.jsonl")
    pinecone_vectors = []

    for triple in tqdm(triples, desc="Embedding Triples"):
        try:
            triple_text = build_text_from_triple(triple)
            embedding = embed_text(triple_text)
            vector_id = str(uuid.uuid4())

            metadata = {
                "subject": str(triple["subject"]),
                "predicate": str(triple["predicate"]),
                "object": str(triple["object"]),
                "institution": str(triple.get("institution", "Unknown")),
                "source": str(triple.get("source", "Unknown"))
            }

            pinecone_vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })
        except Exception as e:
            print(f"Failed to embed triple: {triple}. Error: {e}")

    store_to_pinecone(pinecone_vectors)
    print(f"Stored {len(pinecone_vectors)} triples to Pinecone.")

if __name__ == "__main__":
    main()
