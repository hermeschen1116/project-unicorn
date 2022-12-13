import pytorch_lightning as pl
from torch.utils.data import DataLoader


class QADataModule(pl.LightningDataModule):
	def __init__(self, source_dir: str = 'source/', tokenizer_name: str = 'bert-base-uncased', num_worker: int = 4, batch_size: int = 8):
		super().__init__()

	# def setup(self, stage: str) -> None:
	# 	val_set_split = int(len(self.__val_set) * 0.8)
	# 	test_set_split = len(self.__val_set) - val_set_split
	# 	self.__val_set, self.__test_set = random_split(self.__val_set, [val_set_split, test_set_split])

	def train_dataloader(self) -> DataLoader:
		return DataLoader(self.__train_set, shuffle=True, batch_size=self.__batch_size, num_workers=self.__num_worker)

	def val_dataloader(self) -> DataLoader:
		return DataLoader(self.__val_set, batch_size=self.__batch_size, num_workers=self.__num_worker)

	# def test_dataloader(self) -> DataLoader:
	# 	return DataLoader(self.__test_set, batch_size=self.__batch_size, num_workers=self.__num_worker)

	def predict_dataloader(self) -> DataLoader:
		return DataLoader(self.__predict_set, batch_size=self.__batch_size, num_workers=self.__num_worker)
