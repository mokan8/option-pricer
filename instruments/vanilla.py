from dataclasses import dataclass

@dataclass
class VanillaOption:
    S: float      # Spot price
    K: float      # Strike
    T: float      # Time to maturity (years)
    r: float      # Risk-free rate
    sigma: float  # Volatility
    is_call: bool = True