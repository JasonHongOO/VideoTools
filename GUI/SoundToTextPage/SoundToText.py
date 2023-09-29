import whisper
import os

cur_path = os.path.dirname(os.path.abspath(__file__))   # 當前 python 檔案的位置
file_path = os.path.join(cur_path, "ffmpeg")            # 串接 ffmpeg，注意這是資料夾， path 是資料夾路徑，不是檔案
os.environ["PATH"] = file_path

def SoundToText(path):
    #進行語音轉文字處理
    model = whisper.load_model("base")
    result = model.transcribe(path)
    print("Audio Context : ", result["text"])