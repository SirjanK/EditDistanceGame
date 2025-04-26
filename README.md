# Edit Distance Game

What is the shortest path from a word to another where edges between words exist if they are one edit distance away from each other?

## Loader
The loader python library loads words from the Oxford dictionary and creates a graph where each node is a word and edges exist between words that are one edit distance away from each other.

This dumps two files under `data/`:
1. `words.txt` - a list of words where the line number will be the index of the word in the graph.
2. `graph.bin` - a binary file containing the graph

Invoke simply by `python loader.py`.

## Finder
The C++ finder program finds the shortest path between two words in the graph. It uses a breadth-first search algorithm to find the shortest path.

The Loader has to run first to create the graph and dump to `data/` before running the finder.

Invoke using: `./finder <word1> <word2>`.
