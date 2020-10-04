import streamlit as st
import pydeck as pdk
from PIL import Image
import datetime
import pandas as pd

cordinates = {
    "Costa Rica": [9.939546, -84.095995],
    "Argentina": [-32.898482, -68.820795],
}


def main():

    st.title("Nasa Challange")
    st.markdown("---")
    st.header("Satellite Images")

    option = st.selectbox("Select a Country", ("Costa Rica", "Argentina"))
    date = st.date_input("Date of the image", datetime.date.today())

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

    name_country = option.replace(" ", "_").lower()
    image = Image.open("images/{}.png".format(name_country))
    st.image(image, width=700)
    st.markdown("---")

    st.header("Damage Report")

    data = load_date()
    st.dataframe(data[data["country"] == option])


@st.cache(persist=True)
def load_date():
    data = pd.read_csv("./data/dataset.csv",)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(
        columns={"number_damaged_structures": "number of damaged structures"},
        inplace=True,
    )
    return data


if __name__ == "__main__":
    main()
