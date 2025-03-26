import os
import json
import time
import asyncio
import aiohttp
from typing import List, Dict

MODEL = "gpt-4"
BATCH_SIZE = 10
INPUT_FILE = "triples.jsonl"
OUTPUT_FILE = "cleaned_triples.jsonl"
FAILED_LOG = "failed_triples.log"
CONCURRENT_REQUESTS = 5


def format_prompt(triple: dict) -> str:
    return f"""
Your task is to revise structured data triples to improve their semantic clarity, logical coherence, and suitability for downstream inference tasks.

Original triple: {json.dumps(triple, ensure_ascii=False)}

When rewriting the triple make sure to:
- Ensure the subject and object are well-defined entities or measurable values.
- Use a precise and informative verb for the predicate.
- Structure the triple to support logical inference in downstream tasks.
- Preserve all contextual meaning and key quantitative or qualitative data from the original triple.

Output the result as a JSON object using this key order:
"institution", "object", "predicate", "source", "subject"
"""


async def call_openai(session: aiohttp.ClientSession, prompt: str, semaphore: asyncio.Semaphore, retries: int = 3) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    for attempt in range(retries):
        async with semaphore:
            try:
                async with session.post(url, headers=headers, json=payload) as resp:
                    response = await resp.json()
                    return response['choices'][0]['message']['content']
            except Exception as e:
                await asyncio.sleep(2 ** attempt)
                if attempt == retries - 1:
                    raise e


async def process_single(triple: dict, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> Dict:
    try:
        prompt = format_prompt(triple)
        result = await call_openai(session, prompt, semaphore)
        cleaned = json.loads(result)

        ordered = {
            "institution": cleaned["institution"],
            "object": cleaned["object"],
            "predicate": cleaned["predicate"],
            "source": cleaned["source"],
            "subject": cleaned["subject"],
        }
        return {"status": "success", "data": ordered}

    except Exception as e:
        return {"status": "failed", "data": triple, "error": str(e)}


async def process_batch(batch: List[dict], batch_index: int, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    tasks = [process_single(triple, session, semaphore) for triple in batch]
    results = await asyncio.gather(*tasks)

    with open(OUTPUT_FILE, "a", encoding="utf-8") as out_f, open(FAILED_LOG, "a", encoding="utf-8") as fail_f:
        for i, result in enumerate(results):
            if result["status"] == "success":
                out_f.write(json.dumps(result["data"], ensure_ascii=False) + "\n")
                print(f"[Batch {batch_index} - {i+1}] Success")
            else:
                fail_f.write(json.dumps({
                    "error": result["error"],
                    "data": result["data"]
                }, ensure_ascii=False) + "\n")
                print(f"[Batch {batch_index} - {i+1}] Failed: {result['error']}")


async def rewrite_triples_batched():
    batch = []
    batch_index = 1
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        with open(INPUT_FILE, "r", encoding="utf-8") as in_f:
            for line in in_f:
                try:
                    triple = json.loads(line)
                    batch.append(triple)
                    if len(batch) == BATCH_SIZE:
                        await process_batch(batch, batch_index, session, semaphore)
                        batch = []
                        batch_index += 1
                        await asyncio.sleep(1)  # Optional rate limit control
                except json.JSONDecodeError as e:
                    with open(FAILED_LOG, "a", encoding="utf-8") as fail_f:
                        fail_f.write(json.dumps({
                            "error": f"Invalid JSON line: {str(e)}",
                            "data": line
                        }, ensure_ascii=False) + "\n")

        if batch:
            await process_batch(batch, batch_index, session, semaphore)


if __name__ == "__main__":
    asyncio.run(rewrite_triples_batched())
