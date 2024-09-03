import pickle
import os
from dotenv import find_dotenv, load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import openai
# Load the envionment variables
# load_dotenv()

api_key = "AIzaSyAh4lGJWKH8wp8XSde624-lJtIssYv-Bj0"

# The embeddings function is needed!!
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=api_key)

def load_faiss_embeddings_file(embeddings_path:str):
    """
    This function returns the FAISS db vectorstore for the selected file
    """
    with open(embeddings_path, "rb") as f:
        pkl = pickle.load(f)

    # Load from the saved index
    db = FAISS.deserialize_from_bytes(
        embeddings=embeddings, serialized=pkl
    ) 
    return db 