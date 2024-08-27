import dash_bootstrap_components as dbc
from dash import html

from ._functions import make_guess_row


GUESS_CARD = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Wordler!", className="card-title"),
            make_guess_row(guess_num=1),
            make_guess_row(guess_num=2),
            make_guess_row(guess_num=3),
            make_guess_row(guess_num=4),
            make_guess_row(guess_num=5),
            make_guess_row(guess_num=6)
        ]
    ),
    className='col-sm-7',
    style={'borderTop': 'none', 'borderBottom': 'none', 'borderRadius': '0px'}
)
