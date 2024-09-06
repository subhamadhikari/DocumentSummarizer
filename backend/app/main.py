from fastapi import FastAPI,Depends,HTTPException,Request,Response,File,UploadFile
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import io

import uuid

from pydantic import BaseModel

from starlette.requests import Request

from database.schemas import userschema
from database.models import usermodel
from database.configurations import SessionLocal,engine,Base

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from chat.chat import parse_pdf

from chat.testchat import user_input

import google.generativeai as genai



from langserve import add_routes
from pydantic import BaseModel
from chat.schema import ChatRequest
from chat.chain import answer_chain
from chat.testchat import user_input

from utils.mychat import prepare_chatbot_over_subset
from utils.chatbot import Chatbot
from utils.encrypt import encrypt_pass,verify_pass


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to specify which origins are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

genai.configure(api_key="AIzaSyAh4lGJWKH8wp8XSde624-lJtIssYv-Bj0")

def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post("/signup")
def register(user:userschema.UserSchema,session:Session = Depends(db_session)):
    print("Subham Adhikari!")
    print(user)
    hash_password,salt = encrypt_pass(user.password)
    try:
        new_user = usermodel.User(salt=salt,encrypt_password=hash_password,email = user.email)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except SQLAlchemyError as e:
        print(f" errorxxx : {e.__dict__['orig']}")
        return {"message":"User creation failed!","status":500,"error":f"{e.__dict__['orig']}"}
    return {"message":"user created successfully","status":200}

@app.post("/signin")
def signin(user:userschema.UserSchema,session:Session = Depends(db_session)):
    statement = select(usermodel.User).filter_by(email=user.email)
    user_obj = session.scalars(statement).all()
    if(len(user_obj) == 0) :
        print("not found the user")
        return {"message":"user not found!","status":404}
    else:
        user_obj = user_obj[0]
    isValidUser = verify_pass(user_obj.encrypt_password,user.password,user_obj.salt)
    print("passwrd correct :",isValidUser)
    return {"message":"user found!"}

@app.post("/submitdocument")
async def submitDoc(document:UploadFile,session:Session = Depends(db_session)):
    content = await document.read()
    parse_pdf(io.BytesIO(content),document.filename)
    print("i am here")
    return {"message":"document parsed successfully"}


@app.post("/startchat")
async def startchat(document:UploadFile,session:Session = Depends(db_session)):
    global session_id_temp
    try:

        session_id,chatbot = await prepare_chatbot_over_subset()
        print(session_id,"--new session id")
        print(chatbot,"--chatbot")
        app.chatbot = chatbot
        session_id_temp = session_id

        content = await document.read()
        parse_pdf(io.BytesIO(content),document.filename)
        print("chat system",document.filename)

        # user_input("Give me the summary?")
        # user_input("Hey!")

        return {"message":"document parsed successfully"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    

class Item(BaseModel):
    question: str
    

@app.post("/mychat")
async def mychat(item:Item):
    conversation_id = uuid.uuid4()
    if not hasattr(app, 'chatbot'):
        raise HTTPException(status_code=405, detail="Chatbot not loaded..")
    response = app.chatbot.conversational_chat(item.question,conversation_id,session_id_temp)
    # result = user_input(item.question)

    return {"result":response}
# async def mychat(item:Item):
#     result = user_input(item.question)
#     print(result)
#     return {"result":result}

# Testing


# add_routes(
#     app,
#     answer_chain,
#     path="/mychat",
#     input_type=ChatRequest,
#     config_keys=["metadata", "configurable", "tags"],
# )
