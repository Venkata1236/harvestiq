"""
Diagnosis Crew — orchestrates Disease Analyst + Treatment Advisor agents
and returns a unified structured result for the API.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from app.rag.retriever import get_disease_info
from app.agents.disease_analyst import run_disease_analysis
from app.agents.treatment_advisor import run_treatment_advice


# Thread pool for running agents in parallel
_executor = ThreadPoolExecutor(max_workers=2)


def run_diagnosis_crew(class_name: str, confidence: float) -> dict:
    """
    Run both agents in parallel and return a unified diagnosis result.

    Args:
        class_name: Detected disease class e.g. "Tomato___Early_blight"
        confidence: Model confidence score 0.0-1.0
    Returns:
        Unified dict with RAG data + agent reports
    """
    logger.info(f"Starting diagnosis crew for: {class_name} ({round(confidence*100,1)}%)")

    # Step 1: Get RAG data (fast, no LLM)
    disease_info = get_disease_info(class_name)

    # Step 2: Run both agents in parallel using threads
    with ThreadPoolExecutor(max_workers=2) as executor:
        analyst_future = executor.submit(run_disease_analysis, class_name, confidence)
        advisor_future = executor.submit(run_treatment_advice, class_name, confidence)

        diagnosis_report = analyst_future.result()
        treatment_plan = advisor_future.result()

    logger.success(f"Diagnosis crew completed for: {class_name}")

    return {
        # Raw disease data from RAG
        "disease_name": disease_info["disease_name"],
        "crop": disease_info["crop"],
        "pathogen": disease_info["pathogen"],
        "severity": disease_info["severity"],
        "is_healthy": disease_info["is_healthy"],
        "class_name": class_name,
        "confidence": round(confidence * 100, 1),

        # AI agent outputs
        "diagnosis_report": diagnosis_report,
        "treatment_plan": treatment_plan,

        # Quick-access fields for UI
        "symptoms": disease_info["symptoms"],
        "causes": disease_info["causes"],
        "treatment_summary": disease_info["treatment"],
        "prevention_summary": disease_info["prevention"],
    }


# ── Quick Test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run_diagnosis_crew(
        class_name="Tomato___Early_blight",
        confidence=0.94,
    )

    print(f"\n{'='*60}")
    print(f"Disease  : {result['disease_name']}")
    print(f"Crop     : {result['crop']}")
    print(f"Severity : {result['severity']}")
    print(f"Healthy  : {result['is_healthy']}")
    print(f"\n--- DIAGNOSIS REPORT ---\n{result['diagnosis_report']}")
    print(f"\n--- TREATMENT PLAN ---\n{result['treatment_plan']}")