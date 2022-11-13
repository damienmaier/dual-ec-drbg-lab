"""
Original sage file for the Dual EC PRNG
"""

class RNG:
    def __init__(self):
        p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
        b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        self.E = EllipticCurve(GF(p), [-3,b])

        self.Q = self.E.lift_x(48427683432535470441420506435187576850614353788067201511820511758658877995605)
        self.P = self.E.lift_x(110132242570903543114281108957810642547914101978454713627126079296746570253883)
        self.n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
        self.state = ZZ.random_element(1, self.n)
    def next(self):
        self.state = (self.state * self.P)[0].lift()
        return (self.state * self.Q)[0].lift() >> 8
