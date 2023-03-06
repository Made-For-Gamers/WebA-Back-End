from fastapi import FastAPI
from datalayer.database import Base, engine
from services.email.email_server import EmailServer, EmailModel
from fastapi.middleware.cors import CORSMiddleware

from routers import users, gamejam, contact

 
app = FastAPI()

app.include_router(gamejam.router)
app.include_router(users.router)
app.include_router(contact.router)

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

    #TODO: Test Mail, remove.
    sender_name = "The MFGandalf"
    emailer = EmailServer(sender_name)

   
    receiver_name = "jp"
    receiver_email = "jpl@mfg.gg"
    email_body = '''
    Hello JP. This is a test Email Body. Html enabled Body To follow
'''
    email_model = EmailModel(receiver_name, receiver_email, email_body, "You Shall Pass! Welcome to the 2023 Game Jam!", "Demo Msg")
    
    emailer.send_mail(email_model)
    return {":":")"}
 



