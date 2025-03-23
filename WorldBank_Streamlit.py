import requests
import pandas as pd
import streamlit as st


indicators_WolrdBank = {
"Population growth (annual %)" : "SP.POP.GROW",
"Foreign direct investment, net inflows (BoP, current US$)" : "BX.KLT.DINV.CD.WD",
"Renewable energy consumption (% of total final energy consumption)" : "EG.FEC.RNEW.ZS",
"Individuals using the Internet (% of population)" : "IT.NET.USER.ZS",
"Access to electricity (% of population)" : "EG.ELC.ACCS.ZS",
"Military expenditure (% of GDP)" : "MS.MIL.XPND.GD.ZS",
"GDP (current US$)" : "NY.GDP.MKTP.CD",
"GDP per capita (current US$)" : "NY.GDP.PCAP.CD",
"Inflation, consumer prices (annual %)" : "FP.CPI.TOTL.ZG",
"Unemployment, total (% of total labor force) (modeled ILO estimate)" : "SL.UEM.TOTL.ZS"
}

base_url = "http://api.worldbank.org/v2/country/{}/indicator/{}"

countries_list_arr = ["USA", "CRI"]

params = {
    "format": "json",
    "date": "2010:2023"
}

data_list = []

# Fetch data for each country and each indicator
for indicator_name, indicator_code in indicators_WolrdBank.items():
    for country in countries_list_arr:
        response = requests.get(base_url.format(country, indicator_code), params=params)
        
        # Check if the request is successful
        if response.status_code == 200:
            data = response.json()
            
            # Ensure data is valid and process the response
            if len(data) > 1 and data[1] is not None:
                for entry in data[1]:
                    if entry["value"] is not None:  # Ensure there's a valid value
                        data_list.append({
                            "Date": entry["date"],
                            "Country": country,
                            "Indicator": indicator_name,
                            "Indicator_code": indicator_code,
                            "Value": entry["value"]
                        })
        else:
            print(f"Failed to fetch data for {indicator_name} ({country})")

# Convert the list of data into a DataFrame
df_raw = pd.DataFrame(data_list)

st.title("World Bank Dashboard")
st.text("This is an interactive dashboard I created using streamlit. \nThe dashboard makes an API request for the data. \nThen it builds a dataframe, and then we vizualise it and filter it using streamlit.  ")

# Display the DataFrame
#print(df_raw)

selected_indicator = st.selectbox(
    "Select an indicator:",
    list(indicators_WolrdBank.keys())
)

selected_code = indicators_WolrdBank[selected_indicator]
print(selected_code)

country_list = df_raw['Country'].unique().tolist()

selected_countries = st.multiselect('Select countries to display', options=country_list, default=country_list)


filtered_df1 = df_raw[df_raw['Country'].isin(selected_countries)]


filtered_df2 = filtered_df1[filtered_df1['Indicator_code'] == selected_code]

st.write(filtered_df2)

st.line_chart(filtered_df2, x="Date", y="Value", color="Country")







