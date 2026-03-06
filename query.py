from dotenv import load_dotenv
import os
from openai import OpenAI
from pinecone import Pinecone
import streamlit as st

load_dotenv()

def ask(question):
    # 1. 初始化 OpenAI 和 Pinecone
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY"))
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY") or st.secrets.get("PINECONE_API_KEY"))
    index = pc.Index("esg-rag")
    # 2. 把问题转成向量
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = [question]
    )
    question_vector = response.data[0].embedding
    # 3. 在 Pinecone 检索最相似的3个 chunk
    results = index.query(vector = question_vector, top_k = 3, include_metadata = True)
    
    # 4. 把 chunk 文字拼成 context
    context = "\n\n".join(
        [match["metadata"]["source"] + ": " + match["metadata"].get("text", "") for match in results.matches]
        )
    # 5. 喂给 GPT，返回回答
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role":"system","content":"Answer based on then context provided"},
            {"role":"user","content":f"Context:\n\n{context}\nQuestion:{question}"}
        ]
    )
    answer = response.choices[0].message.content
    sources = [match["metadata"]["source"] for match in results.matches]
    return answer, sources

if __name__ == "__main__":
    answer, sources = ask("What are the Scope 1 and Scope 2 emissions reduction targets across different companies?")
    print(answer)
    print(sources)