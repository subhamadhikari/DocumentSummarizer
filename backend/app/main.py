from fastapi import FastAPI,Depends,HTTPException,Request,Response,File,UploadFile
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import io

from starlette.requests import Request

from database import models,schema
from database.configurations import SessionLocal,engine,Base
from sqlalchemy.orm import Session

from chat.chat import parse_pdf

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specify which origins are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post("/register")
def register(user:schema.UserSchema,session:Session = Depends(db_session)):
    print("Subham Adhikari!")
    # new_user = models.User(first_name=user.first_name, last_name=user.last_name ,email=user.email, encrypt_password=user.password)
    # session.add(new_user)
    # session.commit()
    # session.refresh(new_user)
    return {"message":"user created successfully"}

@app.post("/submitdocument")
async def submitDoc(document:UploadFile,session:Session = Depends(db_session)):
    content = await document.read()
    parse_pdf(io.BytesIO(content),document.filename)

    return {"message":"document parsed successfully"}




