from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# URL syntax '<type_of_database>://<username>:<password>@<ip-address/hostname>/<databe_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db.username}:{settings.db.password}@{settings.db.port}/{settings.db.name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
