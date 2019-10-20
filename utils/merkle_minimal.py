from utils.crypto import SHA256
from utils.constants import ZERO_BYTES32
from math import log2


zerohashes = [ZERO_BYTES32]
for layer in range(1, 100):
    zerohashes.append(SHA256(zerohashes[layer - 1] + zerohashes[layer - 1]))


def calc_merkle_tree_from_leaves(values, layer_count: int=32):
    values = list(values)
    tree = [values[::]]
    for h in range(layer_count):
        if len(values) % 2 == 1:
            values.append(zerohashes[h])
        values = [SHA256(values[i] + values[i + 1]) for i in range(0, len(values), 2)]
        tree.append(values[::])
    return tree


def get_merkle_root(values, pad_to: int=1):
    layer_count = int(log2(pad_to))
    if len(values) == 0:
        return zerohashes[layer_count]
    return calc_merkle_tree_from_leaves(values, layer_count)[-1][0]


def get_merkle_proof(tree, item_index: int):
    proof = []
    for i in range(32):
        subindex = (item_index // 2**i) ^ 1
        proof.append(tree[i][subindex] if subindex < len(tree[i]) else zerohashes[i])
    return proof


def merkleize_chunks(chunks, pad_to: int=1):
    count = len(chunks)
    depth = max(count - 1, 0).bit_length()
    max_depth = max(depth, (pad_to - 1).bit_length())
    tmp = [b'' for _ in range(max_depth + 1)]

    def merge(h, i):
        j = 0
        while True:
            if i & (1 << j) == 0:
                if i == count and j < depth:
                    h = SHA256(h + zerohashes[j])  # keep going if we are complementing the void to the next power of 2
                else:
                    break
            else:
                h = SHA256(tmp[j] + h)
            j += 1
        tmp[j] = h

    # merge in leaf by leaf.
    for i in range(count):
        merge(chunks[i], i)

    # complement with 0 if empty, or if not the right power of 2
    if 1 << depth != count:
        merge(zerohashes[0], count)

    # the next power of two may be smaller than the ultimate virtual size, complement with zero-hashes at each depth.
    for j in range(depth, max_depth):
        tmp[j + 1] = SHA256(tmp[j] + zerohashes[j])

    return tmp[max_depth]
