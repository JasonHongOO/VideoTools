from moviepy.editor import VideoFileClip
from tqdm import tqdm

def Remove_Sound(input_video_path):
    video = VideoFileClip(input_video_path)
    video_without_audio = video.without_audio()
    video_without_audio.write_videofile("./Output/Output(SoundMV).mp4", codec="libx264")     # libx264 = H.264

def Speed_Up(input_video_path):
    video = VideoFileClip(input_video_path)
    video_SpeedUp = video.speedx(2)
    video_SpeedUp.write_videofile("./Output/Output(SpeedUp).mp4", codec="libx264")

def custom_progress_bar(progress):
    tqdm.write(f"Progress: {progress:.2%}")

if __name__ == "__main__":
    input_path = "test.mp4"    # 輸入影片的路徑
    Remove_Sound(input_path)
    Speed_Up(input_path)
