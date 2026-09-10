import pickle
import requests
import streamlit as st

# ============================================================
# EXISTING BACKEND - DO NOT CHANGE
# ============================================================

movies = pickle.load(open("movies.pkl", "rb"))
movies_list = movies["title"].values
recommendations = pickle.load(open("recommendations.pkl", "rb"))


def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]

    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={api_key}&language=en-US",
        timeout=10,
    )

    data = response.json()

    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    movie_indices = recommendations[movie_index]

    recommended_movies = []
    recommended_movies_posters = []

    for index in movie_indices:
        movie_id = movies.iloc[index].movie_id
        recommended_movies.append(movies.iloc[index].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="CineSphere",
    page_icon="🎞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "result" not in st.session_state:
    st.session_state.result = None


# ============================================================
# CSS ONLY
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap');

:root {
    --bg: #050707;
    --text: #eee7da;
    --muted: #96938c;
    --gold: #d2bd99;
    --line: rgba(238,231,218,.16);
}

.stApp {
    background: #050707;
}

.block-container {
    max-width: 1400px;
    padding: 0 3.1rem 1rem;
}

header[data-testid="stHeader"] {
    background: #050707;
}

/* Header */
.cine-header {
    position: absolute !important;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 50;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

.cine-brand {
    display: flex;
    align-items: center;
    white-space: nowrap;
}

.cine-logo {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.55rem;
    letter-spacing: -.035em;
}

.cine-divider {
    width: 1px;
    height: 23px;
    background: rgba(238,231,218,.28);
    margin: 0 16px;
}

.cine-sub {
    color: #8e8b84;
    font-size: .62rem;
    letter-spacing: .28em;
}

.cine-nav {
    display: flex;
    gap: 36px;
    color: #99968f;
    font-size: .82rem;
}

.cine-nav .active {
    color: var(--gold);
    padding-bottom: 13px;
    border-bottom: 1px solid var(--gold);
}

/* Hero */
.cine-hero {
    height: 455px;
    margin: 0 -3.1rem;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: var(--text);
    overflow: hidden;
    border-bottom: 1px solid var(--line);
    background:
        linear-gradient(
            rgba(3,5,5,.58),
            rgba(3,5,5,.58)
        ),
        url("https://primepix.in/storage/media/theaterimag-1-1783318889-wtFCD.jpeg");
    background-size: cover;
    background-position: center;
}

.cine-hero-inner {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    transform: translateY(-25px);
}

.cine-eyebrow {
    color: #b7b1a6;
    font: .63rem 'DM Sans', sans-serif;
    letter-spacing: .34em;
    text-transform: uppercase;
    margin-bottom: 17px;
}

.cine-title {
    font: 500 clamp(3.2rem,5vw,5.3rem)/.92 'Playfair Display', Georgia, serif;
    letter-spacing: -.052em;
    margin-bottom: 20px;
}

.cine-title em {
    color: #e0d1b8;
}

.cine-copy {
    color: #d0cbc2;
    font: 1.03rem 'Playfair Display', Georgia, serif;
}

/* Put the real Streamlit controls over the lower part of the hero. */
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) {
    width: min(650px, 100%);
    margin: -87px auto 0 !important;
    position: relative;
    z-index: 10;
    align-items: center;
}

div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) > div {
    padding-top: 0 !important;
}

/* Selector */
div[data-testid="stSelectbox"] {
    margin: 0 !important;
}

div[data-testid="stSelectbox"] label {
    display: none;
}

div[data-baseweb="select"] {
    margin: 0 !important;
}

div[data-baseweb="select"] > div {
    min-height: 56px;
    background: rgba(6,10,10,.88);
    border: 1px solid rgba(238,231,218,.55);
    border-radius: 999px;
    padding-left: 16px;
    box-shadow: none;
}

div[data-baseweb="select"] > div:hover {
    border-color: rgba(238,231,218,.78);
}

div[data-baseweb="select"] * {
    color: var(--text) !important;
}

/* Recommend */
div[data-testid="stButton"] {
    margin-top: 0 !important;
}

div[data-testid="stButton"] > button {
    min-height: 56px;
    width: 100%;
    border-radius: 999px;
    border: 1px solid rgba(210,189,153,.72);
    background: var(--gold);
    color: #111;
    font: 600 .85rem 'DM Sans', sans-serif;
}

div[data-testid="stButton"] > button:hover {
    background: #e2d1b2;
    border-color: #eadcc5;
}

/* Results */
.results-shell {
    padding-top: 46px;
}

.results-heading {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 21px;
    font-family: 'DM Sans', sans-serif;
}

.results-title {
    color: var(--text);
    font-size: .66rem;
    letter-spacing: .34em;
    text-transform: uppercase;
    white-space: nowrap;
}

.results-line {
    height: 1px;
    background: var(--line);
    flex: 1;
}

