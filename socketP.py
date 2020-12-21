import socket

def createServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Tao socket server
    if server==0 :
        print("Tao socket that bai\n")
        return server, 1
    server.bind(("localhost",80)) 
    if server.listen(5)==0:
        print("Khong the lang nghe\n")
        server.close()
        return server, 1
    return server, 0

def printRequest(request):
    print("-------------HTTP request:\n")
    if "GET / HTTP/1.1" in request:
        print("GET / HTTP/1.1")
    if "GET /index.html HTTP/1.1" in request:
        print("GET /index.html HTTP/1.1")
    if "GET /info.html HTTP/1.1" in request:
        print("GET /info.html HTTP/1.1")
    if "GET /404.html HTTP/1.1" in request:
        print("GET /404.html HTTP/1.1")
    if "GET /lam.jpg HTTP/1.1" in request:
        print("GET /lam.jpg HTTP/1.1")
    if "GET /han.jpg HTTP/1.1" in request:
        print("GET /han.jpg HTTP/1.1")

def printRespone(respone):
    print("-------------HTTP respone:\n")
    if "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html" in respone:
        print("HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html")
    if "HTTP/1.1 200 OK" in respone:
        print("HTTP/1.1 200 OK")
    if "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html" in respone:
        print("HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html")
    if "HTTP/1.1 404 Not Found" in respone:
        print("HTTP/1.1 404 Not Found")
    if "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html" in respone:
        print("HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html")

def sendMoveIndex(server,connector):
    respone= "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html"
    printRespone(respone)
    size=len(respone)
    connector.send(bytes(respone,"utf-8"))
    connector.close()
    server.close()

def sendIndex(server,connector):
    index = open ("index.html", "rb")
    buffer=index.read()
    respone="HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"%len(buffer)
    printRespone(respone)
    respone+=buffer.decode()    
    connector.send(bytes(respone,"utf-8"))
    index.close()
    connector.close()
    server.close()

def sendMove404(server,connector):
    respone="HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html"
    printRespone(respone)
    size=len(respone)
    connector.send(bytes(respone,"utf-8"))
    connector.close()
    server.close()

def send404(server,connector):
    index = open ("404.html", "rb")
    buffer=index.read()
    respone="HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"%len(buffer)
    printRespone(respone)
    respone+=buffer.decode()    
    connector.send(bytes(respone,"utf-8"))
    index.close()
    connector.close()
    server.close()

def sendMoveFiles(server,connector):
    respone="HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/files.html"
    printRespone(respone)
    size=len(respone)
    connector.send(bytes(respone,"utf-8"))
    connector.close()
    server.close()

def sendFiles(server,connector):
    index = open ("files.html", "rb")
    buffer=index.read()
    respone="""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printRespone(respone)
    respone+=buffer.decode()    
    connector.send(bytes(respone,"utf-8"))
    index.close()
    connector.close()
    server.close()

def sendMoveInfo(server,connector):
    respone= "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html"
    printRespone(respone)
    size=len(respone)
    connector.send(bytes(respone,"utf-8"))
    connector.close()
    server.close()


def sendInfo(server,connector):
    index = open ("info.html", "rb")
    buffer=index.read()
    respone="""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printRespone(respone)
    respone+=buffer.decode()    
    connector.send(bytes(respone,"utf-8"))
    index.close()
    connector.close()
    server.close()
    server, r = createServer()
    if r==1:
        return 1
    connector, address = server.accept()
    if(connector):
        request = connector.recv(1024).decode()
        if "GET /lam.jpg HTTP/1.1" in request:
            printRequest(request)
            sendImg(server,connector,"lam.jpg")
        else:
            printRequest(request)
            sendImg(server,connector,"han.jpg")
    connector, address = server.accept()
    if(connector):
        request = connector.recv(1024).decode()
        if "GET /han.jpg HTTP/1.1" in request:
            printRequest(request)
            sendImg(server,connector,"han.jpg")
        else:
            printRequest(request)
            sendImg(server,connector,"lam.jpg")    
    connector.close()
    server.close()

def sendImg(server,connector,img):
    index = open (img, "rb")
    buffer=index.read()
    respone="""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printRespone(respone)
    respone =bytes(respone,"utf-8") +buffer
    connector.send(respone)
    index.close()


def main():
    server, r = createServer()
    print("Server: \n")
    print("IP: localhost\n")
    print("Port: 80\n")
    print("Waiting for Client.\n")
    print("Please enter 'localhost' or 'localhost/index.html' into browser to connect to the server.\n")
    connector, address = server.accept()
    if connector:
        #print("ye")
        request = connector.recv(1024).decode()
        printRequest(request)
        while "GET / HTTP/1.1" not in request and  "GET /index.html HTTP/1.1" not in request:
            print("Wrong addess, try again \n")
            server.close()
            connector.close()
            server, r = createServer()
            if r==1:
                return 1
            connector, address = server.accept()
            if(connector):
                request = connector.recv(1024).decode()
        if "GET / HTTP/1.1" in request:
            printRequest(request)
            sendMoveIndex(server,connector)
            server, r = createServer()
            if r==1:
                return 1
            connector, address = server.accept()
            if(connector):
                while "GET /index.html HTTP/1.1" not in request:
                    request = connector.recv(1024).decode()
                printRequest(request)
                sendIndex(server,connector)
        else:
            printRequest(request)
            sendIndex(server,connector)
        server, r = createServer()
        if r==1:
            return 1
        connector, address = server.accept()
        if(connector):
            request = connector.recv(1024).decode()
            printRequest(request)
        if "POST" in request and  "username=admin&password=admin" in request:
            sendMoveInfo(server,connector)
            server, r = createServer()
            if r==1:
                return 1
            connector, address = server.accept()
            if(connector):
                while "GET /info.html HTTP/1.1" not in request:
                    request = connector.recv(1024).decode()
                printRequest(request)
                sendInfo(server,connector)
            server, r = createServer()
            if r==1:
                return 1
            connector, address = server.accept()
            if(connector):
                request = connector.recv(1024).decode()
                if "GET /index.html HTTP/1.1" in request:
                    printRequest(request)
                    sendIndex(server,connector)
                else:
                   if "GET /files.html HTTP/1.1" in request:
                        printRequest(request)
                        sendFiles(server,connector)

        else:
            if "POST" not in request or  "username=admin&password=admin" not in request:
                sendMove404(server,connector)
                server, r = createServer()
                if r==1:
                    return 1
                connector, address = server.accept()
                if(connector):
                    while "GET /404.html HTTP/1.1" not in request:
                        request = connector.recv(1024).decode()
                    printRequest(request)
                    send404(server,connector)


if __name__ == "__main__":
    main()
