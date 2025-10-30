def calculate_old_regime_tax(annual_income, deductions_80C=0, deductions_80D=0):
    taxable_income = max(0, annual_income - deductions_80C - deductions_80D)
    tax = 0.0

    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = (250000 * 0.05) + (taxable_income - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (taxable_income - 1000000) * 0.30

    if taxable_income <= 500000:
        tax = 0.0
    else:
        tax += tax * 0.04  # health & education cess

    return tax, taxable_income

def calculate_new_regime_tax(annual_income):
    taxable_income = annual_income
    tax = 0.0

    if taxable_income <= 400000:
        tax = 0
    elif taxable_income <= 800000:
        tax = (taxable_income - 400000) * 0.05
    elif taxable_income <= 1200000:
        tax = (400000 * 0.05) + (taxable_income - 800000) * 0.10
    elif taxable_income <= 1600000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (taxable_income - 1200000) * 0.15
    elif taxable_income <= 2000000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (taxable_income - 1600000) * 0.20
    elif taxable_income <= 2400000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (taxable_income - 2000000) * 0.25
    else:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (400000 * 0.25) + (taxable_income - 2400000) * 0.30

    if taxable_income <= 1200000:
        tax = 0.0
    else:
        tax += tax * 0.04  # cess

    return tax, taxable_income

def calculate_sip_end_value(monthly_sip, annual_return_rate_pct, duration_years):
    r = annual_return_rate_pct / 100.0
    monthly_rate = (1 + r) ** (1/12) - 1
    months = duration_years * 12
    if monthly_rate == 0:
        return monthly_sip * months
    corpus = monthly_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    return corpus

def get_monthly_expenses():
    print("Enter your monthly expenses (in ₹):")
    rent = float(input("  Rent: ") or 0)
    food = float(input("  Food: ") or 0)
    travel = float(input("  Travel: ") or 0)
    others = float(input("  Other expenses: ") or 0)
    total = rent + food + travel + others
    return total, {"Rent": rent, "Food": food, "Travel": travel, "Others": others}

def run_yearly_finance_calculation():
    print("\nIndian Personal Finance & SIP Calculator")

    year = 1
    total_sip_corpus = 0

    # Initial input
    monthly_salary = float(input("Enter your monthly gross salary in ₹: "))
    pf_percent = float(input("Enter your PF deduction percentage (e.g., 12 for 12%): ") or 0)
    deductions_80C = float(input("Enter Section 80C deduction in ₹ (max ₹1,50,000, old regime only): ") or 0)
    deductions_80C = min(deductions_80C, 150000)
    deductions_80D = float(input("Enter Section 80D deduction in ₹ (max ₹50,000, old regime only): ") or 0)
    deductions_80D = min(deductions_80D, 50000)
    monthly_sip = float(input("Enter monthly SIP amount in ₹: "))
    expected_return_pct = float(input("Enter expected annual return rate (%) for SIP: "))

    while True:
        print(f"\n--- YEAR {year} ---")

        # Allow salary hike each year
        if year > 1:
            hike_pct = float(input("Enter salary hike percentage for this year: ") or 0)
            monthly_salary *= (1 + hike_pct / 100)

        monthly_expenses, breakdown = get_monthly_expenses()

        annual_salary = monthly_salary * 12
        annual_expenses = monthly_expenses * 12
        pf_contribution = annual_salary * pf_percent / 100
        annual_savings_before_tax = annual_salary - annual_expenses - pf_contribution

        old_tax, old_taxable_income = calculate_old_regime_tax(annual_salary, deductions_80C, deductions_80D)
        new_tax, new_taxable_income = calculate_new_regime_tax(annual_salary)

        inhand_old_annual = annual_salary - old_tax - pf_contribution - annual_expenses
        inhand_new_annual = annual_salary - new_tax - pf_contribution - annual_expenses

        inhand_old_monthly = inhand_old_annual / 12
        inhand_new_monthly = inhand_new_annual / 12

        # SIP corpus update
        total_sip_corpus = calculate_sip_end_value(monthly_sip, expected_return_pct, year)

        print("\nAnnual Summary:")
        print(f"Gross Annual Salary: ₹{annual_salary:,.2f}")
        print(f"Annual Expenses: ₹{annual_expenses:,.2f} (Breakdown: {breakdown})")
        print(f"PF Contribution: ₹{pf_contribution:,.2f}")
        print(f"Annual Savings (before tax): ₹{annual_savings_before_tax:,.2f}")

        print("\nOld Regime:")
        print(f"  Taxable Income: ₹{old_taxable_income:,.2f}")
        print(f"  Tax Payable: ₹{old_tax:,.2f}")
        print(f"  In-Hand Annual: ₹{inhand_old_annual:,.2f}")
        print(f"  In-Hand Monthly: ₹{inhand_old_monthly:,.2f}")

        print("\nNew Regime:")
        print(f"  Taxable Income: ₹{new_taxable_income:,.2f}")
        print(f"  Tax Payable: ₹{new_tax:,.2f}")
        print(f"  In-Hand Annual: ₹{inhand_new_annual:,.2f}")
        print(f"  In-Hand Monthly: ₹{inhand_new_monthly:,.2f}")

        print("\nSIP Investment Summary:")
        total_invested = monthly_sip * 12 * year
        print(f"  Year: {year}")
        print(f"  Total Invested: ₹{total_invested:,.2f}")
        print(f"  Expected Corpus: ₹{total_sip_corpus:,.2f}")

        if inhand_new_annual > inhand_old_annual:
            print("\nRecommendation: New Regime gives more in-hand income this year.")
        elif inhand_old_annual > inhand_new_annual:
            print("\nRecommendation: Old Regime gives more in-hand income this year.")
        else:
            print("\nBoth regimes give similar in-hand income this year.")

        cont = input("\nDo you want to calculate for next year? (y/n): ").lower()
        if cont != 'y':
            print("\nThank you for using the Yearly Finance & SIP Calculator!")
            break
        year += 1

if __name__ == "__main__":
    run_yearly_finance_calculation()
