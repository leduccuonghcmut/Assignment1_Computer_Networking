from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

WIDTH = 900
HEIGHT = 600
SERVER_USERNAME = 'admin'
SERVER_PASSWORD = 'admin'

#---------------------------------SlidePanel Class----------------------------------------------
class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent)
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = abs(start_pos - end_pos)
        
        self.pos = start_pos
        self.in_start_pos = True
        
        self.place(relx=self.start_pos, rely=0, relwidth=self.width, relheight=0.65)
        
    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backward()
    
    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0, relwidth=self.width, relheight=0.65)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False
    
    def animate_backward(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0, relwidth=self.width, relheight=0.65)
            self.after(10, self.animate_backward)
        else:
            self.in_start_pos = True

#---------------------------------SERVER_FE Class----------------------------------------------
class SERVER_FE(ctk.CTk):
    def __init__(self, serverHost, serverPort):
        super().__init__()
        self.username = None
        self.password = None
        self.numberOfPeers = 0

        self.serverHost = serverHost
        self.serverPort = serverPort
        
        #---------------Initial frame of several pages------------------------------
        self.frameInitialPage = ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
        self.frameExecuteLoginButton = ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
        self.frameMainPage = ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
        self.frameListFilesOnSystem = ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
        #--------------------------------------------------------------------------
        
        #-----------Initialize text and animation----------------------------------
        self.outputStatusCenter = ctk.CTkTextbox(self.frameMainPage)
        self.animate_panel = SlidePanel(self.frameMainPage, 1, 0.72)
        self.outputListPeer = ctk.CTkTextbox(self.animate_panel)
        self.outputFileOnSystem = ctk.CTkTextbox(self.frameListFilesOnSystem)
        #-----------------------------------------------------------------------------
        
        self.title("Tracker File Sharing Application")
        self.resizable(False, False)
        self.geometry("900x600")
        
        self.current_frame = self.initialPage()
        self.current_frame.pack()

    def switch_frame(self, frame):
        self.current_frame.pack_forget()
        self.current_frame = frame()
        self.current_frame.pack(padx=0)
        
    def changeTheme(self):
        type = ctk.get_appearance_mode()
        if type == "Light":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def initialPage(self):
        frame_label = ctk.CTkLabel(self.frameInitialPage, text="WELCOME TO\n BITTORENT FILE SHARING", font=("Arial", 40, "bold"))
        frame_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        button_sign_in = ctk.CTkButton(self.frameInitialPage, text="LOG IN", font=("Arial", 20, "bold"),
                                       command=lambda: self.switch_frame(self.executeLoginButton))
        button_sign_in.place(relx=0.4, rely=0.7, anchor=tk.CENTER)
        
        button_sign_up = ctk.CTkButton(self.frameInitialPage, text="CHANGE THEME", font=("Arial", 20, "bold"), 
                                       command=self.changeTheme)
        button_sign_up.place(relx=0.6, rely=0.7, anchor=tk.CENTER)
        
        return self.frameInitialPage

    def executeLoginButton(self):
        home_page = ctk.CTkButton(self.frameExecuteLoginButton, text="HOME PAGE", font=("Arial", 20, "bold"),
                                  command=lambda: self.switch_frame(self.initialPage))
        home_page.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
        
        label_login = ctk.CTkLabel(self.frameExecuteLoginButton, text="LOG IN", font=("Arial", 30, "bold"))
        label_login.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        label_username = ctk.CTkLabel(self.frameExecuteLoginButton, text="Username", font=("Arial", 20, "bold"))
        label_username.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
        
        username_entry = ctk.CTkEntry(self.frameExecuteLoginButton, placeholder_text="Username", width=300, height=4)
        username_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_password = ctk.CTkLabel(self.frameExecuteLoginButton, text="Password", font=("Arial", 20, "bold"))
        label_password.place(relx=0.2, rely=0.6, anchor=tk.CENTER)
        
        password_entry = ctk.CTkEntry(self.frameExecuteLoginButton, placeholder_text="Password", width=300, height=4)
        password_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        button_sign_in = ctk.CTkButton(self.frameExecuteLoginButton, text="CONFIRM", font=("Arial", 20, "bold"), 
                                       command=lambda: self.check_login(username_entry, password_entry))
        button_sign_in.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        return self.frameExecuteLoginButton

    def check_login(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()
    
        if username == SERVER_USERNAME and password == SERVER_PASSWORD:
            self.username = username
            self.password = password
            messagebox.showinfo("Successful!", "Log in completed!")
        else:
            messagebox.showerror("Error!", "Log in again!")
            return

        self.switch_frame(self.mainPage)
        
    def mainPage(self):
        self.outputListPeer.place(relx=0.5, rely=0.55, anchor=ctk.CENTER, relwidth=0.8, relheight=0.8)
        self.outputListPeer.configure(state=DISABLED)
        
        self.outputStatusCenter.place(relx=0.5, rely=0.58, anchor=tk.CENTER, relwidth=0.4, relheight=0.4)
        self.outputStatusCenter.configure(state=DISABLED)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Table State", font=("Arial", 15))
        frame_label.place(relx=0.5, rely=0.81, anchor=tk.CENTER)

        frame_label = ctk.CTkLabel(self.frameMainPage, text="WELCOME ADMIN", font=("Arial", 40, "bold"))
        frame_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="INFORMATION OF TRACKER", font=("Arial", 20, "bold"))
        frame_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Server Host: " + self.serverHost, font=("Arial", 15))
        frame_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Server Port: " + str(self.serverPort), font=("Arial", 15))
        frame_label.place(relx=0.5, rely=0.31, anchor=tk.CENTER)

        btn_view_user = ctk.CTkButton(self.frameMainPage, text="LIST PEERS", font=("Arial", 20, "bold"),
                                      command=lambda: self.animate_panel.animate())
        btn_view_user.place(relx=0.25, rely=0.9, anchor=tk.CENTER)

        btn_show_peer = ctk.CTkButton(self.frameMainPage, text="FILES ON SYSTEM", font=("Arial", 20, "bold"),
                                      command=lambda: self.switch_frame(self.listFilesOnSystem))
        btn_show_peer.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        btn_change_themes = ctk.CTkButton(self.frameMainPage, text="CHANGE THEMES", font=("Arial", 20, "bold"),
                                          command=self.changeTheme)
        btn_change_themes.place(relx=0.75, rely=0.9, anchor=tk.CENTER)
        
        list_header = ctk.CTkLabel(self.animate_panel, text="LIST PEERS", font=("Arial", 30, "bold"))
        list_header.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        return self.frameMainPage
    
    def listFilesOnSystem(self):
        self.outputFileOnSystem.place(relx=0.5, rely=0.58, anchor=tk.CENTER, relwidth=0.4, relheight=0.4)
        self.outputFileOnSystem.configure(state=DISABLED)

        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="LIST OF FILES ON THE SYSTEM", font=("Arial", 45, "bold"))
        frame_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="INFORMATION OF TRACKER", font=("Arial", 20, "bold"))
        frame_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="Server Host: " + self.serverHost, font=("Arial", 15))
        frame_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="Server Port: " + str(self.serverPort), font=("Arial", 15))
        frame_label.place(relx=0.5, rely=0.31, anchor=tk.CENTER)

        btn_BACK = ctk.CTkButton(self.frameListFilesOnSystem, text="BACK", font=("Arial", 20, "bold"),
                                 command=lambda: self.switch_frame(self.mainPage))
        btn_BACK.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        return self.frameListFilesOnSystem

    # Hàm hiển thị dữ liệu lên UI (có thể được gọi từ backend)
    def showPeers(self, informPeer):
        self.outputListPeer.configure(state=NORMAL)
        self.numberOfPeers += 1
        self.outputListPeer.insert(ctk.END, f"{self.numberOfPeers}.  PeerHost: {informPeer[0]}, PeerPort: {informPeer[1]}." + "\n\n")
        self.outputListPeer.see(ctk.END)
        self.outputListPeer.configure(state=DISABLED)
    
    def showListFileOnSystem(self, listFileShared):
        self.outputFileOnSystem.configure(state=NORMAL)
        counter = 1
        self.outputFileOnSystem.delete(1.0, ctk.END)
        for iterator in listFileShared:
            self.outputFileOnSystem.insert(ctk.END, f"{counter}. fileName: \"{iterator.fileName}\"." + "\n")
            for peer in iterator.informPeerLocal:
                self.outputFileOnSystem.insert(ctk.END, f"      [PeerHost: {peer[1]}, PeerPort: {peer[2]}]" + "\n")
            self.outputFileOnSystem.insert(ctk.END, "\n")
            counter += 1
        self.outputFileOnSystem.see(ctk.END)
        self.outputFileOnSystem.configure(state=DISABLED)

    def showStatusCenter(self, typeOfStatement, peerHost, peerPort, fileName):
        self.outputStatusCenter.configure(state=NORMAL)
        if typeOfStatement == "Download":
            self.outputStatusCenter.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} download file \"{fileName}\"" + "\n\n")
        elif typeOfStatement == "Upload":
            self.outputStatusCenter.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} upload file \"{fileName}\"" + "\n\n")
        elif typeOfStatement == "Join to LAN":
            self.outputStatusCenter.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} joined to network" + "\n\n")
        self.outputStatusCenter.see(ctk.END)
        self.outputStatusCenter.configure(state=DISABLED)

# Hàm chạy thử (có thể bỏ khi tích hợp với backend)
if __name__ == "__main__":
    app = SERVER_FE("localhost", 85)
    app.mainloop()