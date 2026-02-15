from fastapi import FastAPI
from pydantic import BaseModel
from instruments.vanilla import VanillaOption
from models.black_scholes import BlackScholes
from models.monte_carlo import MonteCarlo
from models.binomial import BinomialTree
from models.implied_vol import ImpliedVol
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Option Pricer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mokan8.github.io"],  # your site URL
    allow_methods=["*"],
    allow_headers=["*"],
)


class OptionInput(BaseModel):
    S: float
    K: float
    T: float
    r: float
    sigma: float = None  # optional for implied vol
    is_call: bool = True
    market_price: float = None
    is_american: bool = False
    mc_paths: int = 100_000
    binomial_steps: int = 100


@app.post("/price")
def price(option_input: OptionInput):
    # Create VanillaOption
    option = VanillaOption(
        S=option_input.S,
        K=option_input.K,
        T=option_input.T,
        r=option_input.r,
        sigma=option_input.sigma or 0.2,
        is_call=option_input.is_call
    )

    # Set American flag if provided
    if option_input.is_american:
        option.is_american = True

    # Prices
    bs_price = BlackScholes.price(option)
    mc_price = MonteCarlo.price(option, paths=option_input.mc_paths, seed=42)
    binomial_price = BinomialTree.price(option, steps=option_input.binomial_steps)

    # Greeks
    delta = BlackScholes.delta(option)
    gamma = BlackScholes.gamma(option)
    vega = BlackScholes.vega(option)
    theta = BlackScholes.theta(option)
    rho = BlackScholes.rho(option)

    # Implied vol if market_price given
    implied_vol = None
    if option_input.market_price is not None:
        implied_vol = ImpliedVol.solve(option, option_input.market_price)

    return {
        "bs_price": bs_price,
        "mc_price": mc_price,
        "binomial_price": binomial_price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "implied_vol": implied_vol
    }
    