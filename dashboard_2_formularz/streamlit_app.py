import streamlit as st
from datetime import date

from db_connector import DatabaseConnector


connector = DatabaseConnector()

st.title("Dodaj pasażera Titanica")

with st.form("add_passenger"):
    survived = st.radio(
        "Czy pasażer przeżył", options=["Tak", "Nie"], index=0
    )
    survived_int = 1 if survived == "Tak" else 0

    pclass = st.selectbox(
        "Klasa pasażera", options=["", 1, 2, 3]
    )
    pclass = pclass if pclass else None

    name = st.text_input("Imię i nazwisko")

    sex = st.radio(
        "Płeć", options=["male", "female"]
    )

    date_of_birth = st.date_input(
        "Data urodzenia", max_value=date.today(), min_value=date(1900, 1, 1),
    )
    age = int((date.today() - date_of_birth).days / 365)

    fare = st.number_input(
        "Cena", min_value=0.0, step=0.01, max_value=1000.0
    )

    submitted = st.form_submit_button("Dodaj pasażera")
    if submitted:
        df_exist = connector.select_records("titanic")
        next_id = df_exist["PassengerId"].max() + 1

        record = {
            "PassengerId": next_id,
            "Survived": survived_int,
            "Pclass": pclass,
            "Name": name,
            "Sex": sex,
            "Age": age,
            "Fare": fare
        }

        try:
            connector.add_record("titanic", record)
            st.success("Pasażer dodany")
        except Exception as e:
            st.error(f"Coś poszło nie tak: {e}")
