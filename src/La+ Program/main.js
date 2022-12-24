async function request() {
	let company_name = document.getElementById("Name").value
	let city = document.getElementById("City").value
	let nation = document.getElementById("Nation").value
	let industry = document.getElementById("Industry").value
	let investor = document.getElementById("Investor").value
	let valuation = document.getElementById("Last_Valuation").value
	await eel.prediction(company_name, city, nation, industry, investor, valuation)(call_Back)
	// a little weird https://youtu.be/IbGJaTkyuXA?t=239
}

function call_Back(result) {
	document.getElementById("prediction").textContent = result
}
