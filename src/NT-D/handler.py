import json
from typing import Any

from torch import Tensor
from ts.torch_handler.base_handler import BaseHandler


class ModelHandler(BaseHandler):
	def __init__(self):
		self.context: Any = None
		self.initialized: bool = False
		self.explain: bool = False
		self.target: int = 0

	def initialize(self, context) -> None:
		self.context = context
		self.initialized = True

	def preprocess(self, request) -> Tensor:
		input_data: dict = json.load(request)

	def inference(self, model_input):
		return self.model(model_input)

	def postprocess(self, inference_output) -> str:
		return '{:.2f}%'.format(inference_output * 100)

	def handle(self, data, context) -> str:
		model_input: Tensor = self.preprocess(data)
		model_output = self.inference(model_input)

		return self.postprocess(model_output)
