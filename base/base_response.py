from pydantic import BaseModel

class Result(BaseModel):
    result:str
    message:str

class ResultList(BaseModel):
    result:str
    message: str
    body: object