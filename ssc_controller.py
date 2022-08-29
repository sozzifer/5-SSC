from dash import Input, Output, exceptions
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stat
from ssc_view import app
from ssc_model import stat_colours


@app.callback(
    Output("t-dist-fig", "figure"),
    Output("output", "style"),
    Output("current-mu", "children"),
    Output("current-sigma", "children"),
    Output("current-nu", "children"),
    Output("current-alpha", "children"),
    Output("conf-int", "children"),
    Output("nu", "disabled"),
    Output("alpha", "disabled"),
    Output("sr-t", "children"),
    Input("submit", "n_clicks"),
    Input("nu", "value"),
    Input("alpha", "value"),
    Input("mu", "value"),
    Input("sigma", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, nu, alpha, mu, sigma):
    if n_clicks is None or mu is None or sigma is None or nu is None:
        raise exceptions.PreventUpdate
    else:
        x = np.linspace(stat.t.ppf(0.0001, nu, mu, sigma),
                        stat.t.ppf(0.9999, nu, mu, sigma),
                        10000)
        t_x = stat.t.pdf(x, nu, mu, sigma)
        conf_int = stat.t.interval(alpha, nu, mu, sigma)
        t1 = round(conf_int[0], 3)
        t2 = round(conf_int[1], 3)
        alpha_1tail = 1 - ((1 - alpha)/2)
        lower_ci = np.linspace(stat.t.ppf(0.0001, nu, mu, sigma),
                               stat.t.ppf(1-alpha_1tail, nu, mu, sigma),
                               10000)
        t_pdf1 = stat.t.pdf(lower_ci, nu, mu, sigma)
        upper_ci = np.linspace(stat.t.ppf(alpha_1tail, nu, mu, sigma),
                               stat.t.ppf(0.9999, nu, mu, sigma),
                               10000)
        t_pdf2 = stat.t.pdf(upper_ci, nu, mu, sigma)
        sr_t = f"Student's t distribution graph with mean {mu}, standard deviation {sigma}, {nu} degrees of freedom and confidence level {alpha*100}%"
        fig = go.Figure(go.Scatter(x=x,
                                   y=t_x,
                                   name="t distribution",
                                   marker_color=stat_colours["norm"],
                                   hoverinfo="skip"),
                                   layout={"margin": dict(t=20, b=10, l=20, r=20),
                                           "height": 400,
                                           "font_size": 14})
        fig.add_trace(go.Scatter(x=lower_ci,
                                 y=t_pdf1,
                                 name="Probability",
                                 marker_color=stat_colours["norm"],
                                 hoverinfo="skip",
                                 fill="tozeroy",
                                 fillcolor=stat_colours["z"]))
        fig.add_trace(go.Scatter(x=upper_ci,
                                 y=t_pdf2,
                                 marker_color=stat_colours["norm"],
                                 hoverinfo="skip",
                                 fill="tozeroy",
                                 fillcolor=stat_colours["z"],
                                 showlegend=False))
        fig.add_trace(go.Scatter(x=[stat.t.ppf(1-alpha_1tail, nu, mu, sigma)] * 10,
                                 y=np.linspace(0, t_pdf1[-1], 10),
                                 name="Lower CI",
                                 marker_color=stat_colours["+-1std"],
                                 marker_opacity=0,
                                 hovertemplate="Lower CI: %{x:.3f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=[stat.t.ppf(alpha_1tail, nu, mu, sigma)] * 10,
                                 y=np.linspace(0, t_pdf2[0], 10),
                                 name="Upper CI",
                                 marker_color=stat_colours["+-1std"],
                                 marker_opacity=0,
                                 hovertemplate="Upper CI: %{x:.3f}<extra></extra>"))
    return fig, {"display": "inline"}, mu, sigma, nu, f"{alpha:.0%}", f"({t1}, {t2})", False, False, sr_t


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
    # app.run(debug=True)
