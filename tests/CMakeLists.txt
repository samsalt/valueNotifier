# Include cstd.cmake for shared configuration settings
include("${PROJECT_SOURCE_DIR}/cstd.cmake")

add_executable(runUnitTests test_example.cpp)

# Link test executable against gtest & gtest_main
target_link_libraries(runUnitTests gtest gtest_main market_database)

# Now register the executable as a test
add_test(NAME runUnitTests COMMAND runUnitTests)