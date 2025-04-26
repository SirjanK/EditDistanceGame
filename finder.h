#include <vector>
#include <string>


static constexpr const char* WORDS_FILE = "data/words.txt";
static constexpr const char* ADJACENCY_LIST_FILE = "data/adjacency_list.bin";


/// \brief Finds the shortest path between two words in the edit distance graph.
/// \param start The starting word.
/// \param end The ending word.
/// \return A vector of strings representing the shortest path between the two words, or an empty vector if no path exists.
const std::vector<std::string> FindPath(std::string start, std::string end);

/// \brief Load the words from the words file.
/// \param filename The name of the file containing the words.
/// \return A vector of strings representing the words in the file.
const std::vector<std::string> LoadWords(std::string filename);

/// \brief Load the adjacency list from the adjacency list file.
/// \param filename The name of the file containing the adjacency list.
/// \return A vector of vectors representing the adjacency list, where each inner vector contains the indices of the adjacent nodes.
const std::vector<std::vector<uint32_t>> LoadAdjacencyList(std::string filename);

/// \brief Run breadth first search to find the shortest path between two nodes in the adjacency list.
/// \param start The starting node.
/// \param end The ending node.
/// \param adjacencyList The adjacency list.
/// \return A vector of indices representing the path from start to end, or an empty vector if no path exists.
const std::vector<std::uint32_t> BFS(uint32_t start, uint32_t end, const std::vector<std::vector<uint32_t>>& adjacencyList);
