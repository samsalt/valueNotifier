cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
project(MarketTracker LANGUAGES CXX)

# Include cstd.cmake for shared configuration settings
include("${PROJECT_SOURCE_DIR}/cstd.cmake")

add_subdirectory(src/market_database)

# Enable testing functionality
enable_testing()
# Add the GoogleTest submodule
add_subdirectory(extern/googletest)
# Include Google Test's directories
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
add_subdirectory(tests)

# enable_language(CUDA)
# include(CheckLanguage)
# check_language(CUDA)



# We also need to tell CMake where to look for include files. 
# In this case, we're telling it to look in the include directory within our project's source directory.

message("include dir = ${PROJECT_SOURCE_DIR}")


add_executable(my_executable src/main.cpp)
target_link_libraries(my_executable PRIVATE market_database)



# if(NOT DEFINED CMAKE_CUDA_STANDARD)
#     set(CMAKE_CUDA_STANDARD 14)
#     set(CMAKE_CUDA_STANDARD_REQUIRED ON)
# endif()

# for debug
# message("${CUDA_RUNTIME_LIBRARY}")

# add_executable(MarketTrackerServer ${SOURCES})

add_custom_target(runTests ALL
                  COMMAND ${CMAKE_CTEST_COMMAND}
                  DEPENDS runUnitTests)
