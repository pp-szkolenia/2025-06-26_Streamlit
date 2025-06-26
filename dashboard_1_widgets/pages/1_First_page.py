import streamlit as st
import pandas as pd
import time

from db_connector import DatabaseConnector


st.text("Pierwsza strona")

tab1, tab2, tab3, tab4 = st.tabs(["Zakładka 1", "Zakładka 2", "Zakładka 3", "Zakładka 4"])

with tab1:
    st.header("Zawartość zakładki 1")

    values_to_select = ["Select 1", "Select 2", "Select 3", "Select 4"]
    if "selectbox_value" not in st.session_state:
        st.session_state.selectbox_value = values_to_select[0]

    def on_select_change():
        st.session_state.selectbox_value = st.session_state.selectbox_key

    st.selectbox(
        "Label widgetu", values_to_select,
        index=values_to_select.index(st.session_state.selectbox_value),
        key="selectbox_key",
        on_change=on_select_change
    )

    st.write("Wybrano:", st.session_state.selectbox_value)
    # st.session_state.selected_value = selected_option
    st.divider()

    selected_option = st.radio("Label widgetu", ["Radio 1", "Radio 2", "Radio 3", "Radio 4"])
    st.write("Wybrano:", selected_option)
    st.divider()

    selected_options = st.multiselect(
        "Wybierz opcje:", ["Multi 1", "Multi 2", "Multi 3", "Multi 4"])
    st.write("Wybrano:", str(selected_options))
    st.divider()

    checked = st.checkbox("Zaznacz mnie")
    if checked:
        st.write("Pole jest zaznaczone")
    else:
        st.write("Pole nie jest zaznaczone")
    st.divider()

    checked = st.toggle("Włącz/wyłącz", value=True)
    if checked:
        st.write("Toggle jest włączony")
    else:
        st.write("Toggle jest wyłączony")
    st.divider()

    value = st.slider("Wybierz wartość", min_value=10, max_value=30, step=2, value=16)
    st.write("Wybrana wartość:", value)
    st.divider()

    values = st.slider("Wybierz wartości:", min_value=10, max_value=30, step=2, value=[12, 18])
    st.write("Wybrana wartości:", values)
    st.divider()

    text = st.text_input("Wprowadź tekst:")
    st.write("Wprowadzony tekst:", text)
    st.divider()

    number = st.number_input("Podaj liczbę", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
    st.write("Podana liczba:", number)
    st.divider()

    long_text = st.text_area("Wpisz długi tekst")
    st.write("Wpisany tekst:", long_text)
    st.divider()

    date = st.date_input("Podaj datę")
    st.write("Podana data:", date)
    st.divider()

    if st.button("Pokaż wiadomość"):
        st.success("To jest ukryta wiadomość")

    st.divider()

with tab2:
    st.header("Zawartość zakładki 2")
    uploaded_file = st.file_uploader("Wybierz plik .csv", type="csv")
    # print("!!!", type(uploaded_file), "|", uploaded_file)
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.write("Zawartość pliku .csv:")
        st.dataframe(df)
    else:
        st.info("Proszę wczytać plik csv")

    st.divider()
    data = {
        "Kolumna 1": [1, 2, 3, 4],
        "Kolumna 2": ["A", "B", "C", "D"]
    }
    df = pd.DataFrame(data)

    st.write("Przykladowy dataframe")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    # print("!!!", type(csv), "|", csv)

    st.download_button(
        "Pobierz jako csv", data=csv, file_name="dane.csv", mime="text/csv"
    )

with tab3:
    st.header("Zawartość zakładki 3")

    @st.cache_data(show_spinner=False)
    def time_consuming_operation(x):
        time.sleep(4)
        return (x+1)*2

    number = st.number_input("Wpisz liczbę")

    if st.button("Uruchom operację") and number:
        with st.spinner("Trwa przetwarzanie"):
            result = time_consuming_operation(number)
        st.write("Wynik:", result)

    st.divider()
    if st.button("Uruchom proces z progress barem"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        for step in range(20):
            time.sleep(0.5)
            progress_bar.progress((step+1)/20)
            status_text.text(f"Krok {step+1} z 20")

        st.success("Proces zakończony pomyślnie")

with tab4:
    st.header("Zawartość zakładki 4")
    if hasattr(st.session_state, "df"):
        df = st.session_state.df.head(50)
    else:
        df = pd.DataFrame()
    st.dataframe(df)

    st.divider()

    st.table(df)

    st.divider()
    st.json({"a": [1, 2, 3], "b": [4, 5, 6]})
    st.divider()

    DB_PATH = "data.db"
    connector = DatabaseConnector(DB_PATH)
    table_name = st.text_input("Podaj nazwę tabeli")
    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Zapisz zmiany"):
        if edited_df.equals(df):
            st.info("Brak zmian do zapisania")
        else:
            try:
                connector.update_table(table_name, edited_df)
                st.session_state.df = edited_df.copy()
                st.success("Wszystkie zmiany zostały zapisane w bazie danych.")
            except Exception as e:
                st.error(f"Wystąpił błąd podczas zapisu: {e}")
