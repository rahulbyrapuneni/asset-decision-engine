def build_maintenance_schedule(
    starting_annual_maintenance: float,
    annual_growth_rate: float,
    years: int
) -> list:

    schedule = []

    maintenance_cost = starting_annual_maintenance

    for year in range(1, years + 1):

        schedule.append({
            "year": year,
            "maintenance_cost": maintenance_cost
        })

        maintenance_cost = maintenance_cost * (
            1 + annual_growth_rate
        )

    return schedule


def calculate_total_maintenance(
    starting_annual_maintenance: float,
    annual_growth_rate: float,
    years: int
) -> float:

    schedule = build_maintenance_schedule(
        starting_annual_maintenance,
        annual_growth_rate,
        years
    )

    total_maintenance = sum(
        row["maintenance_cost"]
        for row in schedule
    )

    return total_maintenance