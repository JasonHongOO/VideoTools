        
import customtkinter 

from GUI.CTkListbox import *
from GUI.CTkTable import *

import Sys.Const

# ===============================================================================================================
# =========================================       重複的區段(選單)        =========================================
# ===============================================================================================================
def ShareRegion(self, ParentFrame, mode):
    #Drag Box
    self.DragBoxFrame = customtkinter.CTkFrame(ParentFrame)
    self.DragBoxFrame.grid_columnconfigure((0, 1, 2), weight=1)
    self.DragBoxFrame.grid_rowconfigure((0, 1, 2), weight=1)
    self.DragBoxFrame.grid(row=0, column=0, padx=10, pady=(10,5), sticky="nsew")

    self.DragBoxFrame.drop_target_register("DND_Files")
    if mode == "RemoveAudioFrame":
        self.DragBoxFrame.dnd_bind('<<Drop>>', lambda event: self.on_drop(event, "RemoveAudioFrame"))
    elif mode == "SpeendUpFrame":
        self.DragBoxFrame.dnd_bind('<<Drop>>', lambda event: self.on_drop(event, "SpeendUpFrame"))

    self.frameLabel = customtkinter.CTkLabel(self.DragBoxFrame, text="Input Image")
    self.frameLabel.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # listbox
    self.listboxFrame = customtkinter.CTkFrame(ParentFrame)
    self.listboxFrame.grid_columnconfigure(0, weight=1)
    self.listboxFrame.grid_rowconfigure(0, weight=1)
    self.listboxFrame.grid(row=2, column=0, padx=10, pady=(5,5), sticky="nsew")
    self.listbox = CTkListbox(master=self.listboxFrame, text_color = ("#000000","#ffff"), multiple_selection = True)
    self.listbox.grid(row=0, column=0, sticky="nsew")
        
    #Btn Region
    self.BtnRegion = customtkinter.CTkFrame(ParentFrame)
    self.BtnRegion.grid(row=4, column=0, padx=5, pady=(5,5), sticky="nsew")
    self.BtnRegion.grid_columnconfigure((0, 1, 2, 3), weight=1)
    self.BtnRegion.grid_rowconfigure((0), weight=0)
    self.SeleAllBnt = customtkinter.CTkButton(master=self.BtnRegion, border_width=2, text="SeleAll", command=lambda: self.SeleAll_event("RemoveAudioFrame" if mode == "RemoveAudioFrame" else "SpeendUpFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.SeleAllBnt.grid(row=0, column=0, padx=10, sticky="nsew")
    self.CancelSeleAllBtn = customtkinter.CTkButton(master=self.BtnRegion, border_width=2, text="CancelSeleAll", command=lambda: self.CancelSeleAll_event("RemoveAudioFrame" if mode == "RemoveAudioFrame" else "SpeendUpFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.CancelSeleAllBtn.grid(row=0, column=1, padx=10, sticky="nsew")
    self.DeleAllBnt = customtkinter.CTkButton(master=self.BtnRegion, border_width=2, text="DeleAll(BUG)", command=lambda: self.DeleAll_event("RemoveAudioFrame" if mode == "RemoveAudioFrame" else "SpeendUpFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.DeleAllBnt.grid(row=0, column=2, padx=10, sticky="nsew")
    if mode == "RemoveAudioFrame":
        self.ConfirmBnt = customtkinter.CTkButton(master=self.BtnRegion, border_width=2, text="Confirm(A)", command=lambda: self.Confirm_event("RemoveAudioFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    elif mode == "SpeendUpFrame":
        self.ConfirmBnt = customtkinter.CTkButton(master=self.BtnRegion, border_width=2, text="Confirm(B)", command=lambda: self.Confirm_event("SpeendUpFrame"), bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.ConfirmBnt.grid(row=0, column=3, padx=10,  sticky="nsew")

    # Input Entry (底下輸入欄)
    self.BottomInputFrame = customtkinter.CTkFrame(ParentFrame)
    self.BottomInputFrame.grid(row=5, column=0, sticky="ew")
    self.BottomInputFrame.grid_columnconfigure((0,1), weight=1)
    self.BottomInputFrame.grid_columnconfigure((2), weight=0)
    self.BottomInputFrame.grid_rowconfigure((0), weight=0)

    self.Entry = customtkinter.CTkEntry(self.BottomInputFrame, placeholder_text="Input")
    self.Entry.grid(row=0, column=0, columnspan=2, padx=(20, 0), sticky="nsew")

    self.EntryBtn = customtkinter.CTkButton(master=self.BottomInputFrame, fg_color="transparent", border_width=2, text="Input", text_color=("gray10", "#DCE4EE"))
    self.EntryBtn.grid(row=0, column=2, padx=(20, 20), sticky="nsew")

    # textbox
    self.textbox = customtkinter.CTkTextbox(ParentFrame)
    # self.textbox.grid(row=2, column=0, padx=10, pady=(5,5), sticky="nsew")

    # Back Btn
    self.BackBtnRegion = customtkinter.CTkFrame(ParentFrame)
    # self.BackBtnRegion.grid(row=4, column=0, padx=10, pady=(5,5), sticky="nsew")
    self.BackBtnRegion.grid_columnconfigure((0), weight=1)
    self.BackBtnRegion.grid_rowconfigure((0), weight=0)
    self.BackBtn = customtkinter.CTkButton(master=self.BackBtnRegion, border_width=2, text="Back", command=self.Back_event, bg_color=Sys.Const.Bnt_bg_color , fg_color=Sys.Const.Bnt_fg_color , border_color=Sys.Const.Bnt_border_color , text_color=Sys.Const.Bnt_text_color , text_color_disabled=Sys.Const.Bnt_text_color_disabled)
    self.BackBtn.grid(row=0, column=0, padx=10, sticky="nsew")


    # Dictory Record
    self.FrameDictionary[mode + "_ListBoxFrame"] = self.listboxFrame
    self.FrameDictionary[mode + "_ListBox"] = self.listbox
    self.FrameDictionary[mode + "_BtnRegion"] = self.BtnRegion
    self.FrameDictionary[mode + "_textbox"] = self.textbox
    self.FrameDictionary[mode + "_BackBtnRegion"] = self.BackBtnRegion