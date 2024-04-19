from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the database connection
engine = create_engine("sqlite:///shots.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Shot model
class Shot(Base):
    __tablename__ = "shots"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    club = Column(String)
    distance = Column(Integer)

# Define the request model
class ShotRequest(BaseModel):
    user_id: int
    club: str
    distance: int

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.post("/shots")
def create_shot(shot: ShotRequest):
    db = SessionLocal()
    db_shot = Shot(user_id=shot.user_id, club=shot.club, distance=shot.distance)
    db.add(db_shot)
    db.commit()
    db.refresh(db_shot)
    db.close()
    return {"message": "Shot data stored successfully"}