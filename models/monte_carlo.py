import numpy as np

class MonteCarlo:

    @staticmethod
    def price(option, paths=100_000, seed=None):
        """
        Monte Carlo pricer for European vanilla options.

        Parameters:
        - option: VanillaOption object
        - paths: number of simulated price paths
        - seed: random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)

        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma

        # Generate random standard normals
        Z = np.random.randn(paths)

        # Simulate terminal prices using Geometric Brownian Motion
        ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

        # Compute payoffs
        if option.is_call:
            payoffs = np.maximum(ST - K, 0)
        else:
            payoffs = np.maximum(K - ST, 0)

        # Discount to present value
        price = np.exp(-r * T) * np.mean(payoffs)

        return price