def estimate_future_value(
    current_value: float,
    annual_depreciation_rate: float,
    years: int
) -> float:

    future_value = current_value * (
        (1 - annual_depreciation_rate) ** years
    )

    return future_value

def estimate_future_value(
    current_value: float,
    annual_depreciation_rate: float,
    years: int
) -> float:

    future_value = current_value * (
        (1 - annual_depreciation_rate) ** years
    )

    return future_value


def build_depreciation_schedule(
    current_value: float,
    annual_depreciation_rate: float,
    years: int
) -> list:

    schedule = []

    value = current_value

    schedule.append({
        "year": 0,
        "value": value
    })

    for year in range(1, years + 1):

        depreciation_amount = (
            value * annual_depreciation_rate
        )

        value = value - depreciation_amount

        schedule.append({
            "year": year,
            "depreciation_amount": depreciation_amount,
            "value": value
        })

    return schedule