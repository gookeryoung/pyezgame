cmake_minimum_required(VERSION 3.15...3.27)
project(pyezgame LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python with Stable ABI support
find_package(Python 3.9
    REQUIRED COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(
    _pyezgame
    STABLE_ABI
    NOMINSIZE
    src/bindings.cpp
)

target_include_directories(_pyezgame PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/clib)

if(WIN32)
    # Win32 GDI backend - no external deps
    target_link_libraries(_pyezgame PRIVATE user32)
else()
    # SDL2 backend (Linux / macOS)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(SDL2 REQUIRED sdl2)
    target_include_directories(_pyezgame PRIVATE ${SDL2_INCLUDE_DIRS})
    target_link_directories(_pyezgame PRIVATE ${SDL2_LIBRARY_DIRS})
    target_link_libraries(_pyezgame PRIVATE ${SDL2_LIBRARIES})
    target_compile_options(_pyezgame PRIVATE ${SDL2_CFLAGS_OTHER})

    # Optional SDL2 extensions - enable only if dev headers are installed
    pkg_check_modules(SDL2_IMAGE SDL2_image)
    if(SDL2_IMAGE_FOUND)
        target_include_directories(_pyezgame PRIVATE ${SDL2_IMAGE_INCLUDE_DIRS})
        target_link_directories(_pyezgame PRIVATE ${SDL2_IMAGE_LIBRARY_DIRS})
        target_link_libraries(_pyezgame PRIVATE ${SDL2_IMAGE_LIBRARIES})
    else()
        target_compile_definitions(_pyezgame PRIVATE GAMELIB_SDL_DISABLE_IMAGE=1)
    endif()

    pkg_check_modules(SDL2_TTF SDL2_ttf)
    if(SDL2_TTF_FOUND)
        target_include_directories(_pyezgame PRIVATE ${SDL2_TTF_INCLUDE_DIRS})
        target_link_directories(_pyezgame PRIVATE ${SDL2_TTF_LIBRARY_DIRS})
        target_link_libraries(_pyezgame PRIVATE ${SDL2_TTF_LIBRARIES})
    else()
        target_compile_definitions(_pyezgame PRIVATE GAMELIB_SDL_DISABLE_TTF=1)
    endif()

    pkg_check_modules(SDL2_MIXER SDL2_mixer)
    if(SDL2_MIXER_FOUND)
        target_include_directories(_pyezgame PRIVATE ${SDL2_MIXER_INCLUDE_DIRS})
        target_link_directories(_pyezgame PRIVATE ${SDL2_MIXER_LIBRARY_DIRS})
        target_link_libraries(_pyezgame PRIVATE ${SDL2_MIXER_LIBRARIES})
    else()
        target_compile_definitions(_pyezgame PRIVATE GAMELIB_SDL_DISABLE_MIXER=1)
    endif()
endif()

install(TARGETS _pyezgame LIBRARY DESTINATION pyezgame)
install(FILES pyezgame/__init__.py DESTINATION pyezgame)
install(FILES pyezgame/__init__.pyi DESTINATION pyezgame)

# Install Python examples and their assets under pyezgame/
file(GLOB EXAMPLE_PY_FILES ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.py)
install(FILES ${EXAMPLE_PY_FILES} DESTINATION pyezgame/examples)
install(DIRECTORY clib/assets DESTINATION pyezgame/examples)
