from collections import defaultdict

import questionary
from questionary import prompt


def process_word(word):
    letter_counts = defaultdict(int)
    letter_reprs = []
    for letter in word:
        letter_counts[letter] += 1
        letter_reprs.append(f'{letter}{letter_counts[letter]}')
        
    return letter_reprs


def get_tile_results(
    choices, 
    letter_reprs,
    results, 
    kind: str = 'green'
):
    tiles = questionary.checkbox(
        f'Select the {kind} tiles:',
        choices=choices,
    ).ask()
    value = 2 if kind == 'green' else 1
    for tile in tiles:
        results[letter_reprs.index(tile)] = value

    return results


def get_results(guess):
    letter_reprs = process_word(guess[1:])
    choices = [{'name': letter[0], 'value': letter} for letter in letter_reprs]
    results = [0 for _ in range(5)]
    results = get_tile_results(choices, letter_reprs, results, kind='green')
    results = get_tile_results(choices, letter_reprs, results, kind='yellow')
    results = [2] + results
    return results


def print_next_guess(guess: str, guess_prob: float) -> None:
    prompt([{
        "type": "print",
        "name": "next_guess",
        "message": (
            f"\n\U0001F50D Next guess: {guess.lstrip('#')} "
            f"(p={guess_prob*100:.2f}%) \U0001F50D\n"
        ),
    }])


def print_solved() -> None:
    prompt([{
        "type": "print",
        "name": "next_guess",
        "message": (
            "\n\U0001F973 \U0001F388 \U0001F389 \U0001F913 "
            "Congratulations, WordNerd! \U0001F913 \U0001F389 "
            "\U0001F388 \U0001F973"
        )
    }])
    print()


def get_solved() -> bool:
    response = prompt([{
        "type": "confirm",
        "name": "solved",
        "message": "Is the puzzle solved?",
        "default": False,
    }])
    solved = response['solved']
    return solved


def get_initial_guess(remaining_words: list[str]) -> str:
    response = prompt([{
        "type": "text",
        "name": "initial_guess",
        "message": "Please enter your initial guess:",
        "validate": lambda x: f'#{x}' in remaining_words,
    }])
    guess = f"#{response['initial_guess']}"
    return guess
