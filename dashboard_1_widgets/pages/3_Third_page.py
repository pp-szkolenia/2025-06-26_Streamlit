import streamlit as st


users = st.secrets["USERS"]
with st.expander("Sekrety"):
    st.json(users)


if "user" not in st.session_state:
    username = st.text_input("User")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        user = users.get(username)
        if user and user["password"] == password:
            st.session_state.user = {"name": username,
                                     "role": user["role"]}
            st.rerun()
        else:
            st.error("Nieprawidłowe dane")
else:
    role = st.session_state.user["role"]
    st.sidebar.write(f"Zalogowany jako: {st.session_state.user['name']}")

    if st.sidebar.button("Log out"):
        del st.session_state.user
        st.rerun()

    tab1, tab2 = st.tabs(["Ogólne", "Tylko dla adminów"])

    with tab1:
        st.write("Treść widoczna dla wszystkich zalogowanych")

    with tab2:
        if role == "admin":
            st.write("Treść widoczna tylko dla admina")
        else:
            st.error("Brak dostępu do tej zakładki")
