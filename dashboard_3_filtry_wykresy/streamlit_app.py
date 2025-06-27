import streamlit as st
import plotly.express as px

from db_connector import DatabaseConnector


connector = DatabaseConnector()
df = connector.select_records("titanic")


st.set_page_config(layout="wide")

max_unique = 5
numeric_columns = [column for column in df.select_dtypes(include=['number']).columns
                   if df[column].nunique() > max_unique]
categorical_columns = [column for column in df.columns if df[column].nunique() <= max_unique]

st.title("Data dashboard")
st.sidebar.title("Filters")
filtered_df = df.copy()

st.sidebar.header("Numerical")
for column in numeric_columns:
    min_value, max_value = df[column].min(), df[column].max()
    selected = st.sidebar.slider(column, min_value, max_value, [min_value, max_value])
    # filtered_df = filtered_df[(filtered_df[column] >= selec)]
    filtered_df = filtered_df[filtered_df[column].between(*selected)]

st.sidebar.header("Categorical")
for column in categorical_columns:
    options = df[column].unique()
    selected = st.sidebar.multiselect(column, options, default=options)
    filtered_df = filtered_df[filtered_df[column].isin(selected)]

with st.expander("Data"):
    st.dataframe(filtered_df)

col1, _, col2 = st.columns([2, 1, 2])

with col1:
    chart_type = st.selectbox("Chart type", ["histogram", "countplot"])
    if chart_type == "histogram":
        col = st.selectbox("Column", numeric_columns)
        fig = px.histogram(filtered_df, x=col, nbins=20)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
    else:
        col = st.selectbox("Column", categorical_columns)
        fig = px.histogram(filtered_df, x=col)
        fig.update_layout(bargap=0.2)

    st.plotly_chart(fig)


with col2:
    chart_type = st.selectbox("Chart type", ["histogram", "countplot"], key="chart_type_selectobox_2")
    if chart_type == "histogram":
        col = st.selectbox("Column", numeric_columns, key="column_selectbox_2")
        fig = px.histogram(filtered_df, x=col, nbins=20)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
    else:
        col = st.selectbox("Column", categorical_columns, key="column_selectbox_2")
        fig = px.histogram(filtered_df, x=col)
        fig.update_layout(bargap=0.2)

    st.plotly_chart(fig)



