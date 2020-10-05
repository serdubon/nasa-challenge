import streamlit as st
import pydeck as pdk
from PIL import Image
import datetime
import pandas as pd
import time 
import numpy as np
from os.path import join
# import matplotlib as plt

cordinates = {
    "Uruguaiana": [-29.75472, -57.08833],
    "Fortaleza": [-3.71722 -38.54306],
}

population = {
    "Uruguaiana": 116276,
}

def main():
    calculate_cost = True
    st.title("NASA Spaceapps Challenge - Zonda Incorporated")
    st.markdown("---")
    st.header("Flood indfaestructure damage estimation - via Sentinel-Hub ")
    st.markdown("*Sentinel - 1 Mission - European Space Agency*")

    option = st.selectbox("Select a Location", ("Uruguaiana", ))
    date = st.date_input("Date of the image", datetime.date.fromisoformat("2019-01-07"))

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": cordinates[option][0],
                "longitude": cordinates[option][1],
                "zoom": 11,
                "pitch": 20,
            },
        )
    )
    with st.spinner('Processing Sentinel-1 Data'):
        time.sleep(3)
    st.success('Processing complete!')
    name_country = option.replace(" ", "_").lower()
    try:
        image = Image.open("images/{}-{}.jpg".format(name_country, date))
    except Exception:
        image = Image.open(join('images', 'no_data.jpeg'))
        calculate_cost = False
    st.image(image, width=700)
    st.markdown("---")

    st.header("Damage Report")

    data, parameters = load_data()
    data_slice = data[(data["country"] == option) & (data["date"].dt.date == date)]

    st.dataframe(data_slice)
    if calculate_cost:
        st.markdown("---")
        st.header("Cost calculation")
        st.latex('\sum_{0}^{n} unit cost \cdot (floodlevel \cdot damagescale)')
        total_cost = 0
        units = 0
        for struct in data_slice['structure'].unique():
            quantity = data_slice[data_slice["structure"] == struct]["damage"].values[0]
            ratio = parameters[parameters["name"] == struct]["ratio"].values[0]
            damage = ratio * (date.day - 7)
            if damage > 1:
                damage = 1
            unit_cost = parameters[parameters["name"] == struct]["cost"].values[0]
            total_cost += damage * quantity * unit_cost
            units += quantity
        st.markdown(f"* Total cost of flood damage (C5 index) = {total_cost}")
        pop = population[option]
        d1 = round(units / pop * 100000, 2)
        st.markdown(f"* D1 (Critical Infrastructure Damage) = {d1}")
        d5 = round(((date.day - 7) * 0.5) / pop * 100000, 2)
        st.markdown(f"* D5 (Index of Service Disruption) = {d5}")




@st.cache(persist=True)
def load_data():
    data = pd.read_csv("./data/dataset.csv",)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(
        columns={"number_damaged_structures": "number of damaged structures"},
        inplace=True,
    )
    data["date"] = pd.to_datetime(data["date"])
    parameters = pd.read_csv(join('data', 'parameters.csv'))
    return data, parameters


if __name__ == "__main__":
    main()
