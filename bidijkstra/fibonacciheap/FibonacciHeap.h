#ifndef FIBONACCI_HEAP_H
#define FIBONACCI_HEAP_H

#include <set>
#include <map>

namespace std {

    class Node {
        public:
            const unsigned int id;
            const int key;
            int value;
            unsigned int degree;
            bool mark;
            Node* parent;
            set<Node*> children;
            Node(unsigned int, int, int);
    };

    class FibonacciHeap {
        private:
            unsigned int n, currentId;
            Node* min;
            set<Node*> roots;
            map<int, Node*> nodes_map;
            void consolidate();
            void link(Node*, Node*);
            void cut(Node*, Node*);
            void cascadingCut(Node*);
        public:
            FibonacciHeap();
            pair<int, int> getMin();
            pair<int, int> extractMin();
            pair<int, bool> getValue(int);
            void push(int, int);
            bool insert(int, int);
            bool decreaseValue(int, int);
            bool deleteNode(int);
            bool empty();
    };

}

#endif
