import string
import operator
from functools import reduce
from itertools import pairwise

from ..tables import ProbabilityTables


class Solver:
    def __init__(self, constants: ProbabilityTables):
        self.letter_map = constants.letter_map
        self.position_matrix = constants.position_matrix
        self.transition_matrices = constants.transition_matrices
        self.word_data = constants.word_data
        self.words = constants.words

    def get_positional_probability(self, word: str, candidates: list[set]):
        word_prob = []
        for i, letter in enumerate(word):
            if i in {0, 5}:
                continue
            candidate_letters = [self.letter_map[x] for x in candidates[i]]
            position_prob = self.position_matrix[i].copy()

            for letter_idx in set(range(27)) - set(candidate_letters):
                position_prob[letter_idx] = 0.

            position_prob /= position_prob.sum()
            letter_prob = position_prob[self.letter_map[letter]]
            word_prob.append(letter_prob)

        return word_prob


    def get_usage_prob(self, word, remaining_words):
        subset = (
            self.word_data[
                self.word_data.word.isin([w[1:] for w in remaining_words])
            ].copy()
        )
        subset['p'] = subset.p / subset.p.sum()
        usage_prob = subset[subset.word == word[1:]].p.iloc[0]
        return usage_prob


    def get_word_prob(self, word, candidates, remaining_words):
        probs = [
            self.transition_matrices[i, p[0], p[1]]
            for i, p in enumerate(
                pairwise([self.letter_map[letter] for letter in word])
            )
        ]
        probs.extend(self.get_positional_probability(word, candidates))
        probs.append(self.get_usage_prob(word, remaining_words))
        return reduce(operator.mul, probs)


    def check_word(self, word, candidates, must_include):
        if not all(letter in word for letter in must_include):
            return False
        if word[0] not in candidates[0]:
            return False
        if word[1] not in candidates[1]:
            return False
        if word[2] not in candidates[2]:
            return False
        if word[3] not in candidates[3]:
            return False
        if word[4] not in candidates[4]:
            return False
        if word[5] not in candidates[5]:
            return False
        return True


    def make_guess(self, results, previous_guess, must_include, candidates, remaining_words):
        for i, (result, letter) in enumerate(zip(results, previous_guess)):
            if result == 0:
                if letter not in must_include:
                    for pos in candidates:
                        if letter in pos:
                            pos.remove(letter)
                else:
                    if letter in candidates[i]:
                        candidates[i].remove(letter)
            elif result == 1:
                if letter in candidates[i]:
                    candidates[i].remove(letter)
                must_include.add(letter)
            else:
                candidates[i] = set(letter)
                must_include.add(letter)

        remaining_words = [
            word for word in remaining_words 
            if self.check_word(word, candidates, must_include)
        ]
        remaining_word_probs = [
            self.get_word_prob(word, candidates, remaining_words) 
            for word in remaining_words
        ]
        sorted_probs = sorted(
            zip(remaining_words, remaining_word_probs), key=lambda x: x[1]
        )
        total_probs = sum([x[1] for x in sorted_probs])
        guess = sorted_probs[-1][0]
        guess_prob = sorted_probs[-1][1] / total_probs
        return guess, guess_prob, must_include, candidates, remaining_words
    
    def run(self, init_guess='slate'):
        guess = f'#{init_guess}'
        candidates = [set('#' + string.ascii_lowercase) for _ in range(6)]
        remaining_words = self.words[::]
        must_include = set('#')

        tries = 1
        while tries < 6:
            results = input()
            results = [2] + [int(x) for x in results]
            guess, must_include, candidates, remaining_words = self.make_guess(
                results=results,
                previous_guess=guess,
                must_include=must_include,
                candidates=candidates,
                remaining_words=remaining_words
            )
            print(guess)
            tries += 1