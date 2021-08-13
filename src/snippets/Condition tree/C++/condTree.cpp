#include <iostream>
#include <string>

void print(const int a, const int b) {
	std::cout << "a = " << a << ", b = " << b << '\n';
}
void compare(int a, int b) {
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
	std::cout << '\n';
}

int main() {
	for(int a = 1; a <= 3; a++)
		for(int b = 1; b <= 3; b++)
			compare(a, b);
	return 0;
}
