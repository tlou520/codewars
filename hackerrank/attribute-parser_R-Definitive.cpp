//https://www.hackerrank.com/challenges/attribute-parser/problem
//Done 29/07/2025
#include <iostream>
#include <unordered_map>
#include <sstream>
#include <string>
#include <fstream>
#include <vector>
#include <memory>


struct TagData {
    std::string etiquetteNumber;
    std::unordered_map<std::string, std::string> attributes;
    std::vector<std::unique_ptr<TagData>> children;
    TagData* parent = nullptr;

    // Adds a child and sets its parent
    TagData* addChild(std::unique_ptr<TagData> child) {
        child->parent = this;
        children.push_back(std::move(child));
        return children.back().get(); // Return pointer to the added child
    }
};



class Parser {
private:
    int N;
    int Q;
    int index = 0;

    std::vector<std::unique_ptr<TagData>> roots;
    std::unique_ptr<TagData> root_first;  // Owns the initial TagData
    TagData* current;



    std::string etiquetteNumber;
    std::unordered_map<std::string, std::string> attributes;

    Parser(int dummy) { /* another constructor */ }

public:
    
    Parser() {
        std::cin >> N >> Q;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // discard leftover newline
        this->current = nullptr;
    }



    int get_N() const {
        return N;
    }

    int get_Q() const {
        return Q;
    }

    void PrintValue(std::string value)
    {
        std::cout << value << std::endl;
    }
    
    void NotFound()
    {
        std::cout << "Not Found!" << std::endl;
    }

    // Method to parse a line into a Tag object
    void parse(std::string_view line) {
        Parser tag(0);
        
        // Create root
        auto node = std::make_unique<TagData>();

        //Detecting closing tag and returning who is the one that have to close it and not iterate over

        if (line.compare(0, 2, "</") == 0 &&
    line.back() == '>' && line.size() >= 4) {
            std::string_view tag_temp = line.substr(2, line.size() - 3);

            while (current != nullptr) {
                if (current->etiquetteNumber.find(tag_temp) != std::string::npos) {
                    // Match found
                    current = current->parent;
                    return;
                }
                current = current->parent;
            }
            return;
        }

        //It is not closing tag
        // Remove the opening '<' and closing '>'
        line.remove_prefix(1);
        line.remove_suffix(1);
        std::string line_string(line);
        std::istringstream iss(line_string);
        std::string token;


        // If current parent is null then it is a root and store in another root
        if (current == nullptr)
        {
            auto root = std::make_unique<TagData>();
            iss >> root->etiquetteNumber;
            roots.push_back(std::move(root));
            current = roots.back().get();
        }
        // Otherwise is a child
        else
        {
            auto child = std::make_unique<TagData>();
            iss >> child->etiquetteNumber;
            TagData* childPtr = current->addChild(std::move(child));
            current = childPtr;
        }
        
        // Parse remaining tokens as attribute=value
        while (iss >> token) {
            std::string key = token;

            iss >> token; // should be '='
            iss >> token; // should be value

            std::string value = token;

            // Clean the surrounding quotes
            if (!value.empty() && value.front() == '"') value.erase(0, 1);
            if (!value.empty() && value.back() == '"') value.pop_back();

            current->attributes[key] = value;
        }
    }

    void Queries(std::string_view line)
    {
        auto tilde_pos = line.find('~');
        TagData* current = nullptr;
        auto* list = &roots;
        std::string_view token;

        std::string_view path = line.substr(0, tilde_pos);
        std::string_view attribute = line.substr(tilde_pos + 1);

        size_t start = 0;
        // Loop as long as 'start' hasn't walked past the end of 'path'
        while (start <= path.size()) {
            // find the next dot (or npos)
            size_t end = path.find('.', start);
            // compute token length by capping 'end' at path.size()
            size_t len = std::min(end, path.size()) - start;

            // extract and handle this token
            token = path.substr(start, len);

            while (true) {
                bool found = false;
                for (auto& node : *list) {
                    if (node->etiquetteNumber == token) {
                        current = node.get();
                        list = &current->children;
                        
                        found = true;
                        break;
                    }
                }
                if (found)
                {
                    break;
                }
                else
                {
                    std::cout << "Not Found!" << std::endl;
                    return;
                }

                // Update token as needed here (e.g., to next segment in a path)
                // If there's no further token to match, break the loop
            }
            
            start += len + 1;
        }

        
        auto it = current->attributes.find(std::string(attribute));
        if (it != current->attributes.end()) {
            std::cout << it->second << std::endl;
        } else {
            std::cout << "Not Found!" << std::endl;
        }
        return;
    }

};


int main() {
    Parser p;

    std::string line;
    int line_count = 0;
    int line_count_queries = 0;
    // You can access the values like this:
    int first = p.get_N();
    int second = p.get_Q();


    // Read first sectoin of parsing
    while (line_count < first && std::getline(std::cin, line)) {
        p.parse(line);
        ++line_count;
    }

    // From here on, continue reading lines as needed
    while (line_count_queries < second && std::getline(std::cin, line)) {
        p.Queries(line);
        ++line_count_queries;
    }

    return 0;
}