const rndNum = () => Math.floor(Math.random() * 5 + 1);

function main() {
	let a = rndNum();
	let b = rndNum();
	let msg;
	console.log(`a = ${a}, b = ${b}`);

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
	console.log(`${msg}\na = ${a}, b = ${b}`);
}

main()
