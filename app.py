from fastapi import FastAPI
from dto import Req, Res
from service.service import responser
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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

app.mount("/static", StaticFiles(directory="/Users/jay/Desktop/_dev/main/workspace/kimth_lab/current/model_server/obj_src"), name="static")

# API handler
@app.post("/panorama", response_model=Res)
async def read_root(req: Req) -> Res:
	
	res = responser(req)

	return res
