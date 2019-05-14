#include <stdio.h>

#include "../../headers/context.h"
#include "../../headers/client.h"

void confirm(Context* context)
{
    printf("Confirm\n");

    context->confirmed = 1;

    unsigned char data[1] = {200};
    client_sendto((unsigned char *) &data, 1, (struct sockaddr *) &context->confirm_addr_port, sizeof(context->confirm_addr_port));
}

int need_confirm(Context* context)
{
    if(!context->confirmed && context->prepared && context->expected_length == context->received_length)
        return 1;

    return 0;
}