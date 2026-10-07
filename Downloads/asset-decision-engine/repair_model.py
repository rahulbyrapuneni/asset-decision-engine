def build_repair_schedule(
    starting_annual_repairs: float,
    annual_growth_rate: float,
    years: int
) -> list:

    schedule = []

    repair_cost = starting_annual_repairs

    for year in range(1, years + 1):

        schedule.append({
            "year": year,
            "repair_cost": repair_cost
        })

        repair_cost = repair_cost * (
            1 + annual_growth_rate
        )

    return schedule


def calculate_total_repairs(
    starting_annual_repairs: float,
    annual_growth_rate: float,
    years: int
) -> float:

    schedule = build_repair_schedule(
        starting_annual_repairs,
        annual_growth_rate,
        years
    )

    total_repairs = sum(
        row["repair_cost"]
        for row in schedule
    )

    return total_repairs