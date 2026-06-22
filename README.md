# Sales & Revenue Analysis Dashboard (Streamlit)

A professional Streamlit dashboard for sales & revenue analysis with interactive filters, KPI cards, Plotly visualizations, automated insights, and CSV export. Includes a light/dark theme toggle.

## Features

- **Interactive filters**: Date range, Category, Region, Product Name, Customer Name
- **KPI cards**: Total Revenue, Total Sales, Total Profit, Total Orders, Average Order Value
- **Charts (Plotly)**
  - Monthly revenue trend (line)
  - Sales by category (bar)
  - Top 10 products by sales (horizontal bar)
  - Revenue by region (bar)
  - Profit vs Sales (scatter)
  - Discount vs Profit (scatter)
- **Automated insights** based on the filtered dataset
- **Export**: Download filtered data as CSV
- **Theme**: Light/Dark

## Project Structure

```
sales_revenue_dashboard/
  app.py                     # Streamlit entrypoint
  requirements.txt
  generate_dataset.py       # Synthetic dataset generator
  README.md
  TODO.md

  data/
    sample_sales.csv        # Default dataset (used by the dashboard)

  src/
    data.py                  # Load/validate/clean datasets
    dashboard.py             # UI, filters, KPIs, charts, insights
```

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Setup (Local)

1) Create and activate a virtual environment:

```bash
cd /Users/sridharbm/Desktop/sales_revenue_dashboard
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

## Generate/Update the Sample Dataset

The dashboard loads `data/sample_sales.csv` by default. To regenerate it:

```bash
python generate_dataset.py --out data/sample_sales.csv --rows 1500
```

## Run Locally

```bash
streamlit run app.py
```

If port 8501 is already in use:

```bash
streamlit run app.py --server.port 8502
```

Then open the local URL shown in the terminal.

## Dashboard Behavior / Data Requirements

The dataset must contain these columns:

- `Order ID`
- `Order Date`
- `Product Name`
- `Category`
- `Customer Name`
- `Region`
- `Sales Amount`
- `Quantity Sold`
- `Profit`
- `Discount`

Uploaded datasets (CSV/XLSX) are validated against the required schema.

## Streamlit Cloud Deployment

1) Create a repository on GitHub and **push this project**.
2) Ensure `data/sample_sales.csv` is included in the repo.
3) On **Streamlit Community Cloud**:
   - Create a new app and connect your GitHub repo.
   - Set the entrypoint to: `app.py`
4) Deploy.

## Notes

- A `.streamlit/config.toml` file may be used for Cloud configuration.
- The dashboard’s visuals update instantly based on sidebar filters.


