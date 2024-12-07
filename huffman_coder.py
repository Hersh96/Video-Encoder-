from collections import defaultdict
import heapq

class HuffmanCoder:
    class Node:
        def __init__(self, symbol, freq):
            self.symbol = symbol
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    @staticmethod
    def build_frequency_dict(data):
        freq = defaultdict(int)
        for val in data:
            freq[val] += 1
        return freq

    @classmethod
    def build_huffman_tree(cls, freq):
        heap = [cls.Node(symbol, count) for symbol, count in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = cls.Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        return heap[0] if heap else None

    @classmethod
    def generate_huffman_codes(cls, root):
        codes = {}
        def traverse(node, code):
            if node is None:
                return
            if node.symbol is not None:
                codes[node.symbol] = code
                return
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
        traverse(root, "")
        return codes

    @classmethod
    def compress(cls, data):
        if len(data) == 0:
            return {'encoded_data': '', 'codes': {}}

        freq = cls.build_frequency_dict(data)
        root = cls.build_huffman_tree(freq)
        codes = cls.generate_huffman_codes(root)
        encoded_data = ''.join(codes[val] for val in data)
        return {'encoded_data': encoded_data, 'codes': codes}

    @classmethod
    def decompress(cls, encoded_data, codes):
        if not encoded_data or not codes:
            return []

        reverse_codes = {v: k for k, v in codes.items()}
        decoded = []
        current_code = ""
        for bit in encoded_data:
            current_code += bit
            if current_code in reverse_codes:
                decoded.append(reverse_codes[current_code])
                current_code = ""
        return decoded
