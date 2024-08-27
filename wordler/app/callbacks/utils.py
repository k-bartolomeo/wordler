import numpy as np


def pad_seq(seq, kind='num'):
    padding = [np.nan if kind == 'num' else '' for _ in range(6 - len(seq))]
    return [*seq, *padding]