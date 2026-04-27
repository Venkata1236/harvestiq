"""
RAG Retriever — fetches disease knowledge from ChromaDB and structures it
for the API response and CrewAI agents.
"""

from loguru import logger
from app.rag.ingest import get_chroma_client, get_collection


# ── Main Retriever ─────────────────────────────────────────────────────────────
def get_disease_info(class_name: str) -> dict:
    """
    Retrieve structured disease information from ChromaDB by class name.

    Args:
        class_name: e.g. "Tomato___Early_blight" or "Apple___Apple_scab"
    Returns:
        Structured dict with disease details parsed from the document.
    """
    try:
        client = get_chroma_client()
        collection = get_collection(client)

        # Step 1: Try exact metadata match first
        try:
            exact = collection.get(
                where={"class_name": class_name},
                include=["documents", "metadatas"],
            )
            if exact["documents"]:
                document = exact["documents"][0]
                metadata = exact["metadatas"][0]
                logger.info(f"RAG exact match: {class_name}")
                parsed = _parse_document(document)
                parsed["class_name"] = metadata.get("class_name", class_name)
                parsed["similarity_score"] = 1.0
                parsed["raw_document"] = document
                return parsed
        except Exception:
            pass

        # Step 2: Fallback to semantic search
        results = collection.query(
            query_texts=[class_name],
            n_results=1,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"] or not results["documents"][0]:
            logger.warning(f"No document found for class: {class_name}")
            return _fallback_response(class_name)

        document = results["documents"][0][0]
        metadata = results["metadatas"][0][0]
        similarity = round(1 - results["distances"][0][0], 3)

        logger.info(f"RAG semantic match: {class_name} | similarity: {similarity}")

        parsed = _parse_document(document)
        parsed["class_name"] = metadata.get("class_name", class_name)
        parsed["similarity_score"] = similarity
        parsed["raw_document"] = document

        return parsed

    except Exception as e:
        logger.error(f"RAG retrieval failed for {class_name}: {e}")
        return _fallback_response(class_name)


def get_disease_info_by_symptoms(symptoms: str, n_results: int = 3) -> list[dict]:
    """
    Semantic search by symptom description — useful for uncertain predictions.

    Args:
        symptoms: Free text e.g. "yellow spots on tomato leaves with brown centers"
        n_results: Number of closest matches to return
    Returns:
        List of structured disease dicts ordered by similarity
    """
    try:
        client = get_chroma_client()
        collection = get_collection(client)

        results = collection.query(
            query_texts=[symptoms],
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
                parsed = _parse_document(doc)
                parsed["class_name"] = meta.get("class_name", "")
                parsed["similarity_score"] = round(1 - dist, 3)
                matches.append(parsed)

        return matches

    except Exception as e:
        logger.error(f"Symptom-based RAG retrieval failed: {e}")
        return []


# ── Document Parser ────────────────────────────────────────────────────────────
def _parse_document(document: str) -> dict:
    """
    Parse raw text document into structured fields.
    Extracts: disease_name, crop, pathogen, symptoms, causes,
              treatment, prevention, severity, is_healthy
    """
    lines = document.strip().split("\n")
    result = {
        "disease_name": "",
        "crop": "",
        "pathogen": "",
        "symptoms": "",
        "causes": "",
        "treatment": "",
        "prevention": "",
        "severity": "Unknown",
        "is_healthy": False,
    }

    # Detect healthy plant
    if "Status: Healthy" in document:
        result["is_healthy"] = True
        result["disease_name"] = "Healthy"
        result["severity"] = "None"

    current_field = None
    field_map = {
        "Disease:": "disease_name",
        "Status:": "disease_name",
        "Crop:": "crop",
        "Pathogen:": "pathogen",
        "Pest:": "pathogen",
        "Symptoms:": "symptoms",
        "Causes:": "causes",
        "Treatment:": "treatment",
        "Prevention:": "prevention",
        "Severity:": "severity",
        "Maintenance:": "treatment",
        "Preventive Care:": "prevention",
        "Indicators:": "symptoms",
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        matched = False
        for key, field in field_map.items():
            if line.startswith(key):
                value = line[len(key):].strip()
                result[field] = value
                current_field = field
                matched = True
                break

        # Multi-line field continuation
        if not matched and current_field and line:
            if result[current_field]:
                result[current_field] += " " + line
            else:
                result[current_field] = line

    # Clean up whitespace
    for key in result:
        if isinstance(result[key], str):
            result[key] = " ".join(result[key].split())

    return result


# ── Fallback ───────────────────────────────────────────────────────────────────
def _fallback_response(class_name: str) -> dict:
    """Returns a safe fallback when ChromaDB has no matching document."""
    parts = class_name.split("___")
    crop = parts[0].replace("_", " ") if parts else "Unknown"
    disease = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"

    return {
        "disease_name": disease,
        "crop": crop,
        "pathogen": "Unknown",
        "symptoms": "Consult a local agricultural expert for detailed diagnosis.",
        "causes": "Environmental and pathogenic factors — expert assessment recommended.",
        "treatment": "Contact your local agricultural extension office for treatment options.",
        "prevention": "Practice good crop hygiene, proper spacing, and regular monitoring.",
        "severity": "Unknown",
        "is_healthy": False,
        "class_name": class_name,
        "similarity_score": 0.0,
        "raw_document": "",
    }


# ── Quick Test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_classes = [
        "Tomato___Early_blight",
        "Apple___Apple_scab",
        "Tomato___healthy",
        "Corn_(maize)___Northern_Leaf_Blight",
    ]

    for cls in test_classes:
        print(f"\n{'='*60}")
        print(f"Class: {cls}")
        info = get_disease_info(cls)
        print(f"  Disease   : {info['disease_name']}")
        print(f"  Crop      : {info['crop']}")
        print(f"  Severity  : {info['severity']}")
        print(f"  Similarity: {info['similarity_score']}")
        print(f"  Treatment : {info['treatment'][:80]}...")