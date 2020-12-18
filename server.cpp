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
			if (serverSocket.Listen(1) == 0)
			{
				cout << "Khong the lang nghe.";
				serverSocket.Close();
				return 1;
			}
			else
			{
				CSocket Connector;
				if (serverSocket.Accept(Connector))
				{
					cout << "Da co Client ket Noi !!!" << endl << endl;
					//char msg[] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-length: 20\r\n\r\n<h1>Hello World</h1>";
					ifstream index("index.html", ios::out | ios::binary | ios:: ate);
					int size = index.tellg();
					char msg[100000] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lenghth: 1000\r\n\r\n";
					char* buffer = new char[size];
					index.seekg(0, ios::beg);
					index.read(buffer, size);
					index.close();
					
					strcat(msg, buffer);
					delete[]buffer;
					int length = strlen(msg);
					//Connector.Send(&length, sizeof(length), 0);
					Connector.Send(&msg, length, 0);
				}
				Connector.Close();
			}
		}
		serverSocket.Close();
	}
}
