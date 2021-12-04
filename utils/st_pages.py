import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from utils.st_map import st_map
from utils.st_utils import st_html, st_img, create_qrcode, calculate_distance


def show_data():

    with st.sidebar.form("Настройки отображения:"):
        st.info("TODO")
        st.form_submit_button("Применить")

    st.title("Iframe example")
    show_iframe("https://datalens.yandex/1q1jjz2fbxvsu?")

    st.title("Map example")
    st_map(cities=None, lat_key="latitude", lon_key="longitude", info_key="title")
    st_html("map.html", width=800)

    st.title("Dataframe example")
    df_path = st.selectbox("Select file", os.listdir("data"))
    df_path = os.path.join("data", df_path)
    st.text(df_path)
    df = load_df(df_path)
    st.dataframe(df, width=800)


def show_iframe(url, width=800, height=600, scrolling=False):
    components.iframe(url, width=width, height=height, scrolling=scrolling)


def show_info():
    st.subheader("UNDISCOVERED")
    st.balloons()
    col1, col2 = st.columns([3, 2])
    with col1:
        st.info("resivalex@gmail.com")
        st.info("@ABTOHOMHOCTb")
        st.info("maria.s.startseva@gmail.com")
    with col2:
        # st_img("./data/tg.png")
        st.markdown(f""":package: [Иван Решетников](https://t.me/resivalex)""",
                    unsafe_allow_html=True)
        st.markdown(f""":package: [Михаил Корин](https://t.me/ABTOHOMHOCTb)""",
                    unsafe_allow_html=True)
        st.markdown(f""":package: [Мария Старцева](https://t.me/cybermary)""",
                    unsafe_allow_html=True)


@st.experimental_memo
def load_df(df_path):
    df = pd.read_csv(df_path, index_col=0)
    return df
