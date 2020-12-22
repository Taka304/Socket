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
    print("-------------HTTP request:")
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
    if "POST / HTTP/1.1" in request:
        print("POST / HTTP/1.1")
    if "GET /download/han.jpg HTTP/1.1" in request:
        print("GET /download/han.jpg HTTP/1.1")

def printResponse(response):
    print("-------------HTTP response:")
    if "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html" in response:
        print("HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html")
    if "HTTP/1.1 200 OK" in response:
        print("HTTP/1.1 200 OK")
    if "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html" in response:
        print("HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html")
    if "HTTP/1.1 404 Not Found" in response:
        print("HTTP/1.1 404 Not Found")
    if "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html" in response:
        print("HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html")

def sendMoveIndex(server,connector):
    response= "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html"
    printResponse(response)
    size=len(response)
    connector.send(bytes(response,"utf-8"))
    connector.close()
    server.close()

def sendIndex(server,connector):
    index = open ("index.html", "rb")
    buffer=index.read()
    response="HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"%len(buffer)
    printResponse(response)
    response+=buffer.decode()    
    connector.send(bytes(response,"utf-8"))
    index.close()
    connector.close()
    server.close()

def sendMove404(server,connector):
    response="HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html"
    printResponse(response)
    size=len(response)
    connector.send(bytes(response,"utf-8"))
    connector.close()
    server.close()

def send404(server,connector):
    index = open ("404.html", "rb")
    buffer=index.read()
    response="HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"%len(buffer)
    printResponse(response)
    response+=buffer.decode()    
    connector.send(bytes(response,"utf-8"))
    index.close()
    connector.close()
    server.close()

def sendMoveFiles(server,connector):
    response="HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/files.html"
    printResponse(response)
    size=len(response)
    connector.send(bytes(response,"utf-8"))
    connector.close()
    server.close()

def sendFiles(server,connector):
    index = open ("files.html", "rb")
    buffer=index.read()
    response="""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printResponse(response)
    response+=buffer.decode()    
    connector.send(bytes(response,"utf-8"))
    index.close()
    connector.close()
    server.close()


def sendMoveInfo(server,connector):
    response= "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html"
    printResponse(response)
    size=len(response)
    connector.send(bytes(response,"utf-8"))
    connector.close()
    server.close()

def sendInfo(server,connector):
    index = open ("info.html", "rb")
    buffer=index.read()
    response="""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printResponse(response)
    response+=buffer.decode()    
    connector.send(bytes(response,"utf-8"))
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
    response="""HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printResponse(response)
    response =bytes(response,"utf-8") +buffer
    connector.send(response)
    index.close()

def sendFaviconIcon(server, connector):
    index = open("favicon.ico", "rb")
    buffer=index.read()
    response="""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: %d\r\n\r\n"""%len(buffer)
    printResponse(response)
    response+=buffer.decode()    
    connector.send(bytes(response,"utf-8"))
    index.close()
    connector.close()
    server.close()

def MenuDownload(server, connector, request):
    if "GET /download/han.jpg HTTP/1.1" in request:
        file = open("download/han.jpg","rb")
        response="HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nTransfer-Encoding: chunked\r\n\r\n"
    if "GET /download/lam.jpg HTTP/1.1" in request:
        file = open("download/lam.jpg","rb")
        response="HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nTransfer-Encoding: chunked\r\n\r\n"
    if "GET /download/text.pdf HTTP/1.1" in request:
        file = open("download/text.pdf","rb")
        response="HTTP/1.1 200 OK\r\nContent-Type: application/pdf\r\nTransfer-Encoding: chunked\r\n\r\n"
    if "GET /download/video.mp4 HTTP/1.1" in request:
        file = open("download/video.mp4","rb")
        response="HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nTransfer-Encoding: chunked\r\n\r\n"
    if "GET /download/sound.mp3 HTTP/1.1" in request:
        file = open("download/sound.mp3","rb")
        response="HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nTransfer-Encoding: chunked\r\n\r\n"
    printResponse(response)
    response=response.encode()
    CHUNK_SIZE=1000
    while True:
        chunk=file.read(CHUNK_SIZE)
        size=len(chunk)
        if not chunk:
            break
        response +=hex(size)[2:].encode()+"\r\n".encode()+chunk+"\r\n".encode()
    response+="0\r\n\r\n".encode()
    connector.send(response)
    file.close()

def main():
    server, r = createServer()
    print("Server:")
    print("IP: localhost")
    print("Port: 80")
    print("Waiting for Client.")
    print("Please enter 'localhost' or 'localhost/index.html' into browser to connect to the server.\n")
    connector, address = server.accept()
    if connector:
        request = connector.recv(1024).decode()
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
                elif "GET /files.html HTTP/1.1" in request:
                    printRequest(request)                            
                    sendFiles(server,connector)
                    server, r = createServer()
                    if r==1:
                        return 1
                    connector, address = server.accept()
                    if(connector):
                        request = connector.recv(1024).decode()
                        while not "GET /index.html HTTP/1.1" in request:                      
                            MenuDownload(server,connector,request)
                            request = connector.recv(1024).decode()
                        connector.close()
                        server.close()
                        server, r = createServer()
                        if r==1:
                            return 1
                        connector, address = server.accept()
                        if(connector):
                            request = connector.recv(1024).decode()
                        sendIndex(server,connector)

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
