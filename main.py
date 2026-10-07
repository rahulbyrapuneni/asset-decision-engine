import numpy as np

from inputs import (
    current_vehicle,
    replacement_vehicle,
    analysis
)

from depreciation_model import (
    estimate_future_value,
    build_depreciation_schedule
)

from maintenance_model import (
    build_maintenance_schedule,
    calculate_total_maintenance
)

from repair_model import (
    build_repair_schedule,
    calculate_total_repairs
)

from financial_model import (
    calculate_keep_cost,
    calculate_replace_cost,
    calculate_amortization_schedule
)

from monte_carlo import run_repair_simulation

from decision_simulation import run_decision_simulation


# ---DEPRECIATION---

current_vehicle_future_value = estimate_future_value(
    current_value=current_vehicle["current_value"],
    annual_depreciation_rate=current_vehicle[
        "annual_depreciation_rate"
    ],
    years=analysis["years"]
)

replacement_vehicle_future_value = estimate_future_value(
    current_value=replacement_vehicle["purchase_price"],
    annual_depreciation_rate=replacement_vehicle[
        "annual_depreciation_rate"
    ],
    years=analysis["years"]
)

current_vehicle_depreciation_schedule = (
    build_depreciation_schedule(
        current_value=current_vehicle["current_value"],
        annual_depreciation_rate=current_vehicle[
            "annual_depreciation_rate"
        ],
        years=analysis["years"]
    )
)

replacement_vehicle_depreciation_schedule = (
    build_depreciation_schedule(
        current_value=replacement_vehicle["purchase_price"],
        annual_depreciation_rate=replacement_vehicle[
            "annual_depreciation_rate"
        ],
        years=analysis["years"]
    )
)


# ---MAINTENANCE---

current_vehicle_maintenance_schedule = (
    build_maintenance_schedule(
        starting_annual_maintenance=current_vehicle[
            "annual_maintenance"
        ],
        annual_growth_rate=current_vehicle[
            "maintenance_growth_rate"
        ],
        years=analysis["years"]
    )
)

replacement_vehicle_maintenance_schedule = (
    build_maintenance_schedule(
        starting_annual_maintenance=replacement_vehicle[
            "annual_maintenance"
        ],
        annual_growth_rate=replacement_vehicle[
            "maintenance_growth_rate"
        ],
        years=analysis["years"]
    )
)

current_vehicle_total_maintenance = (
    calculate_total_maintenance(
        starting_annual_maintenance=current_vehicle[
            "annual_maintenance"
        ],
        annual_growth_rate=current_vehicle[
            "maintenance_growth_rate"
        ],
        years=analysis["years"]
    )
)

replacement_vehicle_total_maintenance = (
    calculate_total_maintenance(
        starting_annual_maintenance=replacement_vehicle[
            "annual_maintenance"
        ],
        annual_growth_rate=replacement_vehicle[
            "maintenance_growth_rate"
        ],
        years=analysis["years"]
    )
)


# ---REPAIRS---

current_vehicle_repair_schedule = (
    build_repair_schedule(
        starting_annual_repairs=current_vehicle[
            "starting_annual_repairs"
        ],
        annual_growth_rate=current_vehicle[
            "repair_growth_rate"
        ],
        years=analysis["years"]
    )
)

replacement_vehicle_repair_schedule = (
    build_repair_schedule(
        starting_annual_repairs=replacement_vehicle[
            "starting_annual_repairs"
        ],
        annual_growth_rate=replacement_vehicle[
            "repair_growth_rate"
        ],
        years=analysis["years"]
    )
)

current_vehicle_total_repairs = (
    calculate_total_repairs(
        starting_annual_repairs=current_vehicle[
            "starting_annual_repairs"
        ],
        annual_growth_rate=current_vehicle[
            "repair_growth_rate"
        ],
        years=analysis["years"]
    )
)

replacement_vehicle_total_repairs = (
    calculate_total_repairs(
        starting_annual_repairs=replacement_vehicle[
            "starting_annual_repairs"
        ],
        annual_growth_rate=replacement_vehicle[
            "repair_growth_rate"
        ],
        years=analysis["years"]
    )
)


# ---FINANCIAL CALCULATIONS---

keep = calculate_keep_cost(
    current_value=current_vehicle["current_value"],
    future_value=current_vehicle_future_value,
    total_maintenance=current_vehicle_total_maintenance,
    total_repairs=current_vehicle_total_repairs,
    years=analysis["years"]
)

replace = calculate_replace_cost(
    purchase_price=replacement_vehicle["purchase_price"],
    future_value=replacement_vehicle_future_value,
    down_payment=replacement_vehicle["down_payment"],
    annual_interest_rate=replacement_vehicle["interest_rate"],
    loan_months=replacement_vehicle["loan_months"],
    total_maintenance=replacement_vehicle_total_maintenance,
    total_repairs=replacement_vehicle_total_repairs,
    years=analysis["years"],
    taxes_and_fees=replacement_vehicle["taxes_and_fees"]
)


