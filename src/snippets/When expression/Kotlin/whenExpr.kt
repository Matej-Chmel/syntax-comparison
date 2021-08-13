fun printDay(n: Int) {
	val msg = when (n) {
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

fun main() {
	(0..8).forEach(::printDay)
}
