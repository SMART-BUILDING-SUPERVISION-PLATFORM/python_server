import os
import shutil
import subprocess
from dto.dto import Res, Req
from base64 import b64decode


def entry_pano_to_3d(req: Req) -> Res:
	project_id = req.projectId
	pano_base64 = req.panoBase64
	
	save_pano(pano_base64, project_id)
	
	res = Res(
		projectId=project_id,
		description="This came from python server."
	)
	
	return res

def save_pano(
	pano_base64: list[dict[str, str]],
	project_id: int
) -> None:
	
	pano_dir = f'./panorama_src/{project_id}'
	model_dir = f'./gltf_src/{project_id}'
	if os.path.exists(pano_dir):
		shutil.rmtree(pano_dir)
		shutil.rmtree(model_dir)
	
	if not os.path.exists(model_dir):
		os.makedirs(model_dir, exist_ok=True)
	
	# Temporal code
	
	for i in range(len(pano_base64)):
		decoded = b64decode(pano_base64[i]['src'])
		filename = f'./panorama_src/{project_id}/panorama_{i}.jpg'
		# Check if file exists
		if os.path.exists(filename):
			os.remove(filename)  # Remove existing file
		else:
			os.makedirs(os.path.dirname(filename), exist_ok=True)
		
		with open(filename, 'wb') as f:
			f.write(decoded)
		print(f'사용자 >> File {filename} saved.')
		
		make_obj_for_test(filename, project_id, i)
	
	# make_h_v_plane(project_id)
	

def make_obj_for_test(
	filename: str,
	project_id: int,
	i: int
) -> None:
	gltf_filename = f'./gltf_src/{project_id}/panorama_{i}.gltf'
	
	if os.path.exists(filename):
		# Copy the original OBJ file to the destination
		if os.path.exists(gltf_filename):
			os.remove(gltf_filename)
		else:
			os.makedirs(os.path.dirname(gltf_filename), exist_ok=True)
		shutil.copyfile(f'./dummy_gltf/dummy_{i}.gltf', gltf_filename)


# data 경로
data_dir = "/Users/jay/Desktop/_dev/main/workspace/Capstone Design/model_server/"

# PART2. 3D 모델링
# h,v 평면 추출이 실행되었는지 확인 후 3d 모델링 진행
# h,v 평면을 통해 3d 모델링 (To always visualize all the planes, add --mesh_show_back_face.)
def make_3d_model(
	origin_image_dir,
	pano_mask_dir,
	pano_3d_dir,
	image_name
):
	try:
		subprocess.run(["python",
										"./service/PanoPlane360/vis_planes.py",
										"--img", os.path.join(origin_image_dir, image_name),
										"--h_planes", os.path.join(pano_mask_dir, image_name).replace(".jpg", "_h_planes.exr"),
										"--v_planes", os.path.join(pano_mask_dir, image_name).replace(".jpg", "_v_planes.exr"),
										"--mesh",
										"--save_path", pano_3d_dir])
		
		print("3D 모델링 완료")
	except Exception as e:
		print(e)
		return False


# PART1. H, V Segmentation
def make_h_v_plane(
	project_id
):
	origin_image_dir = os.path.join(data_dir, "panorama_src", str(project_id))  # 원본 이미지 경로
	pano_mask_dir = os.path.join(data_dir, "panorama_src", str(project_id), "h_v_plane")  # 원본 이미지 h,v 마스크 경로
	pano_3d_dir = os.path.join(data_dir, "gltf_src", str(project_id))  # 원본 모델 경로
	
	for image_name in os.listdir(origin_image_dir):
		if image_name.endswith(('.jpg', '.jpeg', '.png')):
			try:
				# 1) h,v 평면 추출
				subprocess.run(["python",
												"./service/PanoPlane360/inference.py",
												"--pth", "./service/PanoPlane360/ckpt/mp3d.pth",
												"--glob", os.path.join(origin_image_dir, image_name),
												"--outdir", pano_mask_dir])
				print("h,v 평면 추출 완료")
				
				# 2) h,v 평면을 통해 3d 모델링 (To always visualize all the planes, add --mesh_show_back_face.)
				# vis_planes.py: error: unrecognized
				# arguments: --save_path/Users/jay/Desktop/_dev/main/workspace/Capstone Design/model_server/gltf_src/1
				make_3d_model(origin_image_dir, pano_mask_dir, pano_3d_dir, image_name)
			except Exception as e:
				print(e)
				return False