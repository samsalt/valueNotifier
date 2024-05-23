#include "market_database/dataSource.hpp"
#include <string_view>

dataSource::dataSource(std::string_view sourceName):
    sourceName_(sourceName) {
        std::cout<<sourceName_<<" is created"<<std::endl;
}
void dataSource::updateData() {

}

// dataSource::~dataSource() {}