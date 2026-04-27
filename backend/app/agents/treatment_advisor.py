import os
from dotenv import load_dotenv
from loguru import logger
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.rag.retriever import get_disease_info

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

def run_treatment_advice(class_name: str, confidence: float) -> str:
    disease_info = get_disease_info(class_name)

    prompt = f"""You are a crop protection specialist. Write a treatment plan in markdown.

Disease: {disease_info['disease_name']}
Crop: {disease_info['crop']}
Treatment: {disease_info['treatment']}
Prevention: {disease_info['prevention']}
Severity: {disease_info['severity']}
Is Healthy: {disease_info['is_healthy']}

Write exactly these sections:
## Treatment Plan
- (3 bullet points with specific product names)
## Organic Alternative
(1-2 sentences)
## Prevention
- (3 bullet points)

Max 200 words. Be specific and practical."""

    response = llm.invoke([HumanMessage(content=prompt)])
    logger.info(f"Treatment advice complete for: {class_name}")
    return response.content
