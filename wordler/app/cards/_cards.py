import dash_bootstrap_components as dbc
from dash import html, dcc

from ._guess import GUESS_CARD
from ._how_to import HOW_TO_CARD


CARDS = html.Div(
    [
        dbc.Row([GUESS_CARD, HOW_TO_CARD]),
        dcc.Store(id='current-index'),
        dcc.Store(id='previous-index'),
    ],
    style={'border': 'none'}
)