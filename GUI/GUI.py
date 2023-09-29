import tkinter
import tkinter.messagebox
import customtkinter
import os
import sys
import threading
from PIL import Image

#額外 CTK tool
from GUI.CTkListbox import *
from GUI.CTkTable import *
from tkinterdnd2 import DND_FILES, TkinterDnD

from GUI.MainPage.ShareRegion import ShareRegion
from GUI.MainPage.SideBar import SideBar
from GUI.WelcomePage.Welcome import WelcomeFrame
from GUI.DownloaderPage.Downloader import DownloaderFrame
import VedioProcess
from VideoDownloader.Downloader import VideoGetInfo,VideoDownload
from SoundProcess.SoundToText import SoundToText

# style
import Sys.Const

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Redirect():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        if not text.endswith('\n'): text += '\n'
        self.widget.insert('end', text)
        self.widget.see('end')      # 頁面滑到底 (滑鼠滾輪滑到底)
        
    def flush(self):
       pass


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)       #拖移資料的 library
        self.ListBoxDictionary = {}

        #Image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "BasicIcon")

        
        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.Welcome_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Temp/main.png")),
                                                dark_image=Image.open(os.path.join(image_path, "Temp/main.png")), size=(200, 200))
        self.RemoveAudio_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Black/volume-x.png")),
                                                dark_image=Image.open(os.path.join(image_path, "White/volume-x.png")), size=(20, 20))
        self.SpeedUp_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Black/fast-forward.png")),
                                                dark_image=Image.open(os.path.join(image_path, "White/fast-forward.png")), size=(20, 20))
        self.Downloader_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "Black/download.png")),
                                                dark_image=Image.open(os.path.join(image_path, "White/download.png")), size=(20, 20))

        # configure window
        self.title("JasonHong 的影片處理器")
        self.geometry(f"{1100}x{580}")

        self.FrameDictionary = {}  # Dictionary to store frames  字典
        self.DownloaderDictionary = {}
        self.CurFrame = None        # 應該要設為最後一層，倒不如說應該要初始化第一層
        self.CurListBox = None

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2,), weight=1)


 

        # ===============================================================================================================
        # =========================================       側邊框框(選單)        =========================================
        # ===============================================================================================================
        SideBar(self)

        # ===============================================================================================================
        # =========================================       Welcome Frame        =========================================
        # ===============================================================================================================
        WelcomeFrame(self)

        # ===============================================================================================================
        # =========================================       Remove Audio frame(選單)        =========================================
        # ===============================================================================================================
        # Remove Audio frame
        def RemoveAudioFrame():
            #Layout 配置
            self.RemoveAudioFrame = customtkinter.CTkFrame(self, corner_radius=0)
            # self.RemoveAudioFrame.grid(row=0, rowspan=3, column=1, columnspan=3, sticky="nsew")
            self.RemoveAudioFrame.grid_columnconfigure((0), weight=1)
            self.RemoveAudioFrame.grid_rowconfigure((0, 2), weight=1)

            self.FrameDictionary["RemoveAudioFrame"] = self.RemoveAudioFrame

            ParentFrame = self.RemoveAudioFrame            
            ShareRegion(self, ParentFrame,"RemoveAudioFrame")
        RemoveAudioFrame()

        # ===============================================================================================================
        # =========================================       Speend Up Frame(選單)        =========================================
        # ===============================================================================================================
        # Speend Up Frame
        def SpeendUpFrame():
            #Layout 配置
            self.SpeendUpFrame = customtkinter.CTkFrame(self, corner_radius=0)
            # self.SpeendUpFrame.grid(row=0, rowspan=4, column=1, sticky="nsew")            #一開始不要部屬就部會顯示，不需要再額外 init
            self.SpeendUpFrame.grid_columnconfigure((0), weight=1)
            self.SpeendUpFrame.grid_rowconfigure((0, 2), weight=1)

            self.FrameDictionary["SpeendUpFrame"] = self.SpeendUpFrame

            ParentFrame = self.SpeendUpFrame
            ShareRegion(self, ParentFrame, "SpeendUpFrame")
        SpeendUpFrame()

        # ===============================================================================================================
        # =========================================       Speend Up Frame(選單)        =========================================
        # ===============================================================================================================
        # Downloader Frame
        DownloaderFrame(self)

        # ===============================================================================================================
        # =========================================       Speend Up Frame(選單)        =========================================
        # ===============================================================================================================
        # Sound To Text Frame
        def SoundToTextFrame(self):
            #Layout 配置
            self.SoundToTextFrame = customtkinter.CTkFrame(self, corner_radius=0)
            # self.SpeendUpFrame.grid(row=0, rowspan=4, column=1, sticky="nsew")            #一開始不要部屬就部會顯示，不需要再額外 init
            self.SoundToTextFrame.grid_columnconfigure((0), weight=1)
            self.SoundToTextFrame.grid_rowconfigure((0), weight=1)
            # self.SoundToTextFrame.grid_rowconfigure((2), weight=1)

            self.FrameDictionary["SoundToTextFrame"] = self.SoundToTextFrame

            # Tab
            self.tabview = customtkinter.CTkTabview(self.SoundToTextFrame) #,height=10
            self.tabview.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
            self.tabview.add("InputPath")
            self.tabview.add("DragFile")
            self.tabview.add("FilePath")

            self.tabview.tab("InputPath").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.tabview.tab("DragFile").grid_columnconfigure(0, weight=1)
            self.tabview.tab("FilePath").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

            self.tabview.tab("InputPath").grid_rowconfigure((2), weight=1)
            self.tabview.tab("DragFile").grid_rowconfigure((0,2), weight=1)
            self.tabview.tab("FilePath").grid_rowconfigure(0, weight=1)

                # Tab 1 (InputPath)
            # Input Entry
            self.SoundToTextInputPathInputFrame = customtkinter.CTkFrame(self.tabview.tab("InputPath"))
            self.SoundToTextInputPathInputFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            self.SoundToTextInputPathInputFrame.grid_columnconfigure((0,1), weight=1)
            self.SoundToTextInputPathInputFrame.grid_columnconfigure((2), weight=0)
            self.SoundToTextInputPathInputFrame.grid_rowconfigure((0), weight=1)

            self.SoundToTextInputPathEntry = customtkinter.CTkEntry(self.SoundToTextInputPathInputFrame, placeholder_text="Input URL")
            self.SoundToTextInputPathEntry.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=15, sticky="nsew")

            self.DonloaderPreviewBtn = customtkinter.CTkButton(master=self.SoundToTextInputPathInputFrame, border_width=2, text="Preview", command=lambda: self.Preview_event("SoundToText"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled )
            self.DonloaderPreviewBtn.grid(row=0, column=2, padx=(20, 20), pady=15, sticky="nsew")

            # Btn Region
            self.SoundToTextInputPathBtnFrame = customtkinter.CTkFrame(self.tabview.tab("InputPath"))
            self.SoundToTextInputPathBtnFrame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            self.SoundToTextInputPathBtnFrame.grid_columnconfigure((1, 3, 5), weight=1)
            self.SoundToTextInputPathBtnFrame.grid_columnconfigure((0, 2, 4), weight=0)
            self.SoundToTextInputPathBtnFrame.grid_rowconfigure((0), weight=1)

            self.SoundToTextInputPathVideoLabel = customtkinter.CTkLabel(self.SoundToTextInputPathBtnFrame, text="Video Quality")
            self.SoundToTextInputPathVideoLabel.grid(row=0, column=0, padx=(20,0), pady=10, sticky="nsew")
            self.SoundToTextInputPathVideoOptioneMenu = customtkinter.CTkOptionMenu(self.SoundToTextInputPathBtnFrame, values=["None"], command=lambda Value: self.Change_Video_Quality_event(Value, "SoundToText"))
            self.SoundToTextInputPathVideoOptioneMenu.grid(row=0, column=1, padx=20, pady=(10, 10), sticky="nsew")

            self.SoundToTextInputPathAudioLabel = customtkinter.CTkLabel(self.SoundToTextInputPathBtnFrame, text="Audio Quality")
            self.SoundToTextInputPathAudioLabel.grid(row=0, column=2, pady=10, sticky="nsew")
            self.SoundToTextInputPathAudioOptioneMenu = customtkinter.CTkOptionMenu(self.SoundToTextInputPathBtnFrame, values=["None"], command=lambda Value: self.Change_Audio_Quality_event(Value, "SoundToText"))
            self.SoundToTextInputPathAudioOptioneMenu.grid(row=0, column=3, padx=20, pady=(10, 10), sticky="nsew")
            
            self.SoundToTextInputPathFileTypeLabel = customtkinter.CTkLabel(self.SoundToTextInputPathBtnFrame, text="File Type")
            self.SoundToTextInputPathFileTypeLabel.grid(row=0, column=4, pady=10, sticky="nsew")
            self.SoundToTextInputPathOutputOptioneMenu = customtkinter.CTkOptionMenu(self.SoundToTextInputPathBtnFrame, values=["mp4", "mp3"], command=lambda Value: self.Change_Output_FileType_event(Value, "SoundToText"))
            self.SoundToTextInputPathOutputOptioneMenu.grid(row=0, column=5, padx=20, pady=(10, 10), sticky="nsew")

                
            # Image
            self.SoundToTextInputPathImageFrame = customtkinter.CTkFrame(self.tabview.tab("InputPath"))
            self.SoundToTextInputPathImageFrame.grid(row=2, column=0, padx=5, pady=(5,5), sticky="nsew")
            self.SoundToTextInputPathImageFrame.grid_columnconfigure((1), weight=1)
            self.SoundToTextInputPathImageFrame.grid_rowconfigure((1), weight=1)
            self.SoundToTextInputPathImageLabel = customtkinter.CTkLabel(self.SoundToTextInputPathImageFrame, text="")
            self.SoundToTextInputPathImageLabel.grid(row=1, column=1, pady=10, sticky="nsew")

            # Functional Btn Region
            self.SoundToTextInputPathfuntionalBtnFrame = customtkinter.CTkFrame(self.tabview.tab("InputPath"))
            self.SoundToTextInputPathfuntionalBtnFrame.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nsew")
            self.SoundToTextInputPathfuntionalBtnFrame.grid_columnconfigure((0), weight=1)
            self.SoundToTextInputPathfuntionalBtnFrame.grid_rowconfigure((0), weight=1)

            self.SoundToTextInputPathConfirmBtn = customtkinter.CTkButton(master=self.SoundToTextInputPathfuntionalBtnFrame, border_width=2, text="Download Comfirm", command=lambda: self.SoundToTextBtnFrame_Download_event("SoundToText"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
            self.SoundToTextInputPathConfirmBtn.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")


            self.FrameDictionary["SoundToText_Entry"] = self.SoundToTextInputPathEntry
            self.FrameDictionary["SoundToText_VideoOptioneMenu"] = self.SoundToTextInputPathVideoOptioneMenu
            self.FrameDictionary["SoundToText_AudioOptioneMenu"] = self.SoundToTextInputPathAudioOptioneMenu
            self.FrameDictionary["SoundToText_OutputOptioneMenu"] = self.SoundToTextInputPathOutputOptioneMenu
            self.FrameDictionary["SoundToText_ImageLabel"] = self.SoundToTextInputPathImageLabel                   
            self.FrameDictionary["SoundToText_ImageFrame"] = self.SoundToTextInputPathImageFrame
            self.FrameDictionary["SoundToText_funtionalBtnFrame"] = self.SoundToTextInputPathfuntionalBtnFrame

                # Tab 2 (DragFile)
            #Drag Box
            self.SoundToTextDragFileDragBoxFrame = customtkinter.CTkFrame(self.tabview.tab("DragFile"))
            self.SoundToTextDragFileDragBoxFrame.grid_columnconfigure((0, 1, 2), weight=1)
            self.SoundToTextDragFileDragBoxFrame.grid_rowconfigure((0, 1, 2), weight=1)
            self.SoundToTextDragFileDragBoxFrame.grid(row=0, column=0, padx=5, pady=(5,5), sticky="nsew")

            self.SoundToTextDragFileDragBoxFrame.drop_target_register("DND_Files")
            self.SoundToTextDragFileDragBoxFrame.dnd_bind('<<Drop>>', lambda event: self.on_drop(event, "SoundToTextFrame"))

            self.SoundToTextDragFileLabel = customtkinter.CTkLabel(self.SoundToTextDragFileDragBoxFrame, text="Input Image")
            self.SoundToTextDragFileLabel.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            # listbox
            self.SoundToTextDragFilelistboxFrame = customtkinter.CTkFrame(self.tabview.tab("DragFile"))
            self.SoundToTextDragFilelistboxFrame.grid_columnconfigure(0, weight=1)
            self.SoundToTextDragFilelistboxFrame.grid_rowconfigure(0, weight=1)
            self.SoundToTextDragFilelistboxFrame.grid(row=2, column=0, padx=5, pady=(5,5), sticky="nsew")
            self.SoundToTextDragFilelistbox = CTkListbox(master=self.SoundToTextDragFilelistboxFrame, text_color = ("#000000","#ffff"), multiple_selection = True, height=2)
            self.SoundToTextDragFilelistbox.grid(row=0, column=0, sticky="nsew")
            
            self.FrameDictionary["SoundToTextFrame_ListBox"]=self.SoundToTextDragFilelistbox

            #Btn Region
            self.SoundToTextDragFileBtnRegion = customtkinter.CTkFrame(self.tabview.tab("DragFile"))
            self.SoundToTextDragFileBtnRegion.grid(row=4, column=0, padx=5, pady=(5,5), sticky="nsew")
            self.SoundToTextDragFileBtnRegion.grid_columnconfigure((0, 1, 2), weight=1)
            self.SoundToTextDragFileBtnRegion.grid_rowconfigure((0), weight=0)
            self.SoundToTextDragFileSeleAllBnt = customtkinter.CTkButton(master=self.SoundToTextDragFileBtnRegion, border_width=2, text="SeleAll", command=lambda: self.SeleAll_event("SoundToTextFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
            self.SoundToTextDragFileSeleAllBnt.grid(row=0, column=0, padx=10, sticky="nsew")
            self.SoundToTextDragFileCancelSeleAllBtn = customtkinter.CTkButton(master=self.SoundToTextDragFileBtnRegion, border_width=2, text="CancelSeleAll", command=lambda: self.CancelSeleAll_event("SoundToTextFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
            self.SoundToTextDragFileCancelSeleAllBtn.grid(row=0, column=1, padx=10, sticky="nsew")
            self.SoundToTextDragFileConfirmBnt = customtkinter.CTkButton(master=self.SoundToTextDragFileBtnRegion, border_width=2, text="Confirm", command=lambda: self.SoundToText_Confirm_event("SoundToTextFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
            self.SoundToTextDragFileConfirmBnt.grid(row=0, column=2, padx=10, sticky="nsew")

                # Tab 3 (FilePath)

            # # UserBlock
            # self.SoundToTextMainBodyFrame = customtkinter.CTkFrame(self.SoundToTextFrame, corner_radius=0)
            # self.SoundToTextMainBodyFrame.grid_columnconfigure((0,1), weight=1)
            # self.SoundToTextMainBodyFrame.grid_rowconfigure((0), weight=1)
            # self.SoundToTextMainBodyFrame.grid(row=1, column=0, sticky="nsew")

            # self.SoundToTextLeftTextbox = customtkinter.CTkTextbox(self.SoundToTextMainBodyFrame)   
            # self.SoundToTextLeftTextbox.grid(row=0, column=0, sticky="nsew") 
            # self.SoundToTextRightTextbox = customtkinter.CTkTextbox(self.SoundToTextMainBodyFrame)    
            # self.SoundToTextRightTextbox.grid(row=0, column=1, sticky="nsew")

            self.SoundToTextDebugFrame= customtkinter.CTkFrame(self.SoundToTextFrame)
            self.SoundToTextDebugFrame.grid_columnconfigure((0), weight=1)
            self.SoundToTextDebugFrame.grid_rowconfigure((0), weight=1)
            # self.SoundToTextDebugFrame.grid(row=0, column=0, sticky="nsew")

            self.SoundToTextTextbox = customtkinter.CTkTextbox(self.SoundToTextDebugFrame)   
            self.SoundToTextTextbox.grid(row=0, column=0, sticky="nsew")

            self.SoundToTextBtnFrame= customtkinter.CTkFrame(self.SoundToTextDebugFrame)
            self.SoundToTextBtnFrame.grid_columnconfigure((0), weight=1)
            self.SoundToTextBtnFrame.grid_rowconfigure((0), weight=0)
            self.SoundToTextBtnFrame.grid(row=1, column=0, sticky="nsew")
            self.SoundToTextBackBtn = customtkinter.CTkButton(master=self.SoundToTextBtnFrame, border_width=2, text="Back", command=self.SoundToTextBtnFrame_Back_event, bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
            self.SoundToTextBackBtn.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

            self.FrameDictionary["SoundToText_Textbox"] = self.SoundToTextTextbox
            self.FrameDictionary["SoundToText_BackBtnFrame"] = self.SoundToTextBtnFrame                      #


        SoundToTextFrame(self)

        # ===============================================================================================================
        # =========================================       初始化        =========================================
        # ===============================================================================================================
        self.CurFrame = self.WelcomeFrame

        self.appearance_mode_optionemenu.set("Light")
        customtkinter.set_appearance_mode("Light")
        self.scaling_optionemenu.set("100%")
        new_scaling_float = 1
        customtkinter.set_widget_scaling(new_scaling_float)



    # ===============================================================================================================
    # =========================================       Self Function        =========================================
    # ===============================================================================================================

# SideBar
    def change_appearance_mode_event(self, new_appearance_mode: str):
        print("Change Appearance")
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        print("Change Scaling")
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self,FrameName="None"):
        print("sidebar_button click : " + FrameName)

        #分頁切換(功能切換)
        if self.CurFrame:
            self.CurFrame.grid_forget()
        self.CurFrame = self.FrameDictionary[FrameName]
        self.CurFrame.grid(row=0, rowspan=4, column=1, sticky="nsew")

        #現在使用的 ListBox 更新
        if(FrameName == "SpeendUpFrame" or FrameName == "RemoveAudioFrame"):
            self.listboxFrame = self.FrameDictionary[FrameName + "_ListBoxFrame"]
            self.BtnRegion = self.FrameDictionary[FrameName + "_BtnRegion"]
            self.textbox = self.FrameDictionary[FrameName + "_textbox"]
            self.BackBtnRegion = self.FrameDictionary[FrameName + "_BackBtnRegion"]

        self.RemoveAudioBtn.configure(fg_color=("gray75", "gray25") if FrameName == "RemoveAudioFrame" else "transparent")
        self.SpeendUpBtn.configure(fg_color=("gray75", "gray25") if FrameName == "SpeendUpFrame" else "transparent")
        self.DownloaderBtn.configure(fg_color=("gray75", "gray25") if FrameName == "DownloaderFrame" else "transparent")
        self.SoundToTextFrame.configure(fg_color=("gray75", "gray25") if FrameName == "DownloaderFrame" else "transparent")

# Main Page
    # Share Region
    def SeleAll_event(self, mode):
        print("SeleAll Btn")
        self.CurListBox = self.FrameDictionary[mode + "_ListBox"]
        self.CurListBox.activate("all")
    
    def CancelSeleAll_event(self, mode):
        print("CancelSeleAll Btn")
        self.CurListBox = self.FrameDictionary[mode + "_ListBox"]
        self.CurListBox.deactivate("all")
    
    def DeleAll_event(self, mode):
        print("DeleAll Btn")
        # SelectOption = self.listbox.curselection()   
        # for index in SelectOption:
        #     print(index)
        #     self.ListBoxDeletCacheList.append(index)
        #     self.listbox.delete(index)
        self.CurListBox = self.FrameDictionary[mode + "_ListBox"]
        self.CurListBox.delete("all")

    def Confirm_event(self, Event):
        def process():
            print("Confirm Btn")

            # 把 output 頁面叫出來 (切換頁面)
            self.listboxFrame.grid_forget()
            self.BtnRegion.grid_forget()
            self.textbox.grid(row=2, column=0, padx=10, pady=(5,5), sticky="nsew")
            self.BackBtnRegion.grid(row=4, column=0, padx=10, pady=(5,5), sticky="nsew")

            # 從新導向 output
            old_stdout = sys.stdout
            old_arderr = sys.stderr 
            sys.stdout = Redirect(self.textbox)
            sys.stderr = Redirect(self.textbox)

            # 執行對應的程式
            self.CurListBox = self.FrameDictionary[Event + "_ListBox"]
            SelectOption = self.CurListBox.curselection()
            if len(SelectOption) != 0:
                for ele in SelectOption:
                    print(ele)
                    #name
                    title = self.CurListBox.get(str(ele))
                    partition = title.split(" ")[0]
                    print(f"====== Name ====== : {partition}")
                    #path
                    print(f"====== Path ====== : {self.ListBoxDictionary[str(ele)]}")

                    if Event == "RemoveAudioFrame":    
                        VedioProcess.Remove_Sound(self.ListBoxDictionary[str(ele)])

                    elif Event == "SpeendUpFrame":
                        VedioProcess.Speed_Up(self.ListBoxDictionary[str(ele)])
            else:
                print("==== 未選擇要處理的檔案 ====")

            # 把 output 從新導向回原本
            sys.stdout = old_stdout
            sys.stderr = old_arderr

        threading.Thread(target=process).start()
    
    def Back_event(self):
        print("Back Btn")
        self.textbox.grid_forget()
        self.BackBtnRegion.grid_forget()
        self.listboxFrame.grid(row=2, column=0, padx=10, pady=(5,5), sticky="nsew")
        self.BtnRegion.grid(row=4, column=0, padx=10, pady=(5,5), sticky="nsew")

    def on_drop(self, event, mode):
        PathStr = event.data
        FilePathList = PathStr.split(" ")

        for FilePath in FilePathList:
            # print(FilePath)
            # print(type(FilePath))
            file_name = os.path.basename(FilePath)
            file_size = str(   "{:.2f}".format(os.path.getsize(FilePath) / (1024 * 1024))   ) + "Mb"
            # file_type = os.path.splitext(FilePath)[1]

            formatted_name = f"{file_name:<60}"
            formatted_number = f"{file_size:>60}"
            # formatted_type = f"{type:<30}"

            self.CurListBox = self.FrameDictionary[mode + "_ListBox"]
            self.CurListBox.insert("end", formatted_name + formatted_number)           #屬於不同分頁的 listbox     #因為在外面，所以需要額外處理
            self.ListBoxDictionary[str(self.CurListBox.end_num-1)] = FilePath
            print("file_Index : ", str(self.CurListBox.end_num-1))
            print("file_Name : ", FilePath)

# Download Page
    def Change_Video_Quality_event(self, Value, mode):
        print("Change Video Quality : ", Value, "(",mode,")")
    
    def Change_Audio_Quality_event(self, Value, mode):
        print("Change Audio Quality : ", Value, "(",mode,")")

    def Change_Output_FileType_event(self, Value, mode):
        print("Change Output FileType event : ", Value, "(",mode,")")

    def Preview_event(self, mode):
        print("Preview event")
        self.CurEntry = self.FrameDictionary[mode + "_Entry"]
        self.CurVideoOptioneMenu = self.FrameDictionary[mode + "_VideoOptioneMenu"]
        self.CurAudioOptioneMenu = self.FrameDictionary[mode + "_AudioOptioneMenu"]
        self.CurImageLabel = self.FrameDictionary[mode + "_ImageLabel"]

        # 初始化
        self.DownloaderDictionary = {}

        # 資料
        Info = VideoGetInfo(self.CurEntry.get())
        VideoList, AudioList = ["None"], ["None"]
        VideoCnt, AudioCnt = 1, 1
        for format in Info["formats"]:
            if format["resolution"] == "audio only":
                #字串處理，取出 ( ) 中的字串
                OutputString = ""
                string = format["format"]
                start_index, end_index = string.find("("), string.find(")")
                if start_index != -1 and end_index != -1: OutputString = string[start_index + 1:end_index]
                else: print("Audio String No match found !!!!!!")

                OutputString = str(AudioCnt).ljust(4) + format["ext"].ljust(6) + OutputString
                AudioList.append(OutputString)
                self.DownloaderDictionary[OutputString] = format["format_id"]
                AudioCnt = AudioCnt + 1

            else:       #非音檔
                if format["vcodec"] != "none":
                    OutputString = str(VideoCnt).ljust(4) + format["resolution"].ljust(10) + format["ext"].ljust(6)
                    if format["fps"] != None : OutputString = OutputString + str(int(format["fps"])).ljust(4)
                    if format["acodec"] != "none" : OutputString = OutputString + "(Audio)"
                    VideoList.append(OutputString)
                    self.DownloaderDictionary[OutputString] = format["format_id"]
                    VideoCnt = VideoCnt + 1

        self.CurVideoOptioneMenu.configure(values=VideoList)
        self.CurAudioOptioneMenu.configure(values=AudioList)         

        # 圖片
        from PIL import Image, ImageTk
        from urllib.request import urlopen
        from io import BytesIO

        with urlopen(Info["thumbnails"][-1]["url"]) as u:       # url = self.DownloaderEntry.get() 
            raw_data = u.read()

        # 確定縮小的比例，以保持圖片的長寬比
        image = Image.open(BytesIO(raw_data))
        width, height = image.size
        max_width, max_height = 640, 640
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width, new_height = int(width * ratio), int(height * ratio)
            image.thumbnail((new_width, new_height))
        photo = ImageTk.PhotoImage(image)

        # photo = ImageTk.PhotoImage(data = raw_data)

        self.CurImageLabel.configure(image=photo)

    def Download_event(self, mode):
        def process():
            print("Download event")

            self.CurImageFrame = self.FrameDictionary[mode + "_ImageFrame"]
            self.CurfuntionalBtnFrame = self.FrameDictionary[mode + "_funtionalBtnFrame"]
            self.CurTextbox = self.FrameDictionary[mode + "_Textbox"]
            self.CurBackBtnFrame = self.FrameDictionary[mode + "_BackBtnFrame"]
            self.CurOutputOptioneMenu = self.FrameDictionary[mode + "_OutputOptioneMenu"]
            self.CurEntry = self.FrameDictionary[mode + "_Entry"]
            self.CurVideoOptioneMenu = self.FrameDictionary[mode + "_VideoOptioneMenu"]
            self.CurAudioOptioneMenu = self.FrameDictionary[mode + "_AudioOptioneMenu"]

            # 更新版面
            self.CurImageFrame.grid_forget() 
            self.CurfuntionalBtnFrame.grid_forget() 
            self.CurTextbox.grid(row=2, column=0, padx=5, pady=(5,5), sticky="nsew")
            self.CurBackBtnFrame.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nsew")

            # File Type
            OutputType = self.CurOutputOptioneMenu.get()     # 想要 output 的類型

            # 從新導向 output
            old_stdout = sys.stdout
            old_arderr = sys.stderr
            sys.stdout = Redirect(self.CurTextbox)
            sys.stderr = Redirect(self.CurTextbox)
            if self.CurVideoOptioneMenu.get() != "None" or self.CurAudioOptioneMenu.get() != "None":
                if self.CurVideoOptioneMenu.get() != "None" and self.CurAudioOptioneMenu.get() != "None": VideoDownload(self.CurEntry.get(), self.DownloaderDictionary[self.CurVideoOptioneMenu.get()], self.DownloaderDictionary[self.CurAudioOptioneMenu.get()], OutputType)
                elif self.CurVideoOptioneMenu.get() != "None" : VideoDownload(self.CurEntry.get(), self.DownloaderDictionary[self.CurVideoOptioneMenu.get()], "None", OutputType)
                elif self.CurAudioOptioneMenu.get() != "None" : VideoDownload(self.CurEntry.get(), "None", self.DownloaderDictionary[self.CurAudioOptioneMenu.get()], OutputType)
            else: 
                print("==== 未設定下載的檔案格式 ====")
            # 把 output 從新導向回原本
            sys.stdout = old_stdout
            sys.stderr = old_arderr

        threading.Thread(target=process).start()

    def Download_Back_event(self):
        print("Download Back event")
        self.DownloaderTextbox.grid_forget() 
        self.DownloaderBackBtnFrame.grid_forget()
        self.DownloaderImageFrame.grid(row=2, column=0, padx=5, pady=(5,5), sticky="nsew")
        self.DownloaderfuntionalBtnFrame.grid(row=3, column=0, padx=5, pady=(5,5), sticky="nsew")

# Sound To Text Page
    def SoundToTextBtnFrame_Download_event(self, mode):
        def process():
            print("Download event (SoundToText)")

            # 更新版面
            self.tabview.grid_forget() 
            self.SoundToTextDebugFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

            # File Type
            OutputType = self.SoundToTextInputPathOutputOptioneMenu.get()     # 想要 output 的類型

            # 從新導向 output
            old_stdout = sys.stdout
            old_arderr = sys.stderr
            sys.stdout = Redirect(self.SoundToTextTextbox)
            sys.stderr = Redirect(self.SoundToTextTextbox)

            FilePath = ""
            if self.SoundToTextInputPathVideoOptioneMenu.get() != "None" or self.SoundToTextInputPathAudioOptioneMenu.get() != "None":
                if self.SoundToTextInputPathVideoOptioneMenu.get() != "None" and self.SoundToTextInputPathAudioOptioneMenu.get() != "None": FilePath=VideoDownload(self.CurEntry.get(), self.DownloaderDictionary[self.SoundToTextInputPathVideoOptioneMenu.get()], self.DownloaderDictionary[self.SoundToTextInputPathAudioOptioneMenu.get()], OutputType)
                elif self.SoundToTextInputPathVideoOptioneMenu.get() != "None" : FilePath=VideoDownload(self.CurEntry.get(), self.DownloaderDictionary[self.SoundToTextInputPathVideoOptioneMenu.get()], "None", OutputType)
                elif self.SoundToTextInputPathAudioOptioneMenu.get() != "None" : FilePath=VideoDownload(self.CurEntry.get(), "None", self.DownloaderDictionary[self.SoundToTextInputPathAudioOptioneMenu.get()], OutputType)
            
                # 執行對應程序
                print("執行 Sound To Text 程序")
                print("檔案路徑 : ", FilePath)
                print("待處理...")
            else: 
                print("==== 未設定下載的檔案格式 ====")

            # 把 output 從新導向回原本
            sys.stdout = old_stdout
            sys.stderr = old_arderr

        threading.Thread(target=process).start()

    def SoundToTextBtnFrame_Back_event(self):
        print("Download Back event (SoundToText)")

        self.SoundToTextDebugFrame.grid_forget() 
        self.tabview.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

    def SoundToText_Confirm_event(self, Event):
        def process():
            print("Confirm Btn (SoundToText)")
            # 更新版面
            self.tabview.grid_forget() 
            self.SoundToTextDebugFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

            # 從新導向 output
            old_stdout = sys.stdout
            old_arderr = sys.stderr 
            sys.stdout = Redirect(self.SoundToTextTextbox)
            sys.stderr = Redirect(self.SoundToTextTextbox)

            # 執行對應的程式
            SelectOption = self.SoundToTextDragFilelistbox.curselection()
            if len(SelectOption) != 0:
                for ele in SelectOption:
                    #name
                    title = self.SoundToTextDragFilelistbox.get(str(ele))
                    partition = title.split(" ")[0]
                    print(f"====== Name ====== : {partition}")
                    #path
                    print(f"====== Path ====== : {self.ListBoxDictionary[str(ele)]}")

                    if Event == "SoundToTextFrame":
                        print("待處理...")
                        SoundToText(self.ListBoxDictionary[str(ele)])
            else:
                print("==== 未選擇要處理的檔案 ====")

            # 把 output 從新導向回原本
            sys.stdout = old_stdout
            sys.stderr = old_arderr

        threading.Thread(target=process).start()

        