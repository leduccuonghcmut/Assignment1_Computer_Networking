from tkinter import *
import tkinter as tk
import os
import customtkinter as ctk
from PIL import Image, ImageTk  # Thêm dòng này vào đầu file
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
        
        self.current_frame = None  

    # Gọi trang đầu tiên
        self.switch_frame(self.initialPage)

    def switch_frame(self, frame_function):
        if self.current_frame is not None:
         self.current_frame.pack_forget()  # Chỉ gọi nếu frame hiện tại đã được tạo
    
        self.current_frame = frame_function()  # Tạo frame mới từ hàm
        self.current_frame.pack(fill="both", expand=True)  # Hiển thị frame mới

        
    def changeTheme(self):
        type = ctk.get_appearance_mode()
        if type == "Light":
            ctk.set_appearance_mode("dark")

        else:
            ctk.set_appearance_mode("light")

            self.frameMainPage.configure(fg_color="#909090")  # Màu nền cho frame chính
    
    def initialPage(self):
        # Background color for left side (logo area)
        left_frame = ctk.CTkFrame(self.frameInitialPage, width=500, height=HEIGHT, fg_color="#2B1A47")
        left_frame.place(relx=0, rely=0)
        t1_frame = ctk.CTkFrame(self.frameInitialPage, width=500, height=HEIGHT, fg_color="#2B1A47")
        t1_frame.place(relx=0.5, rely=0)
        # image_path = "C:/Users/Duy/OneDrive - hcmut.edu.vn/mạng máy tính/new1.png"  # Thay đổi đường dẫn tới hình ảnh của bạn
        image_path = os.path.join(os.path.dirname(__file__), "new1.png")
        image = Image.open(image_path)
        new_size = (300, 300)  # Thay đổi width và height theo kích thước bạn muốn
        image = image.resize(new_size, Image.LANCZOS )
        photo = ctk.CTkImage(light_image=image, dark_image=image, size=new_size)
        # Hiển thị ảnh trên label
        image_label = ctk.CTkLabel(self.frameInitialPage, image=photo, text="")
        image_label.place(relx=0.25, rely=0.27, anchor="center")


        # Additional "BK" label 
        bk_label = ctk.CTkLabel(left_frame, text="GROUP: 6", font=("Arial", 20, "bold"), text_color="white")
        bk_label.place(relx=0.46, rely=0.5, anchor=tk.CENTER)

        # "A NETWORK APPLICATION" label
        app_label = ctk.CTkLabel(left_frame, text="A NETWORK APPLICATION", font=("Arial", 20), text_color="white")
        app_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Right side: Login form
        right_frame = ctk.CTkFrame(self.frameInitialPage, width=400, height=350, fg_color="white")
        right_frame.place(relx=0.5, rely=0.2)

        label_login = ctk.CTkLabel(right_frame, text="Login", font=("Arial", 30, "bold"), text_color="black")
        label_login.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        username_entry = ctk.CTkEntry(right_frame, placeholder_text="User Name", width=300, height=40, font=("Arial", 16))
        username_entry.place(relx=0.5, rely=0.35 , anchor=tk.CENTER)

        password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", width=300, height=40, font=("Arial", 16), show="*")
        password_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        button_login = ctk.CTkButton(right_frame, text="Login", font=("Arial", 16, "bold"), fg_color="#4B2E83", 
                                     command=lambda: self.check_login(username_entry, password_entry))
        button_login.place(relx=0.3  , rely=0.8, anchor=tk.CENTER)

        button_signup = ctk.CTkButton(right_frame, text="Signup", font=("Arial", 16, "bold"), fg_color="#FF4D4D", 
                                      command=lambda: messagebox.showinfo("Info", "Signup feature not implemented!"))
        button_signup.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
        
        return self.frameInitialPage

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

        # image_path = "C:/Users/Duy/OneDrive - hcmut.edu.vn/mạng máy tính/logo-removebg-preview.png"  # Thay đổi đường dẫn tới hình ảnh của bạn
        # image = Image.open(image_path)
        # new_size = (300, 300)  # Thay đổi width và height theo kích thước bạn muốn
        # image = image.resize(new_size, Image.LANCZOS )
        # photo = ImageTk.PhotoImage(image)
        # image_label = ctk.CTkLabel(self.frameMainPage, image=photo)
        # image_label.image = photo  # Giữ tham chiếu đến hình ảnh
        # image_label.place(relx=0.8, rely=0.2, anchor=tk.CENTER)
        self.outputStatusCenter.configure(fg_color="white")  # Đặt màu nền thành trắng

        self.outputStatusCenter.place(relx=0.3, rely=0.58, anchor=tk.CENTER, relwidth=0.5, relheight=0.55)
        self.outputStatusCenter.configure(state=DISABLED)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Table State", font=("Arial", 15))
        frame_label.place(relx=0.27, rely=0.89, anchor=tk.CENTER)

        frame_label = ctk.CTkLabel(self.frameMainPage, text="WELCOME ADMIN", font=("Arial", 40, "bold"))
        frame_label.place(relx=0.25, rely=0.1, anchor=tk.CENTER)
        
        # frame_label = ctk.CTkLabel(self.frameMainPage, text="INFORMATION OF TRACKER", font=("Arial", 20, "bold"))
        # frame_label.place(relx=0.3, rely=0.2, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Server Host: " + self.serverHost, font=("Arial", 15))
        frame_label.place(relx=0.15, rely=0.2   , anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Server Port: " + str(self.serverPort), font=("Arial", 15))
        frame_label.place(relx=0.13, rely=0.25, anchor=tk.CENTER)

        btn_view_user = ctk.CTkButton(self.frameMainPage, text="LIST PEERS", font=("Arial", 20, "bold"),
                                      command=lambda: self.animate_panel.animate())
        btn_view_user.place(relx=0.8, rely=0.6, anchor=tk.CENTER)

        btn_show_peer = ctk.CTkButton(self.frameMainPage, text="LIST FILES", font=("Arial", 20, "bold"),
                                      command=lambda: self.switch_frame(self.listFilesOnSystem))
        btn_show_peer.place(relx=0.8, rely=0.7, anchor=tk.CENTER)

        btn_change_themes = ctk.CTkButton(self.frameMainPage, text="COLOFUL", font=("Arial", 20, "bold"),
                                          command=self.changeTheme)
        btn_change_themes.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
        
        list_header = ctk.CTkLabel(self.animate_panel, text="LIST PEERS", font=("Arial", 30, "bold"))
        list_header.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        return self.frameMainPage
    
    def listFilesOnSystem(self):
        self.frameListFilesOnSystem.configure(fg_color="#909090")  # Màu nền cho frame chính
        # image_path = "C:/Users/Duy/OneDrive - hcmut.edu.vn/mạng máy tính/144.png"  # Thay đổi đường dẫn tới hình ảnh của bạn
        image_path = os.path.join(os.path.dirname(__file__), "144.png")

        image = Image.open(image_path)
        new_size = (300, 300)  # Thay đổi width và height theo kích thước bạn muốn
        image = image.resize(new_size, Image.LANCZOS )
        photo = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(self.frameListFilesOnSystem, image=photo, text="")
        image_label.image = photo  # Giữ tham chiếu đến hình ảnh
        image_label.place(relx=0.8, rely=0.3, anchor=tk.CENTER)
        self.outputFileOnSystem.place(relx=0.3, rely=0.58, anchor=tk.CENTER, relwidth=0.5, relheight=0.55)
        self.outputFileOnSystem.configure(state=DISABLED)

        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="LIST OF FILES", font=("Arial", 40, "bold"))
        frame_label.place(relx=0.2, rely=0.1, anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="Server Host: " + self.serverHost, font=("Arial", 15))
        frame_label.place(relx=0.15, rely=0.2   , anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFilesOnSystem, text="Server Port: " + str(self.serverPort), font=("Arial", 15))
        frame_label.place(relx=0.13, rely=0.25, anchor=tk.CENTER)

        btn_BACK = ctk.CTkButton(self.frameListFilesOnSystem, text="BACK", font=("Arial", 20, "bold"),
                                 command=lambda: self.switch_frame(self.mainPage))
        btn_BACK.place(relx=0.8, rely=0.8, anchor=tk.CENTER)

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