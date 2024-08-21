import string
import warnings

from itertools import pairwise

import numpy as np
import pandas as pd


warnings.filterwarnings('ignore')


class Constants:
    def __init__(self, word_data: str):
        self.letter_map = {k:v for v,k in enumerate('#' + string.ascii_lowercase)}
        self.letter_lookup = {k:v for k,v in enumerate('#' + string.ascii_lowercase)}
        self.word_data = pd.read_csv(word_data)
        self.word_data['p'] = self.word_data['count'] / self.word_data['count'].sum()
        self.words = [f'#{w}' for w in self.word_data['word'].tolist()]
        self.transition_matrices = self._init_transition_matrices()
        self.position_matrix = self._init_position_probabilities()

    def _init_transition_matrices(self):
        transition_matrices = [np.zeros((27, 27)) for _ in range(5)]
        for w in self.words:
            letters = [self.letter_map[letter] for letter in w]
            for i, pair in enumerate(pairwise(letters)):
                np.add.at(transition_matrices[i], pair, 1)

        for i, matrix in enumerate(transition_matrices):
            transition_matrices[i] = np.nan_to_num(matrix / matrix.sum(1)[:, None], 0)

        transition_matrices = np.stack(transition_matrices)
        return transition_matrices
    
    def _init_position_probabilities(self):
        position_matrix = np.zeros((6, 27))
        for w in self.words:
            letters = [self.letter_map[letter] for letter in w]
            np.add.at(position_matrix, (np.arange(6), letters), 1)

        position_matrix /= position_matrix.sum(1)[:, None]
        return position_matrix