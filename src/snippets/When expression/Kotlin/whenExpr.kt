fun main() {
	lateinit var msg: String
	val n = (1..8).random()

	msg = when (n) {
		1 -> "Monday"
		2 -> "Tuesday"
		3 -> "Wednesday"
		4 -> "Thursday"
		5 -> "Friday"
		6 -> "Saturday"
		7 -> "Sunday"
		else -> "Invalid day"
	}

	println("$n: $msg")
}
