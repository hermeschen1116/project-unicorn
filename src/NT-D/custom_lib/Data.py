from typing import Optional

import lightning
import numpy as np
from pandas import DataFrame
from torch import Tensor
from torch.utils.data import DataLoader, Dataset, random_split


class CSVDataset(Dataset):
	def __init__(self, data_set: DataFrame, label_feature: str):
		self.__data: Tensor = Tensor(data_set.drop(label_feature, axis=1).astype(np.float32).to_numpy().reshape(-1, 1, len(data_set.columns) - 1))
		self.__label: Tensor = Tensor(data_set[label_feature].astype(np.int32).to_numpy())

	def __getitem__(self, index) -> (Tensor, Tensor):
		return self.__data[index], self.__label[index]

	def __len__(self) -> int:
		return len(self.__label)


class DataModule(lightning.LightningDataModule):
	def __init__(self, data: DataFrame, train_partition: float = 0.8, num_worker: int = 4, batch_size: int = 8):
		super().__init__()
		self.save_hyperparameters()

		# predefined parameters
		self.__train_partition: float = train_partition
		self.__num_worker: int = num_worker
		self.__batch_size: int = batch_size
		# datasets
		self.__train_set: Optional[CSVDataset] = CSVDataset(data, 'Unicorn')
		self.__valid_set: Optional[CSVDataset] = None
		self.__test_set: Optional[Dataset] = None

	def prepare_data(self) -> None:
		return

	def setup(self, stage: str) -> None:
		test_data_partition: int = int(len(self.__train_set) * 0.1)
		train_data_partition: int = len(self.__train_set) - test_data_partition
		valid_data_partition: int = int(train_data_partition * (1 - self.__train_partition))
		train_data_partition -= valid_data_partition
		self.__train_set, self.__valid_set, self.__test_set = random_split(self.__train_set, [train_data_partition, valid_data_partition, test_data_partition])

	def train_dataloader(self) -> DataLoader:
		return DataLoader(self.__train_set, shuffle=True, batch_size=self.__batch_size, num_workers=self.__num_worker)

	def val_dataloader(self) -> DataLoader:
		return DataLoader(self.__valid_set, batch_size=self.__batch_size, num_workers=self.__num_worker)

	def test_dataloader(self) -> DataLoader:
		return DataLoader(self.__test_set, batch_size=self.__batch_size, num_workers=self.__num_worker)

	# def predict_dataloader(self) -> DataLoader:
	# 	return DataLoader(self.__predict_set, batch_size=self.__batch_size, num_workers=self.__num_worker)
