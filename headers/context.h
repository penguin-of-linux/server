#ifndef UNTITLED_CONTEXT_H
#define UNTITLED_CONTEXT_H

#include <netinet/in.h>

typedef struct Context
{
    short prepared;
    int expected_length;
    short received_length;
    int block_number;
    struct sockaddr_in confirm_addr_port;
    short confirmed;
    short has_timer;
    unsigned int time_for_expired;
} Context;

#endif //UNTITLED_CONTEXT_H
