import streamlit as st
from datetime import date
import calendar
import random
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("notes_app.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS notes(
username TEXT,
date TEXT,
note TEXT
)
""")

conn.commit()

# ---------------- LOGIN SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SIDEBAR LOGIN ----------------
st.sidebar.title("🔐 Account")

menu = st.sidebar.selectbox("Account", ["Login", "Register", "Logout"])

if menu == "Register":

    new_user = st.sidebar.text_input("Username")
    new_pass = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Create Account"):
        try:
            c.execute("INSERT INTO users VALUES (?,?)", (new_user, new_pass))
            conn.commit()
            st.sidebar.success("Account created!")
        except:
            st.sidebar.error("User already exists")

elif menu == "Login":

    user = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, password))
        result = c.fetchone()

        if result:
            st.session_state.user = user
            st.sidebar.success("Logged in!")
        else:
            st.sidebar.error("Invalid login")

elif menu == "Logout":
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.sidebar.success("Logged out")

# STOP APP IF NOT LOGGED IN
if st.session_state.user is None:
    st.title("🔐 Please Login First")
    st.stop()

# ---------------- BACKGROUND SELECTOR ----------------
bg_choice = st.sidebar.selectbox(
    "🎨 Choose Background",
    ["Minecraft","Galaxy","Mario","Heaven","Spiderman","Emerald","Diamond","Anime"]
)

backgrounds = {
    "Minecraft": "https://wallpapercave.com/wp/wp5022404.jpg",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564",
    "Mario": "https://4kwallpapers.com/images/walls/thumbs_3t/23948.jpg",
    "Heaven": "https://w.wallhaven.cc/full/m3/wallhaven-m3d3oy.jpg",
    "Spiderman": "https://4kwallpapers.com/images/walls/thumbs_2t/11476.png",
    "Emerald": "https://images.unsplash.com/photo-1524678606370-a47ad25cb82a",
    "Diamond": "https://wallpaperaccess.com/full/175847.jpg",
    "Anime": "https://images8.alphacoders.com/131/thumbbig-1314408.webp"
}

bg_url = backgrounds[bg_choice]

# ---------------- STYLE ----------------
st.markdown(
    f"""
<style>

.stApp {{
background-image: url("{bg_url}");
background-size: cover;
background-attachment: fixed;
}}

h1, h2, h3 {{
color: black;
text-shadow: 1px 1px 2px white;
}}

p, span, label {{
color: black;
}}

.stTextArea textarea {{
background-color: rgba(255,255,255,0.9);
color: black;
border-radius: 10px;
}}

section[data-testid="stSidebar"] {{
background-color: rgba(255,255,255,0.8);
}}

</style>
""",
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.image(
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438",
        use_container_width=True
    )

    st.title("🎮 Mini Games")

    game = st.selectbox("Choose Game", ["Guess the Number", "Rock Paper Scissors"])

    # GAME 1
    if game == "Guess the Number":

        if "number" not in st.session_state:
            st.session_state.number = random.randint(1, 10)

        guess = st.number_input("Guess 1-10", 1, 10)

        if st.button("Check"):
            if guess == st.session_state.number:
                st.success("🎉 Correct!")
                st.session_state.number = random.randint(1, 10)
            elif guess < st.session_state.number:
                st.warning("Too low")
            else:
                st.warning("Too high")

    # GAME 2
    if game == "Rock Paper Scissors":

        choice = st.selectbox("Your move", ["Rock", "Paper", "Scissors"])

        if st.button("Play"):
            bot = random.choice(["Rock", "Paper", "Scissors"])
            st.write("Bot:", bot)

            if choice == bot:
                st.info("Draw")
            elif (
                (choice == "Rock" and bot == "Scissors")
                or (choice == "Paper" and bot == "Rock")
                or (choice == "Scissors" and bot == "Paper")
            ):
                st.success("You win!")
            else:
                st.error("You lose!")

# ---------------- MAIN APP ----------------
st.title("📔 Everyday Notes")

# ---------------- CALENDAR ----------------
st.subheader("📅 Calendar")

month = st.session_state.selected_date.month
year = st.session_state.selected_date.year

cal = calendar.monthcalendar(year, month)

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

cols = st.columns(7)
for i, d in enumerate(days):
    cols[i].caption(d)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            if cols[i].button(str(day), key=f"day{day}"):
                st.session_state.selected_date = date(year, month, day)

# ---------------- NOTES AREA ----------------
st.subheader(f"Notes for {st.session_state.selected_date}")

note = st.text_area("Write your note")

if st.button("Save Note"):

    c.execute(
        "INSERT OR REPLACE INTO notes VALUES (?,?,?)",
        (st.session_state.user, str(st.session_state.selected_date), note)
    )

    conn.commit()
    st.success("Saved!")

# ---------------- SHOW SAVED NOTE ----------------
c.execute(
    "SELECT note FROM notes WHERE username=? AND date=?",
    (st.session_state.user, str(st.session_state.selected_date))
)

saved = c.fetchone()

if saved:
    st.write("### Saved Note")
    st.write(saved[0])

# ---------------- ALL NOTES VIEW ----------------
st.subheader("📜 All Your Notes")

c.execute(
    "SELECT date, note FROM notes WHERE username=? ORDER BY date DESC",
    (st.session_state.user,)
)

rows = c.fetchall()

for r in rows:
    st.write(f"📅 {r[0]}")
    st.write(r[1])
    st.markdown("---")

# ---------------- RESET ----------------
if st.button("Reset All Notes"):
    c.execute("DELETE FROM notes WHERE username=?", (st.session_state.user,))
    conn.commit()
    st.success("All notes deleted")