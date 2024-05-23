# Include cstd.cmake for shared configuration settings
include("${PROJECT_SOURCE_DIR}/cstd.cmake")

# Gather all .cpp files in the current source directory and its subdirectories
file(GLOB market_database_SRC "*.cpp")

# Add a library to the project, linking against the gathered source files
add_library(market_database SHARED ${market_database_SRC})

# for debug
message("${CMAKE_CURRENT_SOURCE_DIR}")

