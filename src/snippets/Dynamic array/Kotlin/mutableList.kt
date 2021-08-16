fun printList(l: List<Int>) = println(l.joinToString(" "))

fun main() {
	val primes = mutableListOf(2, 3, 5, 7, 11)
	printList(primes)

	primes.add(13)
	printList(primes)

	primes.removeAt(0)
	printList(primes)

	println(primes[2])
}
