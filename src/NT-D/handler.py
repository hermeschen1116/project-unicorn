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
		model_input[0] = int(input_data['name_len'])
		# Company Name Special Characters
		model_input[1] = int(input_data['name_sp'])
		# Country
		model_input[2] = int(input_data['country'])
		# City
		model_input[3] = int(input_data['city'])
		# Industry
		model_input[4] = int(input_data['industry'])
		# Investor
		model_input[3] = int(input_data['investor'])
		# Last Valuation
		half = sqrt(10)
		scientific: list = '{:e}'.format(int(input_data['last_valuation'])).split('e')
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
