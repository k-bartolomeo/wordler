from dash import Input, MATCH, ALL, State


class CallbackInputs:
    key_listener = Input('document', 'id')
    current = [Input('last-key', 'data'), Input('current-letters', 'data')]
    init_word = Input('current-letters', 'data')
    inputs = Input('current-letters', 'data')
    single_option = Input({'type': 'switches-inline-input', 'index': MATCH}, 'value')
    collapse = Input({'type': 'predict-button', 'index': ALL}, 'n_clicks')
    letters = [
        Input({'type': 'predict-button', 'index': ALL}, 'n_clicks'),
        State({'type': 'switches-inline-input', 'index': ALL}, 'value'),
        State({'type': 'letter', 'index': ALL}, 'value'),
        State('init-word', 'data'),
        State('guess', 'data'),
        State('guesses', 'data'),
        State('guess-prob', 'data'),
        State('candidates', 'data'),
        State('remaining-words', 'data'),
        State('must-include', 'data')
    ]
    choices = Input('n-remaining', 'data')
    graph = [
        Input('guesses', 'data'),
        Input('guess-prob', 'data')
    ]