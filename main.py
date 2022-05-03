from fastapi import FastAPI, Depends

import models
from database import engine
from dependencies.dependencies import get_db
from routes import students

models.Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(students.router)


@app.get("/")
async def root():
    return {"message": "Hello from the other side :)!"}