# ---LOAN AMORTIZATION---

loan_principal = (
    replacement_vehicle["purchase_price"]
    - replacement_vehicle["down_payment"]
)

amortization = calculate_amortization_schedule(
    principal=loan_principal,
    annual_interest_rate=replacement_vehicle[
        "interest_rate"
    ],
    months=replacement_vehicle["loan_months"]
)


# ---MONTE CARLO REPAIR SIMULATION---

current_vehicle_repair_simulations = (
    run_repair_simulation(
        repair_schedule=current_vehicle_repair_schedule,
        variability=current_vehicle[
            "repair_variability"
        ],
        simulations=analysis["simulations"]
    )
)

replacement_vehicle_repair_simulations = (
    run_repair_simulation(
        repair_schedule=replacement_vehicle_repair_schedule,
        variability=replacement_vehicle[
            "repair_variability"
        ],
        simulations=analysis["simulations"]
    )
)


# ---DECISION SIMULATION---

decision_results = run_decision_simulation(
    current_vehicle_repair_simulations=(
        current_vehicle_repair_simulations
    ),
    replacement_vehicle_repair_simulations=(
        replacement_vehicle_repair_simulations
    ),
    current_vehicle_depreciation=keep["depreciation"],
    replacement_vehicle_depreciation=replace["depreciation"],
    current_vehicle_maintenance=keep["maintenance"],
    replacement_vehicle_maintenance=replace["maintenance"],
    replacement_vehicle_interest=replace["loan_interest"],
    replacement_vehicle_taxes_and_fees=replace[
        "taxes_and_fees"
    ]
)


# ---SIMULATION METRICS---

keep_probability = (
    decision_results["keep_probability"] * 100
)

replace_probability = (
    decision_results["replace_probability"] * 100
)

tie_probability = (
    decision_results["tie_probability"] * 100
)

average_keep_cost = (
    decision_results["keep_costs"].mean()
)

average_replace_cost = (
    decision_results["replace_costs"].mean()
)

median_keep_cost = np.median(
    decision_results["keep_costs"]
)

median_replace_cost = np.median(
    decision_results["replace_costs"]
)

keep_90th_percentile = np.percentile(
    decision_results["keep_costs"],
    90
)

replace_90th_percentile = np.percentile(
    decision_results["replace_costs"],
    90
)


# ---RESULTS---

difference = (
    replace["total_cost"]
    - keep["total_cost"]
)

print("\nASSET DECISION ENGINE")

print("\nKEEP CURRENT VEHICLE")
print(
    f"Depreciation:       "
    f"${keep['depreciation']:,.2f}"
)
print(
    f"Maintenance:        "
    f"${keep['maintenance']:,.2f}"
)
print(
    f"Repairs:            "
    f"${keep['repairs']:,.2f}"
)
print(
    f"Total Cost:         "
    f"${keep['total_cost']:,.2f}"
)

print("\nREPLACE VEHICLE")
print(
    f"Depreciation:       "
    f"${replace['depreciation']:,.2f}"
)
print(
    f"Maintenance:        "
    f"${replace['maintenance']:,.2f}"
)
print(
    f"Repairs:            "
    f"${replace['repairs']:,.2f}"
)
print(
    f"Loan Principal:     "
    f"${replace['loan_principal']:,.2f}"
)
print(
    f"Monthly Payment:    "
    f"${replace['monthly_payment']:,.2f}"
)
print(
    f"Loan Interest:      "
    f"${replace['loan_interest']:,.2f}"
)
print(
    f"Taxes and Fees:     "
    f"${replace['taxes_and_fees']:,.2f}"
)
print(
    f"Total Cost:         "
    f"${replace['total_cost']:,.2f}"
)

print("\nDETERMINISTIC DECISION")

if keep["total_cost"] < replace["total_cost"]:
    print("Recommendation: KEEP")
    print(
        f"Estimated Savings: "
        f"${difference:,.2f}"
    )
else:
    print("Recommendation: REPLACE")
    print(
        f"Estimated Savings: "
        f"${abs(difference):,.2f}"
    )

print("\nMONTE CARLO DECISION RESULTS")
print(
    f"KEEP wins:    "
    f"{keep_probability:.2f}%"
)
print(
    f"REPLACE wins: "
    f"{replace_probability:.2f}%"
)
print(
    f"Ties:         "
    f"{tie_probability:.2f}%"
)

print("\nSIMULATED TOTAL COSTS")

print("\nKEEP")
print(
    f"Average Cost:        "
    f"${average_keep_cost:,.2f}"
)
print(
    f"Median Cost:         "
    f"${median_keep_cost:,.2f}"
)
print(
    f"90th Percentile:     "
    f"${keep_90th_percentile:,.2f}"
)

print("\nREPLACE")
print(
    f"Average Cost:        "
    f"${average_replace_cost:,.2f}"
)
print(
    f"Median Cost:         "
    f"${median_replace_cost:,.2f}"
)
print(
    f"90th Percentile:     "
    f"${replace_90th_percentile:,.2f}"
)