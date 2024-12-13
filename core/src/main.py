from fastapi import FastAPI
from routers import user_router, questions_router, stats_router
from models import database
from fastapi.middleware.cors import CORSMiddleware


database.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(stats_router.router)
app.include_router(user_router.router)
app.include_router(questions_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the game!"}