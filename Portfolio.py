
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "TrickerDatabase.csv.txt"
OUTPUT_FILE = BASE_DIR / "portfolio_summary.csv"


def load_stocks():
    """Load company symbols and names from the supplied dataset."""
    stocks = {}

    try:
        with open(
            DATABASE_FILE, "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                symbol = (row.get("Symbol") or "").strip().upper()
                company = (row.get("Security") or "").strip()

                if symbol and company:
                    stocks[symbol] = company

    except FileNotFoundError:
        print("Error: TrickerDatabase.csv.txt was not found.")
        print("Keep it in the same folder as portfolio.py.")
        raise SystemExit(1)

    if not stocks:
        print("No valid stock records found in the dataset.")
        raise SystemExit(1)

    return stocks


def get_number(prompt, allow_zero=False):
    while True:
        try:
            value = float(input(prompt))

            if value > 0 or (allow_zero and value == 0):
                return value

            print("Enter a valid positive number.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_quantity():
    while True:
        try:
            quantity = int(input("Number of shares: "))

            if quantity > 0:
                return quantity

            print("Quantity must be greater than zero.")

        except ValueError:
            print("Enter a whole number, such as 5 or 10.")


def main():
    stocks = load_stocks()
    portfolio = {}

    print("=" * 65)
    print("       STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 65)
    print(f"Loaded {len(stocks)} company records from your dataset.")
    print("Enter DONE as the ticker when you finish.\n")

    while True:
        ticker = input("Stock ticker: ").strip().upper()

        if ticker == "DONE":
            break

        if ticker not in stocks:
            print("Ticker not found in the supplied dataset.")
            print("Check the ticker symbol and try again.\n")
            continue

        print("Company:", stocks[ticker])

        purchase_price = get_number("Purchase price per share: ")
        quantity = get_quantity()
        current_price = get_number("Current price per share: ")

        invested = purchase_price * quantity
        market_value = current_price * quantity

        if ticker in portfolio:
            old = portfolio[ticker]
            old["quantity"] += quantity
            old["invested"] += invested
            old["market_value"] += market_value
            old["purchase_price"] = (
                old["invested"] / old["quantity"]
            )
            old["current_price"] = (
                old["market_value"] / old["quantity"]
            )
        else:
            portfolio[ticker] = {
                "ticker": ticker,
                "company": stocks[ticker],
                "quantity": quantity,
                "purchase_price": purchase_price,
                "current_price": current_price,
                "invested": invested,
                "market_value": market_value,
            }

        print("Holding added successfully.\n")

    if not portfolio:
        print("No holdings entered. Nothing to save.")
        return

    print("\n" + "=" * 110)
    print("PORTFOLIO SUMMARY")
    print("=" * 110)

    print(
        f"{'Ticker':<9}{'Company':<28}{'Qty':>6}"
        f"{'Invested':>13}{'Market Value':>15}"
        f"{'Profit/Loss':>14}{'Gain/Loss %':>13}"
    )
    print("-" * 110)

    total_invested = 0
    total_market_value = 0

    for item in portfolio.values():
        profit_loss = item["market_value"] - item["invested"]
        percentage = (
            profit_loss / item["invested"] * 100
            if item["invested"] else 0
        )

        total_invested += item["invested"]
        total_market_value += item["market_value"]

        print(
            f"{item['ticker']:<9}"
            f"{item['company'][:27]:<28}"
            f"{item['quantity']:>6}"
            f"{item['invested']:>13.2f}"
            f"{item['market_value']:>15.2f}"
            f"{profit_loss:>14.2f}"
            f"{percentage:>12.2f}%"
        )

        item["profit_loss"] = profit_loss
        item["percentage"] = percentage

    total_profit_loss = total_market_value - total_invested
    total_percentage = (
        total_profit_loss / total_invested * 100
        if total_invested else 0
    )

    print("-" * 110)
    print(f"Total invested capital: {total_invested:.2f}")
    print(f"Total market value:     {total_market_value:.2f}")
    print(f"Total profit/loss:      {total_profit_loss:.2f}")
    print(f"Overall gain/loss:      {total_percentage:.2f}%")

    # Save results to a CSV file
    fields = [
        "ticker", "company", "quantity", "purchase_price",
        "current_price", "invested", "market_value",
        "profit_loss", "percentage_gain_loss"
    ]

    try:
        with open(
            OUTPUT_FILE, "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for item in portfolio.values():
                writer.writerow({
                    "ticker": item["ticker"],
                    "company": item["company"],
                    "quantity": item["quantity"],
                    "purchase_price": f'{item["purchase_price"]:.2f}',
                    "current_price": f'{item["current_price"]:.2f}',
                    "invested": f'{item["invested"]:.2f}',
                    "market_value": f'{item["market_value"]:.2f}',
                    "profit_loss": f'{item["profit_loss"]:.2f}',
                    "percentage_gain_loss": (
                        f'{item["percentage"]:.2f}'
                    ),
                })

        print(f"\nSummary saved to: {OUTPUT_FILE}")

    except (OSError, csv.Error) as error:
        print("Error saving portfolio:", error)


if __name__ == "__main__":
    main()
