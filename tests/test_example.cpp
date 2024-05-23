#include <gtest/gtest.h>
#include "market_database/alphaVantage.hpp"

TEST(alphaSource, create) {
    alphaVantageDataSource avds;

    // Verify that the source name matches the expected value
    const std::string sourceName = "alphaVantage";
    EXPECT_EQ(sourceName, avds.getSourceName());  // Check if 'avds' has the correct source name
    EXPECT_NE("", avds.getApiKey());  // Check if 'avds' has the correct source name

}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}