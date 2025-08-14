# thanks to https://github.com/nmcassa/letterboxdpy/tree/main
from letterboxdpy.watchlist import Watchlist
from letterboxdpy.movie import Movie
import streamlit as st

st.set_page_config(layout="wide")


@st.cache_data
def get_watchlist(username: str):
    return Watchlist(username).get_movies()


st.markdown("""
<style>
.movie-card {
    height: 340px; /* Adjust for poster + text height */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    text-align: center;
    padding: 5px;
}
.movie-poster {
    width: 100%;
    border-radius: 8px;
    object-fit: cover;
    height: 250px; /* fixed poster height */
}
.movie-title {
    display: block;
    margin-top: 6px;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}
.movie-year {
    color: gray;
    font-size: 0.9em;
}
</style>
""", unsafe_allow_html=True)

st.title("letterboxd watchlist overlap tool")
st.text("by ish444n")

usernameStr = st.text_input("enter public letterboxd usernames (comma-separated)",
                            placeholder="username1, username2, etc")

if st.button("find overlap"):
    usernames = [u.strip() for u in usernameStr.split(",")]
    if len(usernames) < 2:
        st.error("at least two usernames, please")
    else:
        progress_text = st.empty()
        progress_bar = st.progress(0)
        with st.spinner("fetching watchlists..."):
            watchlists = [get_watchlist(u) for u in usernames]

        overlap = sorted(set.intersection(*(set(w.keys()) for w in watchlists)))

        if overlap:
            st.subheader("movies on all watchlists:")
            st.text("click on a poster to go to its letterboxd page")
            progress_text.text("displaying movies...")
            progress_bar.progress(0)
            cols_per_row = min(7, len(overlap))
            cols = st.columns(cols_per_row)
            num_overlap = len(overlap)
            for i, idx in enumerate(overlap, start=0):
                movie = Movie(watchlists[0][idx]["slug"])
                col = cols[i % cols_per_row]
                col.markdown(
                    f"""
                    <div class="movie-card">
                        <a href="https://letterboxd.com/film/{movie.slug}/" target="_blank">
                            <img src="{movie.poster}" class="movie-poster">
                        </a>
                        <span class="movie-title">{movie.title}</span>
                        <span class="movie-year">({movie.year})</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if num_overlap > 1:
                    progress = i / (num_overlap - 1)
                    progress_bar.progress(progress)
                    progress_text.text(f"{int(progress * 100)}% — {movie.title}")
                else:
                    percent = 100
                    progress_bar.progress(1.0)
                    progress_text.text(f"100% — {movie.title}")

            progress_bar.progress(1.0)
            progress_text.text("all movies displayed :)")

        else:
            st.info("no common movies found :(")
