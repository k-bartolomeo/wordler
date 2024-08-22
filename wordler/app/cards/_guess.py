import dash_bootstrap_components as dbc
from dash import html

from ._functions import make_guess_row


GUESS_CARD = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Wordler!", className="card-title"),
            make_guess_row(guess_num=1, predict=True),
            make_guess_row(guess_num=2, predict=False),
            make_guess_row(guess_num=3, predict=False),
            make_guess_row(guess_num=4, predict=False),
            make_guess_row(guess_num=5, predict=False),
            make_guess_row(guess_num=6, predict=False)
        ]
    ),
    className="w-75 p-3",
    style={'borderTop': 'none', 'borderBottom': 'none', 'borderRadius': '0px'}
)