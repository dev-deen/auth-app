from database import Base
from sqlalchemy import Column, Integer, String, Enum, Float
import enum

class RoleEnum(str, enum.Enum):
    admin = 'admin'
    employee = 'employee'

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.employee)

class EmployeeModel(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    designation = Column(String(50), nullable=False)
    salary = Column(Float, nullable=False)