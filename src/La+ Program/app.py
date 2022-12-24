# importing library
import eel
import numpy
import torch


# initialize

def count_special_char(name: str) -> int:
	special_char: list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';',
						  '<', '=', '>', '?', '@']
	special_char_count: int = 0
	for c in name:
		if c in special_char:
			special_char_count += 1

	return special_char_count


@eel.expose
def prediction(company: str, city: str, nation: str, industry: str, investor: str, last_valuation: str) -> str:
	model = torch.jit.load('production.pt')
	request: list = [len(company), count_special_char(company), nation, city, industry, investor, last_valuation]
	model_input: torch.Tensor = torch.Tensor(numpy.array(request, dtype=int).reshape(1, -1))

	return '{:.2f}%'.format(model(model_input).item() * 100)


eel.init('.')
# start
eel.start('laplusprogram.html', mode='default')
