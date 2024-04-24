import pandas as pd
import streamlit as st
import pickle
# a library used to hit API key
import requests

#Fetchin the poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=347ed71981148933a4820faa8b838ab6&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # geeting the index
    distances = similarity[movie_index]  # getting the distance
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    # Print the list of those 5 movies
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id # this is the id

        # appending the titles of the top 5 movies in the recommended_movies
        recommended_movies.append(movies.iloc[i[0]].title)


        # callin the fetch poster fucntion ad asaving it in recommended_movies_posters
        # fetch poster from  API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
# rb stands for read binary
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title("Movie Recommender System")


# fetching the movie name
selected_movie_name = st.selectbox(
    'How wo?',
    movies['title'].values)



# creating a button which when clicked our website will return 5 most common movies
if st.button("Recommend"):
    names , posters = recommend(selected_movie_name) # calling the function recomend to get the movies

    # col1, col2, col3, col4, col5 = st.columns(5)

    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])
    num_cols = 5  # Number of columns to display
    cols = st.columns(num_cols)

    # Zip the names and posters into a single list of tuples
    movie_data = list(zip(names, posters))

    # Iterate over the movie data and assign each item to a column
    for col_idx, (movie_name, poster_url) in enumerate(movie_data):
        with cols[col_idx % num_cols]:
            st.text(movie_name)
            st.image(poster_url)