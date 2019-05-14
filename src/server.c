#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>

#include "../headers/client.h"
#include "../headers/data_structures/queue.h"
#include "../headers/event.h"
#include "../headers/server.h"
#include "../headers/data_structures/heap.h"

#define MAX_BUFFER_SIZE 256

void* start_server(void* args)
{
    StsHeader* queue = ((ServerArgs*)args)->queue;
    Heap* heap = ((ServerArgs*)args)->context_heap;

    unsigned char buffer[MAX_BUFFER_SIZE];
    struct sockaddr_in other_addr_port;
    socklen_t other_addr_len = sizeof(other_addr_port);

    while(1)
    {
        Context* context = BinaryHeap.peek(heap);
        int timeout;
        if (context != NULL)
            timeout = (context->time_for_expired - (unsigned int)time(0)) * 1000;
        else
            timeout = 1000;

        int res = client_recvfrom(buffer, MAX_BUFFER_SIZE, (struct sockaddr *) &other_addr_port, &other_addr_len, timeout);

        if (res == 0)
        {
            if (context != NULL)
            {
                BinaryHeap.delete(heap, context);

                Event* event = (Event*) malloc(sizeof(event));
                event->commandId = 0x40;
                event->data[0] = (unsigned char) context->block_number;
                event->data[1] = (unsigned char) context->block_number << 8;
                StsQueue.push(queue, event);
            }

            continue;
        }

        if (res == -1)
        {
            printf("Error\n");
            continue;
        }

        Event* event = (Event*) malloc(sizeof(Event));
        event->sender_addr_port = other_addr_port;
        event->commandId = buffer[0];
        for(int i = 0; i < MAX_BUFFER_SIZE - 1; i++)
            event->data[i] = buffer[i+1];
        StsQueue.push(queue, event);

        if (event->commandId == 0)
            break;
    }

    int status;
    status = client_shutdown();
    //printf("shutdown status: %d\n", status);

    return 0;
}