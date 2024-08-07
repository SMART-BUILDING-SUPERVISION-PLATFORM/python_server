from fastapi import FastAPI
from dto.dto import Req, Res, YoutubeReq, YoutubeRes
from service.service_pano_to_3d import entry_pano_to_3d
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from service.service_record_youtube import youtube_recorder, get_youtube_video

app = FastAPI()

# CORS handler
origins = ["http://localhost:3000"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="/Users/jay/Desktop/_dev/main/workspace/Capstone Design/python_server"), name="static")

# API handler
"""
for receiving the panorama image and project id from the client
because this server cannot reach directly to the DB system.
"""
@app.post("/panorama", response_model=Res)
async def pano_to_3d(req: Req) -> Res:
	return entry_pano_to_3d(req)

@app.post("/youtube", response_model=YoutubeRes)
async def control_youtube(
	req: YoutubeReq
) -> YoutubeRes:
	return youtube_recorder(req)

@app.get("/youtube/{project_id}", response_model=YoutubeRes)
async def get_saved_data(project_id: int) -> YoutubeRes:
	return get_youtube_video(project_id)