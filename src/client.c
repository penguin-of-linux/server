#include <poll.h>

#include "../headers/client.h"

static Client* client = NULL;

Client* create_client(in_addr_t addr, uint16_t port)
{
    int sockid = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    struct sockaddr_in my_addr_port = create_sockaddr_in(addr, port);
    int status = bind(sockid, (struct sockaddr *) &my_addr_port, sizeof(my_addr_port));

    Client* client = (Client*) malloc(sizeof(Client));
    client->sockid = sockid;
    client->status = status;
    client->my_addr_port = my_addr_port;

    return client;
}

int client_shutdown()
{
    return shutdown(client->sockid, 2);
}

struct sockaddr_in create_sockaddr_in(in_addr_t addr, uint16_t port)
{
    struct sockaddr_in result;

    result.sin_family = AF_INET;
    result.sin_port = htons(port);
    result.sin_addr.s_addr = htonl(addr);

    return result;
}

void initialize_client(in_addr_t addr, uint16_t port)
{
    if(client == NULL)
    {
        in_addr_t localhost = addr;
        client = create_client(localhost, port);
        printf("Started with %d post\n", htons((int)client->my_addr_port.sin_port));
    }
}

int client_recvfrom(unsigned char* buffer, size_t buffer_length, struct sockaddr* other_addr_port,
        socklen_t* other_addr_len, int timeout)
{
    struct pollfd fds[1];
    fds[0].fd = client->sockid;
    fds[0].events = POLLIN;

    int res = poll(&fds, 1, timeout);
    if (res == -1)
    {
        printf("Error during recv\n");
    }
    else if (res == 0)
    {
        printf("Timeout during recv {%d ms}\n", timeout);
    }
    else
    {
        if (fds[0].revents & POLLIN )
            fds[0].revents = 0;

        recvfrom(client->sockid, buffer, buffer_length, 0, other_addr_port, other_addr_len);
    }

    return res;
}

void client_sendto(unsigned char* data, size_t data_length, struct sockaddr* other_addr_port, socklen_t other_addr_len)
{
    ssize_t res = sendto(client->sockid, data, data_length, 0, other_addr_port, other_addr_len);
    //printf("Client send status %d\n", res);
}