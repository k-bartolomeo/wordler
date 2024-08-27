import plotly.graph_objects as go

from .utils import pad_seq
from ..utils import Styles


styles = Styles()


def update_graph(guesses, guess_probs):
    guesses = pad_seq(guesses, kind='str')
    guess_probs = pad_seq(guess_probs, kind='num')

    fig = go.Figure(
        data=[go.Scatter(y=guess_probs, line={'color': styles.green})],
        layout={'margin': {'t': 0, 'l': 0, 'r': 0}}
    )
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5],
            ticktext=guesses
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1.0],
            ticktext=['0%', '25%', '50%', '75%', '100%']
        ),
        yaxis_range=[-0.025, 1.025],
        yaxis_title={'text': 'Probability of Correct Guess'},
        xaxis_title={'text': 'Guess'}
    )

    return fig


def display_n_remaining(n_remaining):
    return f'Choices Remaining: {n_remaining:,}'
