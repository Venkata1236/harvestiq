"""
Treatment Advisor Agent — generates a detailed treatment and prevention plan.
"""

from crewai import Agent, Task, Crew
from app.rag.retriever import get_disease_info


def run_treatment_advice(class_name: str, confidence: float) -> str:
    """
    Run the Treatment Advisor agent to produce a full treatment plan.

    Args:
        class_name: e.g. "Tomato___Early_blight"
        confidence: model confidence score (0.0 - 1.0)
    Returns:
        Markdown-formatted treatment plan string
    """
    disease_info = get_disease_info(class_name)

    rag_context = f"""
    Disease Name  : {disease_info['disease_name']}
    Crop          : {disease_info['crop']}
    Pathogen      : {disease_info['pathogen']}
    Treatment     : {disease_info['treatment']}
    Prevention    : {disease_info['prevention']}
    Severity      : {disease_info['severity']}
    Is Healthy    : {disease_info['is_healthy']}
    Confidence    : {round(confidence * 100, 1)}%
    """

    advisor = Agent(
        role="Agricultural Treatment Advisor",
        goal="Create practical, safe, and effective treatment and prevention plans for crop diseases.",
        backstory="""You are a certified crop protection specialist and integrated pest 
        management (IPM) expert. You have advised thousands of farmers across diverse 
        climates and crop types. You always recommend the safest effective treatment first,
        consider organic alternatives, and give precise application instructions. 
        You understand that farmers need practical guidance — not textbook theory.""",
        verbose=False,
        allow_delegation=False,
    )

    task = Task(
        description=f"""
        Create a comprehensive treatment and prevention plan based on the following crop disease data.

        RAG Knowledge Base Data:
        {rag_context}

        Your plan must include:
        1. **Treatment Plan** — Step-by-step treatment with specific products/methods
        2. **Application Instructions** — How and when to apply treatments
        3. **Organic Alternatives** — At least one organic/natural option
        4. **Prevention Strategy** — How to prevent recurrence (4-5 points)
        5. **Recovery Timeline** — Expected recovery time if treatment applied correctly

        If the plant is HEALTHY, skip treatment and focus entirely on:
        - Optimal maintenance schedule
        - Preventive spray calendar
        - Signs to watch for early detection

        Be specific with product names, dosages where known, and timing.
        Use bullet points and markdown headers.
        Keep response under 350 words.
        """,
        expected_output="A detailed markdown treatment plan with specific products, application instructions, organic alternatives, prevention strategy, and recovery timeline.",
        agent=advisor,
    )

    crew = Crew(
        agents=[advisor],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)