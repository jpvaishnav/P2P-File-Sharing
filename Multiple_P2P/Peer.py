import socket
import threading
import platform
import mimetypes
import os
import sys
import time
from pathlib import Path

#Ftech the tracker IP from ip.txt file
file=open('C:\ip.txt','r')
lines=file.readlines()

count=1
ip=""
for l in lines:
    if count==96:
        ip=l[39:52]
        break
    else:
        count+=1

print("Central Server IP is : ")
print(ip)

#fetch the peer ip from host_ip.txt file
file=open('C:\host_ip.txt','r')
lines=file.readlines()

count=1
my_ip=""
for l in lines:
    if count==96:
        my_ip=l[39:52]
        break
    else:
        count+=1

print("Peer IP is : ")
print(my_ip)


class MyException(Exception):
    pass


class Client(object):
    def __init__(self, serverhost=ip, V='P2P-Multiple', DIR='rfc'):
        #describe the serve attributes
        self.SERVER_HOST = serverhost
        self.SERVER_PORT = 7617
        self.V = V
        self.DIR = 'rfc'  # file directory
        Path(self.DIR).mkdir(exist_ok=True)

        self.UPLOAD_PORT = None
        self.shareable = True

    def start(self):
        # connect to server
        print('Connecting to the central server %s:%s' %
              (self.SERVER_HOST, self.SERVER_PORT))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.connect((self.SERVER_HOST, self.SERVER_PORT))
        except Exception:
            print('Server Not Available.')
            return

        print('Connected')
        # upload
        uploader_process = threading.Thread(target=self.init_upload)
        uploader_process.start()
        while self.UPLOAD_PORT is None:
            # wait until upload port is initialized
            pass
        print('Peer is listening on the upload port %s' % self.UPLOAD_PORT)

        # interactive shell
        self.cli()

    def cli(self):
        command_dict = {'1': self.add,
                        '2': self.lookup,
                        '3': self.listall,
                        '4': self.pre_download,
                        '5': self.shutdown}
        while True:
            try:
                req = input('\n1: Add file for sharing\n 2: Fetch a file information\n 3: View the database\n 4: Download file\n 5: Shut Down the peer\n\nEnter your request: ')
                command_dict.setdefault(req, self.invalid_input)()
            except MyException as e:
                print(e)
            except Exception:
                print('System Error.')
            except BaseException:
                self.shutdown()

    def init_upload(self):
        # listen upload port
        self.uploader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.uploader.bind(('', 0))
        self.UPLOAD_PORT = self.uploader.getsockname()[1]
        self.uploader.listen(5)

        while self.shareable:
            #grab the request coming at uploader end
            requester, addr = self.uploader.accept()
            print("upload request is coming: ")
            print(requester, addr)
            handler = threading.Thread(
                target=self.handle_upload, args=(requester, addr))
            handler.start()
        self.uploader.close()

    def handle_upload(self, soc, addr):
        #receive the first header from downloader end
        header = soc.recv(1024).decode().splitlines()
        try:
            print("Received header : ")
            print(header)
            version = header[0].split()[-1]
            num = header[0].split()[-2]
            method = header[0].split()[0]
            print(float(header[3]))
            read_pointer=int(float(header[3]))
            print("read_pointer for this peer is : ", read_pointer)
            portion=int(float(header[4]))
            print("Total portion to be uploaded is : ", portion)
            path = '%s/rfc%s.txt' % (self.DIR, num)
            if version != self.V:
                soc.sendall(str.encode(
                    self.V + ' 505 P2P-CI Version Not Supported\n'))
            elif not Path(path).is_file():
                soc.sendall(str.encode(self.V + ' 404 Not Found\n'))
            elif method == 'GET':
                #send the first header to peer
                #so that he becomes aware about the file size and other attributes beforhand
                header = self.V + ' 200 OK\n'
                header += 'Data: %s\n' % (time.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT", time.gmtime()))
                header += 'OS: %s\n' % (platform.platform())
                header += 'Last-Modified: %s\n' % (time.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(path))))
                header += 'Content-Length: %s\n' % (os.path.getsize(path))
                header += 'Content-Type: %s\n' % (
                    mimetypes.MimeTypes().guess_type(path)[0])
                print("sending first header : ")
                print(header)
                soc.sendall(header.encode())
                # Uploading
                try:
                    print('\nUploading...')

                    send_length = 0
                    #print('working before file path\n')
                    with open(path, 'rb') as file:
                        #print('file opened')
                        file.seek(read_pointer,1)
                        #print('reached till read poiner: ', read_pointer)
                        print('current file position: ', file.tell())
                        to_send = file.read(1024)
                        #print('current file position: ', file.tell())
                        #print("message read: ")
                        #print(to_send)
                        #read file 1024 bytes at a time,
                        #and send unitl the end of portion
                    
                        while send_length<(portion):
                            #send_length += len(to_send.encode())
                            send_length+=1024
                            #print("entered into while loop")
                            soc.sendall(to_send)
                            #print("previous message sent")
                            to_send = file.read(1024)
                            #print("message read: ")
                            #print(to_send)
                            #print('current file position: ', file.tell())
                except Exception:
                    raise MyException('Uploading Failed')
                # total_length = int(os.path.getsize(path))
                # print('send: %s | total: %s' % (send_length, total_length))
                # if send_length < total_length:
                #     raise MyException('Uploading Failed')
                print('Uploading task Completed.')
                # Restore CLI
                print(
                    '\n 1: Add file for sharing\n 2: Fetch a file information\n 3: View the database\n 4: Download file\n 5: Shut Down the peer\n\nEnter your request: ')
            else:
                raise MyException('Bad Request.')
        except Exception:
            soc.sendall(str.encode(self.V + '  400 Bad Request\n'))
        finally:
            soc.close()

    def add(self, num=None, title=None):
        if not num:
            num = input('Enter the File number: ')
            if not num.isdigit():
                raise MyException('Invalid Input.')
            title = input('Enter the File title: ')
        file = Path('%s/rfc%s.txt' % (self.DIR, num))
        #print(file)
        if not file.is_file():
            raise MyException('File Not Exit!')
        msg = 'ADD RFC %s %s\n' % (num, self.V)
        msg += 'Host: %s\n' % socket.gethostname()
        msg += 'Port: %s\n' % self.UPLOAD_PORT
        msg += 'Title: %s\n' % title
        msg += 'IP: %s\n' %(my_ip)
        msg += 'Length: %s\n' %(os.path.getsize(file))
        print(msg)
        self.server.sendall(msg.encode())
        res = self.server.recv(1024).decode()
        print('Recieved response: \n%s' % res)

    def lookup(self):
        num = input('Enter the File number: ')
        title = input('Enter the File title(optional): ')
        msg = 'LOOKUP RFC %s %s\n' % (num, self.V)
        msg += 'Host: %s\n' % socket.gethostname()
        msg += 'Post: %s\n' % self.UPLOAD_PORT
        msg += 'Title: %s\n' % title
        self.server.sendall(msg.encode())
        res = self.server.recv(1024).decode()
        print('Recieved response: \n%s' % res)

    def listall(self):
        l1 = 'LIST ALL %s\n' % self.V
        l2 = 'Host: %s\n' % socket.gethostname()
        l3 = 'Port: %s\n' % self.UPLOAD_PORT
        msg = l1 + l2 + l3
        self.server.sendall(msg.encode())
        res = self.server.recv(1024).decode()
        print('Recieved response: \n%s' % res)

    def pre_download(self):
        #demand the requested file number from peer end using lookup packet 
        num = input('Enter the File number: ')
        msg = 'LOOKUP RFC %s %s\n' % (num, self.V)
        msg += 'Host: %s\n' % socket.gethostname()
        msg += 'Port: %s\n' % self.UPLOAD_PORT
        msg += 'Title: Unkown\n'
        self.server.sendall(msg.encode())
        lines = self.server.recv(1024).decode().splitlines()
        if lines[0].split()[1] == '200':
            # Choose a peer
            total_peers=0
            print('Available peers: ')
            for i, line in enumerate(lines[1:]):
                line = line.split()
                print('%s: %s:%s' % (i + 1, line[-2], line[-1]))
                ip=line[-5]
                fSize=int(line[-4])
                total_peers+=1
            print("All peers ips are : ",ip)
            print("File size is : ",fSize)
            print("Total peers are : ",total_peers)

            
            #path = '%s/rfc%s.txt' % (self.DIR, num)
            #file_size=os.path.getsize(path)
            #print('file size is : ')
            #print(file_size)
            peer_host=[]
            peer_port=[]
            peer_ip=[]
            for i, line in enumerate(lines[1:]):
                print(line)
                line = line.split()
                #print('%s: %s:%s' % (i + 1, line[-2], line[-1]))
                peer_host.append(line[-2])
                peer_port.append(int(line[-1]))
                peer_ip.append(line[-5])
                title=line[-3]
                print('working: ')
                #print(peer_host,peer_port,title,peer_ip)
                #title= line.rsplit(None, 2)[0].split(None, 2)[-1]
            #total_peers=len(peer_host)
            print('Total Peers: ')
            print(total_peers)
            print(peer_host)
            print(peer_port)
            print(peer_ip)
            #print("title : "+str(title))
            
            #except Exception:
            #    raise MyException('Invalid Input.')
            # exclude self
            #if((peer_host, peer_port) == (socket.gethostname(), self.UPLOAD_PORT)):
            #    raise MyException('Do not choose yourself.')
            # send get request
            j=0
            #initiate thread and pass the corresponding portion in the download function
            while j<total_peers:
                downloader = threading.Thread(
                target=self.download, args=(num,title, peer_host[j],peer_port[j],j,fSize,total_peers,peer_ip[j]))
                downloader.start()
                #print('Thread starting'+str(j)+'\n')
                j+=1
            j=0
            content=""
            #combine the content received from different peers
            while j<total_peers:
                path = '%s/rfc%s%s.txt' % (self.DIR, num,j)
                #print('reading from path: ', path)
                with open(path) as fp:
                    content+=fp.read()
                j+=1
                os.remove(path)
            new_path='%s/rfc%s.txt' % (self.DIR, num)
            print('File download at ',new_path)
            with open(new_path,'w') as f:
                f.write(content)
            #print('written on new_path')
        elif lines[0].split()[1] == '400':
            raise MyException('Invalid Input.')
        elif lines[0].split()[1] == '404':
            raise MyException('File Not Available.')
        elif lines[0].split()[1] == '500':
            raise MyException('Version Not Supported.')

    def download(self, num,title, peer_host, peer_port,j,file_size,total_peers,peer_ip):
        try:
            # make connnection
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect_ex return errors
            print("binding Download socket to peer_host and peer_port ")
            soc.connect((peer_ip,peer_port))
            #if soc.connect_ex((peer_host, peer_port)):
                # print('Try Local Network...')
                # if soc.connect_ex(('localhost', peer_port)):
            #    raise MyException('Peer Not Available')
            # make request
            msg = 'GET RFC %s %s\n' % (num, self.V)
            msg += 'Host: %s\n' % socket.gethostname()
            msg += 'OS: %s\n' % platform.platform()
            msg += '%s\n' % (j*(file_size/total_peers)+1)
            msg += '%s\n' % (file_size/total_peers)
            print('message is : '+str(msg))
            soc.sendall(msg.encode())

            # Downloading

            header = soc.recv(1024).decode()
            print('header is : ' + str(header))
            print('Recieve response header: \n%s' % header)
            header = header.splitlines()
            if header[0].split()[-2] == '200':
                path = '%s/rfc%s%s.txt' % (self.DIR, num,j)
                print('Downloading...')
                try:
                    with open(path, 'w') as file:
                        content = soc.recv(1024)
                        while content:
                            #print("content received")
                            #print(content)
                            file.write(content.decode())
                            content = soc.recv(1024)
                except Exception:
                    raise MyException('Downloading Failed')

                total_length = file_size/total_peers
                # print('write: %s | total: %s' % (os.path.getsize(path), total_length))

                if os.path.getsize(path) < total_length:
                    raise MyException('Downloading Failed')

                print('Downloading Completed.')
                # Share file, send ADD request
                print('Sending ADD request for further sharing...')
                if self.shareable:
                    self.add(num, title)
            elif header[0].split()[1] == '400':
                raise MyException('Invalid Input.')
            elif header[0].split()[1] == '404':
                raise MyException('File Not Available.')
            elif header[0].split()[1] == '500':
                raise MyException('Version Not Supported.')
        finally:
            soc.close()
            # Restore CLI
          #  print('\n1: Add, 2: Look Up, 3: List All, 4: Download\nEnter your request: ')

    def invalid_input(self):
        raise MyException('Invalid Input.')

    def shutdown(self):
        print('\nShutting Down...')
        self.server.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        client = Client(sys.argv[1])
    else:
        client = Client()
    client.start()
