from pydantic import BaseModel

class Res(BaseModel):
    projectId: int
    description: str

class Req(BaseModel):
    projectId: int
    panoBase64: list[dict[str, str]]
    
class YoutubeReq(BaseModel):
    projectId: int
    url: str
    startTime: int
    endTime: int

class YoutubeRes(BaseModel):
    projectId: int
    thumbnails: list[str] = []
    videos: list[str] = []