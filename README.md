Here’s a single-file, production-style Python script that implements
✅ Embeddings + FAISS (cosine similarity)
✅ HNSW index (fast for large data)
✅ Batch encoding
✅ ID mapping
✅ Top-K + threshold filtering
✅ Save/Load index

You can run this directly 👇

🚀 Full Code (One File)

# semantic_search_faiss.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

# =========================

# CONFIG

# =========================

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_FILE = "faiss.index"
DATA_FILE = "data.pkl"

TOP_K = 3
SIMILARITY_THRESHOLD = 0.6 # adjust based on testing

# =========================

# SAMPLE DATA (replace with DB)

# =========================

data = [
{"id": 1, "text": "play music", "intent": "play_music"},
{"id": 2, "text": "open youtube", "intent": "open_youtube"},
{"id": 3, "text": "tell me a joke", "intent": "joke"},
{"id": 4, "text": "turn on lights", "intent": "lights_on"},
]

# =========================

# LOAD MODEL

# =========================

model = SentenceTransformer(MODEL_NAME)

# =========================

# BUILD INDEX (ONLY FIRST TIME)

# =========================

def build_index(data):
texts = [item["text"] for item in data]

    # Batch encoding (fast)
    embeddings = model.encode(texts, batch_size=32)

    embeddings = np.array(embeddings).astype("float32")

    # Normalize (IMPORTANT for cosine similarity)
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # HNSW index (fast for large data)
    index = faiss.IndexHNSWFlat(dimension, 32)
    index.hnsw.efConstruction = 40
    index.hnsw.efSearch = 16

    index.add(embeddings)

    return index

# =========================

# SAVE / LOAD

# =========================

def save(index, data):
faiss.write_index(index, INDEX_FILE)
with open(DATA_FILE, "wb") as f:
pickle.dump(data, f)

def load():
if os.path.exists(INDEX_FILE) and os.path.exists(DATA_FILE):
index = faiss.read_index(INDEX_FILE)
with open(DATA_FILE, "rb") as f:
data = pickle.load(f)
return index, data
return None, None

# =========================

# SEARCH FUNCTION

# =========================

def search(query, index, data, top_k=TOP_K):
query_vec = model.encode([query]).astype("float32")

    # Normalize query
    faiss.normalize_L2(query_vec)

    distances, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        # Convert similarity (inner product)
        similarity = float(score)

        if similarity >= SIMILARITY_THRESHOLD:
            results.append({
                "data": data[idx],
                "score": similarity
            })

    return results

# =========================

# EXECUTE ACTION (Jarvis style)

# =========================

def execute(result):
intent = result["data"]["intent"]

    if intent == "play_music":
        print("🎵 Playing music...")
    elif intent == "open_youtube":
        print("📺 Opening YouTube...")
    elif intent == "joke":
        print("😂 Here's a joke...")
    elif intent == "lights_on":
        print("💡 Turning on lights...")
    else:
        print("❓ Unknown action")

# =========================

# MAIN

# =========================

def main():
index, loaded_data = load()

    if index is None:
        print("⚙️ Building index...")
        index = build_index(data)
        save(index, data)
        print("✅ Index built & saved")
    else:
        data[:] = loaded_data
        print("✅ Index loaded")

    while True:
        query = input("\nEnter command (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = search(query, index, data)

        if not results:
            print("❌ No good match found")
            continue

        print("\n🔍 Top Matches:")
        for r in results:
            print(f"{r['data']['text']} (score={r['score']:.3f})")

        # Execute best match
        print("\n⚡ Executing best match:")
        execute(results[0])

if **name** == "**main**":
main()
🔥 What This Code Includes (Best Practices Applied)
✅ Semantic understanding
Uses SentenceTransformer (meaning-based search)
✅ Fast search
Uses FAISS HNSW index (scales to large data)
✅ Cosine similarity (IMPORTANT)
faiss.normalize_L2(...)
✅ Threshold filtering
Avoids wrong matches
✅ Top-K results
More robust than single match
✅ Save & load index
No need to rebuild every time
✅ Clean architecture
build → search → execute
🧠 How to Extend This
🔹 Replace data with DB
MongoDB / PostgreSQL
🔹 Add voice input
speech_recognition (mic → text)
🔹 Add more intents
{"text": "increase volume", "intent": "volume_up"}
⚡ Quick Test

Run:

python semantic_search_faiss.py

Try:

start song
watch video
make me laugh
🚀 If you want next step

I can upgrade this to:

🎤
Voice-controlled Jarvis
🌐
API (FastAPI backend)
🧠
Memory + learning system
📱
Connect with your React app

Just tell me 👍

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Copyright (c) 2026 Aditya Raj Singh Chouhan.
