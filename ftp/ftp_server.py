'''
模擬ftp 文件伺服器 用來傳輸下載檔案
'''
from socket import *
import os 
import sys
import time
import signal  

#文文件路
FILE_PATH = "/home/ubuntu/"
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#將文件服務器功能寫在類中
class FtpServer(object):
    def __init__(self,connfd):
        self.connfd = connfd

    def do_list(self):
        #獲取文件列表清單
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.connfd.send("文件庫沒有資料".encode()) 
            return 
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)

        files = ''
        for file in file_list:
            if file[0] != '.' and os.path.isfile(FILE_PATH + file):
                files = files + file + '#'
        self.connfd.sendall(files.encode())

    def do_get(self,filename):
        try:
            fd = open(FILE_PATH + filename,'rb')
        except:
            self.connfd.send('文件不存在'.encode())
            return 
        self.connfd.send(b'OK')
        time.sleep(0.1)
        #發送文件   
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
        print("文件發送完畢")

#創建套接字，接收客戶端連接，創進新的進程
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    #處理子進程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("Listen the port 8000...")

    while True:
        try:
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("伺服器退出")
        except Exception as e:
            print("伺服器異常:",e)
            continue 

        print("已連接客戶端:",addr)
        #創建子進程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            ftp = FtpServer(connfd)
            #判斷客戶端請求
            while True:
                data = connfd.recv(1024).decode()
                if not data  or data[0] == 'Q':
                    connfd.close()
                    sys.exit("客戶端退出")
                elif data[0] == 'L':
                    ftp.do_list()
                elif data[0] == 'G':
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)

        else:
            connfd.close()
            continue


if __name__ == "__main__":
    main()

