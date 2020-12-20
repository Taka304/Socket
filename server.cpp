#define _AFXDLL
#define _CRT_SECURE_NO_WARNINGS 
#include <iostream>
#include <fstream>
#include <afxsock.h>
using namespace std;

int createServer(CSocket &server, CSocket &connector)
{
	//Tao socket lang nghe
	if (server.Create(80, SOCK_STREAM, NULL) == 0)
	{
		cout << "Tao socket that bai" << endl;
		cout << server.GetLastError();
		return 1;
	}
	//cout << "Thanh cong tao socket" << endl;
	//Lang nghe
	if (server.Listen(5) == 0)
	{
		cout << "Khong the lang nghe.";
		server.Close();
		return 1;
	}
	return 0;
}
void printRequest(char request[])
{
	cout << "-------------HTTP request:" << endl;
	if (strstr(request, "GET / HTTP/1.1") != NULL)
	{
		cout << "GET / HTTP/1.1" << endl;
	}
	if (strstr(request, "GET /index.html HTTP/1.1") != NULL)
	{
		cout << "GET / index.html HTTP/1.1" << endl;
	}
	if (strstr(request, "POST / HTTP/1.1") != NULL)
	{
		cout << "POST / HTTP/1.1" << endl;
	}
	if (strstr(request, "GET /info.html HTTP/1.1") != NULL)
	{
		cout << "GET /info.html HTTP/1.1" << endl;
	}
	if (strstr(request, "GET /404.html HTTP/1.1") != NULL)
	{
		cout << "GET /404.html HTTP/1.1" << endl;
	}
}
void printResponse(char response[])
{
	cout << "-------------HTTP reponse:" << endl;
	if (strstr(response, "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html") != NULL)
	{
		cout << "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html" << endl;
	}
	if (strstr(response,"HTTP/1.1 200 OK") != NULL)
	{
		cout << "HTTP/1.1 200 OK" << endl;
	}
	if (strstr(response, "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html") != NULL)
	{
		cout << "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html" << endl;
	}
	if (strstr(response, "HTTP/1.1 404 Not Found") != NULL)
	{
		cout << "HTTP/1.1 404 Not Found" << endl;
	}
	if (strstr(response, "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html") != NULL)
	{
		cout << "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html" << endl;
	}
}
void sendMoveIndex(CSocket& server, CSocket& connector)
{
	char response[] = "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/index.html";
	printResponse(response);
	int sizem = strlen(response);
	connector.Send(&response, sizem, 0);
	connector.Close();
	server.Close();
}
void sendIndex(CSocket& server, CSocket& connector)
{
	ifstream index("index.html", ios::out | ios::binary | ios::ate);
	streampos size = index.tellg();
	char response[100000] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: 1000\r\n\r\n";
	printResponse(response);
	char* buffer = new char[size];
	index.seekg(0, ios::beg);
	index.read(buffer, size);
	int length = strlen(response);
	strcat(response, buffer);
	connector.Send(&response, length + size, 0);
	index.close();
	delete[]buffer;
	connector.Close();
	server.Close();
}
void sendMove404(CSocket &server, CSocket &connector)
{
	char response[] = "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/404.html";
	printResponse(response);
	int sizem = strlen(response);
	connector.Send(&response, sizem, 0);
	connector.Close();
	server.Close();
}
void send404(CSocket &server, CSocket &connector)
{
	ifstream file404("404.html", ios::out | ios::binary | ios::ate);
	streampos size = file404.tellg();
	char response[10000] = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Lenghth: 10000\r\n\r\n";
	printResponse(response);
	int length = strlen(response);
	char* buff = new char[size];
	file404.seekg(0, ios::beg);
	file404.read(buff, size);
	strcat(response, buff);
	connector.Send(&response, length + size, 0);
	file404.close();
	delete[]buff;
	//cout << msgrcv;
	connector.Close();
	server.Close();
}
void sendMoveInfo(CSocket& server, CSocket& connector)
{
	char response[] = "HTTP/1.1 301 Moved Permanently\r\nLocation: http://localhost:80/info.html";
	printResponse(response);
	int sizem = strlen(response);
	connector.Send(&response, sizem, 0);
	connector.Close();
	server.Close();
}
void sendInfo(CSocket& server, CSocket& connector)
{
	ifstream info("info.html", ios::out | ios::binary | ios::ate);
	streampos size = info.tellg();
	char response[10000] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: 10000\r\n\r\n";
	printResponse(response);
	int length = strlen(response);
	char* buff = new char[size];
	info.seekg(0, ios::beg);
	info.read(buff, size);
	strcat(response, buff);
	connector.Send(&response, length + size, 0);
	info.close();
	delete[]buff;
	//cout << msgrcv;
	connector.Close();
	server.Close();
}
int main(int argc, char *argv[])
{
	int r;
	//Khoi tao MFC
	if (!AfxWinInit(::GetModuleHandle(NULL), NULL, ::GetCommandLine(), 0))
	{
		cout << "MFC failed to initialize!";
		return 1;
	}
	else
	{
		//Khoi tao thu vien socket
		if (!AfxSocketInit())
		{
			cout << "Khong the khoi tao thu vien socket";
			return 1;
		}
		CSocket server, Connector;
		r = createServer(server, Connector);
		if (r == 1)
		{
			return 1;
		}
		cout << "Server:" << endl;
		cout << "IP: localhost" << endl;
		cout << "Port: 80" << endl;
		cout << "Waiting for client." << endl;
		cout << "Please enter 'localhost' or 'localhost/index.html' into browser to connect to the server." << endl << endl;
		if (server.Accept(Connector))
		{				
			//cout << "Da co Client ket Noi !!!" << endl << endl;
			char request[10000];
			Connector.Receive(&request, 10000, 0);
			while (strstr(request, "GET / HTTP/1.1") == NULL && strstr(request, "GET /index.html HTTP/1.1") == NULL)
			{
				cout << "Wrong address, please enter again." << endl;
				server.Close();
				Connector.Close();
				r = createServer(server, Connector);
				if (r == 1)
				{
					return 1;
				}
				if (server.Accept(Connector))
				{
					Connector.Receive(&request, 10000, 0);
				}
			}
			if (strstr(request, "GET / HTTP/1.1") != NULL)
			{
				printRequest(request);
				sendMoveIndex(server, Connector);
				//CSocket server, con;
				r = createServer(server, Connector);
				if (r == 1)
				{
					return 1;
				}
				if (server.Accept(Connector))
				{
					//cout << "Da co Client ket Noi !!!" << endl << endl;
					while (strstr(request, "GET /index.html HTTP/1.1") == NULL)
					{
						Connector.Receive(&request, 100000, 0);
					}
					printRequest(request);
					sendIndex(server, Connector);
				}
			}
			else
			{
				printRequest(request);
				sendIndex(server, Connector);
			}
			//CSocket serverSocket1, serverSocket2, con3;
			r = createServer(server, Connector);
			if (r == 1)
			{
				return 1;
			}
			if (server.Accept(Connector))
			{
				//cout << "Da co Client ket Noi !!!" << endl << endl;
				Connector.Receive(&request, 100000, 0);
				printRequest(request);
				if (strstr(request,"POST") != NULL && strstr(request, "username=admin&password=admin") != NULL)
				{
					sendMoveInfo(server, Connector);
					r = createServer(server, Connector);
					if (r == 1)
					{
						return 1;
					}
					if (server.Accept(Connector))
					{
						//cout << "Da co Client ket Noi !!!" << endl << endl;
						while (strstr(request, "GET /info.html HTTP/1.1") == NULL)
						{
							Connector.Receive(&request, 100000, 0);
						}
						printRequest(request);
						sendInfo(server, Connector);
					}
					else if (strstr(request,"POST") != NULL)
					{
						sendMove404(server, Connector);
						r = createServer(server, Connector);
						if (r == 1)
						{
							return 1;
						}
						if (server.Accept(Connector))
						{
							//cout << "Da co Client ket Noi !!!" << endl << endl;
							while (strstr(request, "GET /404.html HTTP/1.1") == NULL)
							{
								Connector.Receive(&request, 100000, 0);
							}
							printRequest(request);
							send404(server, Connector);
						}
					}
				}
			}					
		}				
	}
	system("pause");
}
