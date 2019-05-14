#include <malloc.h>

#import "../../headers/data_structures/heap.h"

void add(Heap* heap, Context* item);
Heap* create_heap(size_t size);
void heapify(Heap* heap, int i);
Context* pop(Heap* heap);
Context* peek(Heap* heap);
void destroy(Heap* heap);
void delete(Heap* heap, Context* item);

// private

int greater(Context* original, Context* other);

void add(Heap* heap, Context* item)
{
    pthread_mutex_lock(&heap->lock);
    int i = heap->size;
    int parent = (i - 1) / 2;
    heap->data[i] = item;
    while(parent >= 0 && i > 0)
    {
        if(heap->data[i] > heap->data[parent])
        {
            Context* temp = heap->data[i];
            heap->data[i] = heap->data[parent];
            heap->data[parent] = temp;
        }
        i = parent;
        parent = (i - 1) / 2;
    }
    heap->size++;
    heapify(heap, 0);
    pthread_mutex_unlock(&heap->lock);
}

Heap* create_heap(size_t size)
{
    Heap* heap = (Heap*) malloc(sizeof(Heap));
    pthread_mutex_init(&heap->lock, NULL);
    for (int i = 0; i < size; i++)
    {
        heap->data[i] = 0;
    }

    return heap;
}

void heapify(Heap* heap, int i)
{
    int left, right;
    Context* temp;
    left = 2 * i + 1;
    right = 2 * i + 2;

    if (left < heap->size)
    {
        if(greater(heap->data[i], heap->data[left]))
        {
            temp = heap->data[i];
            heap->data[i] = heap->data[left];
            heap->data[left] = temp;
            heapify(heap, left);
        }
    }

    if (right < heap->size)
    {
        if(greater(heap->data[i], heap->data[right]))
        {
            temp = heap->data[i];
            heap->data[i] = heap->data[right];
            heap->data[right] = temp;
            heapify(heap, right);
        }
    }
}

Context* pop(Heap* heap)
{
    pthread_mutex_lock(&heap->lock);
    Context* item = heap->data[0];
    heap->size--;
    heap->data[0] = heap->data[heap->size];
    heap->data[heap->size] = NULL;
    heapify(heap, 0);
    pthread_mutex_unlock(&heap->lock);

    return(item);
}

Context* peek(Heap* heap)
{
    return heap->data[0];
}

void delete(Heap* heap, Context* item)
{
    pthread_mutex_lock(&heap->lock);
    for(int i = 0; i < heap->size; i++)
    {
        if (heap->data[i] == item)
        {
            heap->size--;
            heap->data[i] = heap->data[heap->size];
            heap->data[heap->size] = NULL;
            heapify(heap, i);
            pthread_mutex_unlock(&heap->lock);

            return;
        }
    }
}

void destroy(Heap* heap)
{
    pthread_mutex_destroy(&heap->lock);
}

const struct _BinaryHeap BinaryHeap = {
        create_heap,
        add,
        heapify,
        pop,
        peek,
        delete,
        destroy
};


/// return 1 if original less than other
int greater(Context* original, Context* other)
{
    if (original->time_for_expired > other->time_for_expired)
    {
        return 1;
    }

    return 0;
}