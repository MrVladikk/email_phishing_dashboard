
import streamlit as st # Streamlit для веб-интерфейса
import pandas as pd # pandas для работы с таблицами
import plotly.express as px # plotly для интерактивной визуализации
from io import BytesIO # BytesIO для экспорта в Excel

# функция загрузки начальных данных с кэшированием
@st.cache_data

def load_base_data(path):  # функция принимает путь к CSV
    df = pd.read_csv(path) # читаем CSV и создаём DataFrame
    return df # возвращаем DataFrame

# главная функция приложения
def main():
    st.set_page_config(page_title="Phishing Dashboard", layout="wide") # настраиваем страницу: заголовок браузера и полный экран
    st.title("Phishing Dashboard — Анализ и фильтрация email") # отображаем главный заголовок дашборда
    st.write("Интерактивный дашборд для исследования фишинговых писем по разным признакам.") # отображаем краткое описание под заголовком

    base_data = load_base_data("email_phishing_data.csv")  # загружаем базовые данные
    uploaded = st.sidebar.file_uploader("Загрузить CSV с новыми письмами", type=["csv"]) # загрузка дополнительных писем через файл-аплоудер в сайдбаре
    if uploaded:
        new_data = pd.read_csv(uploaded) # если пользователь загрузил новый файл, читаем его
        st.sidebar.success(f"Загружено {len(new_data)} новых писем") # показываем, сколько писем загружено
        data = pd.concat([base_data, new_data], ignore_index=True) # объединяем базовые и новые данные
    else:
        data = base_data # если нет загрузки, работаем только с базой

    # группируем все фильтры в боковой панели внутри экспандера
    with st.sidebar.expander("🔍 Фильтры по признакам", expanded=True):
        # фильтр по типу письма (метка)
        labels = st.multiselect(
            "Тип письма:", [0, 1], [0, 1],
            format_func=lambda x: "Легитимное" if x == 0 else "Фишинг"
        ) # выберите 0 или 1

        # фильтр по количеству слов
        min_w, max_w = st.slider(
            "Количество слов:",
            int(data.num_words.min()), int(data.num_words.max()),
            (int(data.num_words.min()), int(data.num_words.max()))
        )  # задаём диапазон

        # фильтр по уникальным словам
        min_uw, max_uw = st.slider(
            "Уникальные слова:",
            int(data.num_unique_words.min()), int(data.num_unique_words.max()),
            (int(data.num_unique_words.min()), int(data.num_unique_words.max()))
        )  # диапазон уникальных слов

        # фильтр по стоп-словам
        min_sw, max_sw = st.slider(
            "Стоп-слова:",
            int(data.num_stopwords.min()), int(data.num_stopwords.max()),
            (int(data.num_stopwords.min()), int(data.num_stopwords.max()))
        )  # диапазон стоп-слов

        # фильтр по ссылкам
        min_links, max_links = st.slider(
            "Количество ссылок:",
            int(data.num_links.min()), int(data.num_links.max()),
            (int(data.num_links.min()), int(data.num_links.max()))
        )  # диапазон ссылок

        # фильтр по уникальным доменам
        min_ud, max_ud = st.slider(
            "Уникальные домены:",
            int(data.num_unique_domains.min()), int(data.num_unique_domains.max()),
            (int(data.num_unique_domains.min()), int(data.num_unique_domains.max()))
        )  # диапазон доменов

        # фильтр по email-адресам внутри письма
        min_ea, max_ea = st.slider(
            "Email-адреса:",
            int(data.num_email_addresses.min()), int(data.num_email_addresses.max()),
            (int(data.num_email_addresses.min()), int(data.num_email_addresses.max()))
        )  # диапазон адресов

        # фильтр по орфографическим ошибкам
        min_err, max_err = st.slider(
            "Орфографические ошибки:",
            int(data.num_spelling_errors.min()), int(data.num_spelling_errors.max()),
            (int(data.num_spelling_errors.min()), int(data.num_spelling_errors.max()))
        )  # диапазон ошибок

        # фильтр по срочным ключевым словам
        min_uk, max_uk = st.slider(
            "Срочные слова:",
            int(data.num_urgent_keywords.min()), int(data.num_urgent_keywords.max()),
            (int(data.num_urgent_keywords.min()), int(data.num_urgent_keywords.max()))
        )  # диапазон срочных слов

    # применяем все фильтры к DataFrame
    filtered = data[
        (data.label.isin(labels)) &
        (data.num_words.between(min_w, max_w)) &
        (data.num_unique_words.between(min_uw, max_uw)) &
        (data.num_stopwords.between(min_sw, max_sw)) &
        (data.num_links.between(min_links, max_links)) &
        (data.num_unique_domains.between(min_ud, max_ud)) &
        (data.num_email_addresses.between(min_ea, max_ea)) &
        (data.num_spelling_errors.between(min_err, max_err)) &
        (data.num_urgent_keywords.between(min_uk, max_uk))
    ]  # итоговый фильтр

    # рассчитываем ключевые метрики
    total = len(filtered) # общее количество после фильтра
    phishing_count = filtered.label.sum() # сколько фишинговых
    avg_words = filtered.num_words.mean() # среднее число слов

    col1, col2, col3 = st.columns(3) # отображаем метрики в три колонки
    col1.metric("Всего писем", total)  # общее число
    col2.metric("Фишинг", phishing_count)  # число фишинга
    col3.metric("Среднее слов", f"{avg_words:.1f}")  # среднее слов

    # создаём вкладки для визуализации и таблицы
    tab1, tab2 = st.tabs(["График", "Таблица"])  # две вкладки
    with tab1:
        # гистограмма распределения слов по меткам
        st.subheader("Распределение слов по типу письма")
        fig = px.histogram(
            filtered,
            x="num_words",
            color=filtered.label.map({0: "Legit", 1: "Phishing"}),
            barmode="overlay",
            nbins=40,
            labels={"num_words": "Число слов", "label": "Тип"},
            color_discrete_map={"Legit": "green", "Phishing": "red"}
        )  # создаём фигуру
        fig.update_traces(opacity=0.7)  # задаём прозрачность
        st.plotly_chart(fig, use_container_width=True)  # отображаем график

    with tab2:
        # таблица с отфильтрованными данными
        st.subheader("Таблица писем")
        st.dataframe(filtered.reset_index(drop=True))  # выводим таблицу

    # кнопка для экспорта в Excel
    st.subheader("Экспорт данных")  # раздел экспорта
    def to_excel(df):  # функция конвертации DataFrame в Excel
        out = BytesIO()  # создаём буфер
        df.to_excel(out, index=False, sheet_name="filtered")  # записываем
        return out.getvalue()  # возвращаем байты

    st.download_button(
        label="Скачать .xlsx",
        data=to_excel(filtered),
        file_name="filtered_emails.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )  # кнопка скачивания

# запуск приложения
if __name__ == "__main__":
    main()  # вызываем функцию