from pydantic import BaseModel

class Result(BaseModel):
    result:bool
    message:str

class ResultList(BaseModel):
    result:bool
    message: str
    body: object