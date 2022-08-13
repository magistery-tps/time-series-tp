import torch
from torch.utils.data import Dataset
import pytorch_common.util    as pu


class SequenceDataset(Dataset):
    def __init__(self, features, targets, device=pu.get_device()):
        self.features = torch.tensor(features).unsqueeze(2).float()
        self.targets  = torch.tensor(targets).float()

    def __len__(self): return self.features.shape[0]

    def __getitem__(self, idx):  return self.features[idx, :], self.targets[idx]
