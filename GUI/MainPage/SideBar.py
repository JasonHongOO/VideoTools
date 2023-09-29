  
import customtkinter 

from GUI.CTkListbox import *
from GUI.CTkTable import *

def SideBar(self):
    RowCnt = 5
    # create sidebar frame with widgets
    self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
    self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    self.sidebar_frame.grid_rowconfigure(RowCnt, weight=1)
    self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="JasonHong", font=customtkinter.CTkFont(size=20, weight="bold"))
    self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

    # ============================================  Button  ============================================
    # self.RemoveAudioBtn = customtkinter.CTkButton(self.sidebar_frame, text="RemoveAudio", command=lambda: self.sidebar_button_event("RemoveAudioFrame"))
    self.RemoveAudioBtn = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, border_spacing=10, text="RemoveAudio",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.RemoveAudio_image, anchor="w", command=lambda: self.sidebar_button_event("RemoveAudioFrame"))
    self.RemoveAudioBtn.grid(row=1, column=0, sticky="ew")

    # self.SpeendUpBtn = customtkinter.CTkButton(self.sidebar_frame, text="SpeendUp", command=lambda: self.sidebar_button_event("SpeendUpFrame"))
    self.SpeendUpBtn = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, border_spacing=10, text="SpeendUp",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.SpeedUp_image, anchor="w", command=lambda: self.sidebar_button_event("SpeendUpFrame"))
    self.SpeendUpBtn.grid(row=2, column=0, sticky="ew")

    # self.DownloaderBtn = customtkinter.CTkButton(self.sidebar_frame, text="Downloader", command=lambda: self.sidebar_button_event("DownloaderFrame"))
    self.DownloaderBtn = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, border_spacing=10, text="Downloader",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.Downloader_image, anchor="w", command=lambda: self.sidebar_button_event("DownloaderFrame"))
    self.DownloaderBtn.grid(row=3, column=0, sticky="ew")

    self.SoundToTextBtn = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, border_spacing=10, text="SoundToText",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.Downloader_image, anchor="w", command=lambda: self.sidebar_button_event("SoundToTextFrame"))
    self.SoundToTextBtn.grid(row=4, column=0, sticky="ew")


    # ============================================  Menu  ============================================
    self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
    self.appearance_mode_label.grid(row=RowCnt+1, column=0, padx=20, pady=(10, 0))
    self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
    self.appearance_mode_optionemenu.grid(row=RowCnt+2, column=0, padx=20, pady=(10, 10))
    self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
    self.scaling_label.grid(row=RowCnt+3, column=0, padx=20, pady=(10, 0))
    self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                        command=self.change_scaling_event)
    self.scaling_optionemenu.grid(row=RowCnt+4, column=0, padx=20, pady=(10, 20))