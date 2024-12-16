import streamlit as st
import sys, random, json
sys.path.append("src")
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
from insert_functions import insert_player, get_gb
import pandas as pd
from scraping import get_soup, get_page_trs, should_keep_tr, extract_player_jsons

st.title("Test Queries")
st.subheader("Create different types of queries for supabase to test team ids")

if st.button("Get ALL players and their team name"):
    try:
        response = supabase.table("players").select("player_name, teams(team_name)").execute()

        st.write(response)

    except Exception as e:
        st.error(f'Error: {e}')
        #continue

st.subheader("Get Players by Team Name")
user_input = st.text_input("Enter your Team Name:", "")

if st.button("Search"):
    try:
        if user_input.strip():
            # Step 1: Get team_id from teams table
            response = supabase.from_("teams").select("team_id").eq("team_name", user_input).execute()
            if response.data:
                team_id = response.data[0]["team_id"]
                # Step 2: Get player_name from players table
                players_response = supabase.from_("players").select("player_name").eq("curr_team_id", team_id).execute()
                if players_response.data:
                    player_names = [player["player_name"] for player in players_response.data]
                    st.write(f"Players in {user_input}:")
                    st.write(player_names)
                else:
                    st.error(f"No players found for team '{user_input}'.")
            else:
                st.error(f"Team '{user_input}' not found.")
        else:
            st.error("Please enter a valid team name.")

    except Exception as e:
        st.error(f'Error: {e}')
        #continue