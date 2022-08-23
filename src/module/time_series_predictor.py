import torch
from torch import nn
import pytorch_common.modules as mm


class TimeSeriesPredictor(nn.Module, mm.PredictMixin, mm.FitMixin):
    def __init__(
        self,
        n_hidden_units,
        input_size=1,
        n_layers=2,
        dropout=0.2,
        out_features=1
    ):
        super().__init__()
        self.n_layers       = n_layers
        self.n_hidden_units = n_hidden_units
        self.rnn = nn.LSTM(
            input_size  = input_size,
            hidden_size = self.n_hidden_units,
            batch_first = True,
            dropout     = dropout,
            num_layers  = self.n_layers
        )
        self.linear = nn.Linear(
            in_features  = self.n_hidden_units,
            out_features = out_features
        )

    def forward(self, input_batch):
        batch_size = input_batch.shape[0]
        h0 = torch.zeros(self.n_layers, batch_size, self.n_hidden_units).requires_grad_().to(self.device)
        c0 = torch.zeros(self.n_layers, batch_size, self.n_hidden_units).requires_grad_().to(self.device)

        _, (hidden, _) = self.rnn(input_batch.to(self.device))
        return self.linear(hidden[-1]).squeeze(1)


