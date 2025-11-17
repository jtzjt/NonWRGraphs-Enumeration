# Enumeration of Non-Word-Representable Graphs

## Overview

This repository provides a standalone Python program for enumerating all **non-word-representable graphs** on `n` vertices.  
For a given integer `n`, the script generates all connected, non-isomorphic graphs of order `n`, determines whether each graph is word-representable using the semi-transitive orientation characterization, and outputs all non-word-representable graphs in a compressed `.zip` archive.

The implementation is independent and does not rely on any existing software for word-representability.

---

## Features

- Enumerates all connected, non-isomorphic graphs on `n` vertices via **nauty/geng**.
- Determines word-representability using:
  - 3-colorability pruning (all 3-colorable graphs are word-representable),
  - full semi-transitive orientation backtracking.
- Automatically produces: <n>vertex_nonWR.zip

containing all non-word-representable graphs.
- Each graph is exported as an `n × n` adjacency matrix in `.txt` format.

---

## Requirements

- Python 3.8+
- Install `networkx`:

pip install networkx

Install nauty (provides geng): brew install nauty     # macOS

Verify installation: geng -c 6

# Usage

Run the script with:

python3 find_nonWR_graphs.py n


Examples:

python3 find_nonWR_graphs.py 7
python3 find_nonWR_graphs.py 8


This produces a ZIP archive in the current directory, such as:

7vertex_nonWR.zip
8vertex_nonWR.zip

# Output Format

Inside the ZIP file, each non-word-representable graph is saved as:

nonWR_1.txt
nonWR_2.txt
...


Each file contains an n × n adjacency matrix with entries 0 and 1, for example:

0110110
1011001
1101010
...


These represent all non-word-representable graphs on n vertices, up to isomorphism.

Notes

Practical values are n = 6, 7, 8.

For n ≥ 9, enumeration can become computationally expensive due to the number of candidate graphs.

The method is complete: a graph is non-word-representable if and only if every orientation contains a cycle or a shortcut.
