#include <stdio.h>
#include "../../headers/event_handlers/receive_event_handler.h"
#include "../../headers/client.h"
#include "../../headers/constants.h"

const int RECEIVE_EVENT_CODE = 0x50;

void handle_receive_event(Node* context_btree, Event *event, unsigned char* memory)
{
    int block_number = ((short)(event->data[0])) | ((short)(event->data[1] << 8));

    unsigned char data[BLOCK_SIZE];
    const int memory_idx = block_number * BLOCK_SIZE;
    for (int i = 0; i < BLOCK_SIZE; i++)
    {
        data[i] = memory[memory_idx + i];
    }

    client_sendto((unsigned char *) &data, BLOCK_SIZE,
            (struct sockaddr *) &event->sender_addr_port, sizeof(event->sender_addr_port));

    printf("Block {%d} is sent\n", block_number);
}

int is_receive_event(unsigned char id)
{
    if (id == RECEIVE_EVENT_CODE)
        return 1;

    return 0;
}
