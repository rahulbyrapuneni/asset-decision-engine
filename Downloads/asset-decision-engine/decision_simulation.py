import numpy as np


def run_decision_simulation(
    current_vehicle_repair_simulations: np.ndarray,
    replacement_vehicle_repair_simulations: np.ndarray,
    current_vehicle_depreciation: float,
    replacement_vehicle_depreciation: float,
    current_vehicle_maintenance: float,
    replacement_vehicle_maintenance: float,
    replacement_vehicle_interest: float,
    replacement_vehicle_taxes_and_fees: float
) -> dict:

    keep_costs = (
        current_vehicle_depreciation
        + current_vehicle_maintenance
        + current_vehicle_repair_simulations
    )

    replace_costs = (
        replacement_vehicle_depreciation
        + replacement_vehicle_maintenance
        + replacement_vehicle_repair_simulations
        + replacement_vehicle_interest
        + replacement_vehicle_taxes_and_fees
    )

    keep_wins = keep_costs < replace_costs
    replace_wins = replace_costs < keep_costs
    ties = keep_costs == replace_costs

    keep_probability = keep_wins.mean()
    replace_probability = replace_wins.mean()
    tie_probability = ties.mean()

    return {
        "keep_costs": keep_costs,
        "replace_costs": replace_costs,
        "keep_probability": keep_probability,
        "replace_probability": replace_probability,
        "tie_probability": tie_probability
    }