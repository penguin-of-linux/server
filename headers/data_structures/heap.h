#ifndef UNTITLED_HEAP_H
#define UNTITLED_HEAP_H

#include <pthread.h>

#include "../context.h"

typedef struct Heap {
    Context* data[128];
    int size;
    pthread_mutex_t lock;
} Heap;

typedef struct _BinaryHeap{
    Heap* (* const create_heap)(size_t size);
    void (* const add)(Heap* heap, Context* item);
    void (* const heapify)(Heap* heap, int i);
    Context* (* const pop)(Heap* heap);
    Context* (* const peek)(Heap* heap);
    void (* const delete)(Heap* heap, Context* item);
    void (* const destroy)(Heap* heap);
} _BinaryHeap;

extern _BinaryHeap const BinaryHeap;

#endif //UNTITLED_HEAP_H
