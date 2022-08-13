import pytorch_common.modules as mm


class ModelPredictMixin:
    def validation(self, data_loader):
        return mm.Fn.validation(self, data_loader, self.device)

    def predict(self, features):
        model.eval()
        with torch.no_grad():
            return self(features.to(device))
