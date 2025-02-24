import streamlit as st
import sys, random, json, re, os
sys.path.append("src")

st.title("How to Update a Leagues Teams with ESPN")

st.write("Go to ESPN (https://www.espn.com/soccer/teams/_/league/ENG.1/english-premier-league) and copy the HTML element of the clubs to extract the names and Image URLS")

txt = st.text_area(
    "",
)

st.write(f"You wrote {len(txt)} characters.")


code = '''
[
  {
    "team": "Adana Demirspor",
    "image_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/20765.png&scale=crop&cquality=40&location=origin&w=80&h=80"
  },
]

'''
st.code(code, language=None)
st.write(f"epl.json")

st.write(f"BEFORE using the epl.json, make sure that the team names correspond to the ones on Transfm to AVOID DUPLICATE TEAMS")
