#define _AFXDLL
#define _CRT_SECURE_NO_WARNINGS 
#include <iostream>
#include <fstream>
#include <afxsock.h>
using namespace std;

void SendIndex()
{

}
int main(int argc, char *argv[])
{
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
		CSocket serverSocket;
		//Tao socket lang nghe
		if (serverSocket.Create(8080, SOCK_STREAM, NULL) == 0)
		{
			cout << "Tao socket that bai" << endl;
			cout << serverSocket.GetLastError();
			return 1;
		}
		else
		{
			cout << "Thanh cong tao socket" << endl;
			//Lang nghe
			if (serverSocket.Listen(5) == 0)
			{
				cout << "Khong the lang nghe.";
				serverSocket.Close();
				return 1;
			}
			else
			{
				CSocket Connector, con2;
				if (serverSocket.Accept(Connector))
				{
					cout << "Da co Client ket Noi !!!" << endl << endl;
					char msgrcv[100000];
					Connector.Receive(&msgrcv, 100000, 0);
					//cout << msgrcv;
					if (strstr(msgrcv, "GET /index.html HTTP/1.1") != NULL)
					{
						//cout << msgrcv << endl;
						//char msg[] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-length: 20\r\n\r\n<h1>Hello World</h1>";
						ifstream index("index.html", ios::out | ios::binary | ios::ate);
						int size = index.tellg();
						char msg[100000] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: 1000\r\n\r\n";
						char* buffer = new char[size];
						index.seekg(0, ios::beg);
						index.read(buffer, size);
						int length = strlen(msg);
						strcat(msg, buffer);
						//Connector.Send(&length, sizeof(length), 0);
						Connector.Send(&msg, length + size, 0);
						index.close();
						//cout << msg;
						delete[]buffer;
						//.Receive(&msgrcv, 100000, 0);
						//cout << msgrcv;

					}
					Connector.Close();
					serverSocket.Close();
					CSocket serverSocket1,serverSocket2,con3;
					if (serverSocket1.Create(8080, SOCK_STREAM, NULL) == 0)
					{
						cout << "Tao socket that bai" << endl;
						cout << serverSocket1.GetLastError();
						return 1;
					}
					else
					{
						cout << "Thanh cong tao socket" << endl;
						//Lang nghe
						if (serverSocket1.Listen(5) == 0)
						{
							cout << "Khong the lang nghe.";
							serverSocket1.Close();
							return 1;
						}
						if (serverSocket1.Accept(con2))
						{
							cout << "Da co Client ket Noi !!!" << endl << endl;
							//con2.Receive(&msgrcv, 100000, 0);
							con2.Receive(&msgrcv, 100000, 0);
							if (strstr(msgrcv, "Username=admin&Password=admin") != NULL)
							{
								char msgs2[] = "HTTP/1.1 301 Moved Permanently\r\nLocation: http://127.0.0.1:8080/info.html\r\n\r\n";
								con2.Send(&msgs2, strlen(msgs2), 0);
								con2.Receive(&msgrcv, 100000, 0);
								ifstream info("info.html", ios::out | ios::binary | ios::ate);
								int size = info.tellg();
								char msgs3[10000] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: 10000\r\n\r\n";
								int length = strlen(msgs3);
								char* buff = new char[size];
								info.seekg(0, ios::beg);
								info.read(buff, size);
								strcat(msgs3, buff);
								con2.Send(&msgs3, length + size, 0);
								info.close();
								delete[]buff;
								//cout << msgrcv;
							}
							con2.Close();
							serverSocket1.Close();
						}
					}
					
				}
				

			}
		}
	}
}
