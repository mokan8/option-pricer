from models.black_scholes import BlackScholes

class ImpliedVol:

    @staticmethod
    def solve(option, market_price, tol=1e-6, max_iter=100):
        """
        Solve for implied volatility using Newton-Raphson.
        Falls back to bisection if NR fails.
        """
        sigma = 0.2  # initial guess
        for i in range(max_iter):
            option.sigma = sigma
            price = BlackScholes.price(option)
            vega = BlackScholes.vega(option) * 100  # undo % scaling

            if vega == 0:
                break

            diff = price - market_price
            if abs(diff) < tol:
                return sigma

            sigma -= diff / vega

            # Keep sigma positive
            if sigma <= 0:
                sigma = tol

        # Fallback: bisection
        low, high = 1e-6, 5.0
        for _ in range(max_iter):
            sigma = (low + high) / 2
            option.sigma = sigma
            price = BlackScholes.price(option)
            diff = price - market_price
            if abs(diff) < tol:
                return sigma
            if diff > 0:
                high = sigma
            else:
                low = sigma

        return sigma