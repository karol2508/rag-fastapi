from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
import os


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
embeddings = OpenAIEmbeddings()
vectorstore = None

def process_pdf(file_path: str) -> dict:
    global vectorstore
    
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(pages)
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    
    return {
        "pages": len(pages),
        "chunks": len(chunks)
    }

def load_existing_index() -> bool:
    global vectorstore
    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local(
            "faiss_index", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        return True
    return False

def get_answer(question: str) -> dict:
    global vectorstore
    
    if vectorstore is None:
        loaded = load_existing_index()
        if not loaded:
            return {
                "answer": "No document loaded. Please upload a PDF first.",
                "source": "none"
            }
    
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    source = docs[0].metadata.get("source", "unknown") if docs else "unknown"
    
    messages = [
        SystemMessage(content=f"""You are a helpful assistant that answers questions 
        based on the provided document context. Always base your answers on the context.
        If the answer is not in the context, say so clearly.
        
        Context:
        {context}"""),
        HumanMessage(content=question)
    ]
    
    response = llm.invoke(messages)
    
    return {
        "answer": response.content,
        "source": source
    }