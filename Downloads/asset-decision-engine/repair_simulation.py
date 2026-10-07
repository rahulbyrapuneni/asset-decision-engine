import numpy as np


def simulate_repair_cost(
    expected_repair_cost: float,
    variability: float
) -> float:

    mu = (
        np.log(expected_repair_cost)
        - 0.5 * variability ** 2
    )

    simulated_cost = np.random.lognormal(
        mean=mu,
        sigma=variability
    )

    return simulated_cost