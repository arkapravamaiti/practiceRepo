def calculate_income_tax(salary):
    tax = 0

    # Old Regime slabs
    if salary <= 250000:
        tax = 0
    elif salary <= 500000:
        tax = (salary - 250000) * 0.05
    elif salary <= 1000000:
        tax = (250000 * 0.05) + (salary - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (salary - 1000000) * 0.30

    # Section 87A rebate
    if salary <= 500000:
        tax = 0
    else:
        # Add 4% Health & Education Cess
        tax += tax * 0.04

    return tax


def calculate_pension(salary, contributed):
    # 12% EPF contribution (assumed)
    return salary * 0.12 if contributed else 0


def main():
    try:
        salary = float(input("Enter your annual salary in INR: "))
        if salary < 0:
            print("Salary cannot be negative.")
            return

        contributed = input("Do you contribute to a pension fund? (yes/no): ").strip().lower() == 'yes'

        tax = calculate_income_tax(salary)
        print(f"\nIncome Tax (Old Regime) on INR {salary:,.2f} = INR {tax:,.2f}")

        pension = calculate_pension(salary, contributed)
        if contributed:
            print(f"Estimated Pension Contribution = INR {pension:,.2f}")
            print("You may claim tax benefits under Section 80C.")
        else:
            print("No pension contribution detected.")

    except ValueError:
        print("Invalid input. Please enter a numeric value for salary.")


if __name__ == "__main__":
    main()

