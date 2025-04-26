# Compiler settings
CXX := g++
CXXFLAGS := -Wall -Wextra -g -std=c++11

# Files
SRCS := finder.cpp main.cpp
OBJS := $(SRCS:.cpp=.o)
TARGET := finder

# Build rules
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Implicit rule for .cpp -> .o
%.o: %.cpp finder.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Cleanup
.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET)