def printList(l: list[int]):
	print(" ".join(map(str, l)))

def main():
	primes = [2, 3, 5, 7, 11]
	printList(primes)

	primes.append(13)
	printList(primes)

	del primes[0]
	printList(primes)

	print(primes[2])

if __name__ == "__main__":
	main()
