import pandas as pd
import requests

# World Bank API for GDP Deflator (% change) or CPI
# GDP Deflator indicator: NY.GDP.DEFL.ZS
# CPI indicator: FP.CPI.TOTL

indicator = "NY.GDP.DEFL.ZS"  # Change to FP.CPI.TOTL for CPI
country = "USA"  # Change to your country code or "WLD" for world
start_year = 1957
end_year = 2022

# Fetch data from World Bank API
url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json&per_page=1000"
response = requests.get(url)
data = response.json()[1]  # Data is in second element

# Convert to DataFrame
df = pd.DataFrame(data)
df = df[['date', 'value']].dropna()
df.rename(columns={'date': 'Year', 'value': 'Index'}, inplace=True)
df['Year'] = df['Year'].astype(int)

# Sort by Year ascending
df.sort_values('Year', inplace=True)

# Compute Inflation Factor (Base Year = 2022)
base_year_index = df.loc[df['Year'] == end_year, 'Index'].values[0]
df['Inflation_Factor'] = base_year_index / df['Index']

# Save as CSV for Power BI
df.to_csv('inflation_factors.csv', index=False)

print(df.head(10))
print("CSV file 'inflation_factors.csv' created successfully!")
