import streamlit as st

st.set_page_config(page_title="Streamlit widgets", layout="wide")

st.title("Tytuł strony")
st.header("Nagłówek")
st.subheader("Nagłówek niższego rzędu")

st.markdown("`Tekst` w **markdown**")
st.text("Dowolny tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst  t tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekstekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst tekst")
st.write("Dowolnie", "dużo", "fragmentów", "tekstu")

st.divider()

st.success("Komunikat o powodzeniu operacji")
st.warning("Ostrzeżenie")
st.info("Informacja")
st.error("Błąd")

st.sidebar.text("Sidebar")
st.sidebar.success("Sukces sidebara")

with st.sidebar:
    st.divider()
    st.text("hello")

