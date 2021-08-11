#include <iostream>
#include <random>
#include <string>

auto rndNum() {
	std::mt19937 gen(std::random_device{}());
	std::uniform_int_distribution dis(1, 9);
	return dis(gen);
}

int main() {
	std::string msg;
	auto n = rndNum();

	switch(n) {
	case 1:
		msg = "Monday";
		break;
	case 2:
		msg = "Tuesday";
		break;
	case 3:
		msg = "Wednesday";
		break;
	case 4:
		msg = "Thursday";
		break;
	case 5:
		msg = "Friday";
		break;
	case 6:
		msg = "Saturday";
		break;
	case 7:
		msg = "Sunday";
		break;
	default:
		msg = "Invalid day";
	}

	std::cout << n << ": " << msg << '\n';
	return 0;
}
