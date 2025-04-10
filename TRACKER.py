import socket
import threading
import pickle
import math
from threading import Thread
import time

subFileSize = 512 * 1024  # 512KB

# Biến toàn cục để giao tiếp với UI
SERVER_FEObject = None

#---------------------------------fileShared Class----------------------------------------------
class fileShared:
    def __init__(self, fileName, filePath, peerHost, peerPort, size):
        self.fileName = fileName
        self.numberOfPeer = 1
        self.size = size
        self.pieces = math.ceil(size / subFileSize)
        self.informPeerLocal = [[filePath, peerHost, peerPort]]

#---------------------------------SERVER_BE Class---------------------pyth-------------------------
class SERVER_BE:
    def __init__(self, serverHost, serverPort):
        self.listPeer = []
        self.listFileExist = []
        self.listFileShared = []
        self.serverHost = serverHost
        self.serverPort = serverPort
    
    def implementDownload(self, conn):  
        fileNameDownload = pickle.loads(conn.recv(10240))
        conn.send(bytes("SUCCESS", "utf-8"))
        
        peerHost = str(conn.recv(4096), "utf-8")
        conn.send(bytes("SUCCESS", "utf-8"))
        peerPort = int(str(conn.recv(4096), "utf-8"))
        conn.send(bytes("SUCCESS", "utf-8"))
        
        conn.recv(4096)
        
        fileShareObject = None
        for iterator in self.listFileShared:
            if iterator.fileName == fileNameDownload:
                fileShareObject = iterator
                break
        if fileShareObject != None:
            conn.send(bytes("File exist!", "utf-8"))
            conn.recv(4096)
            pieces = math.ceil(fileShareObject.size / subFileSize)
            conn.sendall(pickle.dumps(fileShareObject.informPeerLocal))
            conn.recv(4096)
            conn.send(bytes(str(pieces), "utf-8"))
            conn.recv(4096)
            SERVER_FEObject.showStatusCenter("Download", peerHost, peerPort, fileNameDownload,pieces)
        else:
            conn.send(bytes("File not exist!", "utf-8"))
            conn.recv(4096)
        
        conn.send(bytes("SUCCESS", "utf-8"))
    
    def implementListenPeer(self):
        serverSocket = socket.socket()
        serverSocket.bind((self.serverHost, self.serverPort))
        serverSocket.listen(10)
    
        while True:
            conn, addr = serverSocket.accept()
            stopFlag = threading.Event()
            condition = Thread(target=self.threadListenPeer, args=[conn, stopFlag])
            condition.start()
            # condition2 = Thread(target=self.threadListen, args=(conn,))
            # condition2.start()
    
    def implementSharing(self, filePath, peerHost, peerPort, size):
        iterator = -1
        pieces = math.ceil(size / subFileSize)  # Giả sử subFileSize đã được định nghĩa
        while True:
            if filePath[iterator] == "\\":
                break
            iterator -= 1
        fileName = filePath[(iterator + 1):]
        
        flagFileExist = False
        for fileSharedObject in self.listFileShared:
            if fileSharedObject.fileName == fileName:
                for informPeerLocal in fileSharedObject.informPeerLocal:
                    if informPeerLocal[1] == peerHost and informPeerLocal[2] == peerPort:
                        flagFileExist = True
                        break
                if flagFileExist:
                    break
                else:
                    flagFileExist = True
                    fileSharedObject.numberOfPeer += 1
                    fileSharedObject.informPeerLocal.append([filePath, peerHost, peerPort])
                    SERVER_FEObject.showListFileOnSystem(self.listFileShared,pieces)
                    break
        
        if not flagFileExist:
            fileShareObject = fileShared(fileName, filePath, peerHost, peerPort, size)
            self.listFileShared.append(fileShareObject)
            self.listFileExist.append(fileName)
            SERVER_FEObject.showListFileOnSystem(self.listFileShared,pieces)
        SERVER_FEObject.showStatusCenter("Upload", peerHost, peerPort, fileName,pieces)
    
    def threadListenPeer(self, conn, stopFlag):
        # conn.settimeout(2)
        # last_request_time = time.time()
        
        while not stopFlag.is_set():
        #   try:  
            typeOfRequest = str(conn.recv(4096), "utf-8")
            # print(f"📥 Server nhận: {typeOfRequest}")  # Debug
            conn.send(bytes("SUCCESS", "utf-8"))  # Xác nhận với client

            if typeOfRequest == "Join to LAN":
                peerInform = pickle.loads(conn.recv(4096))
                conn.send(bytes("SUCCESS", "utf-8"))
                self.listPeer.append(peerInform)
                SERVER_FEObject.showPeers(typeOfRequest,peerInform)
                conn.recv(4096)
                conn.sendall(pickle.dumps(self.listPeer))
                conn.recv(4096)
                conn.send(bytes("SUCCESS", "utf-8"))
                SERVER_FEObject.showStatusCenter(typeOfRequest, peerInform[0], peerInform[1], "","")
            elif typeOfRequest== "Cancel":
                stopFlag.set()
            elif typeOfRequest == "BYE":
                print("disconect")
                conn.send(bytes("SUCCESS", "utf-8"))
                peerInform = pickle.loads(conn.recv(4096))
                conn.send(bytes("SUCCESS", "utf-8"))
                # self.listPeer = [peer for peer in self.listPeer if peer != peerInform]
                SERVER_FEObject.showPeers(typeOfRequest,peerInform)
                SERVER_FEObject.showStatusCenter(typeOfRequest, peerInform[0], peerInform[1], "","")
                # SERVER_FEObject.showListFileOnSystem("","",peerInform[0],peerInform[1],typeOfRequest)
                conn.close()
                stopFlag.set()
            elif typeOfRequest == "Upload":
                filePath = str(conn.recv(4096), "utf-8")
                conn.send(bytes("SUCCESS", "utf-8"))
                peerHost = str(conn.recv(4096), "utf-8")
                conn.send(bytes("SUCCESS", "utf-8"))
                peerPort = int(str(conn.recv(4096), "utf-8"))
                conn.send(bytes("SUCCESS", "utf-8"))
                size = int(str(conn.recv(4096), "utf-8"))
                conn.send(bytes("SUCCESS", "utf-8"))
                self.implementSharing(filePath, peerHost, peerPort, size)
            elif typeOfRequest == "Download":
                self.implementDownload(conn)
            elif typeOfRequest == "fileExist":
                conn.recv(4096)
                conn.sendall(pickle.dumps(self.listFileExist))
                conn.recv(4096)
                conn.send(bytes("SUCCESS", "utf-8"))
        #   except socket.timeout:
        #     #   if time.time() - last_request_time > 3:
        #     #       print("No request received for 10 seconds. Disconnected.")
        #     #       break
        #       continue  
    # def threadListen(self, conn):
    #  conn.settimeout(5)  # Đặt timeout để tránh bị treo vô hạn
    # while True:
    #     try:
    #         data = str(conn.recv(4096), "utf-8")
    #         if not data:
    #             print("🔴 Kết nối bị đóng bởi peer!")
    #             break
    #         if data == "BYE":
    #             print("🔴 Peer yêu cầu ngắt kết nối!")
    #             break
    #     except socket.timeout:
    #         continue  # Nếu timeout, tiếp tục vòng lặp
    #     except ConnectionResetError:
    #         print("🔴 Kết nối bị đóng đột ngột!")
    #         break





            
# Chạy chính
if __name__ == "__main__":
    from server_fe_template import SERVER_FE  # Import UI từ file template
    
  #--------Using when transferring file with Wireless --------------
  # peerHost= socket.gethostbyname_ex(socket.gethostname())[2][1]  
  #-----------------------------------------------------------------
  
  #------Using when transferring file with Ethernet----------------
    serverHost= socket.gethostbyname(socket.gethostname())
  #----------------------------------------------------------------
    serverPort = 1000
    
    SERVER_BEObject = SERVER_BE(serverHost, serverPort)
    condition = Thread(target=SERVER_BEObject.implementListenPeer)
    condition.start()
    SERVER_FEObject = SERVER_FE(serverHost, serverPort)
    SERVER_FEObject.mainloop()