.results-tag {
    color: #a19d95;
    font: italic .83rem 'Playfair Display', Georgia, serif;
    white-space: nowrap;
}

.poster img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid rgba(238,231,218,.12);
    display: block;
    transition: transform .25s ease, filter .25s ease;
}

.poster img:hover {
    transform: translateY(-3px);
    filter: brightness(1.06);
}

.poster-title {
    color: var(--text);
    text-align: center;
    margin-top: 10px;
    font: .91rem/1.2 'Playfair Display', Georgia, serif;
}

/* Footer */
.footer {
    margin-top: 34px;
    padding: 22px 0 4px;
    border-top: 1px solid var(--line);
    display: flex;
    justify-content: space-between;
    color: #797872;
    font: .69rem 'DM Sans', sans-serif;
}

.footer-brand {
    color: var(--text);
    font: 1rem 'Playfair Display', Georgia, serif;
}

.footer-right {
    color: #9a958b;
    font: italic .82rem 'Playfair Display', Georgia, serif;
}

[data-testid="stToolbar"],
#MainMenu,
footer {
    visibility: hidden;
}

/* Shorter screen = tighter composition */
@media (max-height: 850px) and (min-width: 901px) {
    .cine-hero {
        height: 405px;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) {
        margin-top: -78px !important;
    }

    .results-shell {
        padding-top: 34px;
    }

    .poster img {
        max-height: 310px;
    }
}

/* Mobile */
@media (max-width: 900px) {
    .block-container {
        padding: 0 1.15rem 1rem;
    }

    .cine-header {
        margin-left: -1.15rem;
        margin-right: -1.15rem;
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }

    .cine-sub,
    .cine-divider,
    .cine-nav {
        display: none;
    }

    .cine-hero {
        margin-left: -1.15rem;
        margin-right: -1.15rem;
        height: 510px;
    }

    .cine-title {
        font-size: 3rem;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) {
        width: 100%;
        margin-top: -105px !important;
        flex-direction: column;
    }

    .results-heading {
        flex-wrap: wrap;
    }

    .results-tag {
        width: 100%;
    }

    .footer {
        flex-direction: column;
        gap: 14px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# STATIC HEADER - st.html, NOT markdown
# ============================================================

st.html(
    """
    <div class="cine-header">
        <div class="cine-brand">
            <span class="cine-logo">CineSphere</span>
            <span class="cine-divider"></span>
            <span class="cine-sub">FIND MOVIES THAT FEEL LIKE YOU</span>
        </div>

        <div class="cine-nav">
            <span class="active">Home</span>
            <span>About</span>
            <span>GitHub</span>
        </div>
    </div>
    """
)


# ============================================================
# INITIAL VIEW
# ============================================================

if st.session_state.result is None:

    st.html(
        """
        <section class="cine-hero">
            <div class="cine-hero-inner">
                <div class="cine-eyebrow">
                    A MOVIE RECOMMENDER SYSTEM
                </div>

                <div class="cine-title">
                    For the stories<br>
                    <em>you'll love next</em>
                </div>

                <div class="cine-copy">
                    Pick a movie you like, and let's find your next favorite.
                </div>
            </div>
        </section>
        """
    )

    left, right = st.columns([4.1, 1.15], gap="small")

    with left:
        selected_movie_name = st.selectbox(
            "Select a movie",
            movies_list,
            label_visibility="collapsed",
        )

    with right:
        recommend_clicked = st.button(
            "Recommend  →",
            use_container_width=True,
        )

    if recommend_clicked:
        with st.spinner("Finding similar movies..."):
            names, posters = recommend(selected_movie_name)

        st.session_state.result = {
            "movie": selected_movie_name,
            "names": names,
            "posters": posters,
        }

        st.rerun()


# ============================================================
# RESULTS VIEW
# ============================================================

else:

    result = st.session_state.result

    st.html(
        f"""
        <div class="results-shell">
            <div class="results-heading">
                <span class="results-title">
                    Recommendations for {result["movie"]}
                </span>

                <span class="results-line"></span>

                <span class="results-tag">
                    Similar stories. A wider you.
                </span>
            </div>
        </div>
        """
    )

    cols = st.columns(5, gap="medium")

    for col, name, poster in zip(
        cols,
        result["names"],
        result["posters"],
    ):
        with col:
            st.html(
                f"""
                <div class="poster">
                    <img src="{poster}" alt="{name}">
                    <div class="poster-title">{name}</div>
                </div>
                """
            )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        <div>
            <span class="footer-brand">CineSphere</span>
            <span style="
                margin-left:14px;
                padding-left:14px;
                border-left:1px solid rgba(238,231,218,.20);
            ">
                Built with Python + Streamlit
            </span>
        </div>

        <div class="footer-right">
            Same movies. A wider you.
        </div>
    </div>
    """
)
