import pandas as pd
import streamlit as st
import pickle
import requests


# Load movies
movies = pickle.load(open('movies.pkl', 'rb'))

# Movie titles for dropdown
movies_list = movies['title'].values


# Load precomputed recommendations
recommendations = pickle.load(open('recommendations.pkl', 'rb'))


def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]

    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    )

    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):

    # Find index of selected movie
    movie_index = movies[movies['title'] == movie].index[0]

    # Get precomputed top 5 similar movie indices
    movie_indices = recommendations[movie_index]

    recommended_movies = []
    recommended_movies_posters = []

    for index in movie_indices:

        # TMDB movie ID
        movie_id = movies.iloc[index].movie_id

        # Movie title
        recommended_movies.append(
            movies.iloc[index].title
        )

        # Poster
        recommended_movies_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_movies_posters


st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'How would you like to search?',
    movies_list
)


if st.button('Recommend'):

    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])