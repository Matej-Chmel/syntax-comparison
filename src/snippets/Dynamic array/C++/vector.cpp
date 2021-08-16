#include <iostream>
#include <vector>

void printVec(const std::vector<int>& v) {
	const auto lastIdx = v.size() - 1;

	for(size_t i = 0; i < lastIdx; i++)
		std::cout << v[i] << ' ';
	std::cout << v[lastIdx] << '\n';
}

int main() {
	std::vector<int> primes{2, 3, 5, 7, 11};
	printVec(primes);

	primes.push_back(13);
	printVec(primes);

	primes.erase(primes.begin());
	printVec(primes);

	std::cout << primes[2] << '\n';
	return 0;
}
