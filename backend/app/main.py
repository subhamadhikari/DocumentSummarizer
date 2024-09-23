from fastapi import FastAPI,Depends,HTTPException,Request,Response,File,UploadFile,status,BackgroundTasks
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import io

import uuid

from pydantic import BaseModel

from starlette.requests import Request

from database.schemas import userschema,chatschema
from database.models import usermodel,chatmodel
from database.configurations import SessionLocal,engine,Base

from sqlalchemy.orm import Session,aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,func

from chat.chat import parse_pdf

from chat.testchat import user_input

import google.generativeai as genai

from fastapi.security import OAuth2PasswordRequestForm



from langserve import add_routes
from pydantic import BaseModel
from chat.schema import ChatRequest
from chat.chain import answer_chain
from chat.testchat import user_input

from utils.mychat import prepare_chatbot_over_subset
from utils.chatbot import Chatbot
from utils.encrypt import encrypt_pass,verify_pass,create_access_token

from uuid import uuid4

from controller.user_controller import get_current_user,GetCurrentUser


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specify which origins are allowed
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

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    
    class Config:
        orm_mode = True

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

@app.post("/login")
def signin(form_data:OAuth2PasswordRequestForm = Depends(),session:Session = Depends(db_session)):
    statement = select(usermodel.User).filter_by(email=form_data.username)
    user_obj = session.scalars(statement).all()

    if(len(user_obj) == 0) :
        print("not found the user")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User could not be found !"
        )
    else:
        user_obj = user_obj[0]
    isValidUser = verify_pass(user_obj.encrypt_password,form_data.password,user_obj.salt)

    if not isValidUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email or password is incorrect"
        )
    
    return {
        "status_code":status.HTTP_200_OK,
        "access_token":create_access_token(user_obj.email),
        "token_type":"Bearer"
    }


@app.post("/logout")
def logout():
    if hasattr(app,"user"):
        del app.user
    
    if hasattr(app,"session"):
        del app.session

db_gen = db_session()
db = next(db_gen)

currentuser = GetCurrentUser(db=db)
@app.get('/getCurrentUser', summary='Get details of currently logged in user',response_model=userschema.UserResponse)
async def get_me(user:userschema.UserResponse = Depends(currentuser)):
    # app.user = user
    # return user
    if user:
        app.user = user
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# @app.get('/getCurrentUser', summary='Get details of currently logged in user',response_model=userschema.UserResponse)
# async def get_me(user:userschema.UserResponse = Depends(get_current_user)):
#     return user

# @app.post("/signin")
# def signin(user:userschema.UserSchema,session:Session = Depends(db_session)):
#     statement = select(usermodel.User).filter_by(email=user.email)
#     user_obj = session.scalars(statement).all()
#     if(len(user_obj) == 0) :
#         print("not found the user")
#         return {"message":"user not found!","status":404}
#     else:
#         user_obj = user_obj[0]
#     isValidUser = verify_pass(user_obj.encrypt_password,user.password,user_obj.salt)
#     print("passwrd correct :",isValidUser)
#     return {"message":"user found!"}

@app.post("/submitdocument")
async def submitDoc(document:UploadFile,session:Session = Depends(db_session)):
    content = await document.read()
    parse_pdf(io.BytesIO(content),document.filename)
    print("i am here")
    return {"message":"document parsed successfully"}


