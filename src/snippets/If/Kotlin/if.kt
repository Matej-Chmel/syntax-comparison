fun main() {
	var a = (1 until 5).random()
	var b = (1 until 5).random()
	lateinit var msg: String
	println("a = $a, b = $b")

	when {
		a > b -> {
			msg = "a > b"
			a++
		}
		a < b -> {
			msg = "a < b"
			b++
		}
		else -> {
			msg = "a == b"
			a++
			b++
		}
	}
	println("$msg\na = $a, b = $b")
}
