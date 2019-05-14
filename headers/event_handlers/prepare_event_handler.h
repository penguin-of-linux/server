#include "../context.h"
#include "../event.h"

#ifndef UNTITLED_PREPARE_EVENT_HANDLER_H
#define UNTITLED_PREPARE_EVENT_HANDLER_H

Context* handle_prepare_event(Event* event, Node* context_btree, Heap* context_heap);
int is_prepare_event(unsigned char id);

#endif //UNTITLED_PREPARE_EVENT_HANDLER_H
