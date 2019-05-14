#ifndef UNTITLED_RECEIVE_EVENT_HANDLER_H
#define UNTITLED_RECEIVE_EVENT_HANDLER_H

#include "../data_structures/btree.h"
#include "../event.h"

void handle_receive_event(Node* context_btree, Event *event, unsigned char* memory);
int is_receive_event(unsigned char id);

#endif //UNTITLED_RECEIVE_EVENT_HANDLER_H
