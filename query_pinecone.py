import os
import openai
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
from tqdm import tqdm

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

client = OpenAI()

def get_query_embedding(query: str) -> list[float]:
    response = client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def search_pinecone(embedding: list[float], top_k=10):
    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results['matches']

def format_context(matches):
    context = ""
    for m in matches:
        meta = m['metadata']
        triple = f"{meta['subject']} {meta['predicate']} {meta['object']}"
        context += f"- {triple} (from {meta.get('institution', 'Unknown')})\n"
    return context

def ask_openai(question: str, context: str) -> str:
    model="gpt-3.5-turbo",
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Deloitte Vancouver consultant preparing high-level strategic insights for a Partner. "
                "Your task is to synthesize and answer questions using structured semantic triples extracted from academic and institutional documents. "
                "Frame your responses to support decision-making, highlighting comparisons, trends, and actionable findings that are relevant to client needs."
                "Only compare institutions that are explicitly asked about. "
                "Ignore any unrelated institutions even if they appear in the information."
            )
        },
        {
            "role": "user",
            "content": (
                f"Based on the following information:\n\n{context}\n\n"
                f"Answer this question:\n{question}"
            )
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def main():
    print("Ask your question about any of the ten post-secondary institutions (type 'exit' to quit):\n")
    while True:
        user_query = input(" Question: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print(" Exiting. Thank you!")
            break

        print("→ Embedding your query...")
        query_embedding = get_query_embedding(user_query)

        print("→ Searching Pinecone for relevant triples...")
        matches = search_pinecone(query_embedding)

        if not matches:
            print(" No relevant information found.\n")
            continue

        print("→ Found relevant triples. Asking OpenAI...")
        context = format_context(matches)
        answer = ask_openai(user_query, context)

        print("\n Answer:")
        print(answer + "\n")

if __name__ == "__main__":
    main()
