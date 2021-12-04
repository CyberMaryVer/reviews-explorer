import streamlit as st
import json
import requests
from bs4 import BeautifulSoup
from st_constants import API_KEY, MOSCOW
from st_utils import st_img, format_text, color_text


def _find_route(start, end, api_key=API_KEY):
    get_request = lambda \
            x: f"https://api.rasp.yandex.net/v3.0/search/?apikey={api_key}&format=json&from={x[0]}&to={x[1]}" \
               f"&transport_types=train&system=yandex&show_systems=esr&transfers=true&limit=4"
    request_txt = get_request([start, end])
    # try to find direct route
    getpage = requests.get(request_txt)
    getpage_soup = BeautifulSoup(getpage.text, 'html.parser')
    route = json.loads(str(getpage_soup))

    try:
        if len(route['segments']) == 0:
            print("No direct routes")
            route_to_msc, route_from_msc = None, None

            # try to find route to msc
            for moscow_code in MOSCOW:
                request_txt = get_request([start, moscow_code])
                getpage = requests.get(request_txt)
                getpage_soup = BeautifulSoup(getpage.text, 'html.parser')
                route = json.loads(str(getpage_soup))
                if len(route['segments']) != 0:
                    print(moscow_code, len(route['segments']))
                    route_to_msc = route
                    break

            # try to find route from msc
            for moscow_code in MOSCOW:
                request_txt = get_request([moscow_code, end])
                getpage = requests.get(request_txt)
                getpage_soup = BeautifulSoup(getpage.text, 'html.parser')
                route = json.loads(str(getpage_soup))
                if len(route['segments']) != 0:
                    print(moscow_code, len(route['segments']))
                    route_from_msc = route
                    break
            return route_to_msc, route_from_msc

        else:
            return route, None

    except Exception as e:
        print(f"{type(e)}: {e}")
        print(route)


def _unpack_json(trains_data, api_key=API_KEY):
    if "segments" not in trains_data.keys():
        return
    else:
        request_to_db = []
        for idx, segment in enumerate(trains_data['segments']):
            try:
                arrival = segment['arrival']
                departure = segment['departure']
                duration = segment['duration']
                start_date = segment['start_date']
                stops = segment['stops']
                number = segment['thread']['number']
                uid = segment['thread']['uid']
                title = segment['thread']['title']
                url_route = segment['thread']['thread_method_link'].split('?')[-1]
                url_route = f'https://api.rasp.yandex.net/v3/thread/?apikey={api_key}&{url_route}'
                from_esr = segment['from']['codes']['esr']
                from_yandex_code = segment['from']['code']
                to_esr = segment['to']['codes']['esr']
                to_yandex_code = segment['to']['code']
                params = {'arrival': arrival,
                          'departure': departure,
                          'duration': duration,
                          'start_date': start_date,
                          'stops': stops,
                          'number': number,
                          'uid': uid,
                          'title': title,
                          'url_route': url_route,
                          'from_esr': from_esr,
                          'to_esr': to_esr,
                          'from_yandex_code': from_yandex_code,
                          'to_yandex_code': to_yandex_code,
                          }
                request_to_db.append(params)

            except Exception as e:
                print(f"{type(e)}: {e} [{segment}]")

    return request_to_db


def st_schedule(request_to_db, s_start, s_end, transfers=False):
    for idx, train in enumerate(request_to_db):
        col1, col2, col3 = st.columns((6, 6, 2))
        with col1:
            st.markdown(
                f"""* Поезд {train['title']}, номер рейса: {format_text(train['number'])} """,
                unsafe_allow_html=True)
            st.markdown(
                f"""{color_text('ОТПРАВЛЕНИЕ:')} **{train['start_date']}** {train['departure']}""",
                unsafe_allow_html=True)
            st.markdown(
                f"""{color_text('ПРИБЫТИЕ:')} {train['arrival']} """,
                unsafe_allow_html=True)
            st.markdown(f"""в пути {train['duration'] // 3600:.0f} ч {(train['duration'] % 3600) // 60:.0f} мин""")

        with col2:
            with st.expander("Информация о маршруте следования"):
                getpage = requests.get(train['url_route'])
                getpage_soup = BeautifulSoup(getpage.text, 'html.parser')
                route_data = json.loads(str(getpage_soup))

                for stop in route_data['stops']:
                    stop_title = stop['station']['title']
                    stop_type = stop['station']['station_type_name']
                    stop_code = stop['station']['code']

                    # formatting
                    formatted = format_text(stop_title, color=(194, 197, 216)) \
                        if stop_code == s_start or stop_code == s_end \
                        else stop_title

                    # printing
                    st.markdown(f"""* {formatted}, ({stop_type})""", unsafe_allow_html=True)
        with col3:
            st.checkbox("""Послать запрос""", key=f"train_{idx}")
            st_img("./data/train.png")
        st.markdown("----")


def yandex_api(s_start, s_end, api_key=API_KEY):
    trains_data = _find_route(s_start, s_end, api_key)

    if trains_data is not None:
        route1, route2 = trains_data

        if "segments" not in route1.keys() and route2 is None:
            st.error("Поездов между станциями не найдено")
        else:
            st.info("Найдены следующие маршруты:")
            with st.form("routes"):
                request_to_db = _unpack_json(route1)
                st_schedule(request_to_db, s_start, s_end)

                email = st.text_input("e-mail:")
                st.checkbox("Отправить копию на электронную почту")
                submit = st.form_submit_button("OK")
            if submit:
                with open("requests.json", "w") as writer:
                    json.dump(request_to_db, writer)
                st.success("Запрос отправлен. Ждите ответ.")
