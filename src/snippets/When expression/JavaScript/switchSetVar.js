const rndNum = () => Math.floor(Math.random()*8 + 1);

function main() {
	let msg;
	let n = rndNum();

	switch(n) {
	case 1:
		msg = "Monday";
		break;
	case 2:
		msg = "Tuesday";
		break;
	case 3:
		msg = "Wednesday";
		break;
	case 4:
		msg = "Thursday";
		break;
	case 5:
		msg = "Friday";
		break;
	case 6:
		msg = "Saturday";
		break;
	case 7:
		msg = "Sunday";
		break;
	default:
		msg = "Invalid day";
	}
	console.log(`${n}: ${msg}`);
}

main()
