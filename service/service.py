from dto import Res, Req
from base64 import b64decode

virtualtour_url = "http://localhost:8000/"

def a(req: Req):
	project_id = req.projectId
	pano_base64 = req.panoBase64
	res = Res(projectId=project_id, virtualUrl=virtualtour_url, panoBase64=pano_base64,
						description="This came from python server.")
	
	print(f"API GET:   project number {project_id} has been safely delivered.")
	
	decoder(pano_base64)
	
	return res

def decoder(pano_base64: str):
	decoded = b64decode(pano_base64)
	
	filename = 'some_image.jpg'
	with open(filename, 'wb') as f:
		f.write(decoded)
	return decoded