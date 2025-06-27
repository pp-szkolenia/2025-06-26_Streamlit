import streamlit as st
from db_connector import DatabaseConnector
from languages import translate


st.set_page_config(page_title="Todo list", layout="wide")

if "language" not in st.session_state:
    st.session_state["language"] = "en"
if "user" not in st.session_state:
    st.session_state.user = None
if "users" not in st.session_state:
    connector = DatabaseConnector("database/users.json", "database/tasks.json")
    st.session_state.users = connector.load_users()


with st.sidebar:
    lang_in_session = st.session_state.get("language")
    index = ["en", "pl"].index(lang_in_session) if lang_in_session else 0
    lang = st.selectbox("", ["en", "pl"], index=index,
                        format_func=lambda x: "English" if x == "en" else "Polski",
                        key="language_select"
    )
    st.session_state.language = lang

st.title("Todo list dashboard")
st.markdown(f"#### {translate('main_info', lang)}")

if st.session_state.user:
    st.success(f"{translate('login', lang)}: {st.session_state.user['display_name']}")
    if st.button(translate('logout', lang)):
        st.session_state.user = None
        st.rerun()
else:
    with st.form("login_form"):
        username = st.text_input(translate("username", lang))
        password = st.text_input(translate("password", lang), type="password")
        submitted = st.form_submit_button(translate("login", lang))
        if submitted:
            user = next((u for u in st.session_state.users if u["username"] == username
                        and u["password"] == password), None)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error(translate("login_failed", lang))



