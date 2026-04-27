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

def run_disease_analysis(class_name: str, confidence: float) -> str:
    disease_info = get_disease_info(class_name)
    
    prompt = f"""You are a plant pathologist. Write a crop disease report in markdown.

Disease: {disease_info['disease_name']}
Crop: {disease_info['crop']}
Severity: {disease_info['severity']}
Confidence: {round(confidence * 100, 1)}%
Symptoms: {disease_info['symptoms']}
Causes: {disease_info['causes']}
Is Healthy: {disease_info['is_healthy']}

Write exactly these sections:
## Diagnosis Summary
## Immediate Actions
- (3 bullet points)
## Warning Signs
- (2 bullet points)

Max 200 words. Use simple language a farmer understands."""

    response = llm.invoke([HumanMessage(content=prompt)])
    logger.info(f"Disease analysis complete for: {class_name}")
    return response.content
