import whisper
from whisper.utils import get_writer
import os, sys
import tqdm
import json

cur_path = os.path.dirname(os.path.abspath(__file__))   # 當前 python 檔案的位置
file_path = os.path.join(cur_path, "ffmpeg")            # 串接 ffmpeg，注意這是資料夾， path 是資料夾路徑，不是檔案
os.environ["PATH"] = file_path

class _CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n  # Set the initial value
        
    def update(self, n):
        super().update(n)
        self._current += n
        
        # Handle progress here
        print("Progress: " + str(self._current) + "/" + str(self.total))



def SoundToText(path):
    # Inject into tqdm.tqdm of Whisper, so we can see progress
    import whisper.transcribe 
    transcribe_module = sys.modules['whisper.transcribe']
    transcribe_module.tqdm.tqdm = _CustomProgressBar


    #進行語音轉文字處理
    model = whisper.load_model(name="medium", device="cuda", download_root=os.path.dirname(os.path.abspath(__file__)))      #medium
    result = model.transcribe(audio=path, language="Chinese", verbose=1)    #zh    #, fp16=False, verbose=None)

    #寫入檔案，方面後續查看
    # with open("./SoundProcess/Content.json", "w") as output_json_file:
    #     json.dump(result, output_json_file, indent=4)
    # print("Audio Context : ", result["text"])


    # filename = ""
    # input_directory = "."
    # path = f"{input_directory}/{filename}"
    output_directory = "./Output"

    # Save as a TXT file
    txt_writer = get_writer("txt", output_directory)
    txt_writer(result, path)

    # Save as an SRT file
    srt_writer = get_writer("srt", output_directory)
    srt_writer(result, path)

    # Save as an VTT file
    vtt_writer = get_writer("vtt", output_directory)
    vtt_writer(result, path)

    # Save as a TSV file
    tsv_writer = get_writer("tsv", output_directory)
    tsv_writer(result, path)

    # Save as a JSON file
    json_writer = get_writer("json", output_directory)
    json_writer(result, path)



if __name__ == "__main__":
    path = r"C:\Users\JasonHong\Desktop\CODE\Python\Script\Tools\Video\Update\Output\465.mp4"
    SoundToText(path)
    # print(whisper.available_models())