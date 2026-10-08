from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


# =========================
# LLM FACTORY (MULTI PROVIDER)
# =========================
def get_llm():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0
        )

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            temperature=0
        )

    raise ValueError("Invalid LLM_PROVIDER (use openai, groq, ollama)")


# =========================
# VECTOR STORE
# =========================
def load_vector_store():
    embeddings = FastEmbedEmbeddings()

    return Chroma(
        persist_directory="db/chroma",
        embedding_function=embeddings,
        collection_name="jsdocs_collection",
    )


vector_store = load_vector_store()


# =========================
# RETRIEVER (BEST PRACTICE)
# =========================
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.4,
        "k": 5
    }
)


def retrieve_docs(query):
    return retriever.invoke(query)


# =========================
# CONTEXT BUILDER
# =========================
def build_context(docs):
    return "\n\n".join(
        doc.page_content.strip()
        for doc in docs
    )


# =========================
# STRONG RAG PROMPT
# =========================
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful and accurate assistant.

You must follow these rules:

1. Use ONLY the provided context as your main source.
2. If the context contains enough information, answer clearly and fully.
3. If the context is partially relevant, use it to form the best possible answer.
4. If the context is completely unrelated, then say:
   "I don't have enough information in the provided context."
5. Do NOT invent facts that are not supported by the context.
6. Keep answers natural, helpful, and easy to understand.
"""
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
    )
])


# =========================
# RAG PIPELINE
# =========================
def ask(question):
    docs = retrieve_docs(question)

    context = build_context(docs)

    llm = get_llm()
    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content


# =========================
# TEST
# =========================
if __name__ == "__main__":
    question = "what is unity engine?"

    answer = ask(question)

    print("\nANSWER:\n")
    print(answer)