# new chat
@app.post("/startchat")
async def startchat(document:UploadFile,session:Session = Depends(db_session)):
    global session_id_temp
    try:
        session_id = uuid.uuid4()
        print(session_id,"--new session id")

        
        session_id_temp = session_id
        app.session = session_id_temp
        content = await document.read()

        parse_pdf(io.BytesIO(content),document.filename,session_id_temp)

        chatbot = await prepare_chatbot_over_subset(session_id)

        app.chatbot = chatbot
        app.doc_title=document.filename
        print(chatbot,"--chatbot")
        print("chat system",document.filename)

        # change made here
        app.db_session = session

        # user_input("Give me the summary?")
        # user_input("Hey!")

        return {"message":"document parsed successfully"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    
class Item(BaseModel):
    question: str
    

@app.post("/mychat")
async def mychat(item:Item,background_tasks:BackgroundTasks):
    print("first:::call --- mychat")
    conversation_id = uuid.uuid4()
    # session_id = app.session
    if not hasattr(app, 'chatbot'):
        raise HTTPException(status_code=405, detail="Chatbot not loaded..")
    response = app.chatbot.conversational_chat(item.question,conversation_id,session_id_temp)
    # result = user_input(item.question)

    if response is not None:
        message = chatschema.ChatSchema(humanmsg=item.question,aimsg=response,session=str(session_id_temp),timestamp="2023-09-12",)

        if hasattr(app,"user"):
            background_tasks.add_task(savechat,message,app.user,app.db_session)

    return {"result":response}


# old chat
# ,response_model=chatschema.Chat
@app.get("/loadchat")
async def loadchat(chat_session:str,user:userschema.UserResponse=Depends(currentuser),db_session:Session=Depends(db_session)):
    chat = chatmodel.Chat
    statement = select(chat).where(chat.chat_session==chat_session,chat.user_id==user.id).order_by(chat.timestamp)
    result = db_session.execute(statement)
    print("loaded chat:::")
    chats = []
    for chat in result.scalars().all():
        chats.append(chatschema.Chat(humanmsg=chat.human_msg,aimsg=chat.ai_msg))
    print(chats)
    return chats

@app.get("/loadchatlist")
# async def loadchatlist(user:userschema.UserResponse=Depends(currentuser),db_session:Session=Depends(db_session)):
async def loadchatlist(db_session:Session=Depends(db_session)):
    print("okay")
    # return 2
    try:
        user = None
        if app.user:
            print("chatlist bhitra")
            user = app.user
            print(app.user)
        else:
            print("no user")
            return 2
        # Define the row number subquery
        row_number_subquery = (
            db_session.query(
                chatmodel.Chat.chat_id,
                chatmodel.Chat.chat_session,
                chatmodel.Chat.user_id,
                chatmodel.Chat.human_msg,
                chatmodel.Chat.doc_title,
                chatmodel.Chat.timestamp,
                chatmodel.Chat.ai_msg,
                func.row_number().over(
                    partition_by=chatmodel.Chat.chat_session,  # Group by chat session
                    order_by=chatmodel.Chat.chat_id  # Order by chat ID (or timestamp)
                ).label("row_num")
            )
            .filter(chatmodel.Chat.user_id == user.id)  # Filter by current user
            .subquery()
        )

        # Query to select only the first occurrence (row_num = 1) of each chat session
        query = (
            select(row_number_subquery)
            .where(row_number_subquery.c.row_num == 1)
        )

        # Execute the query
        result = db_session.execute(query).all()

        # Process the result to create the chat list
        chat_list = []
        for row in result:
            chat_data = {
                "id": row[0],             # chat_id
                "chat_session": row[1],    # chat_session
                "user_id": row[2],         # user_id
                "human_msg": row[3],       # human_msg
                "doc_title": row[4],       # doc_title
                "timestamp": row[5],       # timestamp
                "ai_msg": row[6],          # ai_msg
            }
            chat_list.append(chat_data)

        return chat_list

    except SQLAlchemyError as e:
        # Rollback the transaction if any error occurs
        db_session.rollback()
        # Log the error and raise an HTTP exception
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db_session.close()


#  ------------------  Saving chats -------------------- #
# @app.post("/pushmessage")
# @app.middleware("http")
async def savechat(message:chatschema.ChatSchema=None,user:userschema.UserSchema = None,session:Session = None):
    # print(message)
    # print("-----------||||||-----------")
    # print(user.id)

        print("user:::in save chat",user)

        try:
            if hasattr(app,"user"):
                print("second:::call --- middleware")
                chat = chatmodel.Chat(chat_session=app.session,user_id=user.id,
                                    human_msg=message.humanmsg,ai_msg=message.aimsg,doc_title=app.doc_title,timestamp=message.timestamp)
                session.add(chat)
                session.commit()
                session.refresh(chat)
        except Exception as e:
            print(e)

        print("Execution finished!! in the background")



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

@app.on_event("shutdown")
def shutdown_event():
    next(db_gen, None) 