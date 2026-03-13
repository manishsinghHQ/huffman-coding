"""
Advanced Huffman Coding Compression Analyzer
=============================================

This Streamlit application demonstrates the Huffman Coding algorithm,
a widely used lossless data compression technique in multimedia systems.

It includes:
1. Text compression using Huffman Coding
2. Huffman tree visualization
3. Encoding and decoding
4. Compression efficiency analysis
5. JPEG-style image compression demo

Author : Manish U
"""

import streamlit as st
import heapq
from collections import defaultdict
from graphviz import Digraph
from PIL import Image
import numpy as np


# ==========================================================
# Huffman Tree Node
# ==========================================================

class Node:

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# ==========================================================
# Frequency Table
# ==========================================================

def build_frequency_table(text):

    freq = defaultdict(int)

    for char in text:
        freq[char] += 1

    return freq


# ==========================================================
# Build Huffman Tree
# ==========================================================

def build_huffman_tree(freq):

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
# Generate Huffman Codes
# ==========================================================

def generate_codes(node, current_code="", codes=None):

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
# Encoding
# ==========================================================

def encode_text(text, codes):

    encoded = ""

    for char in text:
        encoded += codes[char]

    return encoded


# ==========================================================
# Decoding
# ==========================================================

def decode_text(encoded_text, root):

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
# Tree Visualization
# ==========================================================

def visualize_tree(node):

    dot = Digraph()

    def add_nodes_edges(node, parent=None):

        if node is None:
            return

        label = f"{node.char}:{node.freq}" if node.char else f"{node.freq}"

        dot.node(str(id(node)), label)

        if parent:
            dot.edge(str(id(parent)), str(id(node)))

        add_nodes_edges(node.left, node)
        add_nodes_edges(node.right, node)

    add_nodes_edges(node)

    return dot


# ==========================================================
# Streamlit UI
# ==========================================================

st.title("Advanced Huffman Coding Compression Analyzer")

st.markdown("""
This tool demonstrates the **Huffman Coding algorithm**, a fundamental
technique used in **lossless data compression**.

Frequent characters receive **short binary codes**, while rare characters
receive **longer codes**, reducing total storage size.
""")

# ==========================================================
# TEXT COMPRESSION DEMO
# ==========================================================

st.header("Text Compression Demo")

text = st.text_area("Enter text to compress")

if st.button("Run Text Analysis"):

    if text.strip() == "":
        st.warning("Please enter some text")

    else:

        freq = build_frequency_table(text)

        st.subheader("Character Frequency")
        st.write(freq)

        root = build_huffman_tree(freq)

        st.subheader("Huffman Tree")
        dot = visualize_tree(root)
        st.graphviz_chart(dot)

        codes = generate_codes(root)

        st.subheader("Huffman Codes")
        st.write(codes)

        encoded = encode_text(text, codes)

        st.subheader("Encoded Binary")
        st.code(encoded)

        decoded = decode_text(encoded, root)

        st.subheader("Decoded Text")
        st.write(decoded)

        original_bits = len(text) * 8
        compressed_bits = len(encoded)

        ratio = compressed_bits / original_bits

        st.subheader("Compression Efficiency")

        st.write("Original Bits:", original_bits)
        st.write("Compressed Bits:", compressed_bits)
        st.write("Compression Ratio:", round(ratio, 3))


# ==========================================================
# JPEG STYLE IMAGE DEMO
# ==========================================================

st.header("JPEG-Style Image Compression Demo")

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image is not None:

    image = Image.open(uploaded_image)

    gray = image.convert("L")

    st.subheader("Original Grayscale Image")
    st.image(gray, width=300)

    pixels = np.array(gray)

    flat_pixels = pixels.flatten()

    pixel_string = " ".join(map(str, flat_pixels))

    freq = build_frequency_table(pixel_string)

    root = build_huffman_tree(freq)

    codes = generate_codes(root)

    encoded = encode_text(pixel_string, codes)

    decoded = decode_text(encoded, root)

    decoded_pixels = np.array(list(map(int, decoded.split())))

    decoded_pixels = decoded_pixels.reshape(pixels.shape)

    reconstructed = Image.fromarray(decoded_pixels.astype(np.uint8))

    st.subheader("Reconstructed Image After Huffman Decoding")
    st.image(reconstructed, width=300)

    original_bits = flat_pixels.size * 8
    compressed_bits = len(encoded)

    ratio = compressed_bits / original_bits

    st.subheader("Image Compression Analysis")

    st.write("Original Bits:", original_bits)
    st.write("Compressed Bits:", compressed_bits)
    st.write("Compression Ratio:", round(ratio, 3))

    st.success("JPEG-style Huffman compression demo completed.")
