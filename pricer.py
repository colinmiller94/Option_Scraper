import math
from scipy.stats import norm
def Theo(Type, S, X, t, r, b, sigma):
    """
    :param Type: call/put
    :param S: underlying spot price
    :param X: strike price
    :param t: time to expiration (years)
    :param r: interest rate (decimal)
    :param b: dividend rate (decimal)
    :param sigma: volatility
    :return: theoretical option price
    """

    d1 = (math.log(S / X) + (b + sigma * sigma / 2.0) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    if "C" in Type:
        return S * math.exp((b - r) * t) * norm.cdf(d1) - X * math.exp(-r * t) * norm.cdf(d2)
    elif "P" in Type:
        return X * math.exp(-r * t) * norm.cdf(-d2) - S * math.exp((b - r) * t) * norm.cdf(-d1)
    else:
        return 0


def Delta(Type, S, X, t, r, b, sigma):
    """
    :param Type: call/put
    :param S: underlying spot price
    :param X: strike price
    :param t: time to expiration (years)
    :param r: interest rate (decimal)
    :param b: dividend rate (decimal)
    :param sigma: volatility
    :return: option delta
    """
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    if 'C' in Type:
        return math.exp((b-r)*t) * norm.cdf(d1)
    elif 'P' in Type:
        return math.exp((b - r) * t) * (norm.cdf(d1) - 1)



def Gamma(S, X, t, r, b, sigma):
    """
    :param S: underlying spot price
    :param X: strike price
    :param t: time to expiration (years)
    :param r: interest rate (decimal)
    :param b: dividend rate (decimal)
    :param sigma: volatility
    :return: option gamma
    """
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    return math.exp((b-r)*t) * norm.pdf(d1) / (S*sigma * math.sqrt(t))


def Theta(Type, S, X, t, r, b, sigma):
    """
    :param Type: call/put
    :param S: underlying spot price
    :param X: strike price
    :param t: time to expiration (years)
    :param r: interest rate (decimal)
    :param b: dividend rate (decimal)
    :param sigma: volatility
    :return: option theta
    """

    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    term_1 = -S * math.exp((b-r)*t)*norm.pdf(d1)* sigma/ (2 * math.sqrt(t))
    term_2 = (b-r) * S * math.exp((b-r)*t)* norm.cdf(d1)


    if 'C' in Type:
        return (term_1 - term_2 -r * X * math.exp(-r *t) * norm.cdf(d2))/365.0

    elif 'P' in Type:
        return (term_1 + term_2 + r * X * math.exp(-r * t) * norm.cdf(-d2)) / 365.0


def Vega(S, X, t, r, b, sigma):
    """
    :param S: underlying spot price
    :param X: strike price
    :param t: time to expiration (years)
    :param r: interest rate (decimal)
    :param b: dividend rate (decimal)
    :param sigma: volatility
    :return: option vega
    """
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    return (S * math.exp((b-r)*t) * norm.pdf(d1) * math.sqrt(t)) / 100.0
