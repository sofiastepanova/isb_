#include <iostream>
#include <fstream>
#include <bitset>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::bitset<128> random_bits;

    for (int i = 0; i < 128; i++) {
        random_bits[i] = gen() & 1;
    }

    std::cout << random_bits << std::endl;

    std::ofstream out_file("random_bits.txt");
    out_file << random_bits;
    out_file.close();

    return 0;
}