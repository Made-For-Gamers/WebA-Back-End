from pydantic import BaseModel

class Result(BaseModel):
    result:str
    message:str