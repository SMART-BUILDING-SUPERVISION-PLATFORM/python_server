from dto import Res, Req
from base64 import b64decode

def responser(req: Req):
	project_id = req.projectId
	pano_base64 = req.panoBase64
	print(f"API GET: project number {project_id} has been safely delivered.")
	
	decoder(pano_base64)
	
	res = Res(
		projectId=project_id,
		description="This came from python server."
	)
	
	return res

def decoder(pano_base64: str):
	decoded = b64decode(pano_base64)
	
	filename = './panorama_src/panorama_received.jpg'
	with open(filename, 'wb') as f:
		f.write(decoded)
		

