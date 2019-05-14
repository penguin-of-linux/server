#include <stdio.h>
#include <stdlib.h>

#include "../headers/consumer.h"
#include "../headers/event_handlers/confirm_handler.h"
#include "../headers/event_handlers/prepare_event_handler.h"
#include "../headers/event_handlers/put_event_handler.h"
#include "../headers/event_handlers/send_event_handler.h"
#include "../headers/event_handlers/time_expired_handler.h"
#include "../headers/event_handlers/receive_event_handler.h"
#include "../headers/data_structures/queue.h"

void handle_event(StsHeader* queue, Event* event, Node* context_btree, Heap* context_heap, void* memory)
{
    Context* context = NULL;
    if(is_put_command(event->commandId))
    {
        context = handle_put_event(queue, context_btree, event, context_heap, memory);
    }

    if(is_prepare_event(event->commandId))
    {
        context = handle_prepare_event(event, context_btree, context_heap);
    }

    if(is_send_event(event->commandId))
    {
        handle_send_event(event);
    }

    if(is_receive_event(event->commandId))
    {
        handle_receive_event(context_btree, event, memory);
    }

    if(is_time_expired_event(event->commandId))
    {
        handle_time_expired_event(queue, context_btree, event);
    }

    if(context != NULL && need_confirm(context))
    {
        confirm(context);
    }
}

void* start_consumer(void* args)
{
    StsHeader* queue = ((ConsumerArgs*)args)->queue;
    Node* context_btree = ((ConsumerArgs*)args)->context_btree;
    unsigned char* memory = ((ConsumerArgs*)args)->memory;
    Heap* heap = ((ConsumerArgs*)args)->context_heap;

    int commandId = -1;
    do
    {
        if(StsQueue.empty(queue) == 0)
        {
            Event* event = (Event*) StsQueue.pop(queue);
            commandId = event->commandId;
            handle_event(queue, event, context_btree, heap, memory);
            free(event);
        }
    } while(commandId != 0);

    return 0;
}