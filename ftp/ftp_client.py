from socket import * 
import sys 
import time 

class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd 

    def do_list(self):
        self.sockfd.send(b'L') #發送請求
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print("文件列表展示完畢\n")
        else:
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
            print("%s 客戶端下載完畢\n"%filename)
        else:
            print(data)

    def do_put(self,filename):
        try:
            f = open(filename,'rb')
        except:
            print("沒有找到文件")
            return 

        self.sockfd.send(('P ' + filename).encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break 
                self.sockfd.send(data)
            f.close()
            print("%s 客戶端上傳完畢"%filename)
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')

def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return 
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)  #文件伺服器地址
    sockfd = socket()

    try:
        sockfd.connect(ADDR)
    except:
        print("連接伺服器失敗")
        return

    ftp = FtpClient(sockfd) #功能類對象
    while True:
        print("========== 命令选项 ==========")
        print("********** list *************")
        print("********* get file **********")
        print("********* put file **********")
        print("********** quit *************")
        print("===============================")

        cmd = input("請輸入命令: ")

        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd.strip() == "quit":
            ftp.do_quit()
            sockfd.close()
            sys.exit("謝謝使用")
        else:
            print("請輸入正確命令!")
            continue
   
if __name__ == "__main__":
    main()
