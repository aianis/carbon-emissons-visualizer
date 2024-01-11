import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Interactive CO2 Emissions Visualizer")
st.markdown("This web app visualizes CO2 emissions data from 1751 to date. Some data may be available only after certain years. Data source from [Our World in Data](https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions).")


st.image("./co2_image.jpg", width=700, caption = "Image by Unsplash.com @ Marek Piwnicki")


#View in full screen for better experience
st.markdown("**View Charts/Maps in full screen for better experience.**")

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = pd.read_csv(url)

# Drop rows with missing 'co2' or 'iso_code' values 
df = df.dropna(subset=["co2", "iso_code"])

# sort the dataframe by year in ascending order
df = df.sort_values(by=["year"], ascending=True)

# Get the list of unique years
years = df['year'].unique()

# Sidebar
st.sidebar.header('Choose a Year(since 1751)')
selected_year = st.sidebar.selectbox('Year', options=years)

# Filter the dataframe for the selected year
df_selected_year = df.loc[df["year"] == selected_year]

# 1. Create the choropleth map
fig1 = px.choropleth(df, locations="iso_code", color="co2", hover_name="country", animation_frame="year", color_continuous_scale="RdYlBu_r", range_color=[df["co2"].min(), df["co2"].max()])
fig1.update_layout(title=f"CO2 Emissions by Country Over Time", coloraxis_colorbar_title="CO2 Emissions (Million Metric Tonnes)")
st.plotly_chart(fig1)

# 2. Global CO2 Emissions Over Time
df_by_year = df.groupby("year").sum().reset_index()
fig2 = px.line(df_by_year, x="year", y="co2", title=f"Global CO2 Emissions Over Time (Million Metric Tonnes)")
st.plotly_chart(fig2)

# 3. CO2 Emissions by Sector Over Time (Stacked Bar Chart)
df_by_year = df_selected_year.groupby("year").sum().reset_index().dropna(subset=["coal_co2", "oil_co2", "gas_co2", "flaring_co2", "cement_co2", "land_use_change_co2", "other_industry_co2"])
fig3 = px.bar(df_by_year, x="year", y=["coal_co2", "oil_co2", "gas_co2", "flaring_co2", "cement_co2", "land_use_change_co2", "other_industry_co2"], title=f"CO2 Emissions by Sector Over Time in {selected_year}")
fig3.update_layout(barmode="stack", xaxis_title="Year", yaxis_title="CO2 Emissions (Million Metric Tonnes)")
st.plotly_chart(fig3)

# 4. Bubble Chart: CO2 Emissions vs GDP per Capita
df_selected_year = df_selected_year.dropna(subset=["co2_per_gdp"])
fig4 = px.scatter(df_selected_year, x="co2_per_gdp", y="co2", size="co2", hover_name="country", color="country", log_x=True, size_max=50, trendline="ols")
fig4.update_layout(title=f"CO2 Emissions vs GDP per Capita in {selected_year} (Million Metric Tonnes)")
st.plotly_chart(fig4)

# 5. Trade CO2 of Top 10 Regions and Countries
df_selected_year = df_selected_year.dropna(subset=["trade_co2"])
df_selected_year = df_selected_year.sort_values(by=["trade_co2"], ascending=False).head(10)
fig5 = px.violin(df_selected_year, y="trade_co2", x="country", hover_name="country", color="country", box=True, points="all")
fig5.update_layout(title=f"Trade CO2 of Top 10 Regions and Countries in {selected_year} (Million Metric Tonnes)")
st.plotly_chart(fig5)

