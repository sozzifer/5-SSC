import numpy as np
import plotly.graph_objects as go
import scipy.stats as stat

# Colour palette
stat_colours = {
    "norm": "#d10373",
    "z": "rgba(158, 171, 5, 0.5)",
    "mean": "#f49103",
    "+-1std": "#0085a1",
    "+-2std": "#003896",
    "+-3std": "#6a2150"
}


# Generate t distribution for mean (mu), standard deviation (sigma), degrees of freedom (nu) and confidence level (alpha) user entry (two-sided confidence interval)
def t_dist_2_sided(mu, sigma, nu, alpha):
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
    return x, t_x, t1, t2, alpha_1tail, lower_ci, t_pdf1, upper_ci, t_pdf2

# Generate t distribution for mean (mu), standard deviation (sigma), degrees of freedom (nu) and confidence level (alpha) user entry (one-sided confidence interval)
def t_dist_1_sided(mu, sigma, nu, alpha):
    x = np.linspace(stat.t.ppf(0.0001, nu, mu, sigma),
                    stat.t.ppf(0.9999, nu, mu, sigma),
                    10000)
    t_x = stat.t.pdf(x, nu, mu, sigma)
    conf_int = stat.t.interval(1 - ((1 - alpha)*2), nu, mu, sigma)
    t1 = round(conf_int[0], 3)
    t2 = round(conf_int[1], 3)
    lower_ci = np.linspace(stat.t.ppf(0.0001, nu, mu, sigma),
                           stat.t.ppf(alpha, nu, mu, sigma),
                           10000)
    t_pdf1 = stat.t.pdf(lower_ci, nu, mu, sigma)
    upper_ci = np.linspace(stat.t.ppf(1-alpha, nu, mu, sigma),
                           stat.t.ppf(0.9999, nu, mu, sigma),
                           10000)
    t_pdf2 = stat.t.pdf(upper_ci, nu, mu, sigma)
    return x, t_x, t1, t2, lower_ci, t_pdf1, upper_ci, t_pdf2


# Create blank figure (UX)
def create_blank_fig():
    x = np.linspace(stat.t.ppf(0.0001, 10),
                    stat.t.ppf(0.9999, 10),
                    10000)
    t_x = stat.t.pdf(x, 10)
    blank_fig = go.Figure(
        go.Scatter(x=x,
                   y=t_x,
                   marker_color=stat_colours["norm"]),
        layout={"margin": dict(t=20, b=10, l=20, r=20),
                "height": 400,
                "font_size": 14})
    blank_fig.update_xaxes(tick0=-6, dtick=1)
    blank_fig.update_layout(dragmode=False)
    return blank_fig

