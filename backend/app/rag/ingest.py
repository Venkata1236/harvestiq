"""
ChromaDB ingestion script — loads 38 disease documents into vector store.
Run once to populate: python -m app.rag.ingest
"""

import chromadb
from loguru import logger
from pathlib import Path

from app.rag.knowledge_base.diseases import DISEASE_KNOWLEDGE
from app.core.config import settings


# ── Constants ──────────────────────────────────────────────────────────────────
EMBED_MODEL = "all-MiniLM-L6-v2"       # Free, fast, good quality
COLLECTION_NAME = "crop_diseases"


# ── ChromaDB Client ────────────────────────────────────────────────────────────
def get_chroma_client() -> chromadb.PersistentClient:
    """Returns persistent ChromaDB client — data survives server restarts."""
    db_path = Path(settings.CHROMA_DB_PATH)
    db_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(db_path))


def get_collection(client: chromadb.PersistentClient):
    """Get or create collection using ChromaDB's built-in embedding function."""
    from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
    
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )


# ── Ingestion ──────────────────────────────────────────────────────────────────
def ingest_diseases(force: bool = False) -> int:
    """
    Ingest all 38 disease documents into ChromaDB.
    
    Args:
        force: If True, clears existing collection and re-ingests.
    Returns:
        Number of documents ingested.
    """
    client = get_chroma_client()

    # Delete and recreate if force
    if force:
        try:
            client.delete_collection(COLLECTION_NAME)
            logger.info("Cleared existing collection for re-ingestion")
        except Exception:
            pass

    collection = get_collection(client)

    # Check if already populated
    existing_count = collection.count()
    if existing_count > 0 and not force:
        logger.info(
            f"Collection already has {existing_count} documents — skipping ingestion. "
            "Use force=True to re-ingest."
        )
        return existing_count

    # Prepare documents, ids, and metadata
    documents = []
    ids = []
    metadatas = []

    for disease in DISEASE_KNOWLEDGE:
        documents.append(disease["document"].strip())
        ids.append(disease["id"])
        metadatas.append({
            "class_name": disease["class_name"],
            "id": disease["id"],
        })

    # Ingest in batches of 10 (safe for memory)
    batch_size = 10
    total = len(documents)

    logger.info(f"Ingesting {total} disease documents into ChromaDB...")

    for i in range(0, total, batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]

        collection.upsert(
            documents=batch_docs,
            ids=batch_ids,
            metadatas=batch_meta,
        )
        logger.info(f"Ingested batch {i // batch_size + 1} — {min(i + batch_size, total)}/{total}")

    final_count = collection.count()
    logger.success(f"ChromaDB ready — {final_count} disease documents indexed ✅")
    return final_count


# ── Query ──────────────────────────────────────────────────────────────────────
def query_disease(class_name: str, n_results: int = 1) -> dict:
    """
    Query ChromaDB for a specific disease by class name.
    
    Args:
        class_name: Detected class e.g. "Tomato___Early_blight"
        n_results: Number of results to return
    Returns:
        Dict with document text and metadata
    """
    client = get_chroma_client()
    collection = get_collection(client)

    # First try exact metadata match
    try:
        results = collection.query(
            query_texts=[class_name],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        if results["documents"] and results["documents"][0]:
            return {
                "document": results["documents"][0][0],
                "metadata": results["metadatas"][0][0],
                "similarity": 1 - results["distances"][0][0],  # cosine → similarity
                "found": True,
            }
    except Exception as e:
        logger.error(f"ChromaDB query failed: {e}")

    return {"document": "", "metadata": {}, "similarity": 0.0, "found": False}


def query_by_symptoms(symptoms_text: str, n_results: int = 3) -> list:
    """
    Query ChromaDB using symptom description for semantic search.
    
    Args:
        symptoms_text: Free text description of symptoms
        n_results: Number of similar diseases to return
    Returns:
        List of matching disease documents
    """
    client = get_chroma_client()
    collection = get_collection(client)

    results = collection.query(
        query_texts=[symptoms_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    matches = []
    if results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            matches.append({
                "document": doc,
                "class_name": meta.get("class_name", ""),
                "similarity": round(1 - dist, 3),
            })

    return matches


# ── Standalone runner ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    count = ingest_diseases(force=True)
    print(f"\n✅ Done — {count} documents in ChromaDB")

    # Quick test query
    print("\n🔍 Test query: 'Tomato___Early_blight'")
    result = query_disease("Tomato___Early_blight")
    print(f"Found: {result['found']}")
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Document preview: {result['document'][:200]}...")