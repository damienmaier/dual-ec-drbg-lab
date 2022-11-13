from unittest import TestCase

from sage.all_cmdline import *

import dualec
import dualec2
import dualec_attack


class Test(TestCase):
    def test_clone_dual_ec_drbg(self):
        original_drbg = dualec.RNG()
        cloned_drbg = dualec_attack.clone_dual_ec_drbg(original_drbg.next(), original_drbg.next())
        for _ in range(10):
            self.assertEqual(cloned_drbg.next(), original_drbg.next())

    def test_clone_dual_ec2_drbg(self):
        original_drbg = dualec2.RNG2()
        cloned_drbg = dualec_attack.clone_dual_ec2_drbg(original_drbg.next(), original_drbg.next())
        for _ in range(10):
            self.assertEqual(cloned_drbg.next(), original_drbg.next())

    def test_discrete_logarithm(self):
        elliptic_curve = EllipticCurve(
            GF(Integer(115792089210356248762697446949407573530086143415290314195533631308867097853951)),
            [-Integer(3), (Integer(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b))]
        )

        Q = elliptic_curve.lift_x(
            Integer(48427683432535470441420506435187576850614353788067201511820511758658877995605))

        exponent = 2 ** 20-1

        self.assertEqual(exponent, dualec_attack.discrete_logarithm(Q, [exponent * Q, 2 ** 100 * Q]))
