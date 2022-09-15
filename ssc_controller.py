from dash import Input, Output, exceptions
import numpy as np
import plotly.graph_objects as go
import scipy.stats as stat
from ssc_model import stat_colours, t_distribution
from ssc_view import app

# app.callback Outputs and Inputs are all associated with unique elements in *_view.py though the first argument (component_id) and control/are controlled by the second argument (component_property)


# Callback function to update t distribution graph, results and associated screen reader text based on user entry values (mu (mean), sigma (standard deviation), degrees of freedom (nu) and confidence level (alpha))
@app.callback(
    # Graph Outputs
    Output("t-dist-fig", "figure"),
    Output("sr-t", "children"),
    # Results hidden until callback triggered
    Output("results", "style"),
    # Results
    Output("current-mu", "children"),
    Output("current-sigma", "children"),
    Output("current-nu", "children"),
    Output("current-alpha", "children"),
    Output("conf-int", "children"),
    # User Input for degrees of freedom/confidence level disabled until mean/SD set
    Output("nu", "disabled"),
    Output("alpha", "disabled"),
    # Inputs
    Input("submit", "n_clicks"),
    Input("mu", "value"),
    Input("sigma", "value"),
    Input("nu", "value"),
    Input("alpha", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, mu, sigma, nu, alpha):
    if n_clicks is None or mu is None or sigma is None or nu is None:
        raise exceptions.PreventUpdate
    else:
        x, t_x, t1, t2, alpha_1tail, lower_ci, t_pdf1, upper_ci, t_pdf2 = t_distribution(mu, sigma, nu, alpha)
        # Screen reader text
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
        fig.update_layout(dragmode=False)
    return fig, sr_t, {"display": "inline"}, mu, sigma, nu, f"{alpha:.0%}", f"({t1}, {t2})", False, False


if __name__ == "__main__":
    # app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
