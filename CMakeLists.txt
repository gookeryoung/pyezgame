cmake_minimum_required(VERSION 3.15)
project(gameui LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

pybind11_add_module(_gameui src/bindings.cpp)

target_include_directories(_gameui PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/clib)

if(WIN32)
    target_link_libraries(_gameui PRIVATE user32)
endif()

install(TARGETS _gameui LIBRARY DESTINATION gameui)
install(FILES gameui/__init__.py DESTINATION gameui)
install(FILES gameui/__init__.pyi DESTINATION gameui)

# Install Python examples and their assets under gameui/
file(GLOB EXAMPLE_PY_FILES ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.py)
install(FILES ${EXAMPLE_PY_FILES} DESTINATION gameui/examples)
install(DIRECTORY examples/assets DESTINATION gameui/examples)
