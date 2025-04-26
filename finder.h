#include <vector>


/// \brief This function finds the shortest path between two words in the edit distance graph.
/// \param start The starting word.
/// \param end The ending word.
/// \return A vector of strings representing the shortest path between the two words, or an empty vector if no path exists.
const std::vector<std::string> find_path(const std::string start, const std::string end);
