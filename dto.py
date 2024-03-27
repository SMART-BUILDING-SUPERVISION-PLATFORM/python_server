from pydantic import BaseModel

class Res(BaseModel):
    projectId: int
    description: str

class Req(BaseModel):
    projectId: int
    panoBase64: str