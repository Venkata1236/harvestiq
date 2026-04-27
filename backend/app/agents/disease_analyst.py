"""
Disease Analyst Agent — diagnoses crop disease from model prediction + RAG context.
"""

from crewai import Agent, Task, Crew
from app.rag.retriever import get_disease_info


def run_disease_analysis(class_name: str, confidence: float) -> str:
    """
    Run the Disease Analyst agent to produce a structured diagnosis report.

    Args:
        class_name: e.g. "Tomato___Early_blight"
        confidence: model confidence score (0.0 - 1.0)
    Returns:
        Markdown-formatted diagnosis report string
    """
    # Fetch RAG context first
    disease_info = get_disease_info(class_name)

    # Build context string for the agent
    rag_context = f"""
    Disease Name  : {disease_info['disease_name']}
    Crop          : {disease_info['crop']}
    Pathogen      : {disease_info['pathogen']}
    Symptoms      : {disease_info['symptoms']}
    Causes        : {disease_info['causes']}
    Severity      : {disease_info['severity']}
    Is Healthy    : {disease_info['is_healthy']}
    Model Class   : {class_name}
    Confidence    : {round(confidence * 100, 1)}%
    """

    analyst = Agent(
        role="Agricultural Disease Analyst",
        goal="Analyze crop disease diagnosis results and provide clear, accurate disease assessments for farmers.",
        backstory="""You are a senior plant pathologist with 20 years of experience diagnosing 
        crop diseases across Asia, Africa and the Americas. You specialize in translating 
        technical disease data into clear, actionable information that farmers can understand 
        and act upon immediately. You are precise, empathetic, and always prioritize farmer 
        safety and crop recovery.""",
        verbose=False,
        allow_delegation=False,
    )

    task = Task(
        description=f"""
        Analyze the following crop disease diagnosis and produce a structured assessment report.

        RAG Knowledge Base Data:
        {rag_context}

        Your report must include:
        1. **Diagnosis Summary** — What disease was detected, which crop, how confident
        2. **What This Means** — Plain language explanation of the disease impact
        3. **Severity Assessment** — How serious is this (None / Low / Moderate / High / Critical)
        4. **Immediate Actions** — What the farmer should do TODAY (3-5 bullet points)
        5. **Watch For** — Warning signs that the situation is worsening

        If the plant is HEALTHY, focus on maintenance and prevention instead of treatment.
        Write in clear, simple language a farmer can understand.
        Format with markdown headers and bullet points.
        Keep response under 300 words.
        """,
        expected_output="A structured markdown disease assessment report with diagnosis summary, severity, immediate actions, and warning signs.",
        agent=analyst,
    )

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)