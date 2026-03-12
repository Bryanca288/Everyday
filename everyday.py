import streamlit as st
from datetime import date
import calendar
import random

# ---------------- BACKGROUND SELECTOR ----------------
bg_choice = st.sidebar.selectbox(
    "🎨 Choose Background",
    ["Minecraft","Galaxy","Mario","Heaven","Spiderman","Emerald","Diamond","Anime"]
)

backgrounds = {
    "Minecraft": "https://wallpapers.com/images/hd/minecraft-grass-block-texture-1920x1080.jpg",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564",
    "Mario": "https://wallpapers.com/images/hd/super-mario-bros-background-1920x1080.jpg",
    "Heaven": "https://images.unsplash.com/photo-1502082553048-f009c37129b9",
    "Spiderman": "https://wallpapers.com/images/hd/spiderman-4k-background.jpg",
    "Emerald": "https://images.unsplash.com/photo-1524678606370-a47ad25cb82a",
    "Diamond": "https://images.unsplash.com/photo-1603570419981-0c0f7f29d0e2",
    "Anime": "https://wallpapers.com/images/hd/anime-landscape-1920x1080.jpg"
}

bg_url = backgrounds[bg_choice]

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stTextArea textarea {{
        background-color: rgba(255,255,255,0.85);
    }}
    .stButton button {{
        background-color: rgba(0,0,0,0.6);
        color: white;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "notes_by_date" not in st.session_state:
    st.session_state.notes_by_date = {}
    st.session_state.selected_date = date.today()

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.image(
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438",
        use_container_width=True
    )

    st.title("🎮 Mini Games")

    game = st.selectbox("Choose Game", ["Guess the Number", "Rock Paper Scissors"])

    # -------- GAME 1 --------
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

    # -------- GAME 2 --------
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

    # ---------------- HOLIDAY LIST ----------------
    st.markdown("---")
    st.subheader("🎉 Holiday List")

    holidays = {
        "Jan 1": "New Year's Day",
        "Feb 25": "EDSA People Power Revolution",
        "Apr 9": "Araw ng Kagitingan",
        "May 1": "Labor Day",
        "Jun 12": "Independence Day",
        "Aug 21": "Ninoy Aquino Day",
        "Aug (Last Mon)": "National Heroes Day",
        "Nov 1": "All Saints' Day",
        "Nov 30": "Bonifacio Day",
        "Dec 25": "Christmas Day",
        "Dec 30": "Rizal Day"
    }

    for day, name in holidays.items():
        st.write(f"📅 **{day}** - {name}")

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
    st.session_state.notes_by_date[str(st.session_state.selected_date)] = note
    st.success("Saved!")

# ---------------- SHOW SAVED NOTE ----------------
saved = st.session_state.notes_by_date.get(str(st.session_state.selected_date))

if saved:
    st.write("### Saved Note")
    st.write(saved)

# ---------------- RESET ----------------
if st.button("Reset All Notes"):
    st.session_state.notes_by_date = {}
    st.success("All notes deleted")