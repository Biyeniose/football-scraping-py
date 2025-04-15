import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from src.init_supabase import supabase
from scraping import update_player_stats, get_player_transfers, parse_money_string, extract_loan_fee, get_team_id, get_player_ids, get_clubs_per_league, update_team_nation_ids, update_leagues_youth_teams, insert_leagues_youth_teams, save_player_transfers_byname
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER, POR_ID, NED_ID, BELG_ID, SCOT_ID, ENG2_ID, SAUDI_ID



st.title("Page for Scraping Players Previous year stats")

endings = ["U23", "U20", "U21", "U18", "U17", "U19", "U16", "U-15", "U15", "Yth", "Yth.", "Youth", "Aca", "Academy", "Yout", "B", "II", "Sub-17", "Sub-15", "CF You"]


st.subheader("Scrape Clubs of Player")
st.write("For inserting player transfer")
if st.button("Button for scraping Player's Transfers"):
    name = "Iliman Ndiaye"

    try:

        save_player_transfers_byname(name)


    except Exception as e:
        st.write(f"Error fetching players: {e}")
        #return []
    
    #st.write(player_names)




st.subheader("Scrape Transfers of Clubs in a League")
st.write("Insert transfers of all players of a certain LEAGUE")
if st.button("Button for scraping of a League's Players' Transfers"):
    
    
    #league_id = 3
    #team_id = 1103
    """
    try:
        players_response = supabase.table('players').select('player_name').eq('curr_team_id', team_id).execute()

        player_names = [player['player_name'] for player in players_response.data]
        #return player_names

    except Exception as e:
        st.write(f"Error fetching players: {e}")
        #return []
    """
    #st.write(player_names)
    epl_teams = supabase.table("teams").select("team_id, transfm_season_url").eq("league_id", ITA_ID).execute()
    #teams = ["Newcastle", "Bor"]

    for i in epl_teams.data:
        team_id = i["team_id"]

        try:
            players_response = supabase.table('players').select('player_name').eq('curr_team_id', team_id).execute()

            player_names = [player['player_name'] for player in players_response.data]

            for i in player_names:
                st.write(i)
                save_player_transfers_byname(i)


            #return player_names

        except Exception as e:
            st.write(f"Error fetching players: {e}")
            #return []
   



st.write("----------------------------------")

st.subheader("In the case where the Youth teams are not updated with the proper nations")
st.subheader("Update League's Youth teams")
if st.button("Button for Updating a league's Youth squads"):
    clubs = get_clubs_per_league(291)
    #st.write(clubs)

    for i in clubs:
        name = i["team_name"]
        st.write(name)
        update_leagues_youth_teams(name)
        st.write("----------------------")


st.subheader("Insert new League's Youth teams")
st.write("Insert the Youth teams of a League")
if st.button("Button for inserting a league's Youth squads"):
    clubs = insert_leagues_youth_teams(291)
    #st.write(clubs)

    for i in clubs:
        name = i["team_name"]
        st.write(name)
        insert_leagues_youth_teams(name)
        st.write("----------------------")


st.write("----------------------------------")
st.subheader("Insert Indv team's Youth teams")
if st.button("Button adding Youth versions of teams"):
    club_name = "Stade Rennais"

    input_name = "Rennes"

    response = supabase.table("teams").select("logo_url, nation_id").eq("team_name", club_name).execute()
    logo = response.data[0]["logo_url"]
    nation_id = response.data[0]["nation_id"]


    for j in endings:
        new_name = input_name + " " + j
        #st.write(new_name)

        data = {
            "team_id": random.randint(100000, 999999),
            "team_name": new_name,
            "logo_url": logo,
            "league_id": 1111,
            "nation_id": nation_id,
        }
        #st.write(data)

        try:
            resp = supabase.table("teams").insert(data).execute()
            #resp = supabase.table("teams").update(data).eq("team_name", new_name).execute()

            st.write(resp)
        except Exception as e:
                st.error(f'{new_name}')
                st.error(f'Error = {e}')

    
st.write("----------------------------------")

st.subheader("Quick test")
st.write("Make sure teams from that league have the correct nation_id column")
if st.button("Button for updating nation_ids"):
    update_team_nation_ids(20)



