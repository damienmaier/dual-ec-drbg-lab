import functools

from sage.all_cmdline import *

import dualec
import dualec2


lift_x = functools.partial(dualec.RNG().E.lift_x, all=True)


def next_state(state_times_Q):
    d = Integer(94055013642250167747369562496124155724387099203394376242127859919568606997696)
    inverse_d = inverse_mod(d, dualec.RNG().n)
    return (inverse_d * state_times_Q)[0].lift()


def clone_dual_ec_drbg(output1, output2):
    rng = dualec.RNG()

    def shift_left(filling):
        return (output1 << 8) + filling

    def state_matches_output2(state2_candidate):
        expected_output = (state2_candidate * rng.Q)[0].lift() >> 8
        return expected_output == output2

    state2 = next(
        filter(state_matches_output2,
               map(next_state,
                   map(lambda a: a[0],
                       filter(lambda a: a != [],
                              map(lift_x,
                                  map(shift_left,
                                      range(2 ** 8))))))))

    rng.state = state2

    return rng


def discrete_logarithm(base_point, values, min, max):
    m = int(math.sqrt(max - min))

    pairs = dict()
    base_point_to_the_j = 0 * base_point
    for j in range(0, m):
        pairs[base_point_to_the_j] = j
        base_point_to_the_j += base_point

    base_point_to_minus_m = -m * base_point

    y_values = list(map(lambda y: y - min * base_point, values))
    for i in range(0, m):
        found_y_values = list(filter(lambda y: y in pairs, y_values))
        if found_y_values:
            return min + i * m + pairs[found_y_values[0]]
        y_values = list(map(lambda y: y + base_point_to_minus_m, y_values))



def clone_dual_ec2_drbg(output1, output2):
    rng = dualec2.RNG2()

    lifted_output2 = lift_x(output2)
    state2_minus_e = next_state(lift_x(output1)[0])

    state2 = discrete_logarithm(
        rng.Q,
        lifted_output2,
        state2_minus_e,
        state2_minus_e + 2**20
    )

    rng.state = state2
    rng.e = state2 - state2_minus_e

    return rng
