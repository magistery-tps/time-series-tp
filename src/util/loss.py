loss_wrapper = lambda loss_fn: lambda y_pred, y_true: loss_fn(y_pred, y_true).item()
