#ifndef UNTITLED_EVENT_H
#define UNTITLED_EVENT_H

#include <netinet/in.h>

typedef struct Event {
    unsigned char commandId;
    unsigned char data[255]; //max buffer size - 1
    struct sockaddr_in sender_addr_port;
} Event;

#endif //UNTITLED_EVENT_H
