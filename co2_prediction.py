import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

# Load data
url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = pd.read_csv(url)

# Preprocess data
df = df.dropna()
X = df[["year", "population", "gdp"]]  # replace with relevant features
y = df["co2"]  # replace with the target variable
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=1000)
model.fit(X_train, y_train)

# Evaluate model
mse = mean_squared_error(y_test, model.predict(X_test))
st.write(f"Mean Squared Error: {mse}")

# Predict
year = st.slider(
    "Year", min_value=int(df["year"].min()), max_value=int(df["year"].max())
)
population = st.slider(
    "Population",
    min_value=int(df["population"].min()),
    max_value=int(df["population"].max()),
)
gdp = st.slider("GDP", min_value=int(df["gdp"].min()), max_value=int(df["gdp"].max()))
features = scaler.transform([[year, population, gdp]])
prediction = model.predict(features)
st.write(f"Predicted CO2 Emissions: {prediction[0]}")
