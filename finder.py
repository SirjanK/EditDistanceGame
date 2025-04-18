import requests
import json
import os
from typing import List


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
    return set(words)


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


if __name__ == '__main__':
    dictionary = get_dictionary()
    word = input("Enter a word: ")
    suggestions = get_edit_distance_one_words(dictionary, word)
    print(f"Suggestions for '{word}': {suggestions}")
