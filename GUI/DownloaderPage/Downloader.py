       
import customtkinter 

from GUI.CTkListbox import *
from GUI.CTkTable import *

import Sys.Const

def DownloaderFrame(self):
    #Layout 配置
    self.DownloaderFrame = customtkinter.CTkFrame(self, corner_radius=0)
    # self.SpeendUpFrame.grid(row=0, rowspan=4, column=1, sticky="nsew")            #一開始不要部屬就部會顯示，不需要再額外 init
    self.DownloaderFrame.grid_columnconfigure((0), weight=1)
    self.DownloaderFrame.grid_rowconfigure((2), weight=1)
    self.DownloaderFrame.grid_rowconfigure((4), weight=0)

    # Input Entry
    self.URLInputFrame = customtkinter.CTkFrame(self.DownloaderFrame)
    self.URLInputFrame.grid(row=0, column=0, padx=5, pady=(10,5), sticky="ew")
    self.URLInputFrame.grid_columnconfigure((0,1), weight=1)
    self.URLInputFrame.grid_columnconfigure((2), weight=0)
    self.URLInputFrame.grid_rowconfigure((0), weight=1)

    self.DownloaderEntry = customtkinter.CTkEntry(self.URLInputFrame, placeholder_text="Input URL")
    self.DownloaderEntry.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=15, sticky="nsew")

    self.DonloaderPreviewBtn = customtkinter.CTkButton(master=self.URLInputFrame, border_width=2, text="Preview", command=lambda: self.Preview_event("Downloader"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled )
    self.DonloaderPreviewBtn.grid(row=0, column=2, padx=(20, 20), pady=15, sticky="nsew")

    # Btn Region
    self.DownloaderBtnFrame = customtkinter.CTkFrame(self.DownloaderFrame)
    self.DownloaderBtnFrame.grid(row=1, column=0, padx=5, pady=(5,5), sticky="nsew")
    self.DownloaderBtnFrame.grid_columnconfigure((1, 3, 5), weight=1)
    self.DownloaderBtnFrame.grid_columnconfigure((0, 2, 4), weight=0)
    self.DownloaderBtnFrame.grid_rowconfigure((0), weight=1)

    self.DownloaderVideoLabel = customtkinter.CTkLabel(self.DownloaderBtnFrame, text="Video Quality")
    self.DownloaderVideoLabel.grid(row=0, column=0, padx=(20,0), pady=10, sticky="nsew")
    self.DownloaderVideoOptioneMenu = customtkinter.CTkOptionMenu(self.DownloaderBtnFrame, values=["None"], command=lambda Value: self.Change_Video_Quality_event(Value, "Downloader"))
    self.DownloaderVideoOptioneMenu.grid(row=0, column=1, padx=20, pady=(10, 10), sticky="nsew")

    self.DownloaderAudioLabel = customtkinter.CTkLabel(self.DownloaderBtnFrame, text="Audio Quality")
    self.DownloaderAudioLabel.grid(row=0, column=2, pady=10, sticky="nsew")
    self.DownloaderAudioOptioneMenu = customtkinter.CTkOptionMenu(self.DownloaderBtnFrame, values=["None"], command=lambda Value: self.Change_Audio_Quality_event(Value, "Downloader"))
    self.DownloaderAudioOptioneMenu.grid(row=0, column=3, padx=20, pady=(10, 10), sticky="nsew")
    
    self.DownloaderFileTypeLabel = customtkinter.CTkLabel(self.DownloaderBtnFrame, text="File Type")
    self.DownloaderFileTypeLabel.grid(row=0, column=4, pady=10, sticky="nsew")
    self.DownloaderOutputOptioneMenu = customtkinter.CTkOptionMenu(self.DownloaderBtnFrame, values=["mp4", "mp3"], command=lambda Value: self.Change_Output_FileType_event(Value, "Downloader"))
    self.DownloaderOutputOptioneMenu.grid(row=0, column=5, padx=20, pady=(10, 10), sticky="nsew")

    # Image
    self.DownloaderImageFrame = customtkinter.CTkFrame(self.DownloaderFrame)
    self.DownloaderImageFrame.grid(row=2, column=0, padx=5, pady=(5,5), sticky="nsew")
    self.DownloaderImageFrame.grid_columnconfigure((1), weight=1)
    self.DownloaderImageFrame.grid_rowconfigure((1), weight=1)
    self.DownloaderImageLabel = customtkinter.CTkLabel(self.DownloaderImageFrame, text="")
    self.DownloaderImageLabel.grid(row=1, column=1, pady=10, sticky="nsew")

    # Functional Btn Region
    self.DownloaderfuntionalBtnFrame = customtkinter.CTkFrame(self.DownloaderFrame)
    self.DownloaderfuntionalBtnFrame.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nsew")
    self.DownloaderfuntionalBtnFrame.grid_columnconfigure((0), weight=1)
    self.DownloaderfuntionalBtnFrame.grid_rowconfigure((0), weight=1)

    self.DonloaderConfirmBtn = customtkinter.CTkButton(master=self.DownloaderfuntionalBtnFrame, border_width=2, text="Download Comfirm", command=lambda: self.Download_event("Downloader"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.DonloaderConfirmBtn.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    # textbox
    self.DownloaderTextbox = customtkinter.CTkTextbox(self.DownloaderFrame)    

    # Back Btn
    self.DownloaderBackBtnFrame = customtkinter.CTkFrame(self.DownloaderFrame)
    self.DownloaderBackBtnFrame.grid_columnconfigure((0), weight=1)
    self.DownloaderBackBtnFrame.grid_rowconfigure((0), weight=0)
    self.DownloaderBackBtn = customtkinter.CTkButton(master=self.DownloaderBackBtnFrame, border_width=2, text="Back", command=self.Download_Back_event, bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.DownloaderBackBtn.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    self.FrameDictionary["DownloaderFrame"] = self.DownloaderFrame
    self.FrameDictionary["Downloader_Entry"] = self.DownloaderEntry
    self.FrameDictionary["Downloader_VideoOptioneMenu"] = self.DownloaderVideoOptioneMenu
    self.FrameDictionary["Downloader_AudioOptioneMenu"] = self.DownloaderAudioOptioneMenu
    self.FrameDictionary["Downloader_OutputOptioneMenu"] = self.DownloaderOutputOptioneMenu
    self.FrameDictionary["Downloader_ImageLabel"] = self.DownloaderImageLabel
    self.FrameDictionary["Downloader_ImageFrame"] = self.DownloaderImageFrame
    self.FrameDictionary["Downloader_funtionalBtnFrame"] = self.DownloaderfuntionalBtnFrame
    self.FrameDictionary["Downloader_Textbox"] = self.DownloaderTextbox
    self.FrameDictionary["Downloader_BackBtnFrame"] = self.DownloaderBackBtnFrame