import os
import json
from yt_dlp import YoutubeDL
import subprocess

cur_path = os.path.dirname(os.path.abspath(__file__))   # 當前 python 檔案的位置
file_path = os.path.join(cur_path, "ffmpeg")            # 串接 ffmpeg，注意這是資料夾， path 是資料夾路徑，不是檔案
os.environ["PATH"] = file_path

def extract_video_data_from_url(url):
    command = ['./yt-dlp/yt-dlp.exe', "--dump-json",url]
    output = subprocess.run(command, capture_output=True, text=True, check=True)
    output_stdout = output.stdout
    output_json_start_index = output_stdout.index("{")
    output_json_str = output_stdout[output_json_start_index:]
    output_json = json.loads(output_json_str)
    video_data = output_json

    #寫入檔案，方面後續查看
    with open("./Content.json", "w") as output_json_file:
        json.dump(output_json, output_json_file, indent=4)

    #影片基本資訊
    title = video_data["title"]             #標題
    thumbnail = video_data["thumbnail"]     #封面
    duration = video_data["duration"]       #長度

    #影片格式
    formats = video_data["formats"]

def VideoGetInfo(url):
    with YoutubeDL() as ydl:
        #取出資訊
        info_json = ydl.extract_info(url, download=False)
        #寫入檔案，方面後續查看
        with open("./Content.json", "w") as output_json_file:
          json.dump(info_json, output_json_file, indent=4)
        #取出影片的所有解析度
        # ydl.list_formats(info_json)
    
    return info_json

def VideoSettingOption(Title, Video_ID, Audio_ID, mode):
    FormatString = ""
    if Video_ID != "None" or Audio_ID != "None" : 
        if Video_ID != "None" and Audio_ID != "None" : FormatString = Video_ID + "+" +  Audio_ID
        elif Video_ID != "None" : FormatString = Video_ID
        elif Audio_ID != "None" : FormatString = Audio_ID

    if(mode == "mp4"):
        ydl_opts = {
            'format': FormatString,  # 使用特定的音檔和影片格式 ID
            'outtmpl': f'./Output/{Title}(JasonHong).' + '%(ext)s',  # 下載的文件名格式
            # 'progress_hooks': [progress_hook],
        }
    elif(mode == "mp3"): 
        ydl_opts = {
            'format': 'bestaudio/best',  # 使用最佳音訊品質
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # 轉換為 MP3 格式
                'preferredquality': '192',  # 設定 MP3 的品質 (bitrate)
            }],
            'outtmpl': f'./Output/{Title}(JasonHong).' + '%(ext)s',  # 下載的文件名格式
        }
    
    return ydl_opts

def VideoDownload(url, Video_ID="None", Audio_ID="None", mode="mp4"):
    # def progress_hook(response):
        # if response['status'] == 'downloading':
            # print(response)
            #寫入檔案，方面後續查看
            # with open("./Downloading.json", "w") as output_json_file:
            #     json.dump(response, output_json_file, indent=4)

    # 影片資料
    video_data = VideoGetInfo(url)
    Title = video_data["title"].replace('[', ' ').replace(']', ' ').replace('【', ' ').replace('】', ' ')
    
    # Setting
    ydl_opts = VideoSettingOption(Title, Video_ID, Audio_ID, mode)

    # download
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f'./Output/{Title}(JasonHong).{mode}'    #返回路徑


# url = "https://www.youtube.com/watch?v=oRaNp3BljuE&ab_channel=%E7%B4%85%E6%9C%88"
# url = "https://www.facebook.com/watch?v=928553878250919"
# extract_video_data_from_url(url)
# VideoDownload(url)
# https://www.youtube.com/watch?v=oRaNp3BljuE&ab_channel=%E7%B4%85%E6%9C%88