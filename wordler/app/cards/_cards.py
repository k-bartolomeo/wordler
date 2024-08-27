import dash_bootstrap_components as dbc
from dash import html, dcc

from ._info import INFO_CARD
from ._guess import GUESS_CARD


CARDS = html.Div([dbc.Row([GUESS_CARD, INFO_CARD])], style={'border': 'none'})
