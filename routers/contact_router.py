import json
from fastapi import APIRouter
from pydantic import BaseModel
from base.base_response import Result
from config import settings
from services.email.email_server_service import EmailServer, EmailModel


import requests

from services.racaptcha.recaptcha_gcp_service import RecaptchaGCPEnterprise

CONTACT_ADDR = settings.CONTACTADDR
RECAPTCHA_SECRET = settings.RECAPTCHASECRET
RECAPTCHA_URL = "https://recaptchaenterprise.googleapis.com"

router = APIRouter()

router = APIRouter(
    prefix="/contact",
    tags=["contact"], 
    responses={404: {"description": "Not found"}},
) 
 
class ContactSchema(BaseModel):
    first_name: str 
    last_name: str 
    email: str
    message : str
    recaptcha_token : str

  
@router.post('/contact', tags=["contact"])
def contact(contact: ContactSchema):

    verified = RecaptchaGCPEnterprise(contact.recaptcha_token, "contact_submission")
 
    print("RECAPTCHA TOKEN 1:") 
    if(verified == False):
         return Result(result=False,message="Captcha verification failed")
    
    sender_name = "MFG.GG Contact Form"
    emailer = EmailServer(sender_name)

    receiver_name = "Team-MFG"
    receiver_email = "jpl@mfg.gg"
    email_body = f'''
    You received a new contact message from: {contact.first_name} {contact.last_name} \n with email: {contact.email}
    \n Message: \n \n
    {contact.message}
    '''
    subject = f'Contact Us Message From {contact.email}'

    email_model = EmailModel(receiver_name, receiver_email, email_body, subject, "Demo Msg")
    emailer.send_mail(email_model)

    return Result(result=True,message="Contact Us Mail Sent")
