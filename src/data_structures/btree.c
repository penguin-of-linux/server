#include <stdlib.h>
#include "../../headers/data_structures/btree.h"
#include "../../headers/context.h"

// public
void insert(Node* root, Context* key);
const Node* search(const Node* node, int key);
Node* create_empty_node();
void remove(Node* root, int key);
Context* get_or_create(Node* root, int key);

// private
void divide_node(Node* node, Node* left, Node* right);
void internal_insert(Node* node, Context* key);
void insert_simple(Node *node, Context* key);
void insert_simple_internal(Node *node, Context* key, int with_children_moving); // костыль
void insert_child_instead_two(Node *node, Node *parent, int idx);
Node* remove_simple(Node *node, int hash);
Node* remove_internal(Node* node, Node* parent, int hash);
Node* remove_from_leaf(Node* node, Node* parent, int hash);
Node* union_simple(Node* left, Node* right);
Node* union_node_with_any_neighbour(Node* node, Node* parent);

int get_key_position(const Node *node, int hash);
Node* get_child_by_hash(const Node *node, int hash);
int get_key_position_to_insert(Node *node, Context* key);
int get_child_position(Node* node, Node* child);
int get_neighbour_for_remove(Node* node, Node* parent);

int get_hash(Context* context);
Context* get_context_by_block_number(const Node* node, int block_number);

void insert(Node* root, Context* key)
{
    internal_insert(root, key);
    if (root->key_length == 2 * M - 1)
    {
        Node* left = create_empty_node();
        Node* right = create_empty_node();
        Context* medium_key = root->keys[M -1 ];
        divide_node(root, left, right);
        Node* new_root = create_empty_node();
        insert_simple(new_root, medium_key);
        new_root->children[0] = left;
        new_root->children[1] = right;
        new_root->is_leaf = 0;
        free(root);
        *root = *new_root;
    }
}

const Node* search(const Node* node, int key)
{
    if (get_key_position(node, key) != -1)
        return node;

    Node* child = get_child_by_hash(node, key);
    if (child == NULL)
        return NULL;

    return search(child, key);
}

void remove(Node* root, int key)
{
    root = remove_internal(root, NULL, key);
    if (root->key_length == 0)
    {
        if (root->children[0] != NULL)
        {
            *root = *root->children[0];
        }
    }
}

Node* create_empty_node()
{
    Node* node = (Node*) malloc(sizeof(Node));
    node->key_length = 0;
    node->is_leaf = 1;
    for(int i = 0; i < 2 * M; i++)
    {
        node->children[i] = NULL;
        node->keys[i] = NULL;
    }

    return node;
}

Context* get_or_create(Node* root, int key)
{
    Context* context;
    const Node* node = Btree.search(root, key);
    if (node == NULL)
    {
        context = (Context*) malloc(sizeof(Context));

        context->received_length = 0;
        context->prepared = 0;
        context->expected_length = 0;
        context->block_number = key;
        context->confirmed = 0;
        context->has_timer = 0;
        context->time_for_expired = 0;

        Btree.insert(root, context);
    } else {
        context = get_context_by_block_number(node, key);
    }

    return context;
}

const struct _Btree Btree = {
        insert,
        search,
        create_empty_node,
        remove,
        get_or_create
};

// private

void internal_insert(Node* node, Context* key)
{
    if (node->is_leaf)
    {
        insert_simple(node, key);
    }
    else
    {
        Node* child = get_child_by_hash(node, get_hash(key));
        internal_insert(child, key);

        if (child->key_length == 2 * M - 1)
        {
            Node* left = create_empty_node();
            Node* right = create_empty_node();
            divide_node(child, left, right);
            Context* medium_key = child->keys[M - 1];
            insert_simple(node, medium_key);

            int insert_position = get_key_position(node, get_hash(medium_key));
            node->children[insert_position] = left;
            node->children[insert_position + 1] = right;
        }
    }
}

Node* remove_internal(Node* node, Node* parent, int hash)
{
    if (node->is_leaf)
    {
        return remove_from_leaf(node, parent, hash);
    }
    else
    {
        get_key_position(node, hash);
        Node* child = get_child_by_hash(node, hash);
        int idx = get_child_position(node, child);
        child = remove_internal(child, node, hash);
        if (child->key_length < M - 1)
        {
            union_node_with_any_neighbour(child, node);
            return node;
        }
        node->children[idx] = child;
        return node;
    }
}

// node1 and node2 - result of division
void divide_node(Node* node, Node* left, Node* right)
{
    for(int i = 0; i < M; i++)
    {
        if (i < M - 1)
        {
            left->keys[i] = node->keys[i];
            left->key_length++;
        }
        if (!node->is_leaf)
        {
            left->children[i] = node->children[i];
            left->is_leaf = 0;
        }
    }

    for(int i = M; i < 2 * M; i++)
    {
        if (i < 2 * M - 1)
        {
            right->key_length++;
            right->keys[i - M] = node->keys[i];
        }
        if (!node->is_leaf)
        {
            right->children[i - M] = node->children[i];
            right->is_leaf = 0;
        }
    }

    node->is_leaf = 0;
}

// node1 и node2 - ноды, которые получаются в результате переполнения
void insert_simple(Node *node, Context* key)
{
    insert_simple_internal(node, key, 1);
}

void insert_simple_internal(Node *node, Context* key, int with_children_moving)
{
    int insert_position = get_key_position_to_insert(node, key);

    for(int i = node->key_length + 1; i > insert_position; i--)
    {
        if (i < node->key_length + 1)
            node->keys[i] = node->keys[i - 1];
        if (!node->is_leaf && with_children_moving)
            node->children[i] = node->children[i - 1];
    }

    node->keys[insert_position] = key;

    node->key_length++;
}

