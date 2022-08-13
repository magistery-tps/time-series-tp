import numpy as np
import random
import torch


def set_seed(value):
    random.seed(value)
    np.random.seed(value)
    torch.manual_seed(value)
