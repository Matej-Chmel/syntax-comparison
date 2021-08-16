const printArr = (arr) => console.log(arr.join(" "));

function main() {
	const arr = [2, 3, 5, 7, 11]
	printArr(arr);

	arr.push(13);
	printArr(arr);

	arr.splice(0, 1);
	printArr(arr);

	console.log(arr[2]);
}

main()
