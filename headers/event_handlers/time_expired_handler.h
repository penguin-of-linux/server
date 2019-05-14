#ifndef UNTITLED_TIME_EXPIRED_HANDLER_H
#define UNTITLED_TIME_EXPIRED_HANDLER_H

#include "../event.h"
#include "../data_structures/queue.h"

void handle_time_expired_event(StsHeader* queue, Node* context_btree, Event *event);
int is_time_expired_event(unsigned char id);


#endif //UNTITLED_TIME_EXPIRED_HANDLER_H
