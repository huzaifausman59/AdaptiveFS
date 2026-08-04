#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> numbers = {1, 2, 3, 4, 5};
    cout << "Sum: ";
    int total = 0;
    for (int n : numbers) {
        total += n;
    }
    cout << total << endl;
    return 0;
}
