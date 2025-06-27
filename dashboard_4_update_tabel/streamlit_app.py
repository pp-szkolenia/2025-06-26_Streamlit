import streamlit as st
import pandas as pd
import sqlite3


st.set_page_config(page_title="SQLite Titanic Dashboard", layout="wide")
st.title("SQLite Titanic Dashboard")

@st.cache_resource
def get_connection():
    return sqlite3.connect("data.db", check_same_thread=False)


conn = get_connection()

st.subheader("SQL query")
user_query = st.text_area("Enter your SQL query below:", value="SELECT * FROM titanic;", height=200)

if st.button("Execute SQL"):
    try:
        df = pd.read_sql(user_query, conn)
        st.session_state["df_original"] = df.copy()
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")

if "df_original" in st.session_state:
    edited_df = st.data_editor(st.session_state["df_original"], num_rows="dynamic",
                               disabled=["Age", "Survived"])

    if st.button("Save change in database"):
        # ---
        # if 4 in edited_df["Pclass"]:
            # st.error("Błąd walidacji")
            # st.exception("Bład walidacji")
        # --
        try:
            edited_df.to_sql("titanic", conn, if_exists="replace", index=False)
        except Exception as e:
            st.error(f"Error saving to database: {e}")
