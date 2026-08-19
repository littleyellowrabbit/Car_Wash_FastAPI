from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class SQLBase(DeclarativeBase):
    pass

class User(SQLBase):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(15),nullable=False)
    permission : Mapped[str] = mapped_column(String(15),nullable=False)