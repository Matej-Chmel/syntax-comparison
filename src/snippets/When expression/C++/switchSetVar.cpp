#include <iostream>
#include <string>

void printDay(const int n) {
	std::string msg;

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
}

int main() {
	for(int i = 0; i <= 8; i++)
		printDay(i);
	return 0;
}
