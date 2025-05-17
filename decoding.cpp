#include <iostream>
#include "huffman.hpp"
using namespace std;

// function takes the input arguments and then call the decompress function
int main(int argc, char* argv[]) {
    if (argc != 3) {
        cout << "Try again there are no files.";
		exit(1);
	}

    huffman f(argv[1], argv[2]);
    f.decompress();
    // above function follows the decompressing protocol
    cout << "Decompressed successfully" << endl;

    return 0;
}
