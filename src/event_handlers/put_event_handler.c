#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#include "../../headers/event_handlers/put_event_handler.h"
#include "../../headers/client.h"
#include "../../headers/data_structures/btree.h"
#include "../../headers/constants.h"

const int PUT_COMMAND__ID = 0x20;

Context* handle_put_event(StsHeader* queue, Node* context_btree, Event *event, Heap* context_heap, unsigned char* memory)
{
    printf("in put\n");
    short block_number = ((short)(event->data[0])) | ((short)(event->data[1] << 8));
    int offset = ((int)(event->data[2])) | ((int)(event->data[3] << 8)) | ((int)(event->data[4] << 16)) | ((int)(event->data[5] << 24));
    short length = ((short)(event->data[6])) | ((short)(event->data[7] << 8));

    Context* context = Btree.get_or_create(context_btree, block_number);

    context->block_number = block_number;
    context->received_length += length;

    const int data_idx = 8;
    const int memory_idx = block_number * BLOCK_SIZE + offset;

    for(int i = memory_idx, j = data_idx; j < data_idx + length; j++, i++)
    {
        memory[i] = event->data[j];
    }

    if(!context->prepared)
    {
        context->has_timer = 1;
        context->time_for_expired = (unsigned int) (time(0) + 10);
        BinaryHeap.add(context_heap, context);
    }

    printf("Put handler. Block number: %d, offset: %d, length: %d\n", block_number, offset, length);

    return context;
}

int is_put_command(unsigned char id)
{
    if (id == PUT_COMMAND__ID)
        return 1;

    return 0;
}