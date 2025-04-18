import requests
import os
from typing import List, Dict
from collections import defaultdict
import pickle


URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"


def download_dictionary():
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


def get_dictionary():
    """
    Get the dictionary from the file
    """
    if not os.path.exists("dictionary.txt"):
        download_dictionary()

    with open("dictionary.txt", "r") as file:
        words = file.read().splitlines()
    return set([word.lower() for word in words])


def get_edit_distance_one_words(dictionary: set, word: str) -> List[str]:
    words = []
    def try_and_add(word):
        if word in dictionary:
            words.append(word)

    # try deletions
    for i in range(len(word)):
        try_and_add(word[:i] + word[i + 1:])

    # try additions
    for i in range(len(word) + 1):
        for c in "abcdefghijklmnopqrstuvwxyz":
            try_and_add(word[:i] + c + word[i:])
    
    # try substitutions
    for i in range(len(word)):
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c != word[i]:
                try_and_add(word[:i] + c + word[i + 1:])
    
    return words


def construct_adjacency_list(dictionary: set, word: str) -> Dict[str, List[str]]:
    """
    Construct an adjacency list for the given word
    """
    if os.path.exists("adjacency_list.pkl"):
        with open("adjacency_list.pkl", "rb") as file:
            adjacency_list = pickle.load(file)
        print("Adjacency list loaded from file.")
        return adjacency_list
    
    adjacency_list = defaultdict(list)
    for w in dictionary:
        for word in get_edit_distance_one_words(dictionary, w):
            adjacency_list[w].append(word)
    with open("adjacency_list.pkl", "wb") as file:
        pickle.dump(adjacency_list, file)
    print("Adjacency list constructed and saved.")
    return adjacency_list


def shortest_path_bfs(adjacency_list: Dict[str, List[str]], start: str, end: str) -> List[str]:
    """
    Find the shortest path from start to end using BFS
    """
    queue = [(start, [start])]
    visited = set()

    while queue:
        current_word, path = queue.pop(0)
        if current_word == end:
            return path
        visited.add(current_word)
        for neighbor in adjacency_list[current_word]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return []


if __name__ == '__main__':
    dictionary = get_dictionary()
    # ask for two words to find shortest path between them
    start_word = input("Enter the start word: ")
    end_word = input("Enter the end word: ")
    start_word = start_word.strip().lower()
    end_word = end_word.strip().lower()
    if start_word not in dictionary or end_word not in dictionary:
        print("Both words must be in the dictionary.")
    else:
        adjacency_list = construct_adjacency_list(dictionary, start_word)
        path = shortest_path_bfs(adjacency_list, start_word, end_word)
        if path:
            print("Shortest path:", " -> ".join(path))
        else:
            print("No path found.")
