from typing import Optional

import numpy as np
import pytorch_lightning as pl
from pandas import DataFrame
from sklearn.model_selection import KFold
from torch import tensor
from torch.utils.data import DataLoader, Dataset, random_split, Subset


class CSVDataset(Dataset):
	def __init__(self, data_set: DataFrame, label_feature: str):
		self.__data: tensor = tensor(data_set.drop(label_feature, axis=1).astype(np.float))
		self.__label: tensor = tensor(data_set[label_feature].astype(np.int))

	def __getitem__(self, index) -> (tensor, tensor):
		return self.__data[index], self.__label[index]

	def __len__(self) -> int:
		return len(self.__label)


class QADataModule(pl.LightningDataModule):
	def __init__(self, data: DataFrame, train_partition: float = 0.9, num_worker: int = 4, batch_size: int = 8):
		super().__init__()
		self.save_hyperparameters(logger=False)

		# predefined parameters
		self.__train_partition: float = train_partition
		self.__num_worker: int = num_worker
		self.__batch_size: int = batch_size
		self.__num_folds: Optional[int] = None
		# datasets
		self.__folds: Optional[list] = None
		self.__train_data: Optional[Dataset] = CSVDataset(data, 'Unicorn')
		self.__train_folds: Optional[Subset] = None
		self.__valid_folds: Optional[Subset] = None
		self.__test_set: Optional[Dataset] = None

	def prepare_data(self) -> None:
		return

	def setup(self, stage: str) -> None:
		train_data_partition = int(len(self.__val_set) * self.__train_partition)
		test_data_partition = len(self.__val_set) - train_data_partition
		self.__train_data, self.__test_set = random_split(self.__train_data, [train_data_partition, test_data_partition])

	def setup_folds(self, num_folds: int = 5) -> None:
		self.__num_folds = num_folds
		self.__folds = [fold for fold in KFold(num_folds).split(range(len(self.__train_data)))]

	def setup_fold_index(self, fold_index: int) -> None:
		train_index, valid_index = self.splits[fold_index]
		self.__train_folds = Subset(self.__train_data, train_index)
		self.__valid_folds = Subset(self.__train_data, valid_index)

	def train_dataloader(self) -> DataLoader:
		return DataLoader(self.__train_folds, shuffle=True, batch_size=self.__batch_size, num_workers=self.__num_worker)

	def val_dataloader(self) -> DataLoader:
		return DataLoader(self.__valid_folds, batch_size=self.__batch_size, num_workers=self.__num_worker)

	def test_dataloader(self) -> DataLoader:
		return DataLoader(self.__test_set, batch_size=self.__batch_size, num_workers=self.__num_worker)

	# def predict_dataloader(self) -> DataLoader:
	# 	return DataLoader(self.__predict_set, batch_size=self.__batch_size, num_workers=self.__num_worker)
