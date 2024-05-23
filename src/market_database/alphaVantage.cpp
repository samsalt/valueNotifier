#include "market_database/alphaVantage.hpp"
#include <fstream>

alphaVantageDataSource::alphaVantageDataSource() : dataSource("alphaVantage")
{
    std::ifstream apiKeyFile("AlphaVantageAPIKey");
    if (apiKeyFile.is_open()) {
        try {
        std::getline(apiKeyFile, apiKey_);
        apiKeyFile.close();
        } catch (const std::runtime_error& e) {
            // Handle the exception here, for example:
            std::cerr << "Failed to read API key: " << e.what() << std::endl;
    }
    } else {
        // Handle the case where the file is not open correctly
        std::cerr << "Failed to open AlphaVantageAPIKey file." << std::endl;
    }
}

alphaVantageDataSource::~alphaVantageDataSource() = default;