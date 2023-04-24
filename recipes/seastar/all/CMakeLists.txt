cmake_minimum_required(VERSION 3.10)
project(test_package)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(CheckSymbolExists)
add_subdirectory("source_subfolder")
