import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from datetime import datetime
from src.init_supabase import supabase
from scraping import insert_team_past_stats, update_team_past_players, insert_team_past_players, update_curr_stats, update_or_insert_teams_current_players
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER, POR_ID, NED_ID, BELG_ID, SCOT_ID, ENG2_ID, SAUDI_ID

year = 2023

transfm_head = "https://www.transfermarkt.com/"

st.title("Scraping Past Squads while going into Player Bio Page to see if retired and get more info")

st.subheader("FOR UPDATING RETIRED COLUMN OF ALL PLAYERS SINCE I DID IT WRONG THE FIRST TIME")
if st.button("Button for Updating Team's past players + RETIRED PLAYERS"):
    #name = "Casemiro"
    team_name = "Inter"
    teams = ["Man Utd", "Tottenham", "Bayern Munich", "Inter", "Liverpool", "West Ham"]

    for i in teams:
        update_team_past_players(i)

st.write("---------------------------")

st.subheader("Insert Team's past players into PLAYERS table")
if st.button("Button for INSERTING Team's past PLAYERS into players table"):
    #name = "Casemiro"
    team_name = "Real Madrid"
    teams = ["Real Betis", "Sevilla FC", "Real Sociedad", "B. Leverkusen", "Everton"]
    teams = ["Lazio", "Leicester", "LOSC Lille", "Monaco"]


    for i in teams:
        insert_team_past_players(i)

st.subheader("INSERT Teams previous year Players Stats into PLAYER_STATS table")
if st.button("Button for INSERTING Team's past PLAYER stats into player_stats table"):
    #name = "Casemiro"
    team_name = "Real Madrid"
    teams = ["Real Madrid", "Barcelona", "Man Utd", "Man City", "Arsenal", "Paris SG", "Chelsea", "FC Porto", "Benfica", "Liverpool", "Tottenham", "AC Milan", "Juventus", "Inter"]
    teams = ["Lazio", "Leicester", "LOSC Lille", "Monaco"]


    for i in teams:
        insert_team_past_stats(i)

st.write("---------------------------")

st.header("FOR player_stats TABLE")
st.subheader("Update or Insert player_stats table with CURRENT Season All Comps G/A")
st.write("Use this for first inserting the player into player_stats table")
if st.button("Button for Inserting current G/A of this season"):
    team_name = "Real Madrid"

    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_name").eq("league_id", 1).execute()

    for i in epl_teams.data:
        team_name = i["team_name"]
        update_curr_stats(team_name, "insert")

st.write("After the players are inserted in player_stats table you can now update them")
if st.button("Button for UPDATING player_stats table with current G/A of this season"):
    team_name = "Real Madrid"
    # REPLACE LEAGUE ID 
    epl_teams = supabase.table("teams").select("team_name").eq("league_id", 7).execute()

    for i in epl_teams.data:
        team_name = i["team_name"]
        update_curr_stats(team_name, "update")


st.write("---------------------------")

st.header("FOR players TABLE")
st.subheader("Update or Insert players table with NEW Player's Bio data of a Team (current season)")
st.write("Goes to Transfm Current season page of the team and updates Players Bio info into players table, if Player DNE then it inserts them in the players table with Bio info")
if st.button("Button for Update/Insert curr players"):
    team_name = "Brighton"

    epl_teams = supabase.table("teams").select("team_name").eq("league_id", 20).execute()

    for i in epl_teams.data:
        team_name = i["team_name"]
        update_or_insert_teams_current_players(team_name)



