from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()


def get_llm():
    return ChatGroq(
        model=os.getenv("MODEL"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )
