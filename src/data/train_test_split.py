def train_test_split(df, test_percent = 0.3):
    train_set_size = round(df.shape[0] - (df.shape[0]*test_percent))

    train_set = df.loc[:train_set_size, :]
    test_set  = df.loc[train_set_size:, :]

    return train_set, test_set