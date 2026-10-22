from typing import List

from fastapi import Depends, HTTPException, status, FastAPI
from database import get_db
from sqlalchemy.orm import Session
from database import Base, engine
from models import UserModel
from schemas import EmployeeResponse, UserRegister, UserResponse
from auth import create_access_token, require_admin, verify_password, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication API",
    description="API for user authentication and authorization",
    version="1.0.0",
)

@app.post("/user-register", response_model=UserResponse)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user_in.username) | (UserModel.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )
    hashed_password = get_password_hash(user_in.password)
    new_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/user/login', response_model=UserResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/employees", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db), user: UserModel = Depends(require_admin)):
    employees = db.query(UserModel).all()
    return employees

@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db), user: UserModel = Depends(require_admin)):
    employee = db.query(UserModel).filter(UserModel.id == employee_id).first()
    if not employee: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    db.delete(employee)
    db.commit()
    return None