import numpy as np
from bs import black_scholes_price

def generate_surface(S_vals, vol_vals, K, T, r, mode="price", ref_price=None):
    Z = np.zeros((len(S_vals), len(vol_vals)))

    for i, S in enumerate(S_vals):
        for j, vol in enumerate(vol_vals):
            price = black_scholes_price(S, K, T, r, vol)

            if mode == "price":
                Z[i, j] = price
            else:
                Z[i, j] = price - ref_price

    return Z
