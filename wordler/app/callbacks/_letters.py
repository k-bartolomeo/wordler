import string

from ..utils import Constants, Styles
from ...solver import Solver
from ...tables import ProbabilityTables


styles = Styles()
constants = Constants()
tables = ProbabilityTables('wordler/data/words_and_counts.csv')
solver = Solver(tables=tables)


def update_current_letters(last_key: str | list, current_letters: list) -> list:
    """Updates initial guess letters given last key pressed

    Takes input from global keydown event listener and updates Dash 
    store tracking initial guess letters depending on current state 
    of initial guess row. Uses the following logic:

        1.  If the last key pressed isn't a string character (e.g., 
            the page was just loaded), return the original, empty list.
        2.  If the last key pressed was either 'Backspace' or 'Delete',
            do the following:
                -   Check if the list of current letters has five valid
                    entries (i.e., a full word has been entered in the 
                    initial guess row).
                -   If the list has five entries, delete the last 
                    element in the list.
                -   If it does not, then find the index of the last 
                    non-empty string in the last and delete that instead.
        3.  If the last key pressed was an alphabetical character and 
            there are still empty strings in the current letters list,
            replace the first occurrence of an empty string with the 
            character of the key pressed.

    Parameters
    ----------
    last_key
        Last key pressed.
    current_letters
        List of letters currently displayed in the initial guess row.

    Returns
    -------
    list[str]
        Updated list of letters to display in the initial guess row
        depending on what the last key pressed was.
    """
    if not isinstance(last_key, str):
        return current_letters
    characters = set(string.ascii_lowercase)
    last_empty = current_letters.index('') if '' in current_letters else -1

    if last_key in {'Backspace', 'Delete'}:
        if last_empty == -1:
            current_letters[-1] = ''
        elif last_empty in {1, 2, 3, 4}:
            current_letters[last_empty - 1] = ''
        else:
            current_letters[0] = ''
    elif last_key in characters and last_empty != -1:
        current_letters[last_empty] = last_key

    return current_letters


def get_init_word(current_letters: list[str]) -> str:
    """Stores current letters as word in dcc.Store object

    Converts list of current letters in initial guess row to single
    string for downstream use, only if a full five-letter word has 
    been entered into this row. Otherwise, it returns an empty 
    string.

    Parameters
    ----------
    current_letters
        List of letters in initial guess row.

    Returns
    -------
    str
        Single string representation of word in initial guess row.
    """
    if len(current_letters) == 5:
        return ''.join(current_letters)
    return ''


def update_inputs(current_letters: list[str]) -> list[str]:
    """Moves letters from dcc.Store to individual dbc.Input components"""
    return current_letters


def single_option(input_value: list) -> tuple[list, dict]:
    """Ensures that only single checklist option is selected
    
    Checklist items displayed underneath each letter tile. Selecting
    of checklist items provides feedback from Wordle about previous 
    guess to app. Function takes value of selected checklist item - 
    either 'Yellow' or 'Green' - and updates background color of 
    corresponding letter tile. Other checklist item that was not 
    selected is disabled. If checklist item is de-selected, function 
    then enables both checklist items and returns corresponding tile's
    background color to gray.

    Parameters
    ----------
    input_value
        Value of currently selected checklist item represented as 
        single-element list. If no checklist item selected, value is 
        an empty list.

    Returns
    -------
    tuple[list, dict]
        Two-item tuple where first item is list of dictionaries with 
        updated checklist options. Second item is background color of 
        corresponding letter tile.
    """
    letter_style = styles.letter_col_input.copy()
    if input_value == []:
        # If nothing is selected, default background color and 
        # checklist options are returned.
        return constants.checklist_options.copy(), letter_style
    val = input_value[0]

    # Value of 1 corresponds to selecting color 'Yellow'. 'Green' 
    # checklist item disabled and background of corresponding letter
    # tile updated to yellow.
    if val == 1:
        options = [
            {'label': 'Yellow', 'value': 1},
            {'label': 'Green', 'value': 2, 'disabled': True}
        ]
        letter_style['backgroundColor'] = styles.yellow

    # Value of 2 corresponds to selecting color 'Green'. 'Yellow'
    # checklist item disabled and background of corresponding letter
    # tile updated to green.
    elif val == 2:
        options = [
            {'label': 'Yellow', 'value': 1, 'disabled': True},
            {'label': 'Green', 'value': 2}
        ]
        letter_style['backgroundColor'] = styles.green
    else:
        letter_style['backgroundColor'] = styles.gray

    return options, letter_style


