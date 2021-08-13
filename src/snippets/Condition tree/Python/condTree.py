def compare(a: int, b: int):
	printNums(a, b)

	if a > b:
		msg = "a > b"
		a += 1
	elif a < b:
		msg = "a < b"
		b += 1
	else:
		msg = "a == b"
		a += 1
		b += 1

	print(msg)
	printNums(a, b)
	print()

def printNums(a, b):
	print(f"{a = }, {b = }")

def main():
	for a in range(1, 4):
		for b in range(1, 4):
			compare(a, b)

if __name__ == "__main__":
	main()
