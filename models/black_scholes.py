import numpy as np
from scipy.stats import norm


class BlackScholes:

    @staticmethod
    def price(option):
        S = option.S
        K = option.K
        T = option.T
        r = option.r
        sigma = option.sigma

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option.is_call:
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return price
    @staticmethod
    def delta(option):
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        return norm.cdf(d1) if option.is_call else -norm.cdf(-d1)

    @staticmethod
    def gamma(option):
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        return norm.pdf(d1) / (S * sigma * np.sqrt(T))

    @staticmethod
    def vega(option):
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        return S * norm.pdf(d1) * np.sqrt(T) / 100  # per 1% vol

    @staticmethod
    def theta(option):
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option.is_call:
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                     - r * K * np.exp(-r * T) * norm.cdf(d2))
        else:
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                     + r * K * np.exp(-r * T) * norm.cdf(-d2))
        return theta / 365  # per day

    @staticmethod
    def rho(option):
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option.is_call:
            return K * T * np.exp(-r * T) * norm.cdf(d2) / 100  # per 1% rate
        else:
            return -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100