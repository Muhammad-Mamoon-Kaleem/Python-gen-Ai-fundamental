# from dotenv import load_dotenv
# import os
# from langchain_openai import ChatOpenAI
# load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")
# # print("OPENAI_API_KEY:", openai_api_key)
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0.7, max_tokens=1000);
# res = llm.invoke("who is the president of USA?")
# print(res)


from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    groq_api_key=groq_api_key
)

# response = llm.invoke(
#     "Explain LangChain in simple words."
# )

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a language translation assistant. Just Translate the text into {language}."
    ),
    (
        "user",
        "{text}"
    ),
])

# final_prompt = prompt.format_messages(
#     language="urdu",
#     text=" im learning langchain and groq llm"
# )

# response = llm.invoke(final_prompt)

# print(response.content)

parser = StrOutputParser()

chain = prompt | llm | parser 
# response = chain.invoke({
#     "language": "urdu",
#     "text": "wonderful langchain and groq llm"
# })

inputs = [
    {
        "language": "French",
        "text": "Hello, how are you?"
    },
    {
        "language": "German",
        "text": "Good morning"
    },
    {
        "language": "Spanish",
        "text": "I love programming"
    }
]

responses = chain.batch(inputs)

# print(responses)
for response in responses:
    print(response)