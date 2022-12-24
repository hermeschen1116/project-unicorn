async function request() {
	let company = document.getElementById('Name').value
	let city = document.getElementById('City').value
	let nation = document.getElementById('Nation').value
	let industry = document.getElementById('Industry').value
	let investor = document.getElementById('Investor').value
	let valuation = document.getElementById('Last_Valuation').value
	await eel.prediction(company, nation, city, industry, investor, valuation)(call_Back)
}

function call_Back(result) {
	document.getElementById('prediction').textContent = result
}
