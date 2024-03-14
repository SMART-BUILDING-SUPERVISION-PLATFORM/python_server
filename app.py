from fastapi import FastAPI
from dto import Req, Res
from service.service import a
from fastapi.middleware.cors import CORSMiddleware
import time

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

# API handler
@app.post("/panorama", response_model=Res)
async def read_root(req: Req) -> Res:
	print(12341234)
	res = a(req)
	time.sleep(5)

	return res
