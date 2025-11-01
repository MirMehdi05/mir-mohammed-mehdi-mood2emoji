# app.py
import streamlit as st
from textblob import TextBlob
import re

st.set_page_config(page_title="Mood2Emoji", page_icon="🙂", layout="centered")

PROFANITY = {"badword1", "badword2", "uglyword"}

def contains_profanity(text):
    text_lower = text.lower()
    for p in PROFANITY:
        if re.search(rf"\b{re.escape(p)}\b", text_lower):
            return True
    return False

def analyze_mood(text):
    if contains_profanity(text):
        return "neutral", "Contains inappropriate language — cannot display mood."
    stripped = text.strip()
    if len(stripped) == 0:
        return "neutral", "No text entered."
    blob = TextBlob(stripped)
    polarity = blob.sentiment.polarity
    if polarity > 0.15:
        return "happy", "Sounds happy!"
    elif polarity < -0.15:
        return "sad", "Sounds sad."
    else:
        return "neutral", "Sounds neutral or unclear."

EMOJI = {"happy": "😀", "neutral": "😐", "sad": "😞"}

st.title("Mood2Emoji — Kid-safe Text Mood Detector")
st.markdown("Type a short sentence. The app returns a kid-friendly emoji and short explanation.")

with st.form("mood_form"):
    user_text = st.text_input("Enter a short sentence:", max_chars=200)
    teacher_mode = st.checkbox("Teacher Mode (show simple diagram)", value=False)
    submitted = st.form_submit_button("Detect Mood")

if submitted:
    mood, explanation = analyze_mood(user_text)
    emoji = EMOJI.get(mood, EMOJI["neutral"])
    st.markdown("### Result")
    st.markdown(f"<div style='font-size:48px'>{emoji}</div>", unsafe_allow_html=True)
    st.write(explanation)

if teacher_mode:
    diagram = """
[User types sentence] --> [Safety check: profanity?] --> if bad => [Neutral fallback/explain]
                                     |
                                     v
                             [TextBlob sentiment]
                              /      |        \
                        polarity>0.15 neutral  polarity<-0.15
                          |          |             |
                         😀         😐            😞
                     "Sounds happy" "Neutral" "Sounds sad"
"""
    st.code(diagram, language="text")

st.caption("Built with Streamlit + TextBlob — kid-safe and educational.")
