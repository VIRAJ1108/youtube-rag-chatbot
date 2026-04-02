from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def create_vectorstore(chunks):
    documents = []

    for chunk in chunks:
        doc = Document(
            page_content=chunk["text"],
            metadata={
                "start": chunk["start"],
                "end": chunk["end"]
            }
        )
        documents.append(doc)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)

    return vectorstore