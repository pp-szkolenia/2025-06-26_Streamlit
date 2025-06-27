import streamlit as st
import pandas as pd
import plotly.express as px

from db_connector import DatabaseConnector


connector = DatabaseConnector()
df = connector.select_records("cars")

df["offer_timestamp"] = pd.to_datetime(df["offer_timestamp"])
# st.dataframe(df)
st.set_page_config(layout="wide")
st.title("Cars Dashboard")
filtered = df.copy()

max_unique = 15
numeric_cols = [col for col in df.select_dtypes(["number"]).columns
                if df[col].nunique() > max_unique]
categorical_cols = [col for col in df.columns if df[col].nunique() <= max_unique]
datetime_cols = [col for col in df.select_dtypes("datetime").columns]
text_cols = [col for col in df.select_dtypes("object").columns if col not in categorical_cols]


def render_filters(columns, func, data):
    for i in range(0, len(columns), 3):
        st_columns = st.columns([3, 0.5, 3, 0.5, 3])
        subset = columns[i:i+3]
        for j, col in enumerate(subset):
            with st_columns[j*2]:
                data = func(col, data)
    return data


with st.expander("Filtry numeryczne"):
    def numeric_filter(col, data):
        col_min, col_max = df[col].min(), df[col].max()
        state_key = f"{col}_range"
        if state_key not in st.session_state:
            st.session_state[state_key] = (col_min, col_max)

        current_min, current_max = st.session_state[state_key]
        min_val, max_val = st.slider(col, col_min, col_max, (current_min, current_max),
                                     key=f"{col}_slider")

        return data[data[col].between(min_val, max_val)]

    filtered = render_filters(numeric_cols, numeric_filter, filtered)


with st.expander("Filtry kategoryczne"):
    def categorical_filter(col, data):
        options = df[col].dropna().unique().tolist()
        selected = st.multiselect(col, options, default=options, key=f"{col}_multiselect")
        return data[data[col].isin(selected)]

    filtered = render_filters(categorical_cols, categorical_filter, filtered)

with st.expander("Filtry dat"):
    def datetime_filter(col, data):
        dates = pd.to_datetime(data[col])
        min_date, max_date = dates.min().date(), dates.max().date()

        st.markdown(f"**{col}**")
        col_start, col_end = st.columns(2)

        with col_start:
            start_date = st.date_input(f"{col} - od", value=min_date, min_value=min_date, max_value=max_date,
                          key=f"{col}_start")
        with col_end:
            end_date = st.date_input(f"{col} - do", value=max_date, min_value=min_date, max_value=max_date,
                          key=f"{col}_end")
        return data[data[col].dt.date.between(start_date, end_date)]


    filtered = render_filters(datetime_cols, datetime_filter, filtered)

with st.expander("Filtry tekstowe"):
    def text_filter(col, data):
        pattern = st.text_input(f"Search {col}")
        if pattern:
            return data[data[col].str.contains(pattern, na=False)]
        else:
            return data

    filtered = render_filters(text_cols, text_filter, filtered)


with st.expander("Dane"):
    st.dataframe(filtered)
