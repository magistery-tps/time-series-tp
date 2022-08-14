import numpy as np


def standarizer(train_set, test_set, columns):
    norm_train_set, norm_test_set = train_set.copy(),  test_set.copy()

    for col in columns:
        mean, stdev = train_set[col].mean(), train_set[col].std()
        norm_train_set[f'norm_{col}'] = train_set[col].apply(lambda x: (x - mean) / stdev)
        norm_test_set[f'norm_{col}']  = test_set[col].apply(lambda x: (x - mean) / stdev)

    return norm_train_set, norm_test_set


def variable_to_sequences(variable, window_size):
    sliding_window_view = np.lib.stride_tricks.sliding_window_view
    return np.array([seq for seq in sliding_window_view(variable, window_size)])


def features_target_split(sequences, target_size=1):
    features, targets = [], []
    for seq in sequences:
        seq_len = len(seq)
        features.append(seq[:seq_len-target_size])

        if target_size == 1:
            targets.append(seq[seq_len-target_size])
        else:
            targets.append(seq[-target_size:])

    return np.array(features), np.array(targets)