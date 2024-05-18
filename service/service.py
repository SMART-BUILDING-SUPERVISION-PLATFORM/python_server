import os
import shutil
from dto import Res, Req
from base64 import b64decode

def responser(req: Req):
	project_id = req.projectId
	pano_base64 = req.panoBase64
	print(f"API GET: project number {project_id} has been safely delivered.")
	
	decoder(pano_base64, project_id)
	
	res = Res(
		projectId=project_id,
		description="This came from python server."
	)
	
	return res

def decoder(pano_base64: str, project_id: int):
	decoded = b64decode(pano_base64)
	
	filename = f'./panorama_src/project_{project_id}.jpg'
	# Check if file exists
	if os.path.exists(filename):
		os.remove(filename)  # Remove existing file
	
	with open(filename, 'wb') as f:
		f.write(decoded)
	
	obj_maker(filename, project_id)
	
	
# 여기서 jpg to obj 소스 삽입하여 실제 obj 파일 생성(지금은 더미 파일만 생성)
def obj_maker(filename: str, project_id: int):
	obj_filename = f'./obj_src/project_{project_id}.obj'
	
	if os.path.exists(filename):
		# Copy the original OBJ file to the destination
		shutil.copyfile('./dummy_obj/dummy.obj', obj_filename)
	else:
		print(f"Error: File {filename} does not exist.")