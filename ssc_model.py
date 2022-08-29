import plotly.graph_objects as go
import scipy.stats as stat
import numpy as np

stat_colours = {
    "norm": "#d10373",
    "z": "rgba(158, 171, 5, 0.5)",
    "mean": "#f49103",
    "+-1std": "#0085a1",
    "+-2std": "#003896",
    "+-3std": "#6a2150"
}

def create_blank_fig():
    x = np.linspace(stat.t.ppf(0.0001, 10),
                    stat.t.ppf(0.9999, 10),
                    10000)
    t_x = stat.t.pdf(x, 10)
    blank_fig = go.Figure(
        go.Scatter(x=x, y=t_x, marker_color=stat_colours["norm"]),
                   layout={"margin": dict(t=20, b=10, l=20, r=20),
                           "height": 400,
                           "font_size": 14})
    blank_fig.update_xaxes(tick0=-6, dtick=1)
    blank_fig.update_layout(dragmode=False)
    return blank_fig
