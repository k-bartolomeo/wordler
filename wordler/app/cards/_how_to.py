import dash_bootstrap_components as dbc
from dash import html


HOW_TO_CARD = dbc.Card(
    dbc.CardBody(
        [
            html.H1("How to Play", className="card-title"),
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
        ]
    ),
    className="w-25 p-3",
    style={"borderTop": "none", "borderBottom": "none", "borderRadius": "0px"},
)
