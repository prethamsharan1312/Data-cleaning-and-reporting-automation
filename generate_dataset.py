"""Synthetic sales dataset generator.

Creates a CSV with >= 1000 records containing:
Order ID, Order Date, Product Name, Category, Customer Name,
Region, Sales Amount, Quantity Sold, Profit, Discount.

Run:
  python generate_dataset.py --out data/sample_sales.csv --rows 1500
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class DatasetConfig:
    rows: int = 1500
    seed: int = 42


def generate_dataset(cfg: DatasetConfig) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed)

    categories = ["Electronics", "Home", "Fashion", "Books", "Sports", "Beauty"]
    products_by_cat = {
        "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
        "Home": ["Blender", "Air Purifier", "Vacuum Cleaner", "Coffee Maker"],
        "Fashion": ["T-Shirt", "Jeans", "Sneakers", "Jacket"],
        "Books": ["Fiction Novel", "Science Text", "Business Guide", "Comics"],
        "Sports": ["Yoga Mat", "Dumbbells", "Football", "Treadmill"],
        "Beauty": ["Skincare Serum", "Sunscreen", "Hair Conditioner", "Lip Balm"],
    }

    customers = [
        "Ava Johnson",
        "Noah Smith",
        "Sophia Martinez",
        "Liam Brown",
        "Mia Davis",
        "Ethan Wilson",
        "Isabella Anderson",
        "James Taylor",
        "Charlotte Thomas",
        "Benjamin Jackson",
        "Amelia White",
        "Lucas Harris",
    ]

    regions = ["North America", "Europe", "Asia", "South America", "Africa", "Oceania"]

    start = pd.Timestamp("2022-01-01")
    end = pd.Timestamp("2024-12-31")
    order_dates = pd.to_datetime(
        rng.integers(start.value // 10**9, end.value // 10**9, size=cfg.rows), unit="s"
    )

    category = rng.choice(categories, size=cfg.rows, p=[0.18, 0.16, 0.18, 0.14, 0.18, 0.16])

    product = np.empty(cfg.rows, dtype=object)
    for i, c in enumerate(category):
        product[i] = rng.choice(products_by_cat[c])

    customer = rng.choice(customers, size=cfg.rows)
    region = rng.choice(regions, size=cfg.rows)

    quantity = rng.integers(1, 21, size=cfg.rows)

    # Base prices by category/product-ish
    base_price_by_category = {
        "Electronics": 260,
        "Home": 90,
        "Fashion": 45,
        "Books": 25,
        "Sports": 70,
        "Beauty": 35,
    }

    base = np.array([base_price_by_category[c] for c in category], dtype=float)

    # Product price variance
    price_multiplier = rng.normal(1.0, 0.18, size=cfg.rows).clip(0.6, 1.5)
    unit_price = base * price_multiplier

    # Discounts (0% to 30%) skewed towards small discounts
    discount = rng.beta(2.0, 7.0, size=cfg.rows) * 0.30

    # Sales Amount after discount
    sales_amount = quantity * unit_price * (1.0 - discount)

    # Profit: margin depends on category and discount; add noise
    margin_by_category = {
        "Electronics": 0.28,
        "Home": 0.34,
        "Fashion": 0.32,
        "Books": 0.42,
        "Sports": 0.30,
        "Beauty": 0.36,
    }
    base_margin = np.array([margin_by_category[c] for c in category], dtype=float)

    # Higher discounts tend to reduce profit margin slightly
    margin = base_margin * (1.0 - 0.9 * discount) + rng.normal(0, 0.02, size=cfg.rows)
    margin = np.clip(margin, 0.05, 0.7)

    profit = sales_amount * margin + rng.normal(0, sales_amount * 0.02, size=cfg.rows)
    profit = np.clip(profit, 0, None)

    order_id = np.arange(100000, 100000 + cfg.rows)

    df = pd.DataFrame(
        {
            "Order ID": order_id,
            "Order Date": order_dates.date.astype(str),
            "Product Name": product,
            "Category": category,
            "Customer Name": customer,
            "Region": region,
            "Sales Amount": sales_amount.round(2),
            "Quantity Sold": quantity,
            "Profit": profit.round(2),
            "Discount": (discount * 100).round(2),  # store as percentage
        }
    )

    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="data/sample_sales.csv")
    parser.add_argument("--rows", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cfg = DatasetConfig(rows=args.rows, seed=args.seed)
    df = generate_dataset(cfg)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()

