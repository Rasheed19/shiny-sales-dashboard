import pandas as pd
from dataclasses import dataclass


@dataclass
class SideBarFilter:

    cities: list[str]
    customer_types: list[str]
    gender: list[str]


@dataclass
class KPIsBarChartData:
    df_filtered: pd.DataFrame
    sales_by_product_line: pd.DataFrame
    sales_by_hour: pd.DataFrame


def cleaned_data() -> pd.DataFrame:

    df = pd.read_excel(
        io="./data/supermarket_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour

    return df


def get_sidebar_filter() -> SideBarFilter:

    df = cleaned_data()
    cities = df["City"].unique().tolist()
    customer_types = df["Customer_type"].unique().tolist()
    gender = df["Gender"].unique().tolist()

    return SideBarFilter(cities=cities, customer_types=customer_types, gender=gender)


def get_filtered_data(
    cities: list[str], customers: list[str], genders: list[str]
) -> KPIsBarChartData:

    df = cleaned_data()

    if cities:
        df = df[df["City"].isin(cities)]

    if customers:
        df = df[df["Customer_type"].isin(customers)]

    if genders:
        df = df[df["Gender"].isin(genders)]

    sales_by_product_line = (
        df[["Product line", "Total"]]
        .groupby(by="Product line")
        .sum()
        .sort_values(by="Total", ascending=False)
        .reset_index()
    )

    sales_by_hour = (
        df[["Hour", "Total"]]
        .groupby(by="Hour")
        .sum()
        .sort_values(by="Total", ascending=False)
        .reset_index()
    )
    sales_by_hour["Hour"] = sales_by_hour["Hour"].astype(str)

    return KPIsBarChartData(
        df_filtered=df,
        sales_by_product_line=sales_by_product_line,
        sales_by_hour=sales_by_hour,
    )
