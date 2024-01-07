import pandas as pd
import plotly.express as px

# Read data from URL
url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = pd.read_csv(url)

# Data Exploration and Cleaning
print(df.head(5))
print(df.isnull().sum())
print(df.describe())

# 1. Global CO2 Emissions Over Time
df_by_year = df.groupby("year").sum().reset_index()
fig1 = px.line(
    df_by_year, x="year", y="co2", title="Global CO2 Emissions Over Time in Tonnes"
)
fig1.show()

# 2. CO2 Emissions by Country in 2017 choropleth map
df_2017 = df.loc[df["year"] == 2017].dropna(subset=["co2"])
fig2 = px.choropleth(
    df_2017,
    locations="iso_code",
    color="co2",
    hover_name="country",
    color_continuous_scale=px.colors.diverging.RdYlBu_r,
    range_color=[df_2017["co2"].min(), df_2017["co2"].max()],
)
fig2.update_layout(title="CO2 Emissions by Country in 2017")
fig2.show()

# 4. CO2 Emissions by Sector Over Time (Stacked Bar Chart)
df_by_year = (
    df.groupby("year")
    .sum()
    .reset_index()
    .dropna(
        subset=[
            "coal_co2",
            "oil_co2",
            "gas_co2",
            "flaring_co2",
            "cement_co2",
            "land_use_change_co2",
            "other_industry_co2",
        ]
    )
)
fig4 = px.bar(
    df_by_year,
    x="year",
    y=[
        "coal_co2",
        "oil_co2",
        "gas_co2",
        "flaring_co2",
        "cement_co2",
        "land_use_change_co2",
        "other_industry_co2",
    ],
    title="CO2 Emissions by Sector Over Time",
)
fig4.update_layout(barmode="stack")
fig4.show()

# Bubble Chart: CO2 Emissions vs GDP per Capita
fig_alternative = px.scatter(
    df_2017,
    x="co2_per_gdp",
    y="co2",
    size="co2", 
    hover_name="country",
    color="iso_code",
    log_x=True,  
    size_max=50,  
    trendline="ols",
)

fig_alternative.update_layout(title="CO2 Emissions vs GDP per Capita (Bubble Chart)")
fig_alternative.show()

# 6. Trade CO2 of Top 10 Regions and Countries in 2017 (Violin Plot)
df_2017 = df.loc[df["year"] == 2017].dropna(subset=["trade_co2"])
df_2017 = df_2017.sort_values(by=["trade_co2"], ascending=False).head(10)
fig6 = px.violin(
    df_2017,
    y="trade_co2",
    x="country",
    hover_name="country",
    color="country",
    box=True,
    points="all",
)
fig6.update_layout(title="Trade CO2 of Top 10 Regions and Countries in 2017")
fig6.show()
