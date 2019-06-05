#include <stdio.h>
#include "../../headers/event_handlers/receive_event_handler.h"
#include "../../headers/client.h"
#include "../../headers/constants.h"

const int RECEIVE_EVENT_CODE = 0x50;

void handle_receive_event(Node* context_btree, Event *event, unsigned char* memory)
{
    int block_number = ((short)(event->data[0])) | ((short)(event->data[1] << 8));
    int offset = ((int)(event->data[2])) | ((int)(event->data[3] << 8)) | ((int)(event->data[4] << 16)) | ((int)(event->data[5] << 24));

    unsigned char data[MAX_DATA_LENGTH];
    const int memory_idx = block_number * BLOCK_SIZE + offset;
    for (int i = 0; i < MAX_DATA_LENGTH; i++)
    {
        data[i] = memory[memory_idx + i];
    }

    client_sendto((unsigned char *) &data, MAX_DATA_LENGTH,
            (struct sockaddr *) &event->sender_addr_port, sizeof(event->sender_addr_port));

    printf("Block {%d} is sent\n", block_number);
}

int is_receive_event(unsigned char id)
{
    if (id == RECEIVE_EVENT_CODE)
        return 1;

    return 0;
}
