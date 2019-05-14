#include "data_structures/queue.h"
#include "data_structures/btree.h"
#include "data_structures/heap.h"

#ifndef UNTITLED_CONSUMER_H
#define UNTITLED_CONSUMER_H

typedef struct ConsumerArgs
{
    StsHeader* queue;
    Node* context_btree;
    unsigned char* memory;
    Heap* context_heap;
} ConsumerArgs;

void* start_consumer(void* args);

#endif //UNTITLED_CONSUMER_H
