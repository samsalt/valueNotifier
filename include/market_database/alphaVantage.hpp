#pragma once
#include "market_database/dataSource.hpp"

class alphaVantageDataSource : public dataSource
{
public:
    explicit alphaVantageDataSource();
    ~alphaVantageDataSource() override;

    // Returns the API key used by this data source.
    // The API key is a unique identifier provided by Alpha Vantage.
    std::string getApiKey() const { return apiKey_; }
    // Sets the API key to be used by this data source.
    // This method can be used to set the API key at runtime or during object initialization.
    void setApiKey(std::string apiKey) { apiKey_ = apiKey; }

    // void fetchData(const std::vector<std::string>& symbols, const std::vector<std::string>& fields = {});
    void fetchData() const;

private:
    std::string apiKey_{};
};