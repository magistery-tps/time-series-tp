import torch
from torch import nn
from .model_predict_mixin import model_predict_mixin
import pytorch_common.modules as mm


class TimeSeriesPredictor(nn.Module, model_predict_mixin, mm.FitMixin):
    def __init__(self, input_size, n_hidden_units, n_layers=2, dropout=0.2):
        super().__init__()
        self.n_layers       = n_layers
        self.n_hidden_units = n_hidden_units
        self.rnn = nn.GRU(
            input_size  = input_size,
            hidden_size = self.n_hidden_units,
            batch_first = True,
            dropout     = dropout,
            num_layers  = self.n_layers
        )
        self.linear = nn.Linear(
            in_features  = self.n_hidden_units,
            out_features = 1
        )

    def forward(self, input_batch):
        _, hidden = self.rnn(input_batch.to(self.device))
        return self.linear(hidden[-1]).squeeze(1)