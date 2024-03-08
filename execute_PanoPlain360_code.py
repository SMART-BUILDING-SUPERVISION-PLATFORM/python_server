import os
import subprocess

def model_run():
  # 현재 디렉토리 경로 확인
  current_dir = os.getcwd()
  
  # 상세 data 경로 지정
  origin_input_dir = current_dir  # 원본 이미지 경로
  pano_output_dir = os.path.join(current_dir, "image100_Pano")  # 원본 h,v 결과 이미지 경로
  pano_3d_output_dir = os.path.join(current_dir, "image100_Pano_3D")  # 원본 모델 경로
  print(f"origin_input_dir: {origin_input_dir}")
  print(f"pano_output_dir: {pano_output_dir}")
  print(f"pano_3d_output_dir: {pano_3d_output_dir}")
  
  # 적용하고자 하는 이미지 지정
  image_name = os.path.join(origin_input_dir, "\some_image.jpg")
  
  ### 원본 이미지에 대하여
  # h,v 평면 추출
  plane_inference = subprocess.run(
      ["python", "CCC_PanoPlane360/PanoPlane360/inference.py", "--pth", "CCC_PanoPlane360/PanoPlane360/ckpt/mp3d.pth",
       "--glob", origin_input_dir + image_name, "--outdir", pano_output_dir])
  # print(plane_inference)
  
  # h,v 평면 추출이 실행되었는지 확인
  if plane_inference.returncode == 0:
      # h,v 평면을 통해 3d 모델링 (To always visualize all the planes, add --mesh_show_back_face.)
      subprocess.run(["python", "CCC_PanoPlane360/PanoPlane360/vis_planes.py", "--img", origin_input_dir + image_name,
                      "--h_planes", pano_output_dir + image_name.replace(".jpg", "") + ".h_planes.exr", "--v_planes",
                      pano_output_dir + image_name.replace(".jpg", "") + ".v_planes.exr", "--mesh", "--save_path",
                      pano_3d_output_dir])
  else:
      print("error")

# data 경로 지정
# data_dir = os.path.join(current_dir, "data")

# custom_input_dir = os.path.join(data_dir, "image100_custom") # SAM 처리 이미지 경로
# custom_output_dir = os.path.join(data_dir, "image100_custom_Pano") # SAM h,v 결과 이미지 경로
# custom_3d_output_dir = os.path.join(data_dir, "image100_custom_Pano_3D") # SAM 모델 경로

# ### custom 이미지에 대하여
#
# # h,v 평면 추출
# plane_inference = subprocess.run(["python", "CCC_PanoPlane360/PanoPlane360/inference.py", "--pth", "CCC_PanoPlane360/PanoPlane360/ckpt/mp3d.pth", "--glob", custom_input_dir+image_name, "--outdir", custom_output_dir])
# print(plane_inference.returncode)
#
# #  h,v 평면 추출이 성공적으로 실행되었는지 확인
# if plane_inference.returncode == 0:
#     # h,v 평면을 통해 3d 모델링
#     subprocess.run(["python", "CCC_PanoPlane360/PanoPlane360/vis_planes.py", "--img", origin_input_dir+image_name, "--h_planes", custom_output_dir+image_name.replace(".jpg", "")+".h_planes.exr", "--v_planes", custom_output_dir+image_name.replace(".jpg", "")+".v_planes.exr", "--mesh_show_back_face", "--save_path", custom_3d_output_dir])
# else:
#     print("error")