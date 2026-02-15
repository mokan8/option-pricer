from instruments.vanilla import VanillaOption
from models.black_scholes import BlackScholes
from models.monte_carlo import MonteCarlo
from models.binomial import BinomialTree
from models.implied_vol import ImpliedVol

if __name__ == "__main__":

    option = VanillaOption(
        S=100,      # Spot price
        K=100,      # Strike
        T=1.0,      # Maturity in years
        r=0.05,     # Risk-free rate
        sigma=0.2,  # Volatility
        is_call=True
    )

    print(f"Black–Scholes Price: {BlackScholes.price(option):.4f}")
    print(f"Delta: {BlackScholes.delta(option):.4f}")
    print(f"Gamma: {BlackScholes.gamma(option):.4f}")
    print(f"Vega: {BlackScholes.vega(option):.4f}")
    print(f"Theta: {BlackScholes.theta(option):.4f}")
    print(f"Rho: {BlackScholes.rho(option):.4f}")


    mc_price = MonteCarlo.price(option, paths=100_000, seed=42)
    print(f"Monte Carlo Price: {mc_price:.4f}")



    # European option (same as before)
    bt_price = BinomialTree.price(option, steps=100)
    print(f"Binomial Tree Price (European): {bt_price:.4f}")

    # Example: American option
    option.is_american = True
    bt_american_price = BinomialTree.price(option, steps=100)
    print(f"Binomial Tree Price (American): {bt_american_price:.4f}")

    # Assume market price slightly higher than Black-Scholes
    market_price = 12.0

    iv = ImpliedVol.solve(option, market_price)
    print(f"Implied Volatility: {iv:.4f}")
