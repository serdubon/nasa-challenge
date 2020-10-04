import streamlit as st
import pydeck as pdk
from PIL import Image
import datetime
import pandas as pd
import time 
from os.path import join

cordinates = {
    "Uruguaiana": [-29.75472, -57.08833],
    "Fortaleza": [-3.71722 -38.54306],
}


def main():

    st.title("Nasa Challange")
    st.markdown("---")
    st.header("Satellite Images")

    option = st.selectbox("Select a Location", ("Uruguaiana", "Fortaleza"))
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
    
    st.image(image, width=700)
    st.markdown("---")

    st.header("Damage Report")

    data = load_data()
    data_slice = data[(data["country"] == option) & (data["date"].dt.date == date)]

    st.dataframe(data_slice)
    st.markdown("---")

    st.header("Cost calculation")
    st.info('')


@st.cache(persist=False, ttl=10)
def load_data():
    data = pd.read_csv("./data/dataset.csv",)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(
        columns={"number_damaged_structures": "number of damaged structures"},
        inplace=True,
    )
    data["date"] = pd.to_datetime(data["date"])
    return data


if __name__ == "__main__":
    main()
