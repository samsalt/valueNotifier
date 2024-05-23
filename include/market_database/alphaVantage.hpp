#pragma once
#include "market_database/dataSource.hpp"

class alphaVantageDataSource : public dataSource {
    public:
        explicit alphaVantageDataSource();
        ~alphaVantageDataSource() override;
    private:
};