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

@app.post("/cars/")
async def create_car(car: CarBase, db: db_dependency):
    db_cars = models.Car(Brand=car.Brand, Model=car.Model, Prod_Year=car.Prod_Year)
    db.add(db_cars)
    db.commit()
    db.refresh(db_cars)

@app.post("/cars/{Car_ID}/rate")
async def create_car_rating(carrating: CarRatingBase, db: db_dependency):
    db_carrating = models.Car_Rating(Car_ID = carrating.Car_ID, Car_Grade=carrating.Car_Grade)
    if carrating.Car_Grade >= 1 and carrating.Car_Grade <= 5:
        db.add(db_carrating)
        db.commit()
        db.refresh(db_carrating)
    else:
        raise HTTPException(status_code=404, detail='Invalid Grade')
    
@app.get("/cars/top10")
async def get_top10(db: db_dependency, limit: int = 10):
    results = (
        db.query(
            models.Car_Rating.Car_ID, 
            func.avg(models.Car_Rating.Car_Grade),
            models.Car.Brand,
            models.Car.Model
            )
            .join(models.Car, models.Car_Rating.Car_ID == models.Car.ID)
            .group_by(models.Car_Rating.Car_ID, models.Car.Brand, models.Car.Model)
            .order_by(desc(func.avg(models.Car_Rating.Car_Grade)))
            .all()
    )
    response = [
        {
            "Car_ID": car_id,
            "average_grade": avg_grade,
            "Brand": brand,
            "Model": model
        } 
        for car_id, avg_grade, brand, model in results
    ]

    return response

