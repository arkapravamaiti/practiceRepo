def calculate_old_regime_tax(annual_income, deductions_80C=0, deductions_80D=0):
    """Calculate income tax under the old regime (FY 2025-26 assumptions) with deductions."""
    taxable_income = max(0, annual_income - deductions_80C - deductions_80D)
    tax = 0.0

    # Old regime slabs (unchanged for FY 2025-26)  
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = (250000 * 0.05) + (taxable_income - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (taxable_income - 1000000) * 0.30

    # Rebate under Section 87A: if taxable income ≤ ₹5 lakh then tax = 0  
    if taxable_income <= 500000:
        tax = 0.0
    else:
        tax += tax * 0.04  # add 4% health & education cess

    return tax, taxable_income

def calculate_new_regime_tax(annual_income):
    """Calculate income tax under the new regime (FY 2025-26) without most deductions."""
    taxable_income = annual_income
    tax = 0.0

    # New regime slabs from FY 2025-26  
    # 0-4 lakh: 0%  
    # 4-8 lakh: 5%  
    # 8-12 lakh: 10%  
    # 12-16 lakh: 15%  
    # 16-20 lakh: 20%  
    # 20-24 lakh: 25%  
    # Above 24 lakh: 30%  
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

    # Rebate under Section 87A: if taxable income ≤ ₹12 lakh then tax = 0  
    if taxable_income <= 1200000:
        tax = 0.0
    else:
        tax += tax * 0.04  # add 4% cess

    return tax, taxable_income

def calculate_sip_end_value(monthly_sip, annual_return_rate_pct, duration_years=1):
    """
    Calculates the corpus at end of `duration_years` years with monthly SIP `monthly_sip`
    and annual return rate `annual_return_rate_pct` (compounded monthly).
    """
    r = annual_return_rate_pct / 100.0
    # monthly rate approximate
    monthly_rate = (1 + r)**(1/12) - 1
    months = duration_years * 12
    if monthly_rate == 0:
        return monthly_sip * months
    corpus = monthly_sip * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
    return corpus

def main():
    try:
        print("\nWelcome to the Comprehensive Indian Personal Finance Calculator (FY 2025-26)")
        print("Option: Monthly inputs → annualised results.")
        print("——————————————————————————————————")

        monthly_salary = float(input("Enter your monthly gross salary in ₹: "))
        if monthly_salary <= 0:
            print("Salary must be a positive number.")
            return

        monthly_expenses = float(input("Enter your total monthly expenses (living + other) in ₹: "))
        if monthly_expenses < 0:
            print("Expenses cannot be negative.")
            return

        # Annualise salary & expenses
        annual_salary = monthly_salary * 12
        annual_expenses = monthly_expenses * 12
        monthly_savings = monthly_salary - monthly_expenses
        annual_savings_before_tax = monthly_savings * 12

        print("\nNow – pension/EPF contribution (if any) and tax-saving deductions (for old regime).")
        pf_percent = float(input("Enter your PF deduction percentage (e.g., 12 for 12%): ") or 0)
        pf_contribution = (annual_salary * pf_percent) / 100.0
        if pf_contribution < 0:
            pf_contribution = 0

        print("\nEnter your tax-saving deductions (only applicable under the old regime):")
        deductions_80C = float(input("Section 80C amount in ₹ (max ₹1,50,000): ") or 0)
        if deductions_80C > 150000:
            deductions_80C = 150000
        deductions_80D = float(input("Section 80D amount in ₹ (max ₹50,000): ") or 0)
        if deductions_80D > 50000:
            deductions_80D = 50000

        # Tax calculations
        old_tax, old_taxable_income = calculate_old_regime_tax(annual_salary, deductions_80C, deductions_80D)
        new_tax, new_taxable_income = calculate_new_regime_tax(annual_salary)

        # Compute in-hand amounts (annual & monthly) for both regimes
        inhand_old_annual = annual_salary - old_tax - pf_contribution - annual_expenses
        inhand_new_annual = annual_salary - new_tax - pf_contribution - annual_expenses
        inhand_old_monthly = inhand_old_annual / 12.0
        inhand_new_monthly = inhand_new_annual / 12.0

        # SIP inputs
        print("\nSIP Investment Calculator:")
        monthly_sip = float(input("Enter monthly SIP amount in ₹: "))
        expected_return_pct = float(input("Enter expected annual return rate (in %): "))
        duration_years = int(input("Enter duration in years: "))

        sip_end_value = calculate_sip_end_value(monthly_sip, expected_return_pct, duration_years)
        total_sip_invested = monthly_sip * 12 * duration_years

        # Output summary
        print("\n==========================================================")
        print("Annual Summary:")
        print(f"Gross Annual Salary:                     ₹{annual_salary:,.2f}")
        print(f"Annual Expenses:                         ₹{annual_expenses:,.2f}")
        print(f"Annual Savings (before tax):             ₹{annual_savings_before_tax:,.2f}")
        print(f"PF Contribution (annual @ {pf_percent}%): ₹{pf_contribution:,.2f}")
        print("——————————————————————————————————")
        print("Old Regime:")
        print(f"  Taxable Income:                        ₹{old_taxable_income:,.2f}")
        print(f"  Tax Payable:                           ₹{old_tax:,.2f}")
        print(f"  In-Hand Annual:                        ₹{inhand_old_annual:,.2f}")
        print(f"  In-Hand Monthly:                       ₹{inhand_old_monthly:,.2f}")
        print("——————————————————————————————————")
        print("New Regime:")
        print(f"  Taxable Income:                        ₹{new_taxable_income:,.2f}")
        print(f"  Tax Payable:                           ₹{new_tax:,.2f}")
        print(f"  In-Hand Annual:                        ₹{inhand_new_annual:,.2f}")
        print(f"  In-Hand Monthly:                       ₹{inhand_new_monthly:,.2f}")
        print("==========================================================")

        # SIP summary
        print("\nSIP Investment Summary:")
        print(f"  Total Invested over {duration_years} year(s): ₹{total_sip_invested:,.2f}")
        print(f"  Expected Corpus at end of {duration_years} year(s): ₹{sip_end_value:,.2f}")

        # Recommendation
        if inhand_new_annual > inhand_old_annual:
            print("\nRecommendation: Under the given inputs, you will have **more in-hand income under the New Regime**.")
        elif inhand_old_annual > inhand_new_annual:
            print("\nRecommendation: Under the given inputs, you will have **more in-hand income under the Old Regime**.")
        else:
            print("\nBoth regimes yield similar in-hand income with current inputs.")

    except ValueError:
        print("\nInvalid input detected. Please enter numeric values only.")

if __name__ == "__main__":
    main()
