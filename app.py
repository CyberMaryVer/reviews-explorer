from utils.st_constants import *
from utils.st_utils import *
from utils.st_pages import *

# set page settings
st.set_page_config(page_title="web-app", page_icon=":bar_chart:", layout="wide",
                   menu_items={
                       'Get Help': 'https://www.rferl.org/a/kamchatka-volcanoes-ballistic-missile/31358301.html',
                       'About': "### Undiscovered\n----\nПриложение для анализа отзывов"
                   })


def main():
    side_menu_list = [
        "Общий анализ",
        "Анализ отзывов",
        "Команда",
        "Информация о проекте"
    ]

    side_menu_choice = st.sidebar.selectbox("", side_menu_list, key="side_menu")
    side_menu_idx = side_menu_list.index(side_menu_choice)
    st_img("./images/logo.jfif", sidebar=True, width=300)

    # username = st.session_state["username"]
    if side_menu_idx == 0:
        st_title("Общий анализ данных")
        show_data()

    elif side_menu_idx == 1:
        st_title("Анализ отзывов туристов")
        show_nlp()

    elif side_menu_idx == 2:
        st_title("Команда")
        show_info()

    elif side_menu_idx == 3:
        st_title("Информация о проекте")
        pass


if __name__ == "__main__":
    main()
