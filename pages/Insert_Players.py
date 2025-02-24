import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from src.init_supabase import supabase
from scraping import get_soup, update_league, insert_league, extract_numeric_value, extract_height_value, get_team_players, transform_url_transfm_all_players
from datetime import datetime
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER, POR_ID, NED_ID, BELG_ID, SCOT_ID, ENG2_ID




st.title("Page for Inserting Players of Teams from Transfm")

st.subheader("EPL Players")

if st.button("Insert Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ENG_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        # very important for the current season
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")



if st.button("UPDATE Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ENG_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

if st.button("Insert ENG2 Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ENG2_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        # very important for the current season
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")



if st.button("UPDATE ENG2 Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ENG2_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")


st.subheader("Bundesliga Players")

if st.button("Insert GER Players from Transfm"):
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", GER_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE GER Players from Transfm"):
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", GER_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")


st.subheader("La Liga Players")

if st.button("Insert ESP Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ESP_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE ESP Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ESP_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

st.subheader("Seria A Players")

if st.button("Insert ITA Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ITA_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE ITA Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ITA_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

st.subheader("Ligue1 Players")

if st.button("Insert FRA Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", FRA_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE FRA Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", FRA_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

st.subheader("Liga Portugal Players")

if st.button("Insert POR Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", POR_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE POR Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", POR_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

st.subheader("Eredevise Players")

if st.button("Insert NED Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", NED_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE NED Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", NED_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

st.subheader("Belgium Players")

if st.button("Insert BELG Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", BELG_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE BELG Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", BELG_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")

st.subheader("Scotland Players")

if st.button("Insert SCOT Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", SCOT_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "insert")

if st.button("UPDATE SCOT Players from Transfm"):
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", SCOT_ID).execute()

    for i in epl_teams.data:
        team_id = i["team_id"]
        transfm_url= i["transfm_season_url"]
        transfm_url = transform_url_transfm_all_players(transfm_url)

        get_team_players(team_id, transfm_url, "update")