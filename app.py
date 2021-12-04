import streamlit as st
import pandas as pd
import numpy as np

from utils.st_constants import *
from utils.st_utils import *
from utils.st_pages import *


def main():
    side_menu_list = [
        "Анализ данных",
        "Обновление данных",
        "Команда",
        "Информация о проекте"
    ]

    side_menu_choice = st.sidebar.selectbox("", side_menu_list, key="side_menu")
    side_menu_idx = side_menu_list.index(side_menu_choice)
    st_img("./data/logo_red.jpg", sidebar=True)

    # username = st.session_state["username"]
    if side_menu_idx == 0:
        st_title("Анализ данных")
        show_data()
    elif side_menu_idx == 1:
        st_title("Обновление данных")

    elif side_menu_idx == 2:
        st_title("Команда")

    elif side_menu_idx == 3:
        st_title("Информация о проекте")
        show_info()


if __name__ == "__main__":
    main()