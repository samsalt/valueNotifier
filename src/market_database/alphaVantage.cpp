#include "market_database/alphaVantage.hpp"
#include <fstream>

alphaVantageDataSource::alphaVantageDataSource() : dataSource("alphaVantage")
{
    std::ifstream apiKeyFile("AlphaVantageAPIKey");
    if (apiKeyFile.is_open())
    {
        try
        {
            std::string apiKey;
            std::getline(apiKeyFile, apiKey);
            apiKeyFile.close();
            setApiKey(apiKey);
        }
        catch (const std::runtime_error &e)
        {
            std::cerr << "Failed to read API key: " << e.what() << std::endl;
        }
    }
    else
    {
        // Handle the case where the file is not open correctly
        std::cerr << "Failed to open AlphaVantageAPIKey file." << std::endl;
    }
}

void alphaVantageDataSource::fetchData() const
{
    CURL *curl;
    CURLcode result;

    curl = curl_easy_init();
    if (curl == NULL) {
        // Handle error
    }

    curl_easy_setopt(curl, CURLOPT_URL, "https://www.google.com");
    curl_easy_setopt(curl, CURLOPT_RTSP_TRANSPORT, 1L);

    result = curl_easy_perform(curl);
    if (result != CURLE_OK) {
        // Handle error
    }

    curl_easy_cleanup(curl);
}

alphaVantageDataSource::~alphaVantageDataSource() = default;