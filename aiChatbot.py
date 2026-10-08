from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    groq_api_key=groq_api_key
);

while True:
    user_input = input("User: Enter text to translate or 'exit' to quit: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting the chatbot. Goodbye!")
        break

    response = llm.invoke(user_input)
    print("AI:", response.content)
