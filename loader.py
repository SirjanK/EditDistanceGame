import requests
import os
from typing import List, Dict
from collections import defaultdict
import numpy as np


URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
DATA_DIR = "data/"


def download_dictionary() -> None:
    """
    Download oxford dictionary and store in a file
    """

    response = requests.get(URL)

    if response.status_code == 200:
        with open("dictionary.txt", "w") as file:
            file.write(response.text)
        print("Dictionary downloaded successfully.")
    else:
        print("Failed to download dictionary.")


def get_dictionary() -> List[str]:
    """
    Get the dictionary from the file - sort alphabetically

    :return: List of words from saved dictionary
    """
    if not os.path.exists("dictionary.txt"):
        download_dictionary()

    with open("dictionary.txt", "r") as file:
        words = file.read().splitlines()
    # get a set of words to remove duplicates
    words = set([word.strip().lower() for word in words])
    return sorted(words)


def construct_dictionary_index(dictionary: List[str]) -> Dict[str, List[int]]:
    """
    Construct a dictionary index for fast lookup

    :param dictionary: List of words
    :param dictionary_idx_map: Dictionary mapping words to their indices
    """
    dictionary_idx_map = dict()
    for idx, word in enumerate(dictionary):
        dictionary_idx_map[word] = idx
    return dictionary_idx_map


def get_edit_distance_one_words(word: str, dictionary_idx_map: Dict[str, List[int]]) -> List[int]:
    """
    Get all words in the dictionary that are one edit distance away from the given word

    :param word: The word to check against
    :param dictionary_idx_map: Dictionary mapping words to their indices
    :return: List of indices of words that are one edit distance away
    """

    edit_distance_one_words = set()

    def check_and_add(word: str):
        if word in dictionary_idx_map:
            edit_distance_one_words.add(dictionary_idx_map[word])
    
    # deletion
    for i in range(len(word)):
        check_and_add(word[:i] + word[i+1:])
    
    # substitution
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                check_and_add(word[:i] + c + word[i+1:])
    
    # insertion
    for i in range(len(word) + 1):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            check_and_add(word[:i] + c + word[i:])

    return sorted(edit_distance_one_words)


def construct_adjacency_list(dictionary: List[str], dictionary_idx_map: Dict[str, List[int]]) -> Dict[int, List[int]]:
    """
    Construct an adjacency list for the dictionary

    :param dictionary: List of words
    :param dictionary_idx_map: Dictionary mapping words to their indices
    :return: Adjacency list where each index corresponds to a word and contains a list of indices of words that are one edit distance away
    """

    adjacency_list = defaultdict(list)

    for idx, word in enumerate(dictionary):
        adjacency_list[idx] = get_edit_distance_one_words(word, dictionary_idx_map)

    return adjacency_list


def save_graph(dictionary: List[str], adj_list: Dict[int, List[int]]) -> None:
    """
    Save as .bin file with:
    - First 4 bytes: uint32 node count
    - Subsequent entries: node's neighbor count (uint32) + neighbor IDs (uint32)

    :param dictionary: List of words
    :param adj_list: Adjacency list where each index corresponds to a word and contains a list of indices of words that are one edit distance away
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # save words first
    word_file = os.path.join(DATA_DIR, "words.txt")
    with open(word_file, 'w') as f:
        for word in dictionary:
            f.write(word + '\n')

    filename = os.path.join(DATA_DIR, "graph.bin")
    with open(filename, 'wb') as f:
        # Write total nodes (4 bytes)
        np.array(len(adj_list), dtype='<u4').tofile(f)
        
        # Write each node's neighbors
        for idx in range(len(adj_list)):
            neighbors = adj_list[idx]
            np.array(len(neighbors), dtype='<u4').tofile(f)  # Neighbor count
            np.array(neighbors, dtype='<u4').tofile(f)       # Neighbor IDs


if __name__ == '__main__':
    dictionary = get_dictionary()
    print(f"Dictionary size: {len(dictionary)}")
    dictionary_idx_map = construct_dictionary_index(dictionary)
    print(f"Constructed dictionary index with {len(dictionary_idx_map)} entries.")

    adjacency_list = construct_adjacency_list(dictionary, dictionary_idx_map)
    print(f"Constructed adjacency list with {len(adjacency_list)} entries.")

    # Save the graph to a file
    save_graph(dictionary, adjacency_list)
    print(f"Graph saved to {DATA_DIR}")
