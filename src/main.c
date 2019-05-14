#include <getopt.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#include "../headers/consumer.h"
#include "../headers/server.h"
#include "../headers/data_structures/queue.h"
#include "../headers/data_structures/btree.h"
#include "../headers/data_structures/heap.h"
#include "../headers/client.h"

const int MEMORY_SIZE = 10 * 1024 * 1024;

int main(int argc, char** argv)
{
    uint16_t port = 5100;
    int key;
    int temp;
    do
    {
        key = getopt(argc, argv, "p:");
        switch(key)
        {
            case 'p':
                sscanf(optarg, "%d", &temp);
                port = (uint16_t) temp;
                break;
            default:
                break;
        }
    } while(key != -1);


    pthread_t server_thread, consumer_thread;

    initialize_client((in_addr_t)(0x7f000001), port);

    StsHeader* queue = StsQueue.create();
    Node* btree = Btree.create_empty_node();
    Heap* heap = BinaryHeap.create_heap(128);
    unsigned char* memory = malloc(MEMORY_SIZE);

    ConsumerArgs* consumer_args = (ConsumerArgs*) malloc(sizeof(ConsumerArgs));
    consumer_args->queue = queue;
    consumer_args->context_btree = btree;
    consumer_args->memory = memory;
    consumer_args->context_heap = heap;
    pthread_create(&consumer_thread, NULL, start_consumer, (void*)consumer_args);

    ServerArgs* server_args = (ServerArgs*) malloc(sizeof(ServerArgs));
    server_args->queue = queue;
    server_args->context_heap = heap;
    pthread_create(&server_thread, NULL, start_server, (void*)server_args);

    pthread_join(server_thread, NULL);
    pthread_join(consumer_thread, NULL);

    StsQueue.destroy(queue);

    return 0;
}

