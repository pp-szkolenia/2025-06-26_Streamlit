import streamlit as st

from db_connector import DatabaseConnector
from languages import translate


if "language" not in st.session_state:
    st.session_state.language = "en"
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in.")
    st.stop()
if "users" not in st.session_state:
    connector = DatabaseConnector("../database/users.json", "../database/tasks.json")
    st.session_state.users = connector.load_users()


with st.sidebar:
    lang_in_session = st.session_state.get("language")
    index = ["en", "pl"].index(lang_in_session) if lang_in_session else 0
    lang = st.selectbox("", ["en", "pl"], index=index,
                        format_func=lambda x: "English" if x == "en" else "Polski", key="language_users")
    st.session_state.language = lang

    if st.session_state.user:
        st.markdown(f"**{translate('logged_in_as', lang)}:** {st.session_state.user['display_name']}")


user = st.session_state.user
is_admin = user["role"] == "admin"

st.header(translate("users", lang))

for u in st.session_state.users:
    cols = st.columns([2, 2, 2, 1, 1])
    cols[0].markdown(f"**{translate('display_name', lang)}:** {u['display_name']}")
    cols[1].markdown(f"**{translate('username', lang)}:** {u['username']}")
    cols[2].markdown(f"**{translate('role', lang)}:** {translate(u['role'], lang)}")
    if is_admin and u["role"] != "admin":
        if cols[3].button(translate("delete_user", lang), key=f"delete_user_{u['id']}"):
            st.session_state.users = [usr for usr in st.session_state.users if usr["id"] != u["id"]]
            connector = DatabaseConnector("database/users.json", "database/tasks.json")
            connector.save_users(st.session_state.users)
            st.rerun()


if is_admin:
    with st.expander(translate("add_user", lang)):
        display_name = st.text_input(translate("display_name", lang), key="new_user_display_name")
        username = st.text_input(translate("username", lang), key="new_user_username")
        password = st.text_input(translate("password", lang), type="password", key="new_user_password")
        if st.button(translate("add_user", lang), key="add_user_btn"):
            new_id = max([u["id"] for u in st.session_state.users], default=0) + 1
            st.session_state.users.append({
                "id": new_id,
                "username": username,
                "password": password,
                "role": "user",
                "display_name": display_name
            })
            connector = DatabaseConnector("database/users.json", "database/tasks.json")
            connector.save_users(st.session_state.users)
            st.success(translate("user_created", lang))
            st.rerun()

