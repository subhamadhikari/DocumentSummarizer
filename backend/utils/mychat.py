from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from .chatbot import Chatbot
import uuid

async def prepare_chatbot_over_subset() -> dict:
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key="AIzaSyAh4lGJWKH8wp8XSde624-lJtIssYv-Bj0")

    db = FAISS.load_local(
        r"D:\internship\Verisk\DocumentSummarizer\backend\faiss_index", embeddings, allow_dangerous_deserialization=True)

    chatbot = Chatbot(model_name="gemini-1.5-flash", temperature=0, vectors=db)
    session_id = uuid.uuid4()

    return session_id,chatbot
