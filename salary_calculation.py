def calculate_old_regime_tax(income, deductions_80C=0, deductions_80D=0):
    """Calculate income tax under the old regime with deductions."""
    taxable_income = max(0, income - deductions_80C - deductions_80D)

    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = (250000 * 0.05) + (taxable_income - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (taxable_income - 1000000) * 0.30

    # Rebate under Section 87A (for taxable income ≤ ₹5 lakh)
    if taxable_income <= 500000:
        tax = 0
    else:
        tax += tax * 0.04  # 4% Cess

    return tax, taxable_income


def calculate_new_regime_tax(income):
    """Calculate income tax under the new regime (FY 2024–25)."""
    taxable_income = income
    tax = 0

    if taxable_income <= 300000:
        tax = 0
    elif taxable_income <= 600000:
        tax = (taxable_income - 300000) * 0.05
    elif taxable_income <= 900000:
        tax = (300000 * 0.05) + (taxable_income - 600000) * 0.10
    elif taxable_income <= 1200000:
        tax = (300000 * 0.05) + (300000 * 0.10) + (taxable_income - 900000) * 0.15
    elif taxable_income <= 1500000:
        tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (taxable_income - 1200000) * 0.20
    else:
        tax = ((300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) +
               (300000 * 0.20) + (taxable_income - 1500000) * 0.30)

    # Rebate up to ₹7,00,000 (Section 87A)
    if taxable_income <= 700000:
        tax = 0
    else:
        tax += tax * 0.04  # 4% Cess

    return tax, taxable_income


def calculate_pf(salary, pf_percent):
    """Calculate Provident Fund deduction."""
    return (salary * pf_percent) / 100 if pf_percent > 0 else 0


def collect_expenses():
    """Collect annual living expenses from the user."""
    print("\n💸 Let's estimate your yearly living expenses.")
    print("👉 Enter values in ₹ per year (press Enter to skip any item).")

    rent = float(input("🏠 Annual House Rent: ") or 0)
    food = float(input("🍱 Food & Groceries: ") or 0)
    travel = float(input("🚗 Travel or Commute: ") or 0)
    maintenance = float(input("🧾 Maintenance & Utilities: ") or 0)
    medical = float(input("💊 Medical & Medicines: ") or 0)
    entertainment = float(input("🎬 Entertainment & Leisure: ") or 0)
    insurance = float(input("🛡️  Insurance Premiums (non-tax-saving): ") or 0)
    emi = float(input("🏦 Loan EMI Payments (annual total): ") or 0)
    other = float(input("📦 Other Miscellaneous Expenses: ") or 0)

    total_expenses = sum([rent, food, travel, maintenance, medical, entertainment, insurance, emi, other])
    print(f"\n✅ Total Estimated Annual Expenses: ₹{total_expenses:,.2f}")
    print("-" * 60)
    return total_expenses


def collect_deductions():
    """Collect possible tax-saving deductions under 80C/80D."""
    print("\n📘 Let's capture your tax-saving investments.")
    print("💡 Tip: Investing in ELSS, PPF, NPS, or LIC policies can help reduce taxable income.")

    deductions_80C = float(input("💰 Section 80C (EPF, PPF, ELSS, LIC, etc., max ₹1.5L): ") or 0)
    deductions_80C = min(deductions_80C, 150000)
    deductions_80D = float(input("💉 Section 80D (Medical Insurance Premiums, max ₹25K or ₹50K for senior): ") or 0)
    deductions_80D = min(deductions_80D, 50000)

    total_deductions = deductions_80C + deductions_80D
    print(f"\n✅ Total Deductions Claimed: ₹{total_deductions:,.2f}")
    print("-" * 60)
    return deductions_80C, deductions_80D


def main():
    try:
        print("\n💰 Welcome to the **Comprehensive Indian Personal Finance Calculator** (FY 2024–25)")
        print("👋 Let's figure out your tax, expenses, and actual in-hand income for better planning.")
        print("-" * 70)

        salary = float(input("💼 Enter your *Annual Gross Salary* (in ₹): "))
        if salary <= 0:
            print("⚠️ Salary must be a positive number. Please restart the calculator.")
            return

        pf_percent = float(input("🏦 Enter your PF deduction percentage (e.g., 12 for 12%): ") or 0)
        pf_deduction = calculate_pf(salary, pf_percent)
        print(f"✅ Your annual PF contribution will be ₹{pf_deduction:,.2f}.")
        print("-" * 60)

        # Collect tax-saving investments
        deductions_80C, deductions_80D = collect_deductions()

        # Calculate taxes under both regimes
        old_tax, old_taxable = calculate_old_regime_tax(salary, deductions_80C, deductions_80D)
        new_tax, new_taxable = calculate_new_regime_tax(salary)

        # Collect expenses
        expenses = collect_expenses()

        savings_goal = float(input("\n💵 How much do you plan to save annually? (in ₹): ") or 0)
        print(f"✅ Noted. You're aiming to save ₹{savings_goal:,.2f} this year.")
        print("-" * 60)

        # Compute net in-hand
        in_hand_old = salary - old_tax - pf_deduction - expenses - savings_goal
        in_hand_new = salary - new_tax - pf_deduction - expenses - savings_goal

        # Monthly breakdown
        monthly_old = in_hand_old / 12
        monthly_new = in_hand_new / 12

        # Summary output
        print("\n📊 Your Personal Finance Summary:")
        print("=" * 60)
        print(f"Gross Annual Salary:             ₹{salary:,.2f}")
        print(f"Provident Fund ({pf_percent}%):        ₹{pf_deduction:,.2f}")
        print(f"80C Deductions:                  ₹{deductions_80C:,.2f}")
        print(f"80D Deductions:                  ₹{deductions_80D:,.2f}")
        print(f"Total Annual Expenses:           ₹{expenses:,.2f}")
        print(f"Planned Annual Savings:          ₹{savings_goal:,.2f}")
        print("-" * 60)
        print(f"Old Regime Taxable Income:       ₹{old_taxable:,.2f}")
        print(f"New Regime Taxable Income:       ₹{new_taxable:,.2f}")
        print(f"Tax Payable (Old Regime):        ₹{old_tax:,.2f}")
        print(f"Tax Payable (New Regime):        ₹{new_tax:,.2f}")
        print("-" * 60)
        print(f"Final Annual In-Hand (Old):      ₹{in_hand_old:,.2f}")
        print(f"Final Annual In-Hand (New):      ₹{in_hand_new:,.2f}")
        print(f"Monthly Take-Home (Old):         ₹{monthly_old:,.2f}")
        print(f"Monthly Take-Home (New):         ₹{monthly_new:,.2f}")
        print("=" * 60)

        # Insights
        if in_hand_new > in_hand_old:
            print("✅ You’ll have more in-hand under the **New Tax Regime**.")
        elif in_hand_old > in_hand_new:
            print("✅ You’ll have more in-hand under the **Old Tax Regime**.")
        else:
            print("🤝 Both regimes provide the same in-hand income.")

        # Validation check
        total_outflow = pf_deduction + expenses + savings_goal
        if total_outflow > salary:
            print("\n⚠️ Warning: Your planned expenses and savings exceed your annual income!")
            print("   💡 Consider lowering your savings goal or cutting down on expenses.")

        print("\n💡 Tip: Regularly review your budget every 3 months to stay on track with savings goals.")
        print("🧮 Thank you for using the Indian Personal Finance Calculator! 🇮🇳")

    except ValueError:
        print("\n❌ Invalid input detected. Please enter numbers only.")


if __name__ == "__main__":
    main()
