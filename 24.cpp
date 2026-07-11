#include <iostream>   // For console input/output (cin, cout)
#include <string>     // For std::string
#include <vector>     // For dynamic arrays (std::vector)
#include <fstream>    // For file handling (reading/writing files)
#include <stdexcept>  // For standard exceptions

// ========================== CLASS (OOP) ==========================
class Rectangle {
private:
    double width, height;

public:
    // Constructor (initializer list)
    Rectangle(double w, double h) : width(w), height(h) {}

    // Method (member function)
    double area() const {
        return width * height;
    }

    // Getter (encapsulation)
    double getWidth() const { return width; }
    double getHeight() const { return height; }

    // Static method (belongs to class, not instance)
    static std::string shapeName() {
        return "Rectangle";
    }
};

// ========================== FUNCTIONS ==========================

// Pass by value (copy)
int add(int a, int b) {
    return a + b;
}

// Pass by reference (modifies original variable)
void increment(int &num) {
    num += 1;
}

// Pass by const reference (read-only, avoids copying)
void printString(const std::string &text) {
    std::cout << "String: " << text << std::endl;
}

// Function with default argument
void greet(std::string name = "Guest") {
    std::cout << "Hello, " << name << "!" << std::endl;
}

// ========================== MAIN ==========================
int main() {
    // ---- 1. VARIABLES & DATA TYPES ----
    int integer = 42;                 // Whole number
    double pi = 3.14159;              // Floating point
    char letter = 'A';                // Single character
    bool isCodingFun = true;          // Boolean (true/false)
    std::string name = "Alice";       // String (text)

    std::cout << "\n--- FUNDAMENTALS DEMO ---\n";

    // ---- 2. INPUT / OUTPUT ----
    std::cout << "Integer: " << integer << std::endl;
    std::cout << "Double: " << pi << std::endl;
    std::cout << "Char: " << letter << std::endl;
    std::cout << "Bool: " << std::boolalpha << isCodingFun << std::endl; // prints 'true'

    int userAge;
    std::cout << "Enter your age: ";
    std::cin >> userAge;  // Take user input
    std::cout << "You are " << userAge << " years old.\n";

    // ---- 3. CONDITIONALS (if/else, switch) ----
    if (userAge >= 18) {
        std::cout << "You are an adult." << std::endl;
    } else {
        std::cout << "You are a minor." << std::endl;
    }

    switch (userAge % 2) {
        case 0: std::cout << "Your age is even.\n"; break;
        case 1: std::cout << "Your age is odd.\n"; break;
    }

    // ---- 4. LOOPS (for, while, do-while) ----
    std::cout << "\nFor loop (0 to 4): ";
    for (int i = 0; i < 5; ++i) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    std::cout << "While loop (countdown 3 to 1): ";
    int count = 3;
    while (count > 0) {
        std::cout << count << " ";
        --count;
    }
    std::cout << std::endl;

    std::cout << "Do-while (runs at least once): ";
    int x = 0;
    do {
        std::cout << x << " ";
        ++x;
    } while (x < 0);  // condition false, but runs once
    std::cout << std::endl;

    // ---- 5. ARRAYS & VECTORS (standard library dynamic array) ----
    int fixedArr[3] = {10, 20, 30};   // C-style array (fixed size)
    std::cout << "C-array first element: " << fixedArr[0] << std::endl;

    std::vector<int> nums = {5, 10, 15, 20};  // Dynamic, resizable
    nums.push_back(25);  // Add element at end

    std::cout << "Vector elements: ";
    for (int val : nums) {   // Range-based for loop
        std::cout << val << " ";
    }
    std::cout << std::endl;

    // ---- 6. POINTERS & REFERENCES ----
    int value = 100;
    int *ptr = &value;       // Pointer stores address of value
    int &ref = value;        // Reference is an alias to value

    std::cout << "Value: " << value << std::endl;
    std::cout << "Pointer deref: " << *ptr << std::endl;  // Access via pointer
    std::cout << "Reference: " << ref << std::endl;

    *ptr = 200;  // Change via pointer
    std::cout << "After *ptr=200, value: " << value << std::endl;

    // ---- 7. FUNCTION CALLS ----
    std::cout << "\nAdd(5,3) = " << add(5, 3) << std::endl;

    int num = 10;
    increment(num);  // Pass by reference
    std::cout << "After increment(num): " << num << std::endl;

    greet("Bob");
    greet();  // Uses default argument "Guest"

    // ---- 8. CLASSES & OBJECTS ----
    Rectangle rect(4.5, 3.2);
    std::cout << "\nRectangle width: " << rect.getWidth()
              << ", height: " << rect.getHeight() << std::endl;
    std::cout << "Area: " << rect.area() << std::endl;
    std::cout << "Shape name (static): " << Rectangle::shapeName() << std::endl;

    // ---- 9. FILE HANDLING (write & read) ----
    std::ofstream outFile("example.txt");  // Create/write file
    if (outFile.is_open()) {
        outFile << "Hello, file!\nThis is line 2.";
        outFile.close();
        std::cout << "\n✅ File written successfully.\n";
    } else {
        std::cout << "❌ Failed to write file.\n";
    }

    std::ifstream inFile("example.txt");
    std::string line;
    if (inFile.is_open()) {
        std::cout << "File contents:\n";
        while (std::getline(inFile, line)) {
            std::cout << line << std::endl;
        }
        inFile.close();
    } else {
        std::cout << "❌ Failed to read file.\n";
    }

    // ---- 10. EXCEPTION HANDLING ----
    try {
        int divisor;
        std::cout << "\nEnter a number to divide 100 by: ";
        std::cin >> divisor;

        if (divisor == 0) {
            throw std::runtime_error("Division by zero is not allowed!");
        }
        double result = 100.0 / divisor;
        std::cout << "100 / " << divisor << " = " << result << std::endl;

    } catch (const std::exception &e) {
        std::cout << "⚠️  Error caught: " << e.what() << std::endl;
    }

    std::cout << "\n--- Program finished successfully ---\n";
    return 0;  // Indicate successful execution
}