from random import randint

def main():
	a = randint(1, 5)
	b = randint(1, 5)
	print(f"{a = }, {b = }")

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

	print(msg, f"{a = }, {b = }", sep="\n")

if __name__ == "__main__":
	main()
