#include "market_database/dataSource.hpp"
const std::vector<std::string>& getTickerList() {
    static const std::vector<std::string> tickerList = {
        "AAPL", 
        "GOOG", 
        "MSFT", 
        "AMZN" 
    };
    return tickerList;
}