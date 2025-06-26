import streamlit as st
import plotly.express as px


df = st.session_state.df

col1, _, col2 = st.columns([3, 1, 3])

# Histogram
with col1:
    fig_hist = px.histogram(
        df, x="Age", nbins=30,
        title="Rozkład wieku pasażerów"
    )
    st.plotly_chart(fig_hist)

# Barplot
with col2:
    sex_counts = df["Sex"].value_counts().reset_index()
    sex_counts.columns = ["Sex", "Count"]
    fig_bar = px.bar(
        sex_counts,
        x="Sex", y="Count",
        title="Liczba pasażerów wg płci"
    )
    st.plotly_chart(fig_bar)

st.divider()

left, _, right = st.columns([3, 1, 3])

with left:
    left_1, left_2 = st.columns(2)
    with left_1:
        st.text("Left 1")
    with left_2:
        st.text("Left 2")


with right:
    right_1, right_2 = st.columns(2)
    with right_1:
        st.text("Right 1")
    with right_2:
        st.text("Right 2")

        a, b = st.columns(2)
        with a:
            st.text("A")
        with b:
            st.text("B")

            b1, b2 = st.columns(2)
            with b1:
                st.text("b1")
            with b2:
                st.text("b2")


st.divider()

with st.expander("Rozwiń"):
    st.write("Ukryta zawartość")

st.divider()

import time
placeholder = st.empty()
text = "hello world"
for i in range(1, len(text) + 1):
    placeholder.write(text[:i])
    time.sleep(1)