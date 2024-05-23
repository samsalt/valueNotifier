#pragma once
#include "market_database/dataSource.hpp"

class alphaVantageDataSource : public dataSource
{
public:
    explicit alphaVantageDataSource();
    ~alphaVantageDataSource() override;
    // Returns the API key used by this data source.
    // The API key is a unique identifier provided by Alpha Vantage.
    std::string getApiKey() const  { return apiKey_; } // <STOP EDITTING HERE>

private:
    std::string apiKey_{};
};