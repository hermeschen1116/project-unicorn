import json
from math import sqrt
from typing import Any

import numpy
import numpy as np
from numpy import array
from sklearn import preprocessing
from torch import Tensor
from ts.torch_handler.base_handler import BaseHandler


class ModelHandler(BaseHandler):
	def __init__(self):
		super().__init__()
		self.context: Any = None
		self.initialized: bool = False
		self.explain: bool = False
		self.target: int = 0

	def initialize(self, context) -> None:
		self.context = context
		self.initialized = True

	def preprocess(self, request) -> Tensor:
		input_data: dict = json.load(request)
		model_input: array = numpy.zeros(7, dtype=np.float16)
		# Company Name Length
		model_input[0] = len(input_data['''company name'''])
		# Company Name Special Characters
		special_char: list = [
			'!', '"', '#', '$', '%', '&', "'",
			'(', ')', '*', '+', ',', '-', '.',
			'/', '0', '1', '2', '3', '4', '5',
			'6', '7', '8', '9', ':', ';', '<',
			'=', '>', '?', '@'
		]
		special_char_count: int = 0
		for c in input_data['''company name''']:
			if c in special_char:
				special_char_count += 1
		model_input[1] = special_char_count
		# Country
		country: dict = {'united states': 0, 'china': 1}
		if input_data['''country'''].lower() in country.keys():
			model_input[2] = country['''country''']
		else:
			model_input[2] = len(country)
		# City
		city: dict = {'san francisco': 0, 'new york': 1}
		if input_data['''city'''].lower() in city.keys():
			model_input[3] = city['''city''']
		else:
			model_input[3] = len(city)
		# Industry
		industry: dict = {
			'artificial intelligence': 0,
			'fintech': 1,
			'internet software & services': 2,
			'analytics': 3,
			'biotechnology': 4,
			'health care': 5,
			'e-commerce & direct-to-consumer': 6
		}
		if input_data['''industry'''].lower() in industry.keys():
			model_input[4] = industry['''industry''']
		model_input[4] = len(industry)
		# Investor
		investor: dict = {
			'andreessen horowitz': 0,
			'techstars': 1,
			'alumni ventures': 2,
			'y combinator': 3,
			'sequoia capital': 4,
			'500 global': 5,
			'insight partners': 6
		}
		if input_data['''investor'''].lower() in investor.keys():
			model_input[5] = investor['''investor''']
		model_input[5] = len(investor)
		# Last Valuation
		half = sqrt(10)
		scientific: list = '{:e}'.format(input_data['''last valuation''']).split('e')
		tail: float = float(scientific[0])
		power: int = int(scientific[1])
		if tail >= half:
			power += 1
		model_input[6] = power

		return Tensor(model_input)

	def inference(self, model_input, **kwargs) -> Tensor:
		data_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
		scaled_data: Tensor = Tensor(array(data_scaler.fit_transform(model_input)))

		return self.model(scaled_data)

	def postprocess(self, inference_output) -> str:
		return '{:.2f}%'.format(inference_output * 100)

	def handle(self, data, context) -> str:
		model_input: Tensor = self.preprocess(data)
		model_output = self.inference(model_input)

		return self.postprocess(model_output)
