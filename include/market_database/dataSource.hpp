#pragma once
#include <string_view>
#include <string>
#include <iostream>

class dataSource {
    public:
    // Constructor is deleted to disallow default construction
    // dataSource() = delete;
    dataSource() = default;

    // Constructor takes a string_view for the source name
    dataSource(std::string_view sourceName);

    // Copy constructor and assignment operator are deleted to disallow copying
    dataSource(const dataSource&) = delete;
    dataSource& operator=(const dataSource&) = delete;

    // Move constructor and assignment operator are deleted to disallow moving
    dataSource(dataSource&&) = delete;
    dataSource& operator=(dataSource&&) = delete;

    // Destructor is default-generated
    virtual ~dataSource() = default;

    void updateData();

    std::string getSourceName() const { return sourceName_; }
    private:
    std::string sourceName_ {};
};