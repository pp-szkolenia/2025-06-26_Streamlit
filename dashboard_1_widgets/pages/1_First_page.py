import streamlit as st


st.text("Pierwsza strona")

tab1, tab2, tab3, tab4 = st.tabs(["Zakładka 1", "Zakładka 2", "Zakładka 3", "Zakładka 4"])

with tab1:
    st.header("Zawartość zakładki 1")
    st.write("To jest zawartość pierwszej zakładki")

with tab2:
    st.header("Zawartość zakładki 2")
    st.write("To jest zawartość drugiej zakładki")

with tab3:
    st.header("Zawartość zakładki 3")
    st.write("To jest zawartość trzeciej zakładki")

with tab4:
    st.header("Zawartość zakładki 4")
    st.write("To jest zawartość czwartej zakładki")
