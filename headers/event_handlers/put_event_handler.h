#include "../context.h"
#include "../event.h"
#include "../data_structures/queue.h"
#include "../data_structures/btree.h"
#include "../data_structures/heap.h"

#ifndef UNTITLED_PUT_EVENT_HANDLER_H
#define UNTITLED_PUT_EVENT_HANDLER_H

Context* handle_put_event(StsHeader* queue, Node* context_btree, Event *event, Heap* context_heap, unsigned char* memory);
int is_put_command(unsigned char id);

#endif //UNTITLED_PUT_EVENT_HANDLER_H
