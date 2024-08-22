import dash_bootstrap_components as dbc
from dash import html

from ..utils import Styles
from ..utils import Constants

styles = Styles()
constants = Constants()


def make_letter_column(row: int, col: int, predict: bool, end_col: bool) -> dbc.Col:
    children = [
        dbc.Input(
            id={
                'type': 'letter',
                'index': f'{row}{col}'

            },
            size='lg', 
            className='mb-3', 
            maxlength=1, 
            style=styles.letter_col_input,
            disabled=False if row == 1 else True,
            autofocus=True if row == 1 and col == 1 else False
        )
    ]
    if predict:
        children.append(
            dbc.Checklist(
                options=constants.checklist_options,
                value=[],
                id={
                    'type': 'switches-inline-input',
                    'index': f'{row}{col}'
                },
                inline=True,
                switch=True
            )
        )
        if end_col:
            children.append(
                dbc.Button(
                    'Predict', 
                    id='predict-button', 
                    n_clicks=0, 
                    style=styles.predict_button)
            )
    letter_column = dbc.Col(children)

    return letter_column


def make_guess_row(guess_num: int, predict: bool) -> html.Div:
    guess_cols = [
        html.H5(f'Guess #{guess_num}:'), 
        *[
            make_letter_column(row=guess_num, col=i, predict=predict, end_col=False)
            for i in range(1,5)
        ]
    ]
    guess_cols.append(
        make_letter_column(row=guess_num, col=5, predict=predict, end_col=True)
    )
    guess_row = html.Div(dbc.Row(guess_cols))
    return guess_row
