cmake_minimum_required(VERSION 3.13)
project(untitled C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pthread")

add_executable(untitled src/main.c src/server.c headers/server.h src/data_structures/queue.c headers/data_structures/queue.h headers/consumer.h src/consumer.c headers/event.h headers/event_handlers/put_event_handler.h src/event_handlers/put_event_handler.c src/dictionary.c headers/dictionary.h headers/client.h src/client.c headers/context.h headers/event_handlers/prepare_event_handler.h src/event_handlers/prepare_event_handler.c headers/event_handlers/confirm_handler.h src/event_handlers/confirm_handler.c headers/event_handlers/send_event_handler.h src/event_handlers/send_event_handler.c headers/event_handlers/time_expired_handler.h src/event_handlers/time_expired_handler.c headers/data_structures/btree.h src/data_structures/btree.c headers/data_structures/heap.h src/data_structures/heap.c headers/event_handlers/receive_event_handler.h src/event_handlers/receiver_event_handler.c headers/constants.h)