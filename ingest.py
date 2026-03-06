from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
from pinecone import Pinecone

# 后面会 import 更多，先留空


def load_docs(data_dir):
    docs = []
    paths = Path(data_dir).glob("*.md")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        docs.append({"source": path.name, "text":text})
    return docs


def chunk_text(doc, chunk_size=500, overlap=100):
    chunks = []
    text = doc["text"]
    source = doc["source"]
    start = 0
    chunk_index = 0

    while start < len(text):
        chunk = text[start:start + chunk_size]
        # 1. 取出 text[start: start+chunk_size]
        chunk_id = (f"{source}::chunk_{chunk_index}")
        # 2. 生成 chunk_id = f"{source}::chunk_{chunk_index}"
        chunks.append({"chunk_id":chunk_id,"text":chunk,"metadata":{"source":source,"chunk_index":chunk_index,"text": chunk}})
        # 3. append 进 chunks，包含 chunk_id、text、metadata
        start = start + chunk_size - overlap
        # 4. start = start + chunk_size - overlap
        chunk_index += 1
        # 5. chunk_index += 1
    return chunks


def embed_texts(texts, batch_size=100):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    vectors = []
    for i in range(0,len(texts),batch_size):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(
            model = "text-embedding-3-small",
            input = batch
            )
        for item in response.data:
            vectors.append(item.embedding)
    return vectors


def build_records(chunks, vectors):
    records = []
    for chunk, vector in zip(chunks,vectors):
        records.append({"id":chunk["chunk_id"],"values":vector,"metadata":chunk["metadata"]})
    return records


if __name__ == "__main__":
    docs = load_docs("output")
    print(f"loaded {len(docs)} docs")
    print(docs[0]["source"])
    print(docs[0]["text"][:200])
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)
    print(len(all_chunks))
    print(all_chunks[0])
    sample_texts = [c["text"] for c in all_chunks[:3]]
    vectors = embed_texts(sample_texts)
    print(f"Vectors: {len(vectors)}")
    print(f"Dimension: {len(vectors[0])}")
    records = build_records(all_chunks[:3], vectors)
    print(f"Records: {len(records)}")
    print(records[0]["id"])
    print(len(records[0]["values"]))
    print(records[0]["metadata"])

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("esg-rag")
    all_texts = [c["text"] for c in all_chunks]
    all_vectors = embed_texts(all_texts)
    all_records = build_records(all_chunks,all_vectors)
    for i in range(0,len(all_records),100):
        index.upsert(vectors = all_records[i:i+100])
    stats = index.describe_index_stats()
    print(stats.total_vector_count)

