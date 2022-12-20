import lightning
import numpy
from torch import optim, nn, Tensor
from torchmetrics.classification import BinaryAccuracy


class Model(lightning.LightningModule):
	def __init__(self, learning_rate: float = 1e-4):
		super(Model, self).__init__()

		# predefined variables
		self.learning_rate: float = learning_rate
		# model
		self.linear_1 = nn.Linear(7, 5)
		self.linear_2 = nn.Linear(5, 1)
		self.activation = nn.Sigmoid()
		self.loss_fn = nn.BCELoss()

	def configure_optimizers(self):
		return optim.Adam(self.parameters(), lr=self.learning_rate)

	def forward(self, input_batch):
		linear_output = self.linear_1(input_batch)
		linear_output = self.linear_2(linear_output)

		return self.activation(linear_output)

	@staticmethod
	def stack_output(output: list) -> Tensor:
		concat_list: list = []
		for o in output:
			concat_list += o.tolist()

		return Tensor(numpy.array(concat_list))

	def training_step(self, input_batch, input_batch_idx, dataloader_idx: int = 0) -> dict:
		# forward
		data_batch, label_batch = input_batch
		predict_batch = self.forward(data_batch)
		train_loss = self.loss_fn(predict_batch.flatten(), label_batch)

		# log
		self.log('loss', train_loss, on_epoch=True, on_step=True, prog_bar=True)

		return {'loss': train_loss}

	def validation_step(self, input_batch, input_batch_idx, dataloader_idx: int = 0) -> dict:
		# forward
		data_batch, label_batch = input_batch
		predict_batch = self.forward(data_batch)
		valid_loss = self.loss_fn(predict_batch.flatten(), label_batch)

		# log
		self.log('valid_loss', valid_loss, on_epoch=True, on_step=True, prog_bar=True)

		return {'valid_loss': valid_loss}

	def on_test_epoch_start(self) -> None:
		print('Test starts')

	def test_step(self, input_batch, input_batch_idx, dataloader_idx: int = 0) -> dict:
		# forward
		data_batch, label_batch = input_batch
		predict_batch = self.forward(data_batch)

		return {'truth_batch': label_batch, 'predict_batch': predict_batch.flatten()}

	def test_epoch_end(self, batch_output) -> None:
		all_predict: Tensor = self.stack_output([batch['predict_batch'] for batch in batch_output])
		all_truth: Tensor = self.stack_output([batch['truth_batch'] for batch in batch_output])
		metric = BinaryAccuracy()
		accuracy = metric(all_predict, all_truth)
		self.log('Accuracy', accuracy, on_epoch=True, prog_bar=True)
		print('Test Accuracy: {:.2f}%'.format(accuracy * 100))

	def on_test_epoch_end(self) -> None:
		print('Test ends')

	def on_predict_start(self) -> None:
		print('start to predict...')

	def predict_step(self, input_data, input_data_idx, dataloader_idx: int = 0) -> dict:
		output = self.forward(input_data)

		return output

	def on_predict_end(self) -> None:
		print('prediction ends')
