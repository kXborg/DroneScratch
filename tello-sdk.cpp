#include <iostream>
#include <thread>
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")
using namespace std;

void recv(SOCKET sock) 
{
    char buffer[1518];
    int count = 0;
    while (true) 
    {
        try 
            {
                sockaddr_in server;
                int server_len = sizeof(server);
                int recv_len = recvfrom(sock, buffer, sizeof(buffer), 0, (sockaddr*)&server, &server_len);
                if (recv_len > 0) {
                    buffer[recv_len] = '\0';
                    cout << buffer << endl;
            }
        }
        catch (...) 
        {
            cerr << "\nExit . . .\n";
            break;
        }
    }
}

int main() 
{
    WSADATA wsaData;
    int iResult = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (iResult != 0) 
    {
        cerr << "WSAStartup failed: " << iResult << endl;
        return 1;
    }

    // Create a UDP socket
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET) 
    {
        cerr << "socket creation failed: " << WSAGetLastError() << endl;
        return 1;
    }

    // Bind the socket to a local address
    sockaddr_in locaddr;
    locaddr.sin_family = AF_INET;
    locaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    locaddr.sin_port = htons(9000);

    if (bind(sock, (sockaddr*)&locaddr, sizeof(locaddr)) == SOCKET_ERROR) 
    {
        cerr << "bind failed: " << WSAGetLastError() << endl;
        closesocket(sock);
        return 1;
    }

    sockaddr_in tello_address;
    tello_address.sin_family = AF_INET;
    tello_address.sin_addr.s_addr = inet_addr("192.168.10.1");
    tello_address.sin_port = htons(8889);

    cout << "\r\n\r\nTello C++ Demo.\r\n" << endl;
    cout << "Tello: command takeoff land flip forward back left right" << endl;
    cout << "       up down cw ccw speed speed?" << endl;
    cout << "end -- quit demo.\r\n" << endl;

    // Create a thread to receive data from the socket
    thread recvThread(recv, sock);

    while (true) {
        try {
            string msg;
            getline(cin, msg);

            if (msg.empty()) 
            {
                break;
            }

            if (msg == "end") 
            {
                cout << "..." << endl;
                closesocket(sock);
                break;
            }

            // Send data
            int sent = sendto(sock, msg.c_str(), msg.length(), 0, (sockaddr*)&tello_address, sizeof(tello_address));
            if (sent == SOCKET_ERROR) 
            {
                cerr << "sendto failed: " << WSAGetLastError() << endl;
                closesocket(sock);
                break;
            }
        }
        catch (...) 
        {
            cerr << "\n . . .\n";
            closesocket(sock);
            break;
        }
    }

    recvThread.join();
    WSACleanup();

}