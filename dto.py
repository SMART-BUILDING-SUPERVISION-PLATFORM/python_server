from pydantic import BaseModel

class Res(BaseModel):
    projectId: int
    virtualUrl: str
    panoBase64: str
    description: str

class Req(BaseModel):
    projectId: int
    panoBase64: str