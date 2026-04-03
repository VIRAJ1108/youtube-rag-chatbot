from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def get_rag_chain():
    prompt = PromptTemplate(
        template="""
You are a helpful assistant.

Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

Instructions:
- First, try to answer the question directly
- If exact answer is not available, say so clearly
- Then provide related useful information from the context
- Combine insights from multiple parts if relevant
- Do NOT assume who said something unless explicitly stated
- If speaker is unclear, say "The speaker mentions..."
- Include timestamps for each key point
- Do NOT merge statements from different parts unless clearly connected
""",
        input_variables=["context", "question"]
    )

    model = ChatGoogleGenerativeAI(
        model= "gemini-2.5-flash",
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )

    chain = prompt | model

    return chain