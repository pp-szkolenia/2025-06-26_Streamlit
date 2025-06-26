import streamlit as st


if hasattr(st.session_state, "selected_value"):
    selected_option = st.session_state.selected_value
else:
    selected_option = None

st.write("Selectbox:", selected_option)
