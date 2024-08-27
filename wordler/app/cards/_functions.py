import dash_bootstrap_components as dbc
from dash import html

from ..utils import Styles, Constants


styles = Styles()
constants = Constants()


def make_letter_column(row: int, col: int, end_col: bool) -> dbc.Col:
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
            disabled=True,
            autofocus=False
        ),
        dbc.Collapse(
            dbc.Checklist(
                options=constants.checklist_options,
                value=[],
                id={
                    'type': 'switches-inline-input',
                    'index': f'{row}{col}',
                },
                inline=True,
                switch=True
            ),
            id={
                'type': 'collapse-choice',
                'index': f'{row}{col}',
            },
            is_open=True if row == 1 else False
        )
    ]
    if end_col and row < 6:
        children.append(
            dbc.Collapse(
                dbc.Button(
                    'Predict',
                    id={
                        'type': 'predict-button',
                        'index': str(row)
                    },
                    n_clicks=0,
                    style=styles.predict_button
                ),
                id={
                    'type': 'collapse-predict',
                    'index': str(row)
                },
                is_open=True if row == 1 else False
            )
        )
    letter_column = dbc.Col(children)

    return letter_column


def make_guess_row(guess_num: int) -> html.Div:
    guess_cols = [
        html.H5(f'Guess #{guess_num}:'), 
        *[
            make_letter_column(row=guess_num, col=i, end_col=False)
            for i in range(1,5)
        ]
    ]
    guess_cols.append(
        make_letter_column(row=guess_num, col=5, end_col=True)
    )
    guess_row = html.Div(dbc.Row(guess_cols))
    return guess_row
