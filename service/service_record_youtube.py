import os
import math
from dto.dto import YoutubeReq, YoutubeRes
from pytube import YouTube
from moviepy.editor import VideoFileClip
from PIL import Image

# Post
def youtube_recorder(
	req: YoutubeReq
) :
	project_id = req.projectId
	url = req.url
	start_time = req.startTime
	end_time = req.endTime
	
	video_duration = end_time - start_time
	conversion_start_time = convert_time(start_time)
	conversion_end_time = convert_time(end_time)
	
	if start_time == end_time:
		return YoutubeRes(
			projectId=-1,
			thumbnails=None,
			videos=None
		)

	print(f"=======================================================\n"
				f"Start downloading youtube video for project {project_id}.\n"
				f"URL: {url}\n"
				f"Recording time: {conversion_start_time} - {conversion_end_time}\n"
				f"=======================================================")

	downloaded_path = download_video(url, project_id)
	saved_path = make_clip_video(downloaded_path, f"./video_src/{project_id}/clip.mp4", conversion_start_time, conversion_end_time)
	split_clip(saved_path, f"./video_src/{project_id}", video_duration)
		
	return YoutubeRes(
		projectId=project_id,
		thumbnails=[f"http://localhost:8000/static/video_src/{project_id}/frame_{i}.jpg" for i in range(math.floor(video_duration / 5))],
		videos=[f"http://localhost:8000/static/video_src/{project_id}/split_video_{i}.mp4" for i in range(math.floor(video_duration / 5))]
	)


def download_video(url, project_id):
	download_path = f"./video_src/{project_id}/"
	mp4_path = f"original.mp4"
	yt = YouTube(url)
	stream = yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True).first()

	if os.path.exists(download_path + mp4_path):
		os.remove(download_path + mp4_path)
	else:
		os.makedirs(os.path.dirname(download_path + mp4_path), exist_ok=True)
		
	downloaded_path = stream.download(filename=download_path + mp4_path)
	return downloaded_path
	
	
def make_clip_video(path, save_path, start_t, end_t):
	if os.path.exists(save_path):
		os.remove(save_path)
	
	clip_video = VideoFileClip(path).subclip(start_t, end_t)
	clip_video.write_videofile(save_path)
	
	os.remove(path)
	
	return save_path
	

def split_clip(
	path,
	save_path,
	video_duration,
):
	duration_for_cuts = 5
	
	for file in os.listdir(save_path):
		if "split_video_" in file:
			os.remove(f"{save_path}/{file}")
		if "frame_" in file:
			os.remove(f"{save_path}/{file}")
	
	for i in range(math.floor(video_duration / duration_for_cuts)):
		start_time = convert_time(i * duration_for_cuts)
		end_time = convert_time((i + 1) * duration_for_cuts)
		
		clip_video = VideoFileClip(path).subclip(start_time, end_time)
		clip_video.write_videofile(f"{save_path}/split_video_{i}.mp4")
		
		clip = VideoFileClip(f"{save_path}/split_video_{i}.mp4")
		clip.save_frame(f"{save_path}/target_{i}.png", t=1)
		im = Image.open(f"{save_path}/target_{i}.png")
		im.convert('RGB').save(f"{save_path}/frame_{i}.jpg", quality=30)
		os.remove(f"{save_path}/target_{i}.png")
	
	os.remove(path)
	
		
def convert_time(sec):
	hour = math.floor(sec / 3600)
	if hour < 10:
		hour_str = "0" + str(hour)
	else:
		hour_str = str(hour)
		
	minute = math.floor((sec % 3600) / 60)
	if minute < 10:
		minute_str = "0" + str(minute)
	else:
		minute_str = str(minute)
		
	sec = sec % 60
	if sec < 10:
		sec_str = "0" + str(sec)
	else:
		sec_str = str(sec)
		
	return f"{hour_str}:{minute_str}:{sec_str}"

# Get
def get_youtube_video(
	project_id: int
) -> YoutubeRes:
	# Check if there are saved data
	if not os.path.exists(f"./video_src/{project_id}"):
		return YoutubeRes(
			projectId=-1,
			thumbnails=[],
			videos=[]
		)
	
	return YoutubeRes(
		projectId=project_id,
		thumbnails=[f"http://localhost:8000/static/video_src/{project_id}/frame_{i}.jpg" for i in range(5)],
		videos=[f"http://localhost:8000/static/video_src/{project_id}/split_video_{i}.mp4" for i in range(5)]
	)