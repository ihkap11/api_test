from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def health():
    return {"status": "I Am Aokayyy!!"}


# @app.get("/sqlalchemy")
# def test_orm_connection(db: Session = Depends(get_db)):
#     posts = db.query(models.Posts).all()
#     return {"data": posts}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
