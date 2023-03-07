from fastapi import FastAPI 
from services.email.email_server_service import EmailServer, EmailModel
from fastapi.middleware.cors import CORSMiddleware

from routers import contact_router, gamejam_router, user_router, project_router

 
app = FastAPI()

app.include_router(gamejam_router.router)
app.include_router(user_router.router)
app.include_router(contact_router.router)
app.include_router(project_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create the database
# Base.metadata.create_all(engine)

 
@app.get('/')
def index(): 
    return {":":")"}
 



