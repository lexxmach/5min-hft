from fastapi import FastAPI
from src.routers import user_router, questions_router
from src.models import database

database.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

app.include_router(user_router.router)
app.include_router(questions_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the game!"}