from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Car(Base):
    __tablename__ = 'Car'
    ID = Column(Integer(), primary_key=True, index=True)
    Brand = Column(String(50), nullable=False)
    Model = Column(String(50), nullable=False)
    Prod_Year = Column(Integer(), nullable=False)

class Car_Rating(Base):
    __tablename__ = 'CarRating'
    ID = Column(Integer(), primary_key=True, index=True)
    Car_ID = Column(Integer(), ForeignKey('Car.ID')) # onelete = 'cascade'
    Car_Grade = Column(Integer(), nullable=True)
