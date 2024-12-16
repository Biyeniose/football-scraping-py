import streamlit as st
import sys, random, json
sys.path.append("src")
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
from insert_functions import insert_player, get_gb
import pandas as pd
from scraping import get_soup, get_page_trs, should_keep_tr, extract_player_jsons


def fetch_table(table_name):
    try:
        response = supabase.table(table_name).select("*").execute()
    except Exception as e:
        st.error(f"Error fetching {e}")
        return []
    return response.data

# Fetch leagues
def fetch_leagues():
    leagues = fetch_table("leagues")
    return {league["league_id"]: league["league_name"] for league in leagues}

# Fetch teams based on selected league
def fetch_teams(league_id):
    try:
        response = supabase.table("teams").select("*").eq("league_id", league_id).execute()
    except Exception as e:
        st.error(f"Error fetching teams: {e}")
        return []
    return {team["team_id"]: team["team_name"] for team in response.data}

# Fetch players based on selected team
def fetch_players(team_id):
    try:
        response = supabase.table("players").select(
        "player_name, age, curr_gp, curr_goals, curr_assists, position"
        ).eq("curr_team_id", team_id).execute()
    except Exception as e:
        st.error(f"Error fetching players: {e}")
        return []
    return response.data

# Streamlit UI
st.title("Football Database")

# League dropdown
leagues = fetch_leagues()
selected_league = st.selectbox("Select a League", options=leagues.keys(), format_func=lambda x: leagues[x])

# Team dropdown
if selected_league:
    teams = fetch_teams(selected_league)
    selected_team = st.selectbox("Select a Team", options=teams.keys(), format_func=lambda x: teams[x])

# Show Players button
if selected_team:
    if st.button("Show Players"):
        players = fetch_players(selected_team)
        if players:
            # Add G/A column
            for player in players:
                player["G/A"] = player["curr_goals"] + player["curr_assists"]

            # Display player data as a table
            player_df = pd.DataFrame(players)
            st.dataframe(player_df)
        else:
            st.warning("No players found for the selected team.")
