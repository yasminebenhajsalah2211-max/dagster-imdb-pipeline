import pandas as pd
import streamlit as st
import psycopg2
import plotly.express as px

st.set_page_config(
    page_title="IMDb Movies Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #F5C518;
}
.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE ----------
conn = psycopg2.connect(
    host="localhost",
    database="imdb_db",
    user="imdb_user",
    password="imdb_password",
    port=5433
)

df = pd.read_sql("SELECT * FROM imdb_movies", conn)

df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# ---------- HEADER ----------
st.title("🎬 IMDb Movies Dashboard")
st.write("Interactive dashboard based on the IMDb Top Movies dataset.")

# ---------- SIDEBAR ----------
st.sidebar.header("🎛️ Filters")

min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select year range",
    min_year,
    max_year,
    (min_year, max_year)
)

min_rating = st.sidebar.slider(
    "Minimum rating",
    0.0,
    10.0,
    8.0
)

filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["rating"] >= min_rating)
]

# ---------- KPIs ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("🎞️ Movies", len(filtered_df))
col2.metric("⭐ Average Rating", round(filtered_df["rating"].mean(), 2))
col3.metric("🏆 Best Rating", filtered_df["rating"].max())
col4.metric("📅 Years Covered", f"{year_range[0]} - {year_range[1]}")

st.divider()

# ---------- CHART 1 ----------
st.subheader("🏆 Top 10 Movies by Rating")

top_movies = filtered_df.sort_values("rating", ascending=False).head(10)

fig1 = px.bar(
    top_movies,
    x="rating",
    y="title",
    orientation="h",
    color="rating",
    color_continuous_scale="Viridis",
    title="Top 10 Movies by IMDb Rating"
)

fig1.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# ---------- CHART 2 ----------
st.subheader("📅 Number of Movies by Year")

movies_by_year = (
    filtered_df.groupby("year")
    .size()
    .reset_index(name="count")
)

fig2 = px.line(
    movies_by_year,
    x="year",
    y="count",
    markers=True,
    title="Movie Releases Over Time"
)

fig2.update_traces(line=dict(width=3))
st.plotly_chart(fig2, use_container_width=True)

# ---------- CHART 3 ----------
st.subheader("⭐ Rating Distribution")

fig3 = px.histogram(
    filtered_df,
    x="rating",
    nbins=15,
    color_discrete_sequence=["#F5C518"],
    title="Distribution of IMDb Ratings"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------- CHART 4 ----------
st.subheader("🎭 Movies by Genre")

if "genre" in filtered_df.columns:
    genre_df = filtered_df.copy()

    genre_df["genre"] = genre_df["genre"].astype(str)
    genre_df = genre_df.assign(
        genre=genre_df["genre"].str.replace("[", "", regex=False)
                               .str.replace("]", "", regex=False)
                               .str.replace("'", "", regex=False)
                               .str.split(",")
    ).explode("genre")

    genre_df["genre"] = genre_df["genre"].str.strip()

    genre_count = (
        genre_df.groupby("genre")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(10)
    )

    fig4 = px.pie(
        genre_count,
        names="genre",
        values="count",
        title="Top Genres"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ---------- TABLE ----------
st.subheader("📋 Movie Dataset")
st.dataframe(filtered_df, use_container_width=True)