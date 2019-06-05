#ifndef UNTITLED_CONSTANTS_H
#define UNTITLED_CONSTANTS_H

// max upd packet len = 64K, 8 byte - udp header, 20 byte - ip header
// 1024 * 64 - 8 - 20 - 1
#define MAX_DATA_LENGTH 65507
#define BLOCK_SIZE 1024*1024 // 1 Mb

#endif //UNTITLED_CONSTANTS_H
