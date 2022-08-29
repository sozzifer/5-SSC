from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from ssc_model import create_blank_fig

app = Dash(__name__,
           title="Student's t distribution",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width,\
                                   initial-scale=1.0,\
                                   maximum-scale=1.0"
                       }]
           )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody(children=[
                    "This tool will allow you to view the Student's t distribution curve for different confidence levels and degrees of freedom. To display the distribution, enter values for the mean and standard deviation and click ",
                    html.Span("Set mean and SD", className="bold-p"),
                    ". Adjust the degrees of freedom and confidence level to see how this affects the confidence interval.",
                    html.Br(),
                    html.Br(),
                    "Pay particular attention to how the scales of the x and y axes change when you enter different values for the mean, standard deviation, degrees of freedom, and confidence level."
                ])
            ]),
            dbc.Card([
                dbc.CardBody(children=[
                    html.H4("Results"),
                    html.Div([
                        html.P(children=[
                            html.Span("Mean: ", className="bold-p"),
                            html.Span(id="current-mu"),
                            html.Span("Standard deviation: ",
                                      className="bold-p",
                                      style={"margin-left":"10px"}),
                            html.Span(id="current-sigma")
                        ]),
                        html.P(children=[
                            html.Span("Degrees of freedom: ", className="bold-p"),
                            html.Span(id="current-nu"),
                            html.Span("Confidence level: ",
                                      className="bold-p",
                                      style={"margin-left": "10px"}),
                            html.Span(id="current-alpha")
                        ]),
                        html.P(children=[
                            html.Span("Confidence interval: ", className="bold-p"),
                            html.Span(id="conf-int")
                        ])
                    ], id="output", style={"display": "none"}, **{"aria-live": "polite"})
                ])
            ])
        ], xs=12, md=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="t-dist-fig",
                          figure=create_blank_fig(),
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img"),
            html.Div(id="sr-t",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Mean",
                       html_for="mean",
                       className="label"),
            dbc.Input(id="mu",
                      name="mean",
                      value=0,
                      type="number",
                      required=True,
                      debounce=True),
            dbc.Label("Standard deviation",
                       className="label",
                       html_for="standard-deviation"),
            dbc.Input(id="sigma",
                      name="standard-deviation",
                      value=1,
                      min=0.1,
                      type="number",
                      required=True,
                      debounce=True),
            html.Div([
                dbc.Button(id="submit",
                           n_clicks=0,
                           children="Set mean and SD",
                           class_name="button")
            ], className="d-flex justify-content-center"),
        ], xs=12, md=4),
        dbc.Col([
            dbc.Label("Degrees of freedom",
                       className="label",
                       html_for="nu"),
            dcc.Slider(id="nu",
                       value=10,
                       min=1,
                       max=40,
                       step=1,
                       marks={1: {"label": "1"},
                              5: {"label": "5"},
                              10: {"label": "10"},
                              20: {"label": "20"},
                              30: {"label": "30"},
                              40: {"label": "40"}},
                       disabled=True),
            dbc.Label("Confidence level",
                       className="label",
                       html_for="alpha"),
            dcc.Slider(id="alpha",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       step=0.01,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}},
                       disabled=True),
            html.Br()
        ], xs=12, md=8)
    ])
], fluid=True)
