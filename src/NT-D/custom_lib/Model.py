import pytorch_lightning as pl
import torch
from pl_bolts.models import LinearRegression
from torch import optim, nn, Tensor
from torchmetrics.classification import BinaryAccuracy


class Model(pl.LightningModule):
	def __init__(self, learning_rate: float = 1e-4):
		super(Model, self).__init__()

		# predefined variables
		self.learning_rate: float = learning_rate
		# model
		self.__model = LinearRegression(input_dim=6, num_classes=2)
		self.__loss_fn = nn.BCELoss()

	def configure_optimizers(self):
		return optim.Adam(self.parameters(), lr=self.learning_rate)

	def forward(self, input_batch):
		output = self.__model(input_batch)

		return output

	def on_train_epoch_start(self) -> None:
		print('Epoch: {} starts'.format(self.current_epoch))

	def training_step(self, input_batch, input_batch_idx) -> dict:
		# forward
		data_batch, label_batch = input_batch
		predict_batch = self.forward(data_batch)
		train_loss = self.__loss_fn(predict_batch, label_batch)

		# log
		self.log('loss', train_loss, on_step=True, on_epoch=True, prog_bar=True)

		return {'loss': train_loss}

	def on_train_epoch_end(self) -> None:
		print('Train ends')

	def on_validation_epoch_start(self) -> None:
		print('Epoch: {} starts'.format(self.current_epoch))

	def validation_step(self, input_batch, input_batch_idx) -> dict:
		# forward
		data_batch, label_batch = input_batch
		predict_batch = self.forward(data_batch)
		valid_loss = self.__loss_fn(predict_batch, label_batch)

		# log
		self.log('valid_loss', valid_loss, on_step=True, on_epoch=True, prog_bar=True)

		return {'valid_loss': valid_loss}

	def on_validation_epoch_end(self) -> None:
		print('Validation ends')

	def on_test_epoch_start(self) -> None:
		print('Test starts')

	def test_step(self, input_batch, input_batch_idx) -> dict:
		# forward
		data_batch, label_batch = input_batch
		predict_batch = self.forward(data_batch)

		return {'truth_batch': data_batch, 'predict_batch': predict_batch}

	def test_epoch_end(self, batch_output) -> None:
		all_truth: Tensor = torch.stack([batch['truth_batch'] for batch in batch_output], dim=-1)
		all_predict: Tensor = torch.stack([batch['predict_batch'] for batch in batch_output], dim=-1)
		accuracy = BinaryAccuracy()
		print('Test Accuracy: {:.2f}'.format(accuracy(all_predict, all_truth)))

	def on_test_epoch_end(self) -> None:
		print('Test ends')

	def on_predict_start(self) -> None:
		print('start to predict...')

	def predict_step(self, input_data, input_data_idx, dataloader_idx: int = 0) -> dict:
		output = self.forward(input_data)

		return output

	def on_predict_end(self) -> None:
		print('prediction ends')
