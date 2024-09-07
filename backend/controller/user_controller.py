from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from utils.encrypt import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from database.models import usermodel
from database.schemas import userschema

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

class GetCurrentUser:
    def __init__(self, db: Session):
        self.db = db

    def __call__(self, token: str = Depends(reuseable_oauth)):
        try:
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
            )

            expiration = payload.get("exp")
            user = payload.get("sub")

            if datetime.fromtimestamp(expiration) < datetime.now():
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except(jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        statement = select(usermodel.User).filter_by(email=user)
        user_obj = self.db.scalars(statement).all()

        if(len(user_obj) == 0) :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        else:
            user_obj = user_obj[0]

        user = userschema.UserResponse(
            id=user_obj.id,
            email=user_obj.email
        )
        return user

async def get_current_user(db:Session,token: str = Depends(reuseable_oauth))->userschema.UserResponse:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        expiration = payload.get("exp")
        user = payload.get("sub")

        if datetime.fromtimestamp(expiration) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    statement = select(usermodel.User).filter_by(email=user)
    user_obj = db.scalars(statement).all()

    if(len(user_obj) == 0) :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    else:
        user_obj = user_obj[0]

    user = userschema.UserResponse(
        id=user_obj.id,
        email=user_obj.email
    )
    return user