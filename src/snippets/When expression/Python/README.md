```python
try:
	msg = {
		1: "Monday",
		2: "Tuesday",
		3: "Wednesday",
		4: "Thursday",
		5: "Friday",
		6: "Saturday",
		7: "Sunday"
	}[n]
except KeyError:
	msg = "Invalid day"
```
