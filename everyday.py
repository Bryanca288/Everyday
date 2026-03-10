import streamlit as st
from datetime import date
import calendar
import random

# Session state
if "notes_by_date" not in st.session_state:
    st.session_state.notes_by_date = {}
    st.session_state.selected_date = date.today()

# SIDEBAR
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

# MAIN TITLE
st.title("📔 Everyday Notes")

# CALENDAR
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

# NOTES AREA
st.subheader(f"Notes for {st.session_state.selected_date}")

note = st.text_area("Write your note")

if st.button("Save Note"):
    st.session_state.notes_by_date[str(st.session_state.selected_date)] = note
    st.success("Saved!")

# SHOW SAVED NOTE
saved = st.session_state.notes_by_date.get(str(st.session_state.selected_date))

if saved:
    st.write("### Saved Note")
    st.write(saved)

# RESET
if st.button("Reset All Notes"):
    st.session_state.notes_by_date = {}
    st.success("All notes deleted")