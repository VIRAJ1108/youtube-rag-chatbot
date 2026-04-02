from components.loader import load_youtube_transcript
from components.chunking import create_chunks
from components.embeddings import create_vectorstore
from components.retriever import get_retriever
from components.chain import get_rag_chain

# 🔹 Step 1 — Inputs
video_id = "7ARBJQn6QkM"
query = "What did Jensen Huang say about GPUs?"

# 🔹 Step 2 — Load transcript
entries = load_youtube_transcript(video_id)

# 🔹 Step 3 — Chunking
chunks = create_chunks(entries)
print(f"Chunks: {len(chunks)}")

# 🔹 Step 4 — Vector store
vectorstore = create_vectorstore(chunks)

# 🔹 Step 5 — Retriever
retriever = get_retriever(vectorstore)

# 🔹 Step 6 — Retrieve relevant chunks
results = retriever.invoke(query)

print("\n--- Retrieved Chunks ---\n")

for i, doc in enumerate(results):
    print(f"\nResult {i+1}:")
    print(doc.page_content[:200])
    print("Timestamp:", doc.metadata)

# 🔹 Step 7 — Build grounded context (IMPORTANT FIX)
context = "\n\n".join([
    f"[{doc.metadata['start']} - {doc.metadata['end']}]\n{doc.page_content}"
    for doc in results
])

# 🔹 Step 8 — RAG chain
chain = get_rag_chain()

response = chain.invoke({
    "context": context,
    "question": query
})

# 🔹 Step 9 — Final answer
print("\n--- FINAL ANSWER ---\n")
print(response.content)