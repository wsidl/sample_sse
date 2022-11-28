let es = new EventSource("http://localhost/sse");
let alertList = document.getElementById("alerts");

es.addEventListener("NewAlert", event => {
	let main = document.createElement("li");
	if(event.data === "1") return;
	let eventData = JSON.parse(event.data);
	main.innerHTML = `<b>Alert Key</b> = ${eventData["key"]}<br/><b>Server</b> = ${eventData["server"]}<br/><b>Random Number</b> = ${eventData["message"]}`
	alertList.appendChild(main);
});
es.addEventListener("error", err => {
	console.error("EventSource failed with error");
	console.log(Object.keys(err));
	for( let pair of Object.entries(err)){
		console.info(`${pair[0]} = "${pair[1]}"`)
	}
});
