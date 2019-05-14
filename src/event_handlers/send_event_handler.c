#include "../../headers/client.h"
#include "../../headers/event.h"

const int SEND_EVENT_ID = 0x30;

void handle_send_event(Event* event)
{
    //data = get_data()
    unsigned char data[7];
    int host = ((int)(event->data[0])) | ((int)(event->data[1] << 8)) | ((int)(event->data[2] << 16)) | ((int)(event->data[3] << 24));
    short port = ((short)(event->data[4])) | ((short)(event->data[5] << 8));
    data[0] = 0x20; // put command
    data[1] = event->data[6]; // block number
    data[2] = event->data[7];
    data[3] = event->data[8]; // offset
    data[4] = event->data[9];
    data[5] = event->data[10]; // length
    data[6] = event->data[11];

    struct sockaddr_in destination = create_sockaddr_in((in_addr_t)host, (uint16_t) port);

    client_sendto((unsigned char *) &data, 7, (struct sockaddr *) &destination, sizeof(destination));

    printf("Send handler. Destination address: %d, port: %d\n", host, port);
}

int is_send_event(unsigned char id)
{
    if(id == SEND_EVENT_ID)
        return 1;

    return 0;
}

/*# второй таймер и третий
# poll, выбрать все таймеры тикнувшые и найти контексты, которые не подтверждены
# 1 пакет - 1кб
# 1 block - 1 mb
 пропусктная спообность, вероятность ошибок, задержки в еденицах, загрузка канала, случайные ноды и размеры*/