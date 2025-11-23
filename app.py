import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from bs import black_scholes_price, greeks
import plotly.express as px
import numpy as np
from utils import generate_surface

app = dash.Dash(__name__)

app.layout = html.Div(className="app-container", children=[

    html.H1("Black-Scholes Pricer Dashboard"),

    html.Div(className="two-column", children=[

        # LEFT COLUMN — compact controls
        html.Div(className="left-column", children=[

            html.Label("Option Type"),
            dcc.RadioItems(
                id="option-type",
                options=[
                    {"label": "Call", "value": "call"},
                    {"label": "Put", "value": "put"}
                ],
                value="call",
                labelStyle={"display": "inline-block", "margin-right": "15px"}
            ),

            html.Div(className="slider-group", children=[
                html.Label("Spot Price (S)"),
                dcc.Slider(id="spot", min=50, max=200, step=1, value=100,
                        marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            ]),

            html.Div(className="slider-group", children=[
                html.Label("Strike Price (K)"),
                dcc.Slider(id="strike", min=50, max=200, step=1, value=100,
                        marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            ]),

            html.Div(className="slider-group", children=[
                html.Label("Volatility (%)"),
                dcc.Slider(id="vol", min=5, max=150, step=1, value=20,
                        marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            ]),

            html.Div(className="slider-group", children=[
                html.Label("Time to Maturity (Years)"),
                dcc.Slider(id="tau", min=0.01, max=2, step=0.01, value=1,
                        marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            ]),

            html.Div(className="slider-group", children=[
                html.Label("Interest Rate (%)"),
                dcc.Slider(id="rate", min=0, max=10, step=0.1, value=2,
                        marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            ]),
        ]),

        # RIGHT COLUMN — price and greeks on top
        html.Div(className="right-column", children=[

            html.Div(className="top-right-panel", children=[

                # price at top left of right column
                html.Div(id="price-output", className="price-box"),

                # greeks to the right of price
                html.Div(className="greeks-vertical", children=[
                    html.Div(id="delta-box", className="greek-box"),
                    html.Div(id="gamma-box", className="greek-box"),
                    html.Div(id="vega-box", className="greek-box"),
                    html.Div(id="theta-box", className="greek-box"),
                    html.Div(id="rho-box", className="greek-box"),
                ]),
            ]),

            dcc.Graph(id="heatmap", style={"height": "500px", "marginTop": "30px"})
        ])
    ])
])


# ---- PRICE CALLBACK ----
@app.callback(
    Output("price-output", "children"),
    [
        Input("spot", "value"),
        Input("strike", "value"),
        Input("vol", "value"),
        Input("tau", "value"),
        Input("rate", "value"),
        Input("option-type", "value"),
    ]
)
def update_price(S, K, vol, T, r, opt_type):
    price = black_scholes_price(S, K, T, r/100, vol/100, option_type=opt_type)
    return f"${price:,.2f}"


# ---- GREEKS CALLBACK ----
@app.callback(
    [
        Output("delta-box", "children"),
        Output("gamma-box", "children"),
        Output("vega-box", "children"),
        Output("theta-box", "children"),
        Output("rho-box", "children"),
    ],
    [
        Input("spot", "value"),
        Input("strike", "value"),
        Input("vol", "value"),
        Input("tau", "value"),
        Input("rate", "value"),
        Input("option-type", "value"),
    ]
)
def update_greeks(S, K, vol, T, r, opt_type):
    g = greeks(S, K, T, r/100, vol/100, option_type=opt_type)
    return (
        f"Δ Delta: {g['delta']:.4f}",
        f"Γ Gamma: {g['gamma']:.6f}",
        f"V Vega:  {g['vega']:.4f}",
        f"Θ Theta: {g['theta']:.4f}",
        f"ρ Rho:   {g['rho']:.4f}"
    )


# ---- HEATMAP CALLBACK ----
@app.callback(
    Output("heatmap", "figure"),
    [
        Input("strike", "value"),
        Input("tau", "value"),
        Input("rate", "value"),
        Input("option-type", "value"),
    ]
)
def update_heatmap(K, T, r, opt_type):
    S_vals = np.linspace(50, 150, 50)
    vol_vals = np.linspace(0.05, 0.50, 50)

    Z = generate_surface(S_vals, vol_vals, K, T, r/100, mode="price")

    fig = px.imshow(
        Z,
        x=vol_vals,
        y=S_vals,
        aspect="auto",
        color_continuous_scale="Viridis",
        labels={"x": "Volatility", "y": "Spot Price"},
        title="Option Price Heatmap"
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
