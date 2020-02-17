from socket import * 
import sys 
import time 

#基本文件操作功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd 

    def do_list(self):
        self.sockfd.send(b'L') #發送請求
        #等待回覆
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print("文件清單列表展示完畢\n")
        else:
            #由伺服器發送失敗原因
            print(data)


    def do_get(self,filename):
        self.sockfd.send(('G ' + filename).encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
            print("%s 下載完畢\n"%filename)
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')

#網路連接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return 
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)  #文件伺服器位置

    sockfd = socket()

    try:
        sockfd.connect(ADDR)
    except:
        print("連接伺服器失敗")
        return

    ftp = FtpClient(sockfd) #功能類對象
    while True:
        print("======= 請輸入以下選擇 ========")
        print("========== 命令選項 ==========")
        print("********** list *************")
        print("********* get file **********")
        print("********** quit *************")

        cmd = input("請輸入命令: ")

        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd.strip() == "quit":
            ftp.do_quit()
            sockfd.close()
            sys.exit("謝謝使用")
        else:
            print("請輸入正確命令!")
            continue

    
if __name__ == "__main__":
    main()