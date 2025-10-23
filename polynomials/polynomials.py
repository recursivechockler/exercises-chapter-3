from numbers import Number
from numbers import Integral
from functools import reduce

class Polynomial:

    def __init__(self, coefs):
        while coefs and coefs[-1] == 0:
            coefs = coefs[:-1]

        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Polynomial(tuple(-c for c in self.coefficients))

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):

        if isinstance(other, Number):
            return Polynomial(tuple(c * other for c in self.coefficients))
        
        elif isinstance(other, Polynomial):
            result = Polynomial((0,))

            for power, coef in enumerate(other.coefficients):
                product_coefs = tuple([0] * power) + self.coefficients
                product_coefs = tuple(c * coef for c in product_coefs)

                result += Polynomial(product_coefs)
            
            return result
        
        else:
            return NotImplemented
    
    def __rmul__(self, other):
        return self * other  # multiplication commutes
    
    def __pow__(self, power):

        if isinstance(power, Integral):
            if power > 0:
                return reduce(lambda x, y: x * y, [self] * power)
            else:
                return NotImplemented
            
        else:
            return NotImplemented
    
    def __call__(self, scalar):
        return sum(coef * (scalar ** power) for power, coef in enumerate(self.coefficients))

    def dx(self):
        if isinstance(self, Polynomial):
            if self.degree() == 0:
                return Polynomial((0,))

            coefs = [c * power for power, c in enumerate(self.coefficients)]
            return Polynomial(tuple(coefs[1:]))
        
        return NotImplemented
    
def derivative(poly):
    return poly.dx()
