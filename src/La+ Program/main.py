import json

import eel
import requests

host_address: str = 'localhost'
inference_port: int = 8080


@eel.expose
def prediction(company: str, nation: str, city: str, industry: str, investor: str, last_valuation: str) -> str:
	request_data: dict = {'company': company, 'nation': nation, 'city': city, 'industry': industry, 'investor': investor, 'last_valuation': last_valuation}

	result = requests.post('http://{}:{}/predictions/NT-D'.format(host_address, inference_port), data=json.dumps(request_data))

	return '{:.2f}%'.format(result.json() * 100) if type(result.json()) is float else 'Input Error'


eel.init('.')
eel.start('page.html', mode='default')
