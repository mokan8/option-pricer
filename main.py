from instruments.vanilla import VanillaOption
from models.black_scholes import BlackScholes

option = VanillaOption(
    S=100, K=100, T=1, r=0.05, sigma=0.2, is_call=True
)

print(f"Price: {BlackScholes.price(option):.4f}")
print(f"Delta: {BlackScholes.delta(option):.4f}")
print(f"Gamma: {BlackScholes.gamma(option):.4f}")
print(f"Vega: {BlackScholes.vega(option):.4f}")
print(f"Theta: {BlackScholes.theta(option):.4f}")
print(f"Rho: {BlackScholes.rho(option):.4f}")