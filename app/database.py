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


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="cheesecake",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("DB connection successfully established.")
#         break
#     except Exception as error:
#         print(f"Connecting to DB failed \nError: {error}")
#         time.sleep(2)
