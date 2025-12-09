import streamlit as st
import pickle
import pandas as pd
import requests

# ------------------ Recommendation function ------------------

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

# ------------------ Poster function (OMDB) ------------------

def fetch_poster(movie_name):
    api_key = "f59994c4"   # ✅ NO SPACE
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    data = requests.get(url).json()

    if data.get('Response') == 'True':
        return data.get('Poster')
    else:
        return None

# ------------------ Load data ------------------

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------ Streamlit UI ------------------

st.title('🎬 Movie Recommender System')

option = st.selectbox(
    'Select a movie you like',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(option)

    cols = st.columns(5)
    for col, movie in zip(cols, recommendations):
        poster = fetch_poster(movie)
        with col:
            if poster:
                st.image(poster)
            st.caption(movie)
