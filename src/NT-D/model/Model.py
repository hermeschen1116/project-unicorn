import pytorch_lightning as pl
from torch import optim


class Model(pl.LightningModule):
	def __init__(self, learning_rate: float = 1e-4):
		super(Model, self).__init__()

	def configure_optimizers(self):
		return optim.Adam(self.parameters(), lr=self.learning_rate)

	def forward(self, input_batch):
		return output

	def on_train_epoch_start(self) -> None:
		print('Epoch: {} starting to train...'.format(self.current_epoch))

	def training_step(self, input_batch, input_batch_idx) -> dict:
		return {'loss': loss}

	def on_train_epoch_end(self) -> None:
		print('training ends')

	def on_validation_epoch_start(self) -> None:
		print('Epoch: {} starting to validate...'.format(self.current_epoch))

	def validation_step(self, input_batch, input_batch_idx) -> dict:
		return {'val_loss': loss}

	def on_validation_epoch_end(self) -> None:
		print('validation ends')

	def on_test_epoch_start(self) -> None:
		print('start to test...')

	def test_step(self, input_batch, input_batch_idx) -> dict:
		return {'predict': predictions, 'truth': truths}

	def test_epoch_end(self, batch_output) -> None:

	def on_test_epoch_end(self) -> None:
		print('testing ends')

	def on_predict_start(self) -> None:
		print('start to predict...')

	def predict_step(self, input_batch, input_batch_idx, dataloader_idx: int = 0) -> dict:
		return {'questions': questions, 'answers': answers}

	def on_predict_end(self) -> None:
		print('prediction ends')
