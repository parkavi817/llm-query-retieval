# app/services/clause_matcher.py
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from app.core.config import settings
import logging

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=settings.OPENROUTER_API_KEY,
    openai_api_base=settings.OPENROUTER_BASE_URL,
)

def match_clauses(retrieved_chunks, questions):
    responses = []
    for q, chunks in zip(questions, retrieved_chunks):
        context = "\n\n".join(chunks)
        prompt = f"""You are an intelligent assistant trained to answer queries from complex documents (insurance, HR, legal, compliance, etc.).

Your job is to:
- Read the context
- Understand the question
- Extract a direct, fact-based, and explainable answer
- List conditions if needed
- Say 'Not found in the document' if answer is missing

Question: "{q}"

Context:
{context}

Answer:"""

        try:
            response = llm([HumanMessage(content=prompt)])
            answer = response.content
        except Exception as e:
            logging.error(f"LLM error: {e}", exc_info=True)
            answer = f"LLM server error: {e}. Unable to generate answer for this question."

        responses.append(answer.strip())

    return responses
