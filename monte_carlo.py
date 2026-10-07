import numpy as np

from repair_simulation import simulate_repair_cost


def run_repair_simulation(
    repair_schedule: list,
    variability: float,
    simulations: int
) -> np.ndarray:

    results = []

    for _ in range(simulations):

        total_repairs = 0

        for row in repair_schedule:

            simulated_cost = simulate_repair_cost(
                expected_repair_cost=row["repair_cost"],
                variability=variability
            )

            total_repairs += simulated_cost

        results.append(total_repairs)

    return np.array(results)