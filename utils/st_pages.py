import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

from utils.st_utils import st_html, st_iframe, load_df, st_img, st_freqs, st_imgs
from utils.st_constants import *
from utils.trigram import bigram_trigram



def show_data():
    with st.sidebar.form("Настройки отображения:"):
        st.radio("Скачать отчет", ("pdf", "html", "txt"))
        st.form_submit_button("Скачать отчет")

    st.title("ИЗ КАКИХ СТРАН ЕДУТ ТУРИСТЫ")
    st_iframe("https://datalens.yandex/1q1jjz2fbxvsu?")

    st.title("ТРЕНДЫ ПОИСКА В GOOGLE")
    with st.expander("посмотреть"):
        st.text("Жители каких стран искали в гугле Камчатку за последние 5 лет")
        st_html("./html/region.html", width=500, height=600)
        # st_html("./html/recent.html", width=1000, height=400)
        st.text("Темы, связанные с Камчаткой")
        st_html("./html/topics.html", width=500, height=400)
        st.text("Запросы, связанные с Камчаткой")
        st_html("./html/searches.html", width=500, height=400)

    st.title("ПОПУЛЯРНЫЕ ПОСТЫ В TWITTER")
    with st.expander("посмотреть"):
        st.text("Самые популярные твиты про Камчатку за последний месяц")
        st_html("./html/twitter.html", width=500, height=600, scrolling=True)


def show_nlp():
    with st.sidebar:
        choice = st.radio("Анализ отзывов", ("ключевые слова", "по странам", "по достопримечательностям"))

    with st.sidebar.form("Настройки отображения:"):
        st.radio("Скачать отчет", ("pdf", "html", "txt"))
        st.form_submit_button("Скачать отчет")

    if choice == "ключевые слова":
        st.title("КЛЮЧЕВЫЕ СЛОВА")
        st.markdown(f"### в положительных отзывах (8-10)")
        st_img("./images/good.png")
        st.markdown(f"### в негативных отзывах (менее 6)")
        st_img("./images/bad.png")

        st.title('ПО СТРАНАМ (положительные и негативные)')

        st.markdown('## Россия')
        st_imgs(["./images/country-top-words/russia-pos.png", "./images/country-top-words/russia-neg.png"])

        st.markdown('## Великобритания')
        st_imgs(["./images/country-top-words/united-kingdom-pos.png", "./images/country-top-words/united-kingdom-neg.png"])

        st.markdown('## Китай')
        st_img("./images/country-top-words/china-pos.png")

        st.markdown('## Австралия')
        st_img("./images/country-top-words/australia-pos.png")

        st.markdown('## Япония')
        st_img("./images/country-top-words/japan-pos.png")

        st.markdown('## Соединённые Штаты Америки')
        st_img("./images/country-top-words/united-states-pos.png")

        st.markdown('## Германия')
        st_img("./images/country-top-words/germany-pos.png")

        st.markdown('## Индия')
        st_img("./images/country-top-words/india-pos.png")

        st.markdown('## Швейцария')
        st_img("./images/country-top-words/switzerland-pos.png")

        st.markdown('## Италия')
        st_img("./images/country-top-words/italy-pos.png")

        st.markdown('## Израиль')
        st_img("./images/country-top-words/israel-pos.png")

        st.markdown('## Франция')
        st_img("./images/country-top-words/france-pos.png")

    elif choice == "по странам":
        st.title("ОТЗЫВЫ ПО СТРАНАМ")
        st.markdown("По данным Tripadvisor")
        data = pd.read_csv("./data/kamchatka_main2.csv")

        fig = px.scatter_geo(data, locations="iso",
                             color="review_rating",  # which column to use to set the color of markers
                             hover_name="hover",  # column added to hover information
                             size="review_rating",  # size of markers
                             projection="natural earth",
                             animation_frame="year", animation_group="review_rating",  # real-time debugging - delete this line if aomething is going wrong
                             width=1200,
                             opacity=.5)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Средняя оценка и количество отзывов")
            st.dataframe(data.groupby("user_country")["review_rating", "num_review"].mean())
        with col2:
            st.markdown("### Количество отзывов с данной оценкой")
            st.dataframe(data.review_rating.value_counts())

    elif choice == "по достопримечательностям":
        st.title("ОТЗЫВЫ ПО ДОСТОПРИМЕЧАТЕЛЬНОСТЯМ")

        # weird bug on server, so:
        try:
            ugram, bgram, tgram = bigram_trigram()
            is_done = True
        except Exception as e:
            print(e)
            print(e.__traceback__)
            is_done = False

        files = [f for f in os.listdir("data") if "main" not in f and "reviews" not in f]
        sight_name = st.selectbox("Выберите достопримечательность", [SIGHTS[f] for f in files])
        df_file = SIGHTS_INV[sight_name]
        df_path = os.path.join("data", df_file)

        st.markdown(f"### {SIGHTS[df_file]}")
        df = load_df(df_path)
        df = df.Link.reset_index()
        df.columns = ["Номер отзыва", "Текст отзыва"]

        fig = go.Figure(data=[go.Table(
            columnwidth=[10, 400],
            header=dict(values=list(df.columns),
                        fill_color='black',
                        align='left',
                        height=42,
                        font=dict(color='darkslategray', size=16)),
            cells=dict(values=[df["Номер отзыва"], df["Текст отзыва"]],
                       fill_color='black',
                       align='left'))
        ])

        col1, col2 = st.columns((2, 2))

        with col1:
            image_path = os.path.join("images", IMAGES[df_file])
            st_img(image_path)

        with col2:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Анализ триграм и биграм")

        if is_done:
            st_freqs(ugram[df_file], bgram[df_file], tgram[df_file], bi_num=7, tri_num=4)
        # st.dataframe(df, width=1200, height=600)


def show_info():
    st.subheader("UNDISCOVERED")
    st.video("https://www.youtube.com/watch?v=ETp-jv20fRQ")
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
