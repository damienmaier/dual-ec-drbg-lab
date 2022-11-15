import functools

from sage.all_cmdline import *

import dualec
import dualec2

# Returns a list containing the points with a given x coordinate
# If no such point exists, an empty list is returned
lift_x = functools.partial(dualec.RNG().E.lift_x, all=True)

d = Integer(94055013642250167747369562496124155724387099203394376242127859919568606997696)
inverse_d = inverse_mod(d, dualec.RNG().n)


def next_state(state_times_Q):
    """
    From the point `state * Q`, finds the point `state * P` using the backdoor and returns the x coordinate of `state * P`
    """
    return (inverse_d * state_times_Q)[0].lift()


def clone_dual_ec_drbg(output1, output2):
    """
    From the first two outputs of an instance of `dualec.RNG`, creates a clone PRNG.

    The clone PRNG has the exact same state as the original PRNG just after it outputted `output2`.

    Returns the clone PRNG.
    """
    clone_rng = dualec.RNG()

    def untruncate(filling):
        return (output1 << 8) + filling

    def state_matches_output2(state2_candidate):
        candidate_output = (state2_candidate * clone_rng.Q)[0].lift() >> 8
        return candidate_output == output2

    state2 = next(
        filter(state_matches_output2,
               map(next_state,
                   map(lambda a: a[0],
                       filter(lambda a: a != [],
                              map(lift_x,
                                  map(untruncate,
                                      range(2 ** 8)))))))
    )

    clone_rng.state = state2

    return clone_rng


def discrete_logarithm(base_point, values, min_exponent, max_exponent):
    """
    Searches for the discrete logarithm of several points in an interval.

    `base_point` is the base of the discrete logarithm.

    `values` is a list of points.

    The function searches for an integer e in the interval [`min_exponent`, `max_exponent`)
    such that e * `base_point` is equal to one of the elements of `values`.

    The function returns the first found e.
    """
    m = int(math.sqrt(max_exponent - min_exponent))

    pairs = dict()
    base_point_to_the_j = 0 * base_point
    for j in range(0, m):
        pairs[base_point_to_the_j] = j
        base_point_to_the_j += base_point

    base_point_to_minus_m = -m * base_point

    y_values = list(map(lambda y: y - min_exponent * base_point, values))
    for i in range(0, m):
        found_y_values = list(filter(lambda y: y in pairs, y_values))
        if found_y_values:
            return min_exponent + i * m + pairs[found_y_values[0]]
        y_values = list(map(lambda y: y + base_point_to_minus_m, y_values))


def clone_dual_ec2_drbg(output1, output2):
    """
    From the first two outputs of an instance of `dualec2.RNG`, creates a clone PRNG.

    The clone PRNG has the exact same state as the original PRNG just after it outputted `output2`.

    Returns the clone PRNG.
    """
    clone_rng = dualec2.RNG2()

    lifted_output2_points = lift_x(output2)
    state2_minus_e = next_state(lift_x(output1)[0])

    state2 = discrete_logarithm(
        base_point=clone_rng.Q,
        values=lifted_output2_points,
        min_exponent=state2_minus_e,
        max_exponent=state2_minus_e + 2**20
    )

    clone_rng.state = state2
    clone_rng.e = state2 - state2_minus_e

    return clone_rng


if __name__ == "__main__":
    v11 = Integer(47158993444934820804120615356705775493102049634442166933920330463575468537)
    v12 = Integer(347579258611507783115138832575460777805797034981600034217491363903238440725)
    v21 = Integer(75062883201512730874171724409024819190513643228716315531546042467855523724936)
    v22 = Integer(26163388324561385356851885033494971353772464926640706059833778037470118241702)

    clone_drbg1 = clone_dual_ec_drbg(v11, v12)
    print("v13 =", clone_drbg1.next())

    clone_drbg2 = clone_dual_ec2_drbg(v21, v22)
    print("v23 =", clone_drbg2.next())
