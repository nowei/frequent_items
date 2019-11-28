import random
from collections import Counter

# Where p is a prime
def generate_hash(m, p = 131071):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: ((a * x + b) % p) % m

from math import log
def generate_hashes(b, t): 
    h = []
    s = []
    for i in range(t):
        h.append(generate_hash(b))
        # if 0, set to -1, do nothing o/w
        s.append(generate_hash(2))
    return h, s 

def add(C, q):
    for i in range(t):
        if s[i](q):
            C[i][h[i](q)] += 1
        else:
            C[i][h[i](q)] -= 1

# I would've used median of medians, except that only works for odd
def find_median(candidates):
    candidates.sort()
    half = len(candidates) // 2
    if len(candidates) % 2: # if odd
        return (candidates[half] + candidates[half + 1]) / 2
    else:
        return candidates[half]


def estimate(C, q):
    candidates = [C[i][h[i](q)] for i in range(t)]
    return find_median(candidates)

def find_approx_top(S, k, epsilon):
    heap = {}
    min_set = [float('inf'), []]    
    for q in S:
        add(C, q)
        if q in heap: 
            heap[q] += 1
            if q in min_set[1]: 
                min_set[1].remove(q)
        else:
            count = estimate(C, q)
            # keeps top k
            if len(heap) < k:
                heap[q] = count
                if count < min_set[0]:
                    min_set[0] = count
                    min_set[1].clear()
                if count == min_set[0]:
                    min_set[1].append(q)
            # otherwise drop the minimum if necessary
            elif count > min_set[0]:
                heap[q] = count
                if len(min_set[1]) > 0:
                    evicted = min_set[1].pop()
                    del heap[evicted]
        if len(min_set[1]) == 0:
            min_set[0] = float('inf')
            for key, value in heap.items():
                if value < min_set[0]:
                    min_set[0] = value
                    min_set[1].clear()
                if value == min_set[0]:
                    min_set[1].append(key)
        print(heap, min_set)
    return heap

k = 3
epsilon = 1
stream = []
print('using k = {}, epsilon = {}'.format(k, epsilon))
with open('stream.txt', 'r') as f:
    print('reading stream.txt...')
    for line in f:
        stream.append(int(line))

# probability of failure
delta = 0.001
# number of hash tables - O(log(n/delta))
t = 20 * int(log(len(stream)/delta))
# number of things that the hash table hashes to
b = 8 * k #max(k, 32 * /((epsilon * n_k) ** 2))

C = [[0] * b for i in range(t)]
h, s = generate_hashes(b, t)
heap = find_approx_top(stream, k, epsilon)
print('key, value')
print(sorted(heap.items()))
print(sorted(Counter(stream).most_common(k)))