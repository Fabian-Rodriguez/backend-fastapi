from fastapi import FastAPI, Depends, HTTPException, Request, status
import uvicorn
from db.database import Base, engine, get_db
from sqlalchemy.orm import Session
from db.models import User
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,ValidationError

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserCreate(BaseModel):
    username: str
    name: str
    password: str

def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()

@app.get("/")
def index(db: Session = Depends(get_db)):
    return {'message': 'Bienvenido'}

def get_user( user:str, password: str, db: Session):
    return db.query(User).filter(User.username == user and User.password == password).first()

def get_user_by_name( user:str, db: Session):
    return db.query(User).filter(User.username == user).first()

@app.post("/login_user")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        userSelected = jsonable_encoder(get_user(user.username, user.password, db))
        print(userSelected)
        return userSelected["name"]

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    

@app.post("/create_user")
async def create_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    try:
        verify = db.query(User).filter(User.username == user.username).first()
        if verify is not None:
            return 'Nombre existente'
        
        db_item = User(name=user.name, password=user.password, username=user.username)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return {"id": db_item.id}
    except Exception as e:
        print(f"Error in create_user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)