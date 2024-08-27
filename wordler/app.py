import string

from dash import Dash, html, clientside_callback, dcc
import dash_bootstrap_components as dbc

from wordler.app.utils import Constants, Styles
from wordler.solver import Solver
from wordler.tables import ProbabilityTables
from wordler.app.cards import CARDS
from wordler.app.callbacks import (
    CallbackInputs,
    CallbackOutputs,
    keyListener,
    display_n_remaining,
    get_init_word,
    single_option,
    update_collapse,
    update_current_letters, 
    update_graph,
    update_inputs,
    update_letters
)


styles = Styles()
constants = Constants()
inputs = CallbackInputs()
outputs = CallbackOutputs()
tables = ProbabilityTables('wordler/data/words_and_counts.csv')
solver = Solver(tables=tables)
candidates_data = [list('#' + string.ascii_lowercase) for _ in range(6)]

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    CARDS,
    dcc.Store(id='last-key', data={}),
    dcc.Store(id='current-letters', data=['', '', '', '', '']),
    dcc.Store(id='init-word', data=[]),
    dcc.Store(id='guess', data=[]),
    dcc.Store(id='guess-prob', data=[]),
    dcc.Store(id='guesses', data=[]),
    dcc.Store(
        id='candidates',
        data=candidates_data
    ),
    dcc.Store(id='remaining-words', data=solver.words[::]),
    dcc.Store(id='n-remaining', data=2_315),
    dcc.Store(id='must-include', data=[['#']])
], id='document')


clientside_callback(keyListener, outputs.key_listener, inputs.key_listener)
display_n_remaining = app.callback(outputs.choices, inputs.choices)(display_n_remaining)
get_init_word = app.callback(outputs.init_word, inputs.init_word)(get_init_word)
single_option = app.callback(outputs.single_option, inputs.single_option)(single_option)
update_inputs = app.callback(outputs.inputs, inputs.inputs)(update_inputs)
update_collapse = app.callback(outputs.collapse, inputs.collapse)(update_collapse)
update_graph = app.callback(outputs.graph, inputs.graph)(update_graph)

update_letters = (
    app.callback(
        outputs.letters, inputs.letters, prevent_initial_call=True
    )(update_letters)
)

update_current_letters = (
    app.callback(outputs.current, inputs.current)(update_current_letters)
)   

app.run()   