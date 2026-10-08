import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_experimental.text_splitter import SemanticChunker

load_dotenv()


# -------------------------
# LOAD PDF DOCUMENT
# -------------------------
def loadDocument(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    documents = []

    # ✅ FIX: correct PDF file path
    full_path = os.path.join(file_path, "javascript_tutorial.pdf")

    loader = PyPDFLoader(full_path)
    pages = loader.load()

    documents.extend(pages)

    if not documents:
        raise ValueError("No documents found in PDF")

    print(f"Loaded {len(documents)} pages from PDF")
    return documents


# -------------------------
# SEMANTIC CHUNKING
# -------------------------
def chunkDocument(documents):
    embeddings = FastEmbedEmbeddings()

    # ✅ FIX: do NOT overwrite class name
    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=95,
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No chunks found")

    print(f"Chunked {len(chunks)} semantic chunks")
    return chunks


# -------------------------
# VECTOR STORE
# -------------------------
def createVectorStore(chunks, persist_dir="db/chroma", batch_size=32):
    print("Creating vector store...")

    embeddings = FastEmbedEmbeddings()

    vectorStore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir,
        collection_name="jsdocs_collection",
    )

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vectorStore.add_documents(batch)
        print(f"Indexed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

    print("Vector store created successfully")
    return vectorStore


# -------------------------
# MAIN
# -------------------------
def main():
    print("Starting document ingestion...")

    documents = loadDocument("docs")

    chunks = chunkDocument(documents)

    createVectorStore(chunks)

    print("DONE ✅")


if __name__ == "__main__":
    main()