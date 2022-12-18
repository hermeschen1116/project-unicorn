import numpy as np

import pytorch_lightning as pl
from pandas import DataFrame
from torch import tensor
from torch.utils.data import DataLoader, Dataset


class CSVDataset(Dataset):
	def __init__(self, data_set: DataFrame, label_feature: str):
		self.__data: tensor = tensor(data_set.drop(label_feature, axis=1).astype(np.float))
		self.__label: tensor = tensor(data_set[label_feature].astype(np.int))

	def __getitem__(self, index) -> (tensor, tensor):
		return self.__data[index], self.__label[index]

	def __len__(self) -> int:
		return len(self.__label)


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
