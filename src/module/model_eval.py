import pytorch_common.modules as mm


class ModelEvalMixin:
    def validation(self, data_loader):
        return mm.Fn.validation(self, data_loader, self.device)
