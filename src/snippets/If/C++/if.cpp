#include <iostream>
#include <random>
#include <string>

void print(const int a, const int b) {
	std::cout << "a = " << a << ", b = " << b << '\n';
}
auto rndNum() {
	static std::mt19937 gen(std::random_device{}());
	static std::uniform_int_distribution dis(1, 5);
	return dis(gen);
}

int main() {
	auto a = rndNum();
	auto b = rndNum();
	std::string msg;
	print(a, b);

	if(a > b) {
		msg = "a > b";
		a++;
	} else if(a < b) {
		msg = "a < b";
		b++;
	} else {
		msg = "a == b";
		a++;
		b++;
	}

	std::cout << msg << '\n';
	print(a, b);
	return 0;
}
