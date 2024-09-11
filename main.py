from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Annotated
from sqlalchemy import desc

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class CarBase(BaseModel):
    Brand: str
    Model: str
    Prod_Year: int

class CarRatingBase(BaseModel):
    Car_ID: int
    Car_Grade: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
