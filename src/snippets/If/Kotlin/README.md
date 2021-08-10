```kotlin
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
```
