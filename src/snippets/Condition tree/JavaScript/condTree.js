function compare(a, b) {
	let msg;
	print(a, b);

	if(a > b) {
		msg = "a > b";
		a++;
	} else if(a < b) {
		msg = "a < b";
		b++;
	} else {
		msg = "a == b";
		a++;
		b++;
	}
	console.log(msg);
	print(a, b);
	console.log();
}
function print(a, b) {
	console.log(`a = ${a}, b = ${b}`);
}

function main() {
	for(let a = 1; a <= 3; a++)
		for(let b = 1; b <= 3; b++)
			compare(a, b);
}

main()
