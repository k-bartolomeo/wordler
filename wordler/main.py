import string

import typer

from wordler.solver import Solver
from wordler.data import Constants
from wordler.cli.functions import (
    get_results, 
    get_initial_guess,
    get_solved,
    print_next_guess, 
    print_solved,
    
)


constants = Constants('data/words_and_counts.csv')
solver = Solver(constants=constants)

app = typer.Typer()

@app.command()
def start():
    candidates = [set('#' + string.ascii_lowercase) for _ in range(6)]
    remaining_words = solver.words[::]
    must_include = set('#')
    guess = get_initial_guess(remaining_words=remaining_words)

    tries = 1
    while tries < 6:
        solved = get_solved()
        if solved:
            print_solved()
            break

        results = get_results(guess=guess)
        (
            guess, guess_prob, must_include, candidates, remaining_words
        ) = solver.make_guess(
            results=results,
            previous_guess=guess,
            must_include=must_include,
            candidates=candidates,
            remaining_words=remaining_words
        )
        print_next_guess(guess=guess, guess_prob=guess_prob)
        tries += 1


if __name__ == '__main__':
    app()