#include "finder.h"
#include <iostream>


int main(int argc, char* argv[]) {
    // Verify two words are provided
    if(argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <word1> <word2>\n";
        return 1;
    }

    // Convert arguments to string words
    const std::string word1 = argv[1];
    const std::string word2 = argv[2];

    const auto& path = FindPath(word1, word2);

    // Print the path with "->" between words
    if(path.empty()) {
        std::cout << "No path found between " << word1 << " and " << word2 << ".\n";
    } else {
        std::cout << "Path from " << word1 << " to " << word2 << ":\n";
        // Iterate until the second last element to avoid printing "->" after the last word
        for(size_t i = 0; i < path.size() - 1; ++i) {
            std::cout << path[i] << " -> ";
        }
        std::cout << path.back() << "\n"; // Print the last word without "->"
    }

    return 0;
}
