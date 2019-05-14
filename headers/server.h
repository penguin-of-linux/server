#include "data_structures/queue.h"
#include "data_structures/heap.h"

#ifndef UNTITLED_SERVER_H
#define UNTITLED_SERVER_H

typedef struct ServerArgs
{
    StsHeader* queue;
    Heap* context_heap;
} ServerArgs;

void* start_server(void* queue);
#endif //UNTITLED_SERVER_H
