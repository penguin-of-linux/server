#ifndef UNTITLED_BTREE_H
#define UNTITLED_BTREE_H

#include "../context.h"

#define M 50

typedef struct Node {
    int is_leaf;
    int key_length;
    Context* keys[2 * M];
    struct Node* children[2 * M];
} Node;

typedef struct _Btree{
    void (* const insert)(Node* node, Context* key);
    const Node* (* const search)(const Node*, int key);
    Node* (* const create_empty_node)();
    void (* const remove)(Node* root, int key);
    Context* (* const get_or_create)(Node*, int key);
} _Btree;

extern _Btree const Btree;

#endif //UNTITLED_BTREE_H
