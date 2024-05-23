// a pure virtual class
#pragma once
#include <string_view>
#include <string>
#include <iostream>

class dataSource {
    public:
    // Constructor is deleted to disallow default construction
    dataSource() = delete;

    // Constructor takes a string_view for the source name
    dataSource(std::string_view sourceName);

    // Copy constructor and assignment operator are deleted to disallow copying
    dataSource(const dataSource&) = delete;
    dataSource& operator=(const dataSource&) = delete;

    // Move constructor and assignment operator are deleted to disallow moving
    dataSource(dataSource&&) = delete;
    dataSource& operator=(dataSource&&) = delete;

    // make this class pure virtual
    virtual ~dataSource() = 0;

    void updateData();

    std::string getSourceName() const { return sourceName_; }
    private:
    std::string sourceName_ {};
};