#include <iostream>
#include <limits>
#include <set>
#include <vector>

#include "FibonacciHeap.h"

namespace std {

    Node::Node(unsigned int i, int v, int k) : id(i), key(k), value(v) {
        this->degree = 0;
        this->mark = false;
        this->parent = NULL;
    }

    FibonacciHeap::FibonacciHeap() {
        this->n = 0;
        this->currentId = 0;
        this->min = NULL;
    }

    pair<int, int> FibonacciHeap::getMin() {
        if (this->min) {
            return make_pair(this->min->value, this->min->key);
        } else {
            return make_pair(-1, -1);
        }
    }

    pair<int, int> FibonacciHeap::extractMin() {
        if (this->min) {
            Node* z = this->min;
            for (Node* x : z->children) {
                this->roots.insert(x);
                x->parent = NULL;
            }
            this->roots.erase(z);
            this->min = NULL;
            consolidate();
            this->n--;
            auto it = this->nodes_map.find(z->key);
            if (it != this->nodes_map.end()) {
                this->nodes_map.erase(it);
            }
            return make_pair(z->value, z->key);
        } else {
            return make_pair(-1, -1);
        }
    }

    pair<int, bool> FibonacciHeap::getValue(int key) {
        auto it = this->nodes_map.find(key);
        if (it != this->nodes_map.end()) {
            Node* x = it->second;
            return make_pair(x->value, false);
        } else {
            // Key not found.
            return make_pair(-1, true);
        }
    }

    void FibonacciHeap::push(int value, int key) {
        auto it = this->nodes_map.find(key);
        if (it == this->nodes_map.end()) {
            // Insert key.
            Node* x = new Node(this->currentId++, value, key);
            this->roots.insert(x);
            if (!this->min or value < this->min->value) {
                this->min = x;
            }
            this->n++;
            this->nodes_map[key] = x;
        } else {
            // Key already in heap.
            Node* x = it->second;
            if (value < x->value) {
                x->value = value;
                Node* y = x->parent;
                if (y and x->value < y->value) {
                    cut(x, y);
                    cascadingCut(y);
                }
                if (x->value < this->min->value) {
                    this->min = x;
                }
            }
        }
    }

    bool FibonacciHeap::insert(int value, int key) {
        if (this->nodes_map.find(key) == this->nodes_map.end()) {
            Node* x = new Node(this->currentId++, value, key);
            this->roots.insert(x);
            if (!this->min or value < this->min->value) {
                this->min = x;
            }
            this->n++;
            this->nodes_map[key] = x;
            return false;
        } else {
            // Key already in heap.
            return false;
        }
    }

    bool FibonacciHeap::decreaseValue(int value, int key) {
        auto it = this->nodes_map.find(key);
        if (it != this->nodes_map.end()) {
            Node* x = it->second;
            if (value < x->value) {
                x->value = value;
                Node* y = x->parent;
                if (y and x->value < y->value) {
                    cut(x, y);
                    cascadingCut(y);
                }
                if (x->value < this->min->value) {
                    this->min = x;
                }
            }
            return false;
        } else {
            // Key not found.
            return true;
        }
    }

    bool FibonacciHeap::deleteNode(int key) {
        auto it = this->nodes_map.find(key);
        if (it != this->nodes_map.end()) {
            Node* x = it->second;
            decreaseValue(-INT_MAX, x->key);
            extractMin();
            return false;
        } else {
            // Key not found.
            return true;
        }
    }

    bool FibonacciHeap::empty() {
        return this->n == 0;
    }

    void FibonacciHeap::consolidate() {
        unsigned int d;
        vector<Node*> A, R;
        for (unsigned int i=0; i<this->n; i++) {
            A.push_back(NULL);
        }
        for (Node* x : this->roots) {
            R.push_back(x);
        }
        for (Node* x : R) {
            d = x->degree;
            while (A[d]) {
                Node* y = A[d];
                if (x->value > y->value) {
                    // Swap x and y.
                    Node* t = x;
                    x = y;
                    y = t;
                }
                link(y, x);
                A[d] = NULL;
                d++;
            }
            A[d] = x;
        }
        this->min = NULL;
        for (unsigned int i=0; i<this->n; i++) {
            if (A[i]) {
                this->roots.insert(A[i]);
                if (!this->min or A[i]->value < this->min->value) {
                    this->min = A[i];
                }
            }
        }
    }

    void FibonacciHeap::link(Node* y, Node* x) {
        this->roots.erase(y);
        x->children.insert(y);
        x->degree++;
        y->parent = x;
        y->mark = false;
    }

    void FibonacciHeap::cut(Node* x, Node* y) {
        y->children.erase(x);
        y->degree--;
        this->roots.insert(x);
        x->parent = NULL;
        x->mark = false;
    }

    void FibonacciHeap::cascadingCut(Node* y) {
        Node* z = y->parent;
        if (z) {
            if (!y->mark) {
                y->mark = true;
            } else {
                cut(y, z);
                cascadingCut(z);
            }
        }
    }

}
