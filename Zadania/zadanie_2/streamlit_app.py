import streamlit as st
from datetime import datetime
from db_connector import DatabaseConnector


table_name = "cars"
db = DatabaseConnector()

st.title("Dodaj nowe ogłoszenie samochodu")

with st.form("car_form"):
    price = st.number_input("Cena", min_value=0, format="%i")
    currency = st.selectbox("Waluta", ["PLN", "EUR", "USD"], index=0)
    brand = st.text_input("Marka", max_chars=50)
    body = st.selectbox(
        "Typ nadwozia",
        ["Sedan", "SUV", "Hatchback", "Kombi", "Coupe", "Kabriolet", "Van", "Pickup", "Inne"],
        index=0
    )
    fuel = st.selectbox(
        "Rodzaj paliwa",
        ["Benzyna", "Diesel", "Hybryda", "Elektryczny", "LPG", "Inne"],
        index=0
    )
    title = st.text_input("Tytuł ogłoszenia", max_chars=100)

    # Pola opcjonalne
    engine_vol_str = st.text_input("Pojemność silnika [cm3] (opcjonalnie)", help="Wprowadź liczbę lub zostaw puste")
    power_str = st.text_input("Moc [KM] (opcjonalnie)", help="Wprowadź liczbę lub zostaw puste")
    mileage_str = st.text_input("Przebieg [km] (opcjonalnie)", help="Wprowadź liczbę lub zostaw puste")
    prod_year_str = st.text_input("Rok produkcji (opcjonalnie)", help="Wprowadź rok lub zostaw puste")
    drive = st.selectbox("Napęd (opcjonalnie)", ["Przód", "Tył", "4x4"])
    orig_country = st.text_input("Kraj pochodzenia (opcjonalnie)", max_chars=50)
    color = st.text_input("Kolor (opcjonalnie)", max_chars=30)
    gearbox_manual = st.radio(
        "Skrzynia biegów",
        ["Manualna", "Automatyczna"]
    )

    submit = st.form_submit_button("Dodaj ogłoszenie")

if submit:
    if not brand or not title:
        st.error("Proszę wypełnić wszystkie wymagane pola (Marka, Tytuł).")
    else:
        def parse_optional_float(val):
            try:
                return float(val) if val.strip() != "" else None
            except ValueError:
                return None

        def parse_optional_int(val):
            try:
                return int(val) if val.strip() != "" else None
            except ValueError:
                return None

        engine_vol = parse_optional_float(engine_vol_str)
        power = parse_optional_float(power_str)
        mileage = parse_optional_float(mileage_str)
        prod_year = parse_optional_int(prod_year_str)

        offer_timestamp = datetime.now()

        new_record = {
            "price": price, "currency": currency, "brand": brand, "body": body,
            "engine_vol": engine_vol, "fuel": fuel, "drive": drive, "power": power,
            "gearbox_is_manual": gearbox_manual, "prod_year": prod_year,
            "orig_country": orig_country, "mileage": mileage, "color": color,
            "title": title, "offer_timestamp": offer_timestamp
        }

        try:
            db.add_record(table_name, new_record)
            st.success("Ogłoszenie zostało dodane poprawnie!")
        except Exception as e:
            st.error(f"Wystąpił błąd podczas dodawania ogłoszenia: {e}")
