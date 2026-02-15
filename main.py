from instruments.vanilla import VanillaOption
from models.black_scholes import BlackScholes
from models.monte_carlo import MonteCarlo

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