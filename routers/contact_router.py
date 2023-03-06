from fastapi import APIRouter
from pydantic import BaseModel
from base.base_response import Result
from config import settings
from services.email.email_server_service import EmailServer, EmailModel
import requests

CONTACT_ADDR = settings.CONTACTADDR
RECAPTCHA_SECRET = settings.RECAPTCHASECRET
RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

router = APIRouter()

router = APIRouter(
    prefix="/contact",
    tags=["contact"], 
    responses={404: {"description": "Not found"}},
) 

class ContactSchema(BaseModel):
    firstName: str 
    lastName: str 
    email: str
    message : str
    recaptchaToken : str

def verify_captcha(recaptchaToken):
    verified : False

    recaptchaObj = {
        'secret' : RECAPTCHA_SECRET,
        'response' : recaptchaToken
    }

    response = requests.post(RECAPTCHA_URL, json = recaptchaObj)
    verified = response.success

    return verified   

@router.post('/contact', tags=["contact"])
def contact(contact: ContactSchema):

    verified = verify_captcha(contact.recaptchaToken)

    if(verified == False):
         return Result(result=False,message="Captcha verification failed")
    
    sender_name = "MFG.GG Contact Form"
    emailer = EmailServer(sender_name)

    receiver_name = "Team-MFG"
    receiver_email = "jpl@mfg.gg"
    email_body = f'''
    You received a new contact message from: {contact.firstName} {contact.lastName} with email: {contact.email}
    Message:
    {contact.message}
    '''
    subject = f'Contact Us Message From {contact.email}'

    email_model = EmailModel(receiver_name, receiver_email, email_body, subject, "Demo Msg")
    emailer.send_mail(email_model)
    return Result(result=True,message="Contact Us Mail Sent")
