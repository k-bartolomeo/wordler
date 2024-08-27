import dash_bootstrap_components as dbc
from dash import html, dcc

import numpy as np
import plotly.graph_objects as go

from ..utils import Styles


styles = Styles()


fig = go.Figure(
    data=[go.Scatter(y=[np.nan for _ in range(6)], line={'color': styles.green})],
    layout={'margin': {'t': 0, 'l': 0, 'r': 0}}
)
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4, 5],
        ticktext=['' for _ in range(6)]
    )
)
fig.update_layout(
    yaxis=dict(
        tickmode='array',
        tickvals=[0, 0.25, 0.5, 0.75, 1.0],
        ticktext=['0%', '25%', '50%', '75%', '100%']
    ),
    yaxis_range=[-0.025, 1.025],
    yaxis_title={'text': 'Probability of Correct Guess'},
    xaxis_title={'text': 'Guess'}
)


INFO_CARD = dbc.Card(
    dbc.CardBody(
        [
            html.H4("How to Play", style={'marginTop': '3%'}),
            html.P(
                "1. Start by entering your first Wordle guess into the boxes on the left.",
                className="card-text",
            ),
            html.P(
                "2. After Wordle gives you feedback on your guess, highlight the yellow "
                "and green tiles here in Wordler.",
                className="card-text",
            ),
            html.P(
                [
                    "3. Click the ",
                    html.B("Predict"),
                    " button to get Wordler's next guess.",
                ],
                className="card-text",
            ),
            html.P("4. Enter Wordler's guess into Wordle.", className="card-text"),
            html.P("5. Repeat steps 2 through 4 until you win!", className="card-text"),
            html.H4('Choices Remaining: 2,315', id='n-remaining-info', style={'marginBottom': '0%'}),
            dcc.Graph(
                figure=fig,
                config={'staticPlot': True},
                id='word-prob-graph',
                style={'margin': '3%', 'marginRight': '5%', 'marginLeft': '0%'}
            )
        ]
    ),
    className='col-sm-5',
    style={"borderTop": "none", "borderBottom": "none", "borderRadius": "0px"},
)
