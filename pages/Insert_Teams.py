import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
from insert_functions import insert_player, get_gb
from scraping import get_soup, update_league, insert_league, extract_numeric_value, extract_height_value, insert_other_teams_with_logos
import pandas as pd
from datetime import datetime
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER, USA_ID, BELG_ID, SCOT_ID, ENG2_ID, SAUDI_ID, BRAZIL_ID, GREECE_ID, DEN_ID, SWISS_ID, ENG3_ID, FRA2_ID, FRA3_ID, ITA2_ID


# Define the paths to the JSON file
turkey_path = os.path.join('data', 'turkey.json')
epl_path = os.path.join('data', 'epl.json')
epl2_path = os.path.join('data', 'epl2.json')
epl3_path = os.path.join('data', 'eng3.json')

fra2_path = os.path.join('data', 'fra2.json')
fra3_path = os.path.join('data', 'fra3.json')


ger_path = os.path.join('data', 'ger.json')
usa_path = os.path.join('data', 'usa.json')
belg_path = os.path.join('data', 'belgium.json')
scot_path = os.path.join('data', 'scot.json')
saudi_path = os.path.join('data', 'saudi.json')
brazil_path = os.path.join('data', 'bra_seriea.json')
greece_path = os.path.join('data', 'greek_superlig.json')
dan_path = os.path.join('data', 'dan_superlig.json')
swiss_path = os.path.join('data', 'swiss.json')


fotmob_base_url = "https://www.fotmob.com/en-GB"

st.title("Inserting or Updating Leagues' Teams from Transfrmarket")

st.write("-------")

st.header("FOR THIS BUTTON First INSERT the League in the DB then use the picked league_id and Transfm url to insert the Teams from that league")
st.write("Will need seperate code for pages with 2 tabls")
# Button for updating Team data from Transfm   
if st.button("INSERT OTHER teams from Transfm URL"):
    # Transfermkt url for the Team
    url = "https://www.transfermarkt.com/egyptian-premier-league/startseite/wettbewerb/EGY1"
    insert_other_teams_with_logos(url, 774)
st.write("-------")

st.write("EPL teams")

# Button for updating Team data from Transfm   
if st.button("UPDATE EPL teams from Transfm"):
    # Transfermkt url for EPL teams
    epl_transfm_url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1"
    update_league(epl_transfm_url)

if st.button("Insert EPL teams from ESPN json file"):
    insert_league(ENG_ID, epl_path)


st.write("-------")

st.write("Eng Championship teams")

# Button for updating Team data from Transfm   
if st.button("UPDATE EPL2 teams from Transfm"):
    # Transfermkt url for EPL teams
    epl_transfm_url = "https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2"
    update_league(epl_transfm_url)

if st.button("Insert EPL2 teams from ESPN json file"):
    insert_league(ENG2_ID, epl2_path)

st.write("-------")

st.write("ENG 3 teams")
# Button for updating Team data from Transfm   
if st.button("Insert ENG 3 teams from ESPN json file"):
    insert_league(ENG3_ID, epl3_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE ENG 3 teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB3"
    update_league(url)

st.write("-------")

st.write("La Liga teams")

# Button for updating Team data from Transfm   
if st.button("UPDATE La Liga teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/saison_id/2024"
    update_league(url)

st.write("-------")

st.write("Bundesliga teams")
# Button for updating Team data from Transfm   
if st.button("UPDATE Bundesliga teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/saison_id/2024"
    update_league(url)

if st.button("Insert Bundesliga teams from ESPN json file"):
    # function to insert league
    insert_league(GER_ID, ger_path)


    

st.write("-------")

st.write("Seria A teams")
# Button for updating Team data from Transfm   
if st.button("UPDATE Seria A teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1"
    update_league(url)

st.write("-------")

st.write("Ligue 1 teams")
# Button for updating Team data from Transfm   
if st.button("UPDATE Ligue 1 teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1"
    update_league(url)

st.write("-------")

st.write("Ligue 2 teams")
# Button for updating Team data from Transfm   
if st.button("UPDATE Ligue 2 teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/ligue-2/startseite/wettbewerb/FR2"
    update_league(url)

if st.button("Insert Ligue 2 teams from ESPN json file"):
    # function to insert league
    insert_league(FRA2_ID, fra2_path)

st.write("-------")



st.write("Eredevise teams")
# Button for updating Team data from Transfm   
if st.button("UPDATE Eredevise teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1"
    update_league(url)

st.write("-------")

st.write("Portugal teams")
# Button for updating Team data from Transfm   
if st.button("UPDATE Portugal teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/liga-portugal/startseite/wettbewerb/PO1"
    update_league(url)

st.write("-------")

st.write("Turkey teams")
# Button for updating Team data from Transfm   
if st.button("Insert Turkey teams from ESPN json file"):
    insert_league(TURKEY_ID, turkey_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE Turkey teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/super-lig/startseite/wettbewerb/TR1"
    update_league(url)


st.write("-------")

st.write("USA teams (will need special case)")
# Button for updating Team data from Transfm   
if st.button("Insert USA teams from ESPN json file"):
    insert_league(USA_ID, usa_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE USA teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/major-league-soccer/startseite/wettbewerb/MLS1"
    update_league(url)

st.write("-------")

st.write("BELG teams")
# Button for updating Team data from Transfm   
if st.button("Insert BELG teams from ESPN json file"):
    insert_league(BELG_ID, belg_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE BELG teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/jupiler-pro-league/startseite/wettbewerb/BE1"
    update_league(url)

st.write("-------")

st.write("Scotland teams")
# Button for updating Team data from Transfm   
if st.button("Insert SCOT teams from ESPN json file"):
    insert_league(SCOT_ID, scot_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE SCOT teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/scottish-premiership/startseite/wettbewerb/SC1"
    update_league(url)

st.write("-------")

st.write("Saudi teams")
# Button for updating Team data from Transfm   
if st.button("Insert SAUDI teams from ESPN json file"):
    insert_league(SAUDI_ID, saudi_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE SAUDI teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/saudi-professional-league/startseite/wettbewerb/SA1"
    update_league(url)

st.write("-------")

st.write("Brazil teams")
# Button for updating Team data from Transfm   
if st.button("Insert BRAZIL teams from ESPN json file"):
    insert_league(BRAZIL_ID, brazil_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE BRAZIL teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1"
    update_league(url)

st.write("-------")

st.write("Greece teams")
# Button for updating Team data from Transfm   
if st.button("Insert GREECE teams from ESPN json file"):
    insert_league(GREECE_ID, greece_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE GREECE teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/super-league-1/startseite/wettbewerb/GR1"
    update_league(url)


st.write("-------")

st.write("Denmark teams")
# Button for updating Team data from Transfm   
if st.button("Insert Denmark teams from ESPN json file"):
    insert_league(DEN_ID, dan_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE Denmark teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/superliga/startseite/wettbewerb/DK1"
    update_league(url)

st.write("-------")

st.write("Swiss teams")
# Button for updating Team data from Transfm   
if st.button("Insert Swiss teams from ESPN json file"):
    insert_league(SWISS_ID, swiss_path)

# Button for updating Team data from Transfm   
if st.button("UPDATE Swiss teams from Transfm"):
    # Transfermkt url for EPL teams
    url = "https://www.transfermarkt.com/super-league/startseite/wettbewerb/C1"
    update_league(url)