import pandas as pd
from scipy.stats import norm
import numpy as np

def d1(S, K, T, r, sigma):
    return (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S,K,T,r,sigma) - sigma*np.sqrt(T)

def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    D1 = d1(S, K, T, r, sigma)
    D2 = D1 - sigma*np.sqrt(T)

    if option_type == "call":
        return S*norm.cdf(D1) - K*np.exp(-r*T)*norm.cdf(D2)
    else:
        return K*np.exp(-r*T)*norm.cdf(-D2) - S*norm.cdf(-D1)

def greeks(S, K, T, r, sigma, option_type="call"):
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)

    if option_type == "call":
        delta = norm.cdf(D1)
        theta = -(S*norm.pdf(D1)*sigma)/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(D2)
        rho = K*T*np.exp(-r*T)*norm.cdf(D2)
    else:
        delta = norm.cdf(D1) - 1
        theta = -(S*norm.pdf(D1)*sigma)/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-D2)
        rho = -K*T*np.exp(-r*T)*norm.cdf(-D2)

    gamma = norm.pdf(D1) / (S*sigma*np.sqrt(T))
    vega = S*norm.pdf(D1) * np.sqrt(T)

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }
