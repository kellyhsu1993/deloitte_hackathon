from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from query_engine import handle_query  # your function for embedding + RAG

app = FastAPI()

# Allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace with ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_backend(request: Request):
    data = await request.json()
    user_query = data.get("question", "")
    history = data.get("history", [])
    return handle_query(user_query, history)
