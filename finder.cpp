#include "finder.h"
#include <unordered_map>
#include <fstream>
#include <cstdint>
#include <stdexcept>


const std::vector<std::string> FindPath(std::string start, std::string end) {
    // Load words
    const auto& words = LoadWords(WORDS_FILE);

    // Load adjacency list
    const auto& adjacencyList = LoadAdjacencyList(ADJACENCY_LIST_FILE);

    // Create a map from words to indices
    std::unordered_map<std::string, uint32_t> wordToIndex;
    for (uint32_t i = 0; i < words.size(); ++i) {
        wordToIndex[words[i]] = i;
    }

    // Check if start and end words are in the list, return empty vector if not
    if (wordToIndex.find(start) == wordToIndex.end() || wordToIndex.find(end) == wordToIndex.end()) {
        return {};
    }

    // Get the indices of the start and end words
    uint32_t startIndex = wordToIndex[start];
    uint32_t endIndex = wordToIndex[end];

    // Run BFS to find the shortest path
    const auto& pathIndices = BFS(startIndex, endIndex, adjacencyList);

    // Translate the vector of indices back to words
    std::vector<std::string> path;
    for (const auto& index : pathIndices) {
        path.push_back(words[index]);
    }

    return path;
}


const std::vector<std::string> LoadWords(std::string filename) {
    std::vector<std::string> words;
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filename);
    }

    std::string word;
    while (file >> word) {
        words.push_back(word);
    }

    return words;
}


const std::vector<std::vector<uint32_t>> LoadAdjacencyList(std::string filename) {
    std::ifstream file(filename, std::ios::binary);
    if(!file.is_open()) throw std::runtime_error("Cannot open graph.bin file");
    
    uint32_t nodeCount;
    file.read(reinterpret_cast<char*>(&nodeCount), sizeof(nodeCount));
    
    std::vector<std::vector<uint32_t>> adjacencyList(nodeCount);
    
    for (uint32_t i = 0; i < nodeCount; ++i) {
        uint32_t neighborCount;
        file.read(reinterpret_cast<char*>(&neighborCount), sizeof(neighborCount));
        
        std::vector<uint32_t> neighbors(neighborCount);
        if (neighborCount > 0) {
            file.read(reinterpret_cast<char*>(neighbors.data()), 
                     neighborCount * sizeof(uint32_t));
        }
        
        adjacencyList[i] = std::move(neighbors);
    }
    
    return adjacencyList;
}


const std::vector<std::uint32_t> BFS(uint32_t start, uint32_t end, const std::vector<std::vector<uint32_t>>& adjacencyList) {
    std::vector<bool> visited(adjacencyList.size(), false);  // visited boolean array
    std::vector<uint32_t> parent(adjacencyList.size(), UINT32_MAX);  // parent array to reconstruct the path
    std::vector<uint32_t> queue;  // queue for BFS
    
    visited[start] = true;
    queue.push_back(start);
    
    while (!queue.empty()) {
        uint32_t current = queue.front();
        queue.erase(queue.begin());
        
        if (current == end) {
            break;
        }
        
        for (const auto& neighbor : adjacencyList[current]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                parent[neighbor] = current;
                queue.push_back(neighbor);
            }
        }
    }

    // If we didn't reach the end, return an empty vector
    if (parent[end] == UINT32_MAX) {
        return {};
    }
    
    // Reconstruct the path
    std::vector<uint32_t> path;
    for (uint32_t at = end; at != UINT32_MAX; at = parent[at]) {
        path.push_back(at);
    }
    
    std::reverse(path.begin(), path.end());
    
    return path;
}
