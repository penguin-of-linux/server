#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>

#ifndef UNTITLED_CLIENT_H
#define UNTITLED_CLIENT_H

typedef struct Client {
    int sockid;
    int port;
    int status;
    struct sockaddr_in my_addr_port;
} Client;

//Client create_client(in_addr_t addr, uint16_t port);
void initialize_client(in_addr_t addr, uint16_t port);
int client_shutdown();
struct sockaddr_in create_sockaddr_in(in_addr_t addr, uint16_t port);
int client_recvfrom(unsigned char* buffer, size_t buffer_length, struct sockaddr* other_addr_port, socklen_t* other_addr_len, int timeout);
void client_sendto(unsigned char* data, size_t data_length, struct sockaddr* other_addr_port, socklen_t other_addr_len);

#endif //UNTITLED_CLIENT_H
