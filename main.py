from fastapi import FastAPI
from datalayer.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

from routers import users, gamejam

 
app = FastAPI()

app.include_router(gamejam.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create the database
Base.metadata.create_all(engine)

 
@app.get('/')
def index():
    return {":":")"}
 



