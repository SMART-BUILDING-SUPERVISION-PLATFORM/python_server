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
		
import urllib
import m3u8
import streamlink
import subprocess
import os


class stream_youtube:

  def __init__(self, url):
    self.url = url
    self.cont = True

  def get_stream(self, quality):
    """
        Get upload chunk url
        """
    streams = streamlink.streams(self.url)
    stream_url = streams[quality]
    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]  # segment의 맨 처음 것을 기준으로 저장함.

  def start(self, filename, segment_duration=10, default_duration=60):
    '''
        :param filename: save file name ex) projectA
        :param default_duration: 총 녹화시간(초), default 120 ex) 100
        :param segment_duration: 개별 동영상 녹화시간(초) / default 10 ex) 30
        :return: None
        '''
    print(f"Start recording....")
    pre_time_stamp = 0
    total_duration = 0
    duration = 0  # one segment
    while True:
      stream_segment = self.get_stream(quality="best")
      cur_time_stamp = stream_segment.program_date_time.strftime(
          "%Y%m%d-%H%M%S")
      if pre_time_stamp == cur_time_stamp:
        pass
      else:
        print(cur_time_stamp)
        if segment_duration < duration or duration == 0:
          file = open(filename + '_' + str(cur_time_stamp) + '.ts', 'ab+')
          duration = 0
        with urllib.request.urlopen(stream_segment.uri) as response:
          html = response.read()
          file.write(html)
        duration += stream_segment.duration
        total_duration += stream_segment.duration
        pre_time_stamp = cur_time_stamp
      if default_duration < total_duration:
        break
      if not self.cont:
        break

  def end(self):
    print("End recording....")
    self.cont = False
    self.convert_ts_2_mp4()

  def convert_ts_2_mp4(self):
    path = "./"
    file_list = os.listdir(path)
    for file in file_list:
      if file.endswith(".ts"):
        subprocess.run(["ffmpeg", "-i", file, file.replace('.ts', '.mp4')])
        print(f"convert complete: {file}")


stream = stream_youtube(
    url="https://www.youtube.com/live/ON6XV5YCCiI?si=_VVNF9ULIKHNR7Er")

stream.start(filename="projectA")  # Start recording
'''
:param filename: save file name ex) projectA
:param default_duration: 총 녹화시간(초), default 60
:param segment_duration: 개별 동영상 녹화시간(초) / default 10
:return: None
'''

stream.end(
)  # End recording (stream.start의 param인 'default_duration' 보다는 빨리 눌러야 꺼짐. 아니면 default_duration에 꺼짐)

