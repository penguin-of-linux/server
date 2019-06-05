#include "../../headers/client.h"
#include "../../headers/event.h"
#include "../../headers/constants.h"
#include "../../headers/checksum.h"

const int SEND_EVENT_ID = 0x30;

int min(int a, int b)
{
    if (a < b)
        return a;
    return b;
}

void handle_send_event(Event* event, unsigned char* memory)
{
    unsigned char data[MAX_DATA_LENGTH];
    int host = ((int)(event->data[0])) | ((int)(event->data[1] << 8)) | ((int)(event->data[2] << 16)) | ((int)(event->data[3] << 24));
    short port = ((short)(event->data[4])) | ((short)(event->data[5] << 8));
    short block_number = ((short)(event->data[6])) | ((short)(event->data[7] << 8));
    int offset = ((int)(event->data[8])) | ((int)(event->data[9] << 8)) | ((int)(event->data[10] << 16)) | ((int)(event->data[11] << 24));
    short length = ((short)(event->data[12])) | ((short)(event->data[13] << 8));

    struct sockaddr_in destination = create_sockaddr_in((in_addr_t)host, (uint16_t) port);

    for(int k = 0; k < length; k += MAX_DATA_LENGTH)
    {
        int local_offset = offset + k;
        short local_length = (short)min(MAX_DATA_LENGTH, length - k);

        data[0] = 0x20; // put command
        data[1] = event->data[6]; // block number
        data[2] = event->data[7];

        data[3] = (unsigned char)(local_offset & 0xFF); // offset
        data[4] = (unsigned char)(local_offset >> 8 & 0xFF);
        data[5] = (unsigned char)(local_offset >> 16 & 0xFF);
        data[6] = (unsigned char)(local_offset >> 24 & 0xFF);

        data[7] = (unsigned char)(local_length & 0xFF); // length
        data[8] = (unsigned char)(local_length >> 8 & 0xFF);

        const int data_idx = 9;
        const int memory_idx = block_number * BLOCK_SIZE + local_offset;

        for(int i = memory_idx, j = data_idx; j < data_idx + local_length; j++, i++)
        {
            data[j] = memory[i];
        }

        client_sendto((unsigned char *) &data, (size_t)local_length,
                (struct sockaddr *) &destination, sizeof(destination));
    }

    printf("Send handler. Destination address: %d, port: %d, block: %d, offset: %d, len: %d\n", host, port, block_number, offset, length);
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