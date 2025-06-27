import streamlit as st
import pandas as pd
import sqlite3


st.set_page_config(page_title="Cars SQL Dashboard", layout="wide")
st.title("Cars SQL Dashboard")

st.sidebar.empty()

def authenticate(username, password):
    users = st.secrets.get("USERS", {})
    if username in users and password == users[username]["password"]:
        return True
    return False


def get_role(username):
    return st.secrets["USERS"][username]["role"]


if st.session_state.get("authenticated"):
    if st.sidebar.button("Log out"):
        del st.session_state["username"]
        del st.session_state["authenticated"]
        del st.session_state["role"]
        st.rerun()


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


if not st.session_state["authenticated"]:
    with st.form("login"):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")

        if submitted and authenticate(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = get_role(username)
            st.success(f"Welcome {username} ({st.session_state['role']})")
            st.rerun()

        elif submitted:
            st.error("Invalid credentials")
    st.stop()


@st.cache_resource
def get_connection():
    return sqlite3.connect("data.db", check_same_thread=False)


conn = get_connection()

st.subheader("SQL query")
user_query = st.text_area("Write your SQL query:", value="SELECT * FROM cars LIMIT 10;", height=200)

if st.button("Execute SQL"):
    try:
        if not user_query.strip().lower().startswith("select"):
            st.error("Only SELECT queries are allowed")
        else:
            df = pd.read_sql(user_query, conn)
            st.session_state["df_original"] = df.copy()
            st.success("Query executed successfully")
    except Exception as e:
        st.error(f"Error executing query: {e}")


if "df_original" in st.session_state:
    edited_df = st.data_editor(st.session_state["df_original"], num_rows="dynamic")

    if st.session_state["role"] == "admin":
        if st.button("Save changes to database"):
            try:
                edited_df.to_sql("cars", conn, if_exists="replace", index=False)
                st.success("Changes saved to database")
            except Exception as e:
                st.error(f"Error saving to database: {e}")
    else:
        st.info("Only admins can save changes to the database")
