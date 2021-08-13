fun compare(_a: Int, _b: Int) {
	var a = _a
	var b = _b
	lateinit var msg: String
	printNums(a, b)

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
	println(msg)
	printNums(a, b)
	println()
}
fun printNums(a: Int, b: Int) = println("a = $a, b = $b")

fun main() {
	(1..3).forEach { a ->
		(1..3).forEach { b ->
			compare(a, b)
		}
	}
}
