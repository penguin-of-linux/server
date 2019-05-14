#include <stdio.h>
#include "../../headers/data_structures/queue.h"
#include "../../headers/context.h"
#include "../../headers/event.h"
#include "../../headers/data_structures/btree.h"

const int TIME_EXPIRED_EVENT_CODE = 0x40;

void handle_time_expired_event(StsHeader* queue, Node* context_btree, Event *event)
{
    int block_number = ((short)(event->data[0])) | ((short)(event->data[1] << 8));
    Btree.remove(context_btree, block_number);

    printf("Context {%d} removed (time expired)\n", block_number);
}

int is_time_expired_event(unsigned char id)
{
    if (id == TIME_EXPIRED_EVENT_CODE)
        return 1;

    return 0;
}