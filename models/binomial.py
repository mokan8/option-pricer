import numpy as np

class BinomialTree:

    @staticmethod
    def price(option, steps=100):
        """
        Cox-Ross-Rubinstein binomial tree pricer for European or American options.
        Handles early exercise for American options if needed.
        """

        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        dt = T / steps
        u = np.exp(sigma * np.sqrt(dt))       # up factor
        d = 1 / u                             # down factor
        p = (np.exp(r * dt) - d) / (u - d)   # risk-neutral probability

        # Initialize asset prices at maturity
        ST = np.zeros(steps + 1)
        for i in range(steps + 1):
            ST[i] = S * (u ** (steps - i)) * (d ** i)

        # Option values at maturity
        if option.is_call:
            option_values = np.maximum(ST - K, 0)
        else:
            option_values = np.maximum(K - ST, 0)

        # Backward induction
        for step in range(steps - 1, -1, -1):
            for i in range(step + 1):
                option_values[i] = np.exp(-r * dt) * (
                    p * option_values[i] + (1 - p) * option_values[i + 1]
                )

                # For American options, check early exercise
                if hasattr(option, "is_american") and option.is_american:
                    S_t = S * (u ** (step - i)) * (d ** i)
                    if option.is_call:
                        option_values[i] = max(option_values[i], S_t - K)
                    else:
                        option_values[i] = max(option_values[i], K - S_t)

        return option_values[0]