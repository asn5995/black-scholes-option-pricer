# black-scholes-option-pricer
Black-Scholes option pricer with Greeks and an interactive Dash UI for price and PnL surfaces. Built to extend into IV modeling, scenario analysis, and IBKR-based trading automation.

black-scholes-option-pricer/
│
├── app.py                  # Interactive Dash UI
├── bs.py                   # Black-Scholes pricing + Greeks
├── utils.py                # Heatmap + PnL surface functions
├── config.py               # Future settings (optional)
├── requirements.txt        # Dependencies
├── README.md
│
├── assets/
│   └── style.css           # Dash styling
│
├── data/
│   ├── sample_option_chain.csv
│   └── historical_prices.csv
│
└── notebooks/
    └── experiments.ipynb   # Testing & development notebook