Node* remove_from_leaf(Node* node, Node* parent, int hash)
{
    // if parent is NULL then node is root
    if (node->key_length > M - 1 || parent == NULL)
    {
        node = remove_simple(node, hash);
        return node;
    }
    else
    {
        int idx = get_child_position(parent, node);
        int pos = get_neighbour_for_remove(node, parent);
        if (pos == 0)
        {
            Node* new_node = union_node_with_any_neighbour(node, parent);

            remove_simple(new_node, hash);
            return new_node;
        }
        else
        {
            Context* neighbour_key;
            int parent_delimeter_key_idx;
            // если сосед - левый, берем его последний ключ
            if (pos == -1)
            {
                Node* neighbour = parent->children[idx - 1];
                neighbour_key = neighbour->keys[neighbour->key_length - 1];
                remove_simple(neighbour, get_hash(neighbour_key));
                parent_delimeter_key_idx = idx - 1;
            }
                // если сосед - правый, берем его первый ключ
            else
            {
                Node* neighbour = parent->children[idx + 1];
                neighbour_key = neighbour->keys[0];
                remove_simple(neighbour, get_hash(neighbour_key));
                parent_delimeter_key_idx = idx;
            }
            remove_simple(node, hash);
            insert_simple(node, parent->keys[parent_delimeter_key_idx]);
            parent->keys[parent_delimeter_key_idx] = neighbour_key;

            return node;
        }
    }
}

Node* remove_simple(Node *node, int hash)
{
    int remove_position = get_key_position(node, hash);
    for(int i = remove_position; i < node->key_length; i++)
    {
        node->keys[i] = node->keys[i + 1];
    }
    node->keys[node->key_length - 1] = NULL;
    node->key_length--;

    return node;
}

Node* union_simple(Node* left, Node* right)
{
    Node* result = create_empty_node();
    int i;
    for(i = 0 ; i < left->key_length; i++)
    {
        result->keys[i] = left->keys[i];
        result->key_length++;

        if (!left->is_leaf)
        {
            result->children[i] = left->children[i];
            result->is_leaf = 0;
        }
    }
    result->children[i] = left->children[i];

    for(i = 0; i < right->key_length; i++)
    {
        result->keys[i + left->key_length] = right->keys[i];
        result->key_length++;

        if (!right->is_leaf)
        {
            result->children[i + left->key_length + 1] = right->children[i];
            result->is_leaf = 0;
        }
    }
    result->children[i + left->key_length + 1] = right->children[i];

    return result;
}

Node* union_node_with_any_neighbour(Node* node, Node* parent)
{
    Node* left;
    Node* right;
    int parent_delimeter_key_idx;
    int idx = get_child_position(parent, node);
    if (idx > 0)
    {
        left = parent->children[idx - 1];
        right = node;
        parent_delimeter_key_idx = idx - 1;
    }
    else
    {
        right = parent->children[idx + 1];
        left = node;
        parent_delimeter_key_idx = idx;
    }

    Context* key_to_down = parent->keys[parent_delimeter_key_idx];
    Node* new_node = union_simple(left, right);
    insert_simple_internal(new_node, key_to_down, 0);
    remove_simple(parent, get_hash(key_to_down));
    // parent_delimeter_key_idx - чтобы вставлять на место левого
    insert_child_instead_two(new_node, parent, parent_delimeter_key_idx);

    return new_node;
}

// возвращает место между существующими ключами
int get_key_position_to_insert(Node *node, Context* key)
{
    int idx = 0;
    for(idx = 0; idx < node->key_length; idx++)
    {
        if (get_hash(node->keys[idx]) > get_hash(key))
            break;
    }

    return idx;
}

int get_child_position(Node* node, Node* child)
{
    for(int i = 0; i < node->key_length + 1; i++)
    {
        if (node->children[i] == child)
        {
            return i;
        }
    }

    return -1;
}

int get_key_position(const Node *node, int hash)
{
    for(int i = 0; i < node->key_length; i++)
    {
        if (get_hash(node->keys[i]) == hash)
            return i;
    }

    return -1;
}

Node* get_child_by_hash(const Node *node, int hash)
{
    if (node->key_length > 0 && hash < get_hash(node->keys[0]))
        return node->children[0];

    for(int i = 1; i < node->key_length; i++)
    {
        if (hash < get_hash(node->keys[i]))
            return node->children[i];
    }

    return node->children[node->key_length];
}

// возвращает -1, если сосед левый, 1- если правй, 0 - если не найден
int get_neighbour_for_remove(Node* node, Node* parent)
{
    int idx = get_child_position(parent, node);

    // вернуть ревого соседа
    if (idx > 0 && parent->children[idx - 1]->key_length > M - 1)
    {
        return -1;
    }

    // вернуть правого соседа
    if (idx < parent->key_length && parent->children[idx + 1]->key_length > M - 1)
    {
        return 1;
    }

    return 0;
}

void insert_child_instead_two(Node *node, Node *parent, int idx)
{
    parent->children[idx] = node;

    for(int i = idx + 1; i < 2 * M - 1; i++)
        parent->children[i] = parent->children[i + 1];
    parent->children[2 * M - 1] = NULL;
}

int get_hash(Context* context)
{
    return context->block_number;
}

Context* get_context_by_block_number(const Node* node, int block_number)
{
    for(int i = 0; i < node->key_length; i++)
    {
        if (node->keys[i]->block_number == block_number)
            return node->keys[i];
    }

    return NULL;
}