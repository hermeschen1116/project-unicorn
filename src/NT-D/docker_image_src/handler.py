import json
import os
from math import sqrt
from typing import Any

import numpy
import torch
from numpy import array
from sklearn import preprocessing
from torch import Tensor
from ts.torch_handler.base_handler import BaseHandler


class ModelHandler(BaseHandler):
	def __init__(self):
		super().__init__()
		self._context: Any = None
		self.initialized: bool = False
		self.model: Any = None
		self.device: Any = None

	def initialize(self, context) -> None:
		self.manifest = context.manifest
		properties = context.system_properties
		model_dir = properties.get("model_dir")
		self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

		# Read model serialize/pt file
		serialized_file = self.manifest['model']['serializedFile']
		model_pt_path = os.path.join(model_dir, serialized_file)
		if not os.path.isfile(model_pt_path):
			raise RuntimeError("Missing the model.pt file")

		self.model = torch.jit.load(model_pt_path)

		self.initialized = True

	def preprocess(self, request) -> Tensor:
		request_data: Any = request[0].get('data')
		if request_data is None:
			request_data = request[0].get('body')
		input_data: dict = json.loads(request_data)
		model_input: array = numpy.zeros(7, dtype=int)
		# Company Name Length
		model_input[0] = len(input_data['company'])
		# Company Name Special Characters
		special_char: list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
							  ';', '<', '=', '>', '?', '@']
		special_char_count: int = 0
		for c in input_data['company']:
			if c in special_char:
				special_char_count += 1
		model_input[1] = special_char_count
		# Country
		country: dict = {'united states': 0, 'china': 1}
		if input_data['nation'].lower() in country.keys():
			model_input[2] = country[input_data['nation'].lower()]
		else:
			model_input[2] = len(country)
		# City
		city: dict = {'san francisco': 0, 'new york': 1}
		if input_data['city'].lower() in city.keys():
			model_input[3] = city[input_data['city'].lower()]
		else:
			model_input[3] = len(city)
		# Industry
		industry: dict = {'artificial intelligence': 0, 'fintech': 1, 'internet software & services': 2, 'analytics': 3, 'biotechnology': 4, 'health care': 5,
						  'e-commerce & direct-to-consumer': 6}
		if input_data['industry'].lower() in industry.keys():
			model_input[4] = industry[input_data['industry'].lower()]
		else:
			model_input[4] = len(industry)
		# Investor
		investor: dict = {'andreessen horowitz': 0, 'techstars': 1, 'alumni ventures': 2, 'y combinator': 3, 'sequoia capital': 4, '500 global': 5,
						  'insight partners': 6}
		if input_data['investor'].lower() in investor.keys():
			model_input[5] = investor[input_data['investor'].lower()]
		else:
			model_input[5] = len(investor)
		# Last Valuation
		half = sqrt(10)
		scientific: list = '{:e}'.format(int(input_data['last_valuation'])).split('e')
		tail: float = float(scientific[0])
		power: int = int(scientific[1])
		if tail >= half:
			power += 1
		model_input[6] = power

		return Tensor(model_input.reshape(1, -1))

	def inference(self, model_input, **kwargs) -> Tensor:
		with torch.no_grad():
			return self.model(model_input)

	def postprocess(self, inference_output) -> list:
		return [output.item() for output in inference_output]

	def handle(self, data, context) -> list:
		model_input: Tensor = self.preprocess(data)
		model_output = self.inference(model_input)
		response: list = self.postprocess(model_output)

		return response
