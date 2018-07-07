import math
from scipy.stats import norm
def Theo(Type, S, X, t, r, b, sigma):
    #black scholes equation
    d1 = (math.log(S / X) + (b + sigma * sigma / 2.0) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    if "C" in Type:
        return S * math.exp((b - r) * t) * norm.cdf(d1) - X * math.exp(-r * t) * norm.cdf(d2)
    elif "P" in Type:
        return X * math.exp(-r * t) * norm.cdf(-d2) - S * math.exp((b - r) * t) * norm.cdf(-d1)
    else:
        return 0


def Delta(Type, S, X, t, r, b, sigma):
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    if 'C' in Type:
        return math.exp((b-r)*t) * norm.cdf(d1)
    elif 'P' in Type:
        return math.exp((b - r) * t) * (norm.cdf(d1) - 1)



def Gamma(S, X, t, r, b, sigma):
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    return math.exp((b-r)*t) * norm.pdf(d1) / (S*sigma * math.sqrt(t))


def Theta(Type, S, X, t, r, b, sigma):
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    term_1 = -S * math.exp((b-r)*t)*norm.pdf(d1)* sigma/ (2 * math.sqrt(t))
    term_2 = (b-r) * S * math.exp((b-r)*t)* norm.cdf(d1)


    if 'C' in Type:
        return (term_1 - term_2 -r * X * math.exp(-r *t) * norm.cdf(d2))/365.0

    elif 'P' in Type:
        return (term_1 + term_2 + r * X * math.exp(-r * t) * norm.cdf(-d2)) / 365.0


def Vega(S, X, t, r, b, sigma):
    d1 = (math.log(S / X) + (b + sigma ** 2.0 / 2.0) * t) / (sigma * math.sqrt(t))
    return (S * math.exp((b-r)*t) * norm.pdf(d1) * math.sqrt(t)) / 100.0
"""
Type = 'P'
S = 101.0
X = 102.0
t = .30
r = .02
b = .00
sigma = .10

print('Theo: ', Theo(Type,S,X,t,r,b,sigma))

print('Delta: ', Delta(Type,S,X,t,r,b,sigma))
print('Delta2: ', (-1 * Theo(Type,S,X,t,r,b,sigma)+ Theo(Type,S + .001,X,t,r,b,sigma))/.001)

print('Gamma: ', Gamma(S,X,t,r,b,sigma))
print('Gamma2: ', (-1 * Delta(Type,S,X,t,r,b,sigma)+Delta(Type,S + .001,X,t,r,b,sigma))/.001)

print('Theta: ', Theta(Type, S, X, t, r, b, sigma)/365.0)
print('Theta2: ', (-1 * Theo(Type,S,X,t,r,b,sigma)+Theo(Type,S,X,t - .01/365.0,r,b,sigma))/.01)

print('Vega: ', Vega(S, X, t, r, b, sigma)/100.0)
print('Vega2: ', (Theo(Type, S, X, t, r, b, sigma + .01/1000.0)- Theo(Type, S, X, t, r,b, sigma))/.001)


Type = 'P'
S = 101.0
X = 102.0
t = .01
r = .02
b = .00
sigma = .10
print('Vega: ', Vega(S, X, t, r, b, sigma)/100.0)
"""
