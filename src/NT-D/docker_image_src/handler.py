import json
import os
from math import sqrt
from typing import Any

import numpy
import numpy as np
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
		model_input[5] = int(input_data['investor'])
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
		data_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
		scaled_data: Tensor = Tensor(array(data_scaler.fit_transform(model_input)))

		with torch.no_grad():
			return self.model(scaled_data)

	def postprocess(self, inference_output) -> list:
		return [inference_output.item() * 100]

	def handle(self, data, context) -> list:
		model_input: Tensor = self.preprocess(data)
		model_output = self.inference(model_input)

		return self.postprocess(model_output)
