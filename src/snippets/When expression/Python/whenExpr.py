def printDay(n: int):
	try:
		msg = {
			1: "Monday",
			2: "Tuesday",
			3: "Wednesday",
			4: "Thursday",
			5: "Friday",
			6: "Saturday",
			7: "Sunday"}[n]
	except KeyError:
		msg = "Invalid day"

	print(f"{n}: {msg}")

def main():
	for i in range(0, 9):
		printDay(i)

if __name__ == "__main__":
	main()
