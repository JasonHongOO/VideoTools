
import customtkinter 


def WelcomeFrame(self):
    #Layout 配置
    self.WelcomeFrame = customtkinter.CTkFrame(self, corner_radius=0)
    self.WelcomeFrame.grid(row=0, rowspan=3, column=1, columnspan=3, sticky="nsew")
    self.WelcomeFrame.grid_columnconfigure((0), weight=1)
    self.WelcomeFrame.grid_rowconfigure((1), weight=1)
    self.WelcomeFrame.grid_rowconfigure((0, 2), weight=0)

    self.WelcomeLabelFrame = customtkinter.CTkFrame(self.WelcomeFrame, corner_radius=0, fg_color="#f0ffff")
    self.WelcomeLabelFrame.grid(row=0, column=0, sticky="nsew")
    self.WelcomeLabelFrame.grid_columnconfigure((1), weight=1)
    self.WelcomeLabelFrame.grid_columnconfigure((0, 2), weight=0)
    self.WelcomeLabel = customtkinter.CTkLabel(self.WelcomeLabelFrame, fg_color="transparent", text="Welcom To My Main Page", font=customtkinter.CTkFont(size=40, weight="bold"))
    self.WelcomeLabel.grid(row=0, column=1, columnspan=3, pady=(10,10), sticky="nsew")

    self.WelcomeBtnFrame = customtkinter.CTkFrame(self.WelcomeFrame, corner_radius=0, fg_color="#f0ffff")
    self.WelcomeBtnFrame.grid(row=1, column=0, sticky="nsew")
    self.WelcomeBtnFrame.grid_columnconfigure((0), weight=1)
    self.WelcomeBtnFrame.grid_rowconfigure((0), weight=1)
    self.WelcomeBtn = customtkinter.CTkButton(self.WelcomeBtnFrame, fg_color="transparent", text="Welcome", text_color="#ffffff", text_color_disabled="#000000", hover_color="#ffffff", font=customtkinter.CTkFont(size=20, weight="bold"), image=self.Welcome_image, compound="top")
    self.WelcomeBtn.grid(row=0, column=0, sticky="nsew")