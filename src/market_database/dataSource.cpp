#include "market_database/dataSource.hpp"
#include <string_view>

dataSource::dataSource(std::string_view sourceName):
    sourceName_(sourceName) {

}
void dataSource::updateData() {

}

dataSource::~dataSource() = default;