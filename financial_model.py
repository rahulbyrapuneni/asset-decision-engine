def calculate_depreciation(
    current_value: float,
    future_value: float
) -> float:
    return current_value - future_value


def calculate_keep_cost(
    current_value: float,
    future_value: float,
    total_maintenance: float,
    total_repairs: float,
    years: int
) -> dict:

    depreciation = calculate_depreciation(
        current_value,
        future_value
    )

    maintenance = total_maintenance

    total_cost = (
        depreciation
        + maintenance
        + total_repairs
    )

    return {
        "depreciation": depreciation,
        "maintenance": maintenance,
        "repairs": total_repairs,
        "total_cost": total_cost
    }


def calculate_loan_payment(
    principal: float,
    annual_interest_rate: float,
    months: int
) -> float:

    monthly_rate = annual_interest_rate / 12

    if monthly_rate == 0:
        return principal / months

    payment = principal * (
        monthly_rate * (1 + monthly_rate) ** months
    ) / (
        (1 + monthly_rate) ** months - 1
    )

    return payment


def calculate_replace_cost(
    purchase_price: float,
    future_value: float,
    down_payment: float,
    annual_interest_rate: float,
    loan_months: int,
    total_maintenance: float,
    total_repairs: float,
    years: int,
    taxes_and_fees: float = 0
) -> dict:

    depreciation = calculate_depreciation(
        purchase_price,
        future_value
    )

    loan_principal = purchase_price - down_payment

    monthly_payment = calculate_loan_payment(
        loan_principal,
        annual_interest_rate,
        loan_months
    )

    total_loan_payments = monthly_payment * loan_months

    loan_interest = total_loan_payments - loan_principal

    maintenance = total_maintenance

    total_cost = (
        depreciation
        + loan_interest
        + maintenance
        + taxes_and_fees
        + total_repairs
    )

    return {
        "depreciation": depreciation,
        "maintenance": maintenance,
        "loan_principal": loan_principal,
        "monthly_payment": monthly_payment,
        "loan_interest": loan_interest,
        "taxes_and_fees": taxes_and_fees,
        "repairs": total_repairs,
        "total_cost": total_cost
    }

def calculate_amortization_schedule(
    principal: float,
    annual_interest_rate: float,
    months: int
) -> list:

    monthly_payment = calculate_loan_payment(
        principal,
        annual_interest_rate,
        months
    )

    monthly_rate = annual_interest_rate / 12

    balance = principal
    schedule = []

    for month in range(1, months + 1):

        interest_payment = balance * monthly_rate

        principal_payment = (
            monthly_payment - interest_payment
        )

        balance = balance - principal_payment

        if balance < 0:
            balance = 0

        schedule.append({
            "month": month,
            "payment": monthly_payment,
            "principal_payment": principal_payment,
            "interest_payment": interest_payment,
            "remaining_balance": balance
        })

    return schedule