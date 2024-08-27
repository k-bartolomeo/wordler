from dash import Output, MATCH, ALL


class CallbackOutputs:
    key_listener = Output('document', 'id')
    current = Output('current-letters', 'data')
    init_word = Output('init-word', 'data')
    inputs = [
        Output({'type': 'letter', 'index': '11'}, 'value'),
        Output({'type': 'letter', 'index': '12'}, 'value'),
        Output({'type': 'letter', 'index': '13'}, 'value'),
        Output({'type': 'letter', 'index': '14'}, 'value'),
        Output({'type': 'letter', 'index': '15'}, 'value')
    ]
    single_option = [
        Output({'type': 'switches-inline-input', 'index': MATCH}, 'options'),
        Output({'type': 'letter', 'index': MATCH}, 'style')
    ]
    collapse = [
        Output({'type': 'collapse-choice', 'index': ALL}, 'is_open'),
        Output({'type': 'collapse-predict', 'index': ALL}, 'is_open')
    ]
    letters = [
        Output('guess', 'data'),
        Output('guesses', 'data'),
        Output('guess-prob', 'data'),
        Output('candidates', 'data'),
        Output('remaining-words', 'data'),
        Output('n-remaining', 'data'),
        Output('must-include', 'data'),
        Output({'type': 'letter', 'index': ALL}, 'value', allow_duplicate=True)
    ]
    choices = Output('n-remaining-info', 'children')
    graph = Output('word-prob-graph', 'figure')