cmake_minimum_required(VERSION 3.15)
project(pyezgame LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

pybind11_add_module(_pyezgame src/bindings.cpp)

target_include_directories(_pyezgame PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/clib)

if(WIN32)
    target_link_libraries(_pyezgame PRIVATE user32)
endif()

install(TARGETS _pyezgame LIBRARY DESTINATION pyezgame)
install(FILES pyezgame/__init__.py DESTINATION pyezgame)
install(FILES pyezgame/__init__.pyi DESTINATION pyezgame)

# Install Python examples and their assets under pyezgame/
file(GLOB EXAMPLE_PY_FILES ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.py)
install(FILES ${EXAMPLE_PY_FILES} DESTINATION pyezgame/examples)
install(DIRECTORY examples/assets DESTINATION pyezgame/examples)
