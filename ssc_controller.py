from dash import html, Input, Output, State, exceptions
import math
import numpy as np
import plotly.graph_objects as go
import scipy.stats as stat
from ssc_model import stat_colours, t_dist_1_sided, t_dist_2_sided
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
    Output("conf-text", "children"),
    # User Input for degrees of freedom/confidence level disabled until mean/SD set
    Output("nu", "disabled"),
    Output("alpha", "disabled"),
    # Inputs
    Input("submit", "n_clicks"),
    State("mu", "value"),
    State("sigma", "value"),
    Input("one-two-sided", "value"),
    Input("nu", "value"),
    Input("alpha", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, mu, sigma, side, nu, alpha):
    if n_clicks is None or mu is None or sigma is None or nu is None:
        raise exceptions.PreventUpdate
    else:
        # Screen reader text
        sr_t = f"Student's t distribution graph with mean {mu}, standard deviation {sigma}, {nu} degrees of freedom and confidence level {alpha*100}%"
        # Plot two-sided confidence interval
        if side == "<>":
            x, t_x, t1, t2, alpha_1tail, lower_ci, t_pdf1, upper_ci, t_pdf2 = t_dist_2_sided(mu, sigma, nu, alpha)
            fig = go.Figure(go.Scatter(x=x,
                                       y=t_x,
                                       name="t distribution",
                                       marker_color=stat_colours["norm"],
                                       hoverinfo="skip"),
                            layout={"margin": dict(t=20, b=10, l=20, r=20),
                                    "height": 400,
                                    "font_size": 14})
            fig.update_xaxes(dtick=math.ceil(sigma/2))
            fig.add_trace(go.Scatter(x=lower_ci,
                                     y=t_pdf1,
                                     marker_color=stat_colours["norm"],
                                     hoverinfo="skip",
                                     fill="tozeroy",
                                     fillcolor=stat_colours["z"],
                                     showlegend=False))
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
            return fig, sr_t, {"display": "inline"}, mu, sigma, nu, f"{alpha:.0%}",  [html.Span("Confidence interval: ", className="bold-p"), html.Span(f"({t1}, {t2})")], f"{alpha:.0%} of values lie in the range ({t1}, {t2}) and {1-alpha:.0%} lie outside this range (shaded area) - in other words, the probability that a randomly selected value lies between {t1} and {t2} is {alpha:.0%}", False, False
        # Plot one-sided confidence interval
        else:
            x, t_x, t1, t2, lower_ci, t_pdf1, upper_ci, t_pdf2 = t_dist_1_sided(mu, sigma, nu, alpha)
            if side == "<":
                fig = go.Figure(go.Scatter(x=x,
                                           y=t_x,
                                           name="t distribution",
                                           marker_color=stat_colours["norm"],
                                           hoverinfo="skip"),
                                layout={"margin": dict(t=20, b=10, l=20, r=20),
                                        "height": 400,
                                        "font_size": 14})
                fig.update_xaxes(dtick=math.floor(sigma/2))
                fig.add_trace(go.Scatter(x=lower_ci,
                                         y=t_pdf1,
                                         marker_color=stat_colours["norm"],
                                         hoverinfo="skip",
                                         fill="tozeroy",
                                         fillcolor=stat_colours["z"],
                                         showlegend=False))
                fig.add_trace(go.Scatter(x=[stat.t.ppf(alpha, nu, mu, sigma)] * 10,
                                         y=np.linspace(0, t_pdf1[-1], 10),
                                         name="Upper limit for T",
                                         marker_color=stat_colours["+-1std"],
                                         marker_opacity=0,
                                         hovertemplate="Upper limit for T: %{x:.3f}<extra></extra>"))
                fig.update_layout(dragmode=False)
                return fig, sr_t, {"display": "inline"}, mu, sigma, nu, f"{alpha:.0%}", [html.Span("Upper limit for T: ", className="bold-p"), html.Span(f"{t2}")], f"{alpha:.0%} of values are less than {t2} (shaded area) - in other words, the probability that a randomly selected value is less than {t2} is {alpha:.0%}", False, False
            else:
                fig = go.Figure(go.Scatter(x=x,
                                           y=t_x,
                                           name="t distribution",
                                           marker_color=stat_colours["norm"],
                                           hoverinfo="skip"),
                                layout={"margin": dict(t=20, b=10, l=20, r=20),
                                        "height": 400,
                                        "font_size": 14})
                fig.update_xaxes(dtick=math.floor(sigma/2))
                fig.add_trace(go.Scatter(x=upper_ci,
                                         y=t_pdf2,
                                         marker_color=stat_colours["norm"],
                                         hoverinfo="skip",
                                         fill="tozeroy",
                                         fillcolor=stat_colours["z"],
                                         showlegend=False))
                fig.add_trace(go.Scatter(x=[stat.t.ppf(1-alpha, nu, mu, sigma)] * 10,
                                         y=np.linspace(0, t_pdf2[0], 10),
                                         name="Lower limit for T",
                                         marker_color=stat_colours["+-1std"],
                                         marker_opacity=0,
                                         hovertemplate="Lower limit for T: %{x:.3f}<extra></extra>"))
                fig.update_layout(dragmode=False)
                return fig, sr_t, {"display": "inline"}, mu, sigma, nu, f"{alpha:.0%}", [html.Span("Lower limit for T: ", className="bold-p"), html.Span(f"{t1}")], f"{alpha:.0%} of values are greater than {t1} (shaded area) - in other words, the probability that a randomly selected value is greater than {t1} is {alpha:.0%}", False, False


if __name__ == "__main__":
    app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
