import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader

load_dotenv()
from langchain_text_splitters import CharacterTextSplitter, TextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma

def loadDocument(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    loader = DirectoryLoader(path=file_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        raise ValueError(f"No documents found in {file_path}")
    
    print(f"Loaded {len(documents)} documents from {file_path}")

    # for i, doc in enumerate(documents[:2]):
        # print(f"Document {i}: {doc.page_content}")

        # print("-" * 100)
        # print(doc.metadata)
        # print("-" * 100)
        # print(doc.page_content)
        
    return documents

def chunkDocument(documents,chunk_size=500,chunk_overlap=100):
    textSplitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = textSplitter.split_documents(documents)

    if not chunks:
        raise ValueError(f"No chunks found for {documents}")

    print(f"Chunked {len(chunks)} chunks from {len(documents)} documents")
    # for i, chunk in enumerate(chunks[:2]):
    #     print(f"Chunk {i}: {chunk.page_content}")

    #     print("-" * 100)
    #     print(chunk.metadata)
    #     print("-" * 100)
    #     print(chunk.page_content)
    return chunks

def createVectorStore(chunks, persist_dir="db/chroma", batch_size=32):
    print("Creating vector store...")
    embeddings = FastEmbedEmbeddings()
    vectorStore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir,
        collection_name="metadata_collection",
    )
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vectorStore.add_documents(batch)
        print(f"Indexed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")
    print("Vector store created successfully")
    return vectorStore

def main():
    print("Starting document ingestion...")
    documents = loadDocument("docs")
    print("Document ingestion completed")
    chunks = chunkDocument(documents)
    print("Chunking completed")
    vectorStore = createVectorStore(chunks)
    print("Vector store created successfully")
main()