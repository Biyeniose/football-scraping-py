import streamlit as st
import sys, random, json, re
sys.path.append("src")
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
from insert_functions import insert_player, get_gb
from scraping import get_soup, get_page_trs, should_keep_tr, extract_player_jsons
import pandas as pd

st.title("Page for Inserting teams")
st.subheader("Remember this is only for updating an ERRORED TEAM")


if st.button("Update Individual team Players"):
    #
    #stats_page_url= f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"
    stats_page_url= "https://www.transfermarkt.us/bayer-04-leverkusen/leistungsdaten/verein/15/reldata/%262024/plus/1"


    soup = get_soup(stats_page_url)
    clean_trs = should_keep_tr(get_page_trs(soup)) 
    final_json = extract_player_jsons(clean_trs, "insert")
        
    # select the team_id by using transfm_team_id and add to insert data
    curr_team_id = supabase.table("teams").select("team_id").eq("team_transfm_id", 15).execute()

    #st.write(final_json)

    json_response = curr_team_id.data
    if json_response:  # Check if data exists
        team_id = json_response[0]["team_id"]  # Access the first item's team_id
        st.write(f"Extracted team_id: {team_id}")
    else:
        st.write("No data found in the response.")

    for item in final_json:
        #print(f"Name: {item['name']}, Age: {item['age']}")
        st.write(item['player_name'])
        item["curr_team_id"] = 2332

        try:
            response = supabase.table("players").insert(item).execute()
            st.success(f"Player inserted ")

        except Exception as e:
            st.error(f'Error: {e}')
            #continue    
    