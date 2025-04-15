import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from src.init_supabase import supabase
from scraping import update_player_stats
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER, POR_ID, NED_ID, BELG_ID, SCOT_ID, ENG2_ID, SAUDI_ID, BRAZIL_ID



st.title("Page for Scraping Players Current Season Stats")

st.subheader("EPL Players")
if st.button("Button for EPL Scraping Current Seasons Stats"):
    update_player_stats(ENG_ID)

st.subheader("ESP Players")
if st.button("Button ESP for Scraping Current Seasons Stats"):
    update_player_stats(ESP_ID)

st.subheader("ITA Players")
if st.button("Button ITA for Scraping Current Seasons Stats"):
    update_player_stats(ITA_ID)

st.subheader("GER Players")
if st.button("Button GER for Scraping Current Seasons Stats"):
    update_player_stats(GER_ID)

st.subheader("POR Players")
if st.button("Button POR for Scraping Current Seasons Stats"):
    update_player_stats(POR_ID)

st.subheader("TURKEY Players")
if st.button("Button TURKEY for Scraping Current Seasons Stats"):
    update_player_stats(TURKEY_ID)

st.subheader("ENG2 Players")
if st.button("Button ENG2 for Scraping Current Seasons Stats"):
    update_player_stats(ENG2_ID)

st.subheader("BELG Players")
if st.button("Button BELG for Scraping Current Seasons Stats"):
    update_player_stats(BELG_ID)

st.subheader("NED Players")
if st.button("Button NED for Scraping Current Seasons Stats"):
    update_player_stats(NED_ID)

st.subheader("Saudi Players")
if st.button("Button Saudi for Scraping Current Seasons Stats"):
    update_player_stats(SAUDI_ID)

st.subheader("SCOT Players")
if st.button("Button SCOT for Scraping Current Seasons Stats"):
    # get the IDS and Transfm URL of a League's Temas
    # team_ids = get_ids_stats_url(ESP_ID)
    update_player_stats(SCOT_ID)

st.subheader("BRAZIL Players")
if st.button("Button BRAZIL for Scraping Current Seasons Stats"):
    # get the IDS and Transfm URL of a League's Temas
    # team_ids = get_ids_stats_url(ESP_ID)
    update_player_stats(BRAZIL_ID)

