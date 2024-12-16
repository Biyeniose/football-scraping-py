import streamlit as st
import sys, random, json
sys.path.append("src")
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
from insert_functions import insert_player, get_gb
import pandas as pd

# Streamlit UI for viewing tables
st.title("Run Scraping code")
st.subheader("Old code for scraping players")

st.write("Use this code as an example for inserting teams from a league")

def format_slug(slug):
    # Split the slug by dashes, capitalize each part, and join with spaces
    return " ".join(part.capitalize() for part in slug.split("-"))

if st.button("Make Request"):
    # Query Supabase to get the players table data
    #url_gb = "https://tmsi.akamaized.net/kooperationen/sorare/sorare_GB1_5.json"
    #resp = get_gb(url_gb)
    with open("pages/data.json", "r") as file:
        resp = json.load(file) 

    filtered_data = []
    for item in resp:
        if item.get("slug"):
            filtered_data.append(item)

    # Loop through filtered data and insert each item into Supabase
    for item in filtered_data:
        # Generate a random 4-digit player_id
        player_id = random.randint(100000, 999999)
        
        # Format the slug to create a full name
        full_name = format_slug(item["slug"])
        
        # Prepare transf_id
        transf_id = item["spieler_id"]
        
        # Insert into the Supabase players table
        data = {
            "player_id": player_id,
            "full_name": full_name,
            "transf_id": transf_id
        }
        
        try:
            response = supabase.table("players").insert(data).execute()
            st.success("Player inserted successfully!")

        except Exception as e:
            st.error(f'Error: {e}')
            continue
