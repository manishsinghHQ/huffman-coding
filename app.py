"""
Advanced Huffman Coding Compression Analyzer
=============================================

This Streamlit application demonstrates the Huffman Coding algorithm,
a widely used lossless data compression technique in multimedia systems.

Huffman coding works by assigning variable-length binary codes to
characters based on their frequency of occurrence. Characters that
appear more frequently are assigned shorter binary codes, while rare
characters receive longer codes.

This technique minimizes the total number of bits required to represent
the data, making it efficient for storage and transmission.

Applications of Huffman Coding
------------------------------
- JPEG Image Compression
- MPEG Video Compression
- ZIP File Compression
- MP3 Audio Compression

Features of this Application
----------------------------
1. Character Frequency Analysis
2. Huffman Tree Construction
3. Huffman Code Generation
4. Binary Encoding of Text
5. Decoding Verification
6. Compression Efficiency Analysis
7. Huffman Tree Visualization

Author : Manish U
"""

import streamlit as st
import heapq
from collections import defaultdict
from graphviz import Digraph


# ==========================================================
# Huffman Tree Node
# ==========================================================

class Node:
    """
    Represents a single node in the Huffman Tree.

    Parameters
    ----------
    char : str
        Character stored in the node.
        Internal nodes will have value None.

    freq : int
        Frequency of the character in the input text.

    Attributes
    ----------
    left : Node
        Left child node (represents binary '0').

    right : Node
        Right child node (represents binary '1').
    """

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Enables comparison of Node objects inside a
        priority queue (min heap).

        The node with smaller frequency is given higher priority.
        """
        return self.freq < other.freq


# ==========================================================
# Frequency Analysis
# ==========================================================

def build_frequency_table(text):
    """
    Computes the frequency of each character in the input text.

    This information is essential for constructing the Huffman Tree.

    Parameters
    ----------
    text : str
        Input text provided by the user.

    Returns
    -------
    dict
        Dictionary mapping each character to its frequency.

    Example
    -------
    Input: "hello"

    Output:
    {
        'h':1,
        'e':1,
        'l':2,
        'o':1
    }
    """

    freq = defaultdict(int)

    for char in text:
        freq[char] += 1

    return freq


# ==========================================================
# Huffman Tree Construction
# ==========================================================

def build_huffman_tree(freq):
    """
    Constructs the Huffman Tree using a priority queue.

    Algorithm
    ---------
    1. Create a leaf node for each character.
    2. Insert all nodes into a min heap.
    3. Repeatedly remove two nodes with the smallest frequency.
    4. Create a new internal node with combined frequency.
    5. Insert the new node back into the heap.
    6. Repeat until only one node remains (root).

    Parameters
    ----------
    freq : dict
        Frequency table generated from the input text.

    Returns
    -------
    Node
        Root node of the constructed Huffman Tree.
    """

    heap = []

    for char, f in freq.items():
        heapq.heappush(heap, Node(char, f))

    while len(heap) > 1:

        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        heapq.heappush(heap, merged)

    return heap[0]


# ==========================================================
# Huffman Code Generation
# ==========================================================

def generate_codes(node, current_code="", codes=None):
    """
    Traverses the Huffman Tree and generates binary codes
    for each character.

    Tree Traversal Rule
    -------------------
    Left Edge  → append '0'
    Right Edge → append '1'

    Parameters
    ----------
    node : Node
        Current node in the Huffman tree.

    current_code : str
        Binary code constructed during traversal.

    codes : dict
        Dictionary storing final character → code mapping.

    Returns
    -------
    dict
        Mapping of characters to their Huffman binary codes.
    """

    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = current_code

    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)

    return codes


# ==========================================================
# Encoding Process
# ==========================================================

def encode_text(text, codes):
    """
    Converts the original text into a compressed
    binary sequence using Huffman codes.

    Parameters
    ----------
    text : str
        Original user input text.

    codes : dict
        Dictionary containing Huffman codes.

    Returns
    -------
    str
        Encoded binary string.
    """

    encoded = ""

    for char in text:
        encoded += codes[char]

    return encoded


# ==========================================================
# Decoding Process
# ==========================================================

def decode_text(encoded_text, root):
    """
    Decodes a Huffman encoded binary sequence
    back to the original text.

    Parameters
    ----------
    encoded_text : str
        Binary string produced by the encoding stage.

    root : Node
        Root node of the Huffman Tree.

    Returns
    -------
    str
        Decoded text.
    """

    decoded = ""
    current = root

    for bit in encoded_text:

        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            decoded += current.char
            current = root

    return decoded


# ==========================================================
# Huffman Tree Visualization
# ==========================================================

def visualize_tree(node):
    """
    Generates a graphical representation of the Huffman Tree
    using Graphviz.

    Each node shows:
    - Character
    - Frequency

    Returns
    -------
    Digraph
        Graphviz object representing the Huffman Tree.
    """

    dot = Digraph()

    def add_nodes_edges(node, parent=None):

        if node is None:
            return

        node_label = f"{node.char}:{node.freq}" if node.char else f"{node.freq}"

        dot.node(str(id(node)), node_label)

        if parent:
            dot.edge(str(id(parent)), str(id(node)))

        add_nodes_edges(node.left, node)
        add_nodes_edges(node.right, node)

    add_nodes_edges(node)

    return dot


# ==========================================================
# Streamlit User Interface
# ==========================================================

st.title("Advanced Huffman Coding Compression Analyzer")

st.markdown("""
This interactive tool demonstrates the **Huffman Coding algorithm**,
a fundamental technique used in **lossless data compression**.

The algorithm improves storage efficiency by assigning **short binary
codes to frequent characters** and **longer codes to rare characters**.
""")

text = st.text_area("Enter text to compress")

if st.button("Run Analysis"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:

        # Frequency Analysis
        freq = build_frequency_table(text)

        st.header("1️⃣ Character Frequency Analysis")
        st.write(freq)

        # Build Tree
        root = build_huffman_tree(freq)

        st.header("2️⃣ Huffman Tree Visualization")
        dot = visualize_tree(root)
        st.graphviz_chart(dot)

        # Generate Codes
        codes = generate_codes(root)

        st.header("3️⃣ Huffman Codes")
        st.write(codes)

        # Encoding
        encoded = encode_text(text, codes)

        st.header("4️⃣ Encoded Binary")
        st.code(encoded)

        # Decoding
        decoded = decode_text(encoded, root)

        st.header("5️⃣ Decoded Text")
        st.write(decoded)

        # Compression Analysis
        original_bits = len(text) * 8
        compressed_bits = len(encoded)

        ratio = compressed_bits / original_bits

        st.header("6️⃣ Compression Efficiency")

        st.write("Original Bits:", original_bits)
        st.write("Compressed Bits:", compressed_bits)
        st.write("Compression Ratio:", round(ratio, 2))

        st.success("Compression analysis completed successfully.")
