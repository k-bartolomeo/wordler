from dash import (
    Dash, html, Input, Output, MATCH, clientside_callback, ClientsideFunction
)
import dash_bootstrap_components as dbc

from wordler.app.utils import Constants, Styles
from wordler.app.cards import CARDS
from wordler.app.javascript import (
    getCurrentIndex, getPreviousIndex, focusIndex
)


styles = Styles()
constants = Constants()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([CARDS])

@app.callback(
    [
        Output({'type': 'switches-inline-input', 'index': MATCH}, 'options'),
        Output({'type': 'letter', 'index': MATCH}, 'style')
    ],
    Input({'type': 'switches-inline-input', 'index': MATCH}, 'value')
)
def single_option(input_value):
    letter_style = styles.letter_col_input.copy()
    if input_value == []:
        return constants.checklist_options, letter_style
    val = input_value[0]
    if val == 1:
        options = [
            {'label': 'Yellow', 'value': 1},
            {'label': 'Green', 'value': 2, 'disabled': True}
        ]
        letter_style['backgroundColor'] = styles.yellow
    elif val == 2:
        options = [
            {'label': 'Yellow', 'value': 1, 'disabled': True},
            {'label': 'Green', 'value': 2}
        ]
        letter_style['backgroundColor'] = styles.green
    else:
        letter_style['backgroundColor'] = styles.gray

    return options, letter_style


# clientside_callback(
#     ClientsideFunction(namespace='clientside', function_name='getCurrentIndex'),
#     Output('current-index', 'data'),
#     [
#         Input({'type': 'letter', 'index': '11'}, 'value'),
#         Input({'type': 'letter', 'index': '12'}, 'value'),
#         Input({'type': 'letter', 'index': '13'}, 'value'),
#         Input({'type': 'letter', 'index': '14'}, 'value'),
#         Input({'type': 'letter', 'index': '15'}, 'value'),
#     ]
# )
clientside_callback(
    getCurrentIndex,
    Output('current-index', 'data'),
    [
        Input({'type': 'letter', 'index': '11'}, 'value'),
        Input({'type': 'letter', 'index': '12'}, 'value'),
        Input({'type': 'letter', 'index': '13'}, 'value'),
        Input({'type': 'letter', 'index': '14'}, 'value'),
        Input({'type': 'letter', 'index': '15'}, 'value'),
    ]
)

# clientside_callback(
#     ClientsideFunction(namespace='clientside', function_name='getPreviousIndex'),
#     Output('previous-index', 'data'),
#     Input('current-index', 'data')
# )
clientside_callback(
    getPreviousIndex,
    Output('previous-index', 'data'),
    Input('current-index', 'data')
)

# clientside_callback(
#     ClientsideFunction(namespace='clientside', function_name='focusIndex'),
#     Input('current-index', 'data')
# )
clientside_callback(
    focusIndex,
    Input('current-index', 'data')
)

app.run(debug=True)