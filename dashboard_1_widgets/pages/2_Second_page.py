import streamlit as st
import plotly.express as px


df = st.session_state.df

# Histogram
fig_hist = px.histogram(
    df, x="Age", nbins=30,
    title="Rozkład wieku pasażerów"
)
st.plotly_chart(fig_hist)

# Barplot
sex_counts = df["Sex"].value_counts().reset_index()
sex_counts.columns = ["Sex", "Count"]
fig_bar = px.bar(
    sex_counts,
    x="Sex", y="Count",
    title="Liczba pasażerów wg płci"
)
st.plotly_chart(fig_bar)
