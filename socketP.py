
import socket

def createServer(host, port):
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Tao socket server
    Server.bind((host,port)) #rang buoc host vs port
    Server.listen(5) #lang nghe (max 5 client)
    return Server

def readHTTPRequest(Server):
    msg=""
    while(msg == ""): #Khi khong co request -> doc request
        print("Waiting for Client")
        Client, address = Server.accept() #Chap nhan client
        print("Client: ", address," connected to Server")
        msg = Client.recv(1024).decode()
    return Client,msg
                    
def sendIndex(Client): #chuyen file index len request
    f = open("index.html","rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
    Content-Length: %d

    """%len(L) #tao request cho index #Nhớ để khoảng trống chứ k nó k phân biệt được đầu đuôi TT
    print("----HTTP respone index.html: ")
    print(header)
    header += L.decode() # binary -> string
    Client.send(bytes(header,'utf-8'))

def moveToIndex(Client):#chuyen http toi duong dan index
    header = """HTTP/1.1 301 Moved Permanently
Location: http://localhost:8080/index.html

"""
    print("----HTTP respone move to index.html: ")
    print(header)
    Client.send(bytes(header,'utf-8'))

def showIndex(Server,Client,Request): #show file index 
    if "GET /index.html HTTP/1.1" in Request: #Truong hop da co san phan index.html trong duong dan
        sendIndex(Client)
        Server.close()
    if "GET / HTTP/1.1" in Request: #Truong hop khong co index.html trong duong dan
        moveToIndex(Client) #gui request truy cap Index cho Server
        Server.close()
        Server = createServer("localhost",8080)
        Client, Request = readHTTPRequest(Server)
        print("----HTTP request: ")
        print (Request) #In request truoc khi chuyen ve showIndex (Luc nay da co request tao tu readHTTPRequest)
        showIndex(Server, Client, Request)

def checkPass(Request):
    if "POST / HTTP/1.1" not in Request: #tham khao HTTP Protocol de code html
        return False
    if "username=admin&password=admin" in Request: #khi co username&password dung trong Request
        return True
    else:
        return False

#Tuong tu nhu o index, ta gui file info len request, chuyen den http chua info, sau do show Info

def sendInfo(Client):
    f=open("info.html","rb")
    L=f.read()
    header= """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
    print("----HTTP respone info.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header,'utf-8'))
    
def sendImg(Client,Img)
    f=open(Img,"rb")
    L=f.read()
    size=len(bytes)
    header= """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%size
    print("-----HTTP respone info.html: ")
    print
    

def moveToInfo(Client):
    header= """HTTP/1.1 301 Moved Permanently
Location: http://localhost:8080/info.html

"""
    print("---HTTP respont move to info.html: ")
    print(header)
    Client.send(bytes(header,'utf-8'))
    Server.close()

def showInfo(Server,Client): #show file info  
    Server = createServer("localhost",8080)
    Client, Request = readHTTPRequest(Server)
    print("----HTTP request: ")
    print (Request) #In request truoc khi chuyen ve showInfo (Luc nay da co request tao tu readHTTPRequest)
    if "GET /info.html HTTP/1.1" in Request:
        showInfo(Server, Client)
    Server.close()
    
    #Tuong tu nhu o info, ta gui file 404 len request, chuyen den http chua 404, sau do show 404

def send404(Client):
    f=open("404.html","rb")
    L=f.read()
    header= """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
    print("----HTTP respone 404.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header,'utf-8'))

def moveTo404(Client):
    header= """HTTP/1.1 301 Moved Permanently
Location: http://localhost:8080/404.html

"""
    print("---HTTP respont move to info.html: ")
    print(header)
    Client.send(bytes(header,'utf-8'))
    Server.close()

def show404(Server,Client): #show file info  
    Server = createServer("localhost",8080)
    Client, Request = readHTTPRequest(Server)
    print("----HTTP request: ")
    print (Request) #In request truoc khi chuyen ve showInfo (Luc nay da co request tao tu readHTTPRequest)
    if "GET /404.html HTTP/1.1" in Request:
        showInfo(Server, Client)
    Server.close()


if __name__=="__main__": 
    #while True:
        Server = createServer("localhost",8080)
        Client, Request = readHTTPRequest(Server)
        print("----HTTP request: ")
        print (Request)
        showIndex(Server,Client,Request)
        Server = createServer("localhost",8080)
        print("----HTTP request: ")
        print (Request)
        Client, Request = readHTTPRequest(Server)
        if checkPass (Request) == True:
            moveToInfo(Client) #gui request truy cap info cho Server
            showInfo(Server,Client)
        else:  
            moveTo404(Client)
            show404(Server, Client)
            


