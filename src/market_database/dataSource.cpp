#include "market_database/dataSource.hpp"
#include <string_view>

dataSource::dataSource(std::string_view sourceName) : sourceName_(sourceName)
{
    int result = curl_global_init(CURL_GLOBAL_DEFAULT);
    if (result != CURLE_OK)
    {
        std::cerr << "Error: " << result << " in curl_global_init" << std::endl;
    }
}
void dataSource::updateData()
{
}

dataSource::~dataSource() = default;