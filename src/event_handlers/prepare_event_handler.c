#include <stdio.h>
#include <malloc.h>
#include "../../headers/context.h"
#include "../../headers/event.h"
#include "../../headers/data_structures/btree.h"
#include "../../headers/data_structures/heap.h"

const int PREPARE_COMMAND_ID = 0x10;

Context* handle_prepare_event(Event* event, Node* context_btree, Heap* context_heap)
{
    int block_number = ((short)(event->data[0])) | ((short)(event->data[1] << 8));
    int expected_length = ((short)(event->data[2])) | ((short)(event->data[3] << 8));

    Context* context = Btree.get_or_create(context_btree, block_number);

    context->prepared = 1;
    context->expected_length = expected_length;
    context->confirm_addr_port = event->sender_addr_port;

    if(context->has_timer)
    {
        context->has_timer = 0;
        BinaryHeap.delete(context_heap, context);
    }

    printf("Prepare handler. Block number: %d, expected length: %d\n", context->block_number, context->expected_length);

    return context;
}

int is_prepare_event(unsigned char id)
{
    if(id == PREPARE_COMMAND_ID)
        return 1;

    return 0;
}