def update_collapse(buttons: list[int]) -> list[list[int], list[int]]:
    """Handles showing and hiding of feedback checklists and predict button
    
    Takes list of button click counts for all 'Predict' buttons. Each
    button can only be clicked once, so counts essentially act as flag
    denoting whether or not button has been clicked. Checklist 
    components and predict button wrapped with dbc.Collapse. Click of 
    expanded predict button intended to trigger collapse of itself,
    collapse of checklist items in same row, and expansion of checklist
    items and predict button in following row. 
    
    On entire page, there are 5 predict buttons and 30 checklists - 6 
    rows of 5. Show/hide values for predict buttons stored as True/False
    values in 5-item list. Show/hide value for checklist items stored as 
    True/False values in 30-item list. 
    
    Index of first '0' in list of flags denotes row of button that should 
    be displayed. That index used to calculate indices of checklist items
    that should also be displayed. Values for all other indices set to 
    False.

    Parameters
    ----------
    buttons
        List of integers denoting how many times each button on page 
        has been clicked.

    Returns
    -------
    list[list[int], list[int]]
        Two-item list, where each item is also a list. First item is a
        30-item list with True/False values denoting which checklist 
        items should be visible. Second item is a 5-item list with 
        True/False values denoting which predict buttons should be 
        visible.
    """
    show_choices = [False for _ in range(30)]
    show_predicts = [False for _ in range(5)]

    # Find index of first button that hasn't been clicked. If all
    # buttons have been clicked, set value to 5 so checklists in 
    # last row will be displayed. 
    zero_idx = buttons.index(0) if 0 in buttons else 5
    show = [True for _ in range(5)]
    start = zero_idx * 5
    show_choices[start : start + 5] = show

    # `show_predicts` only has 5 items, so don't raise an IndexError
    if zero_idx != 5:
        show_predicts[zero_idx] = True

    return [show_choices, show_predicts]


def update_letters(
    buttons: list[int],
    switches: list[list],
    letters: list[str],
    init_word: str,
    guess: str,
    guesses: list[str],
    guess_probs: list[float],
    candidates: list[list],
    remaining_words: list[str],
    must_include: list[list]
) -> tuple[str, float, list[set], list[str], list[set], list[str]]:
    """Takes Wordle feedback, makes next guess, updates letters

    Takes previous guess, feedback from Wordle, and current game 
    state, and computes next guess using Solver. Updates variables
    responsible for tracking game state and returns them along with
    next guess, next guess probability, and list of letters to be
    displayed in page's letter tiles.
    
    Parameters
    ----------
    buttons
        List of integers denoting number of clicks of each 'Predict'
        button on page, hidden or not.
    switches
        List of lists corresponding to selected checklist options for
        all checklists on page, hidden or not.
    letters
        List of values of all letter tiles on page to be updated with
        next guess.
    init_word
        Initial guess.
    guess
        Previous guess.
    candidates
        List of sets of remaining possible letters for each position
        in word.
    remaining_words
        List of all remaining words in search space given current 
        game state and previous guesses.
    must_include
        Single-item list where item is set of characters that must be
        included in next guess. Set is only wrapped in list because 
        of dcc.Store requirements.

    Returns
    -------
    tuple[str, float, list[set], list[str], list[set], list[str]]
        6-item tuple. First item is next word to guess. Second item 
        is computed probability that next guess is the goal word.
        Third item is updated list of candidates for each word 
        position. Fourth item is updated list of words in search 
        space. Fifth item is updated list with set of characters the
        next guess must include. Sixth item is updated list of letters
        to be displayed in page's letter tiles.
    """
    zero_idx = buttons.index(0) if 0 in buttons else 5
    switch_start = (zero_idx - 1) * 5
    letter_start = zero_idx * 5
    switches = [x[0] if len(x) == 1 else 0 for x in switches]
    if len(guess) == 0:
        guess = init_word
    guess = f'#{guess}'

    # Gets relevant feedback from previous guess and prepends it 
    # with `2` that corresponds to start symbol used by solver.
    feedback = [2, *switches[switch_start : switch_start + 5]]

    # Need to convert `candidates` and `must_include` from lists
    # (which is a dcc.Store) requirement to sets.
    candidates = [set(item) for item in candidates]
    must_include = set(must_include[0])
    guess, guess_prob, must_include, candidates, remaining_words = solver.make_guess(
        results=feedback,
        previous_guess=guess,
        must_include=must_include,
        candidates=candidates,
        remaining_words=remaining_words
    )
    guess = guess.lstrip('#')
    letters[letter_start : letter_start + 5] = list(guess)
    if len(guesses) == 0:
        guesses.extend([init_word.upper(), guess.upper()])
        guess_probs.extend([1/2315, guess_prob])
    else:
        guesses.append(guess.upper())
        guess_probs.append(guess_prob)

    # Now need to convert `candidates` and `must_include` back to
    # the proper dcc.Store type.
    candidates = [list(item) for item in candidates]
    must_include = list(must_include)

    return (
        guess,
        guesses,
        guess_probs, 
        candidates, 
        remaining_words,
        len(remaining_words),
        must_include, 
        letters
    )
