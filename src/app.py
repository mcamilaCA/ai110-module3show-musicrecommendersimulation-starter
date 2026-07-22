"""
Streamlit web app for the Music Recommender Simulation.

Wraps recommender.py in an interactive UI: the user builds a taste profile
with widgets in the sidebar, and gets ranked song recommendations with a
per-feature score breakdown, without touching any code.

Run with:
    streamlit run src/app.py
"""

import os

import streamlit as st

from recommender import recommend_songs

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def score_color(score):
    if score > 80:
        return "green"
    if score < 40:
        return "red"
    return "yellow"


@st.cache_data
def get_songs():
    from recommender import load_songs

    return load_songs(DATA_PATH)


def unique_sorted(songs, field):
    return sorted({song[field] for song in songs if song.get(field)})


st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="centered")

songs = get_songs()

st.title("🎵 Music Recommender")
st.caption("Tell us what you like and we'll rank the catalog for you.")

genres = unique_sorted(songs, "genre")
moods = unique_sorted(songs, "mood")
decades = unique_sorted(songs, "release_decade")

with st.sidebar, st.form("profile_form", border=True):
    st.header("Your taste profile")

    genre = st.selectbox("Favorite genre", genres)
    mood = st.selectbox("Favorite mood", moods)
    energy = st.slider("Energy", 0.0, 1.0, 0.7, 0.05)
    acoustic_choice = st.segmented_control(
        "Do you like acoustic songs?", ["Yes", "No"], default="Yes", required=True
    )

    st.subheader("Optional preferences")
    decade_choice = st.selectbox("Preferred decade", ["Any"] + decades)
    instrumental_choice = st.segmented_control(
        "Instrumental tracks?", ["Any", "Yes", "No"], default="Any", required=True
    )
    clean_only_choice = st.segmented_control(
        "Clean lyrics only?", ["Any", "Yes", "No"], default="Any", required=True
    )
    prefer_popular_choice = st.segmented_control(
        "Prefer popular songs?", ["Any", "Yes", "No"], default="Any", required=True
    )
    danceability = st.slider("Preferred danceability (tie-breaker)", 0.0, 1.0, 0.5, 0.05)

    k = st.slider("How many recommendations?", 1, min(10, len(songs)), 5)

    submitted = st.form_submit_button("Get recommendations", width="stretch")

if submitted:
    st.session_state.user_prefs = {
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "likes_acoustic": acoustic_choice == "Yes",
        "preferred_decade": None if decade_choice == "Any" else decade_choice,
        "wants_instrumental": {"Any": None, "Yes": True, "No": False}[instrumental_choice],
        "clean_only": clean_only_choice == "Yes",
        "prefer_popular": prefer_popular_choice == "Yes",
        "danceability": danceability,
        "k": k,
    }

if "user_prefs" not in st.session_state:
    st.info("Set your preferences in the sidebar and click **Get recommendations** to see your matches.")
else:
    prefs = st.session_state.user_prefs

    st.subheader("Your profile")
    st.write(
        f"**Genre:** {prefs['genre']} · **Mood:** {prefs['mood']} · **Energy:** {prefs['energy']} · "
        f"**Acoustic:** {'Yes' if prefs['likes_acoustic'] else 'No'} · "
        f"**Decade:** {prefs['preferred_decade'] or 'Any'} · "
        f"**Instrumental:** {'Any' if prefs['wants_instrumental'] is None else ('Yes' if prefs['wants_instrumental'] else 'No')} · "
        f"**Clean only:** {'Yes' if prefs['clean_only'] else 'Any'} · "
        f"**Prefer popular:** {'Yes' if prefs['prefer_popular'] else 'Any'}"
    )

    recommendations = recommend_songs(prefs, songs, k=prefs["k"])

    st.subheader("🎧 Top recommendations")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        medal = MEDALS.get(rank, "🎶")
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{medal} #{rank} — {song['title']}** by {song['artist']}")
            with col2:
                st.metric("Score", f":{score_color(score)}[{score:.2f}%]")
            with st.expander("Why this song?"):
                st.code(explanation.strip(), language=None)

    if not recommendations:
        st.info("No songs matched your filters. Try relaxing 'Clean lyrics only' or your decade preference.")
