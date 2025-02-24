import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from src.init_supabase import supabase
from scraping import get_soup, update_league, insert_league, extract_numeric_value, extract_height_value, get_team_players, transform_url_transfm_all_players
from datetime import datetime
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER


st.title("Manaully Search players table for duplicate names")

st.subheader("Search full portion of a Player's name")
txt = st.text_area(
    "",
)

st.write(f"You wrote {txt}")

response = supabase.from_('players').select().text_search('player_name', txt).execute()

st.write(response)

st.subheader("Partially search for a Player's name")
txt2 = st.text_area(key=99, value="xxxx", label="Partial search")

st.write(f"You wrote {txt}")

resp = supabase.table("players").select("*").ilike("player_name", f"%{txt2}%").execute()

st.write(resp)