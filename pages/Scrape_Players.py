import streamlit as st
import sys, random, json, re
sys.path.append("src")
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
from insert_functions import insert_player, get_gb
import pandas as pd
from scraping import get_soup, get_page_trs, should_keep_tr, extract_player_jsons

st.title("Page for Scraping players")
st.write("Remember the teams of a League are first inserted in the DB through a json that has Team Name and Image URL")
st.write("This json is scraped from a Transfm HTML element of a table containing all teams")

st.write("After the Teams of a League hae been inserted then you can run these functions to update the stats")

st.subheader("Buttons for EPL teams")
            
if st.button("Run code to Insert all EPL teams from .json file with Transfm team_id and Transfrm URL for all teams"):
    with open("pages/epl.json", "r") as file:
        resp = json.load(file) 
    
    urls=[]
    for item in resp:
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table

        stats_page_url= f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"

        soup = get_soup(stats_page_url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "insert")
        
        # select the team_id by using transfm_team_id and add to insert data
        curr_team_id = supabase.table("teams").select("team_id").eq("team_transfm_id", transfm_team_id).execute()

        json_response = curr_team_id.data
        if json_response:  # Check if data exists
            team_id = json_response[0]["team_id"]  # Access the first item's team_id
            st.write(f"Extracted team_id: {team_id}")
        else:
            st.write("No data found in the response.")

        for item in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")
            st.write(item['player_name'])
            item["curr_team_id"] = team_id

            try:
                response = supabase.table("players").insert(item).execute()
                st.success(f"Player inserted ")

            except Exception as e:
                st.error(f'Error: {e}')
                #continue


if st.button("Update ALL Players stats for ALL EPL teams"):
    response = supabase.table("teams").select("team_name, team_id, team_transfm_id, curr_season_url").eq("league_id", 2).execute()

    #st.write(response)

    json_response = response.data
    #if json_response:  # Check if data exists
        #team_id = json_response[0]["team_id"]  # Access the first item's team_id
        #st.write(f"Extracted team_id: {team_id}")
    #else:
       # st.write("No data found in the response.")
    errors = []
    
    for item in json_response:
        # Format the slug to create a full name
        team_name = item["team_name"]
        team_transfm_id = item["team_transfm_id"]
        url = item["curr_season_url"]

        soup = get_soup(url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "update")
        #final_json.pop("player_id")
        final_json.pop(0)

        for item2 in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")

            player_name = item2['player_name']
            st.write(player_name)
            #item2["curr_team_id"] = team_id

            try:
                response = supabase.table("players").update(item2).eq("player_name", player_name).execute()
                st.success(f"Player updated")

            except Exception as e:
                errors.append(player_name)
                st.error(f'Error: {e}')
                #continue

        st.write(errors)


st.subheader("Buttons for La Liga teams")

if st.button("Update Transfm TeamIDs and URLs of La Liga Teams"):
    i=1
    with open("pages/laliga.json", "r") as file:
        resp = json.load(file) 
    
    for item in resp:
        
        # Format the slug to create a full name
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table
        data = {
            "team_transfm_id": transfm_team_id,
            "curr_season_url": f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"
        }
        
        try:
            response = supabase.table("teams").update(data).eq("team_name", team_name).execute()
            st.success(team_name)
            st.success("Team updated successfully!")

        except Exception as e:
            st.error(team_name)
            st.error(f'Error: {e}')
            continue


if st.button("Run code to Insert all LaLiga teams AND PLAYERS from .json file with Transfm team_id and Transfrm URL for all teams"):
    with open("pages/laliga.json", "r") as file:
        resp = json.load(file) 
    
    urls=[]
    for item in resp:
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table

        stats_page_url= f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"

        soup = get_soup(stats_page_url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "insert")
        
        # select the team_id by using transfm_team_id and add to insert data
        curr_team_id = supabase.table("teams").select("team_id").eq("team_transfm_id", transfm_team_id).execute()

        json_response = curr_team_id.data
        if json_response:  # Check if data exists
            team_id = json_response[0]["team_id"]  # Access the first item's team_id
            st.write(f"Extracted team_id: {team_id}")
        else:
            st.write("No data found in the response.")

        for item in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")
            st.write(item['player_name'])
            item["curr_team_id"] = team_id

            try:
                response = supabase.table("players").insert(item).execute()
                st.success(f"Player inserted ")

            except Exception as e:
                st.error(f'Error: {e}')
                #continue

if st.button("Update ALL Players stats for ALL La Liga teams"):
    response = supabase.table("teams").select("team_name, team_id, team_transfm_id, curr_season_url").eq("league_id", 1).execute()

    #st.write(response)

    json_response = response.data
    errors = []
    
    for item in json_response:
        # Format the slug to create a full name
        team_name = item["team_name"]
        team_transfm_id = item["team_transfm_id"]
        url = item["curr_season_url"]

        soup = get_soup(url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "update")
        #final_json.pop("player_id")
        final_json.pop(0)

        for item2 in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")

            player_name = item2['player_name']
            st.write(player_name)
            #item2["curr_team_id"] = team_id

            try:
                response = supabase.table("players").update(item2).eq("player_name", player_name).execute()
                st.success(f"Player updated")

            except Exception as e:
                errors.append(player_name)
                st.error(f'Error: {e}')
                #continue

        st.write(errors)


st.subheader("Buttons for Bundesliga teams")

if st.button("Update Transfm TeamIDs and URLs of Bundesliga Teams"):
    i=1
    with open("pages/bundes.json", "r") as file:
        resp = json.load(file) 
    
    for item in resp:
        
        # Format the slug to create a full name
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table
        data = {
            "team_transfm_id": transfm_team_id,
            "curr_season_url": f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"
        }
        
        try:
            response = supabase.table("teams").update(data).eq("team_name", team_name).execute()
            st.success(team_name)
            st.success("Team updated successfully!")

        except Exception as e:
            st.error(team_name)
            st.error(f'Error: {e}')
            continue


if st.button("Run code to Insert all Bundesliga teams  AND PLAYERS from .json file with Transfm team_id and Transfrm URL for all teams"):
    with open("pages/bundes.json", "r") as file:
        resp = json.load(file) 
    
    urls=[]
    for item in resp:
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table

        stats_page_url= f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"

        soup = get_soup(stats_page_url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "insert")
        
        # select the team_id by using transfm_team_id and add to insert data
        curr_team_id = supabase.table("teams").select("team_id").eq("team_transfm_id", transfm_team_id).execute()

        json_response = curr_team_id.data
        if json_response:  # Check if data exists
            team_id = json_response[0]["team_id"]  # Access the first item's team_id
            st.write(f"Extracted team_id: {team_id}")
        else:
            st.write("No data found in the response.")

        for item in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")
            st.write(item['player_name'])
            item["curr_team_id"] = team_id

            try:
                response = supabase.table("players").insert(item).execute()
                st.success(f"Player inserted ")

            except Exception as e:
                st.error(f'Error: {e}')
                #continue

if st.button("Update ALL Players stats for ALL Bundesliga teams"):
    response = supabase.table("teams").select("team_name, team_id, team_transfm_id, curr_season_url").eq("league_id", 3).execute()

    #st.write(response)

    json_response = response.data
    errors = []
    
    for item in json_response:
        # Format the slug to create a full name
        team_name = item["team_name"]
        team_transfm_id = item["team_transfm_id"]
        url = item["curr_season_url"]

        soup = get_soup(url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "update")
        #final_json.pop("player_id")
        final_json.pop(0)

        for item2 in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")

            player_name = item2['player_name']
            st.write(player_name)
            #item2["curr_team_id"] = team_id

            try:
                response = supabase.table("players").update(item2).eq("player_name", player_name).execute()
                st.success(f"Player updated")

            except Exception as e:
                errors.append(player_name)
                st.error(f'Error: {e}')
                #continue

        st.write(errors)


st.subheader("Buttons for Seria A teams")

if st.button("Update Transfm TeamIDs and URLs of Seria A Teams"):
    i=1
    with open("pages/seria.json", "r") as file:
        resp = json.load(file) 
    
    for item in resp:
        
        # Format the slug to create a full name
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table
        data = {
            "team_transfm_id": transfm_team_id,
            "curr_season_url": f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"
        }
        
        try:
            response = supabase.table("teams").update(data).eq("team_name", team_name).execute()
            st.success(team_name)
            st.success("Team updated successfully!")

        except Exception as e:
            st.error(team_name)
            st.error(f'Error: {e}')
            continue


if st.button("Run code to Insert all Seria A teams  AND PLAYERS from .json file with Transfm team_id and Transfrm URL for all teams"):
    with open("pages/seria.json", "r") as file:
        resp = json.load(file) 
    
    urls=[]
    for item in resp:
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table

        stats_page_url= f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"

        soup = get_soup(stats_page_url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "insert")
        
        # select the team_id by using transfm_team_id and add to insert data
        curr_team_id = supabase.table("teams").select("team_id").eq("team_transfm_id", transfm_team_id).execute()

        json_response = curr_team_id.data
        if json_response:  # Check if data exists
            team_id = json_response[0]["team_id"]  # Access the first item's team_id
            st.write(f"Extracted team_id: {team_id}")
        else:
            st.write("No data found in the response.")

        for item in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")
            st.write(item['player_name'])
            item["curr_team_id"] = team_id

            try:
                response = supabase.table("players").insert(item).execute()
                st.success(f"Player inserted ")

            except Exception as e:
                st.error(f'Error: {e}')
                #continue

if st.button("Update ALL Players stats for ALL Seria A teams"):
    response = supabase.table("teams").select("team_name, team_id, team_transfm_id, curr_season_url").eq("league_id", 4).execute()

    #st.write(response)

    json_response = response.data
    errors = []
    
    for item in json_response:
        # Format the slug to create a full name
        team_name = item["team_name"]
        team_transfm_id = item["team_transfm_id"]
        url = item["curr_season_url"]

        soup = get_soup(url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "update")
        #final_json.pop("player_id")
        final_json.pop(0)

        for item2 in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")

            player_name = item2['player_name']
            st.write(player_name)
            #item2["curr_team_id"] = team_id

            try:
                response = supabase.table("players").update(item2).eq("player_name", player_name).execute()
                st.success(f"Player updated")

            except Exception as e:
                errors.append(player_name)
                st.error(f'Error: {e}')
                #continue

        st.write(errors)


st.subheader("Buttons for Ligue 1 teams")

if st.button("Update Transfm TeamIDs and URLs of Ligue 1 Teams"):
    i=1
    with open("pages/ligue1.json", "r") as file:
        resp = json.load(file) 
    
    for item in resp:
        
        # Format the slug to create a full name
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table
        data = {
            "team_transfm_id": transfm_team_id,
            "curr_season_url": f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"
        }
        
        try:
            response = supabase.table("teams").update(data).eq("team_name", team_name).execute()
            st.success(team_name)
            st.success("Team updated successfully!")

        except Exception as e:
            st.error(team_name)
            st.error(f'Error: {e}')
            continue


if st.button("Run code to Insert all Ligue 1 teams from .json file with Transfm team_id and Transfrm URL for all teams"):
    with open("pages/ligue1.json", "r") as file:
        resp = json.load(file) 
    
    urls=[]
    for item in resp:
        team_name = item["team_name"]
        transfm_team_id = item["team_id"]
        url = item["url"]

        # Extracting the part between the first two slashes
        match = re.search(r'^/([^/]+)/', url)
        if match:
            transfm_name = match.group(1)
             # Output: fc-fulh
        # Insert into the Supabase players table

        stats_page_url= f"https://www.transfermarkt.us/{transfm_name}/leistungsdaten/verein/{transfm_team_id}/reldata/%262024/plus/1"

        soup = get_soup(stats_page_url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "insert")
        
        # select the team_id by using transfm_team_id and add to insert data
        curr_team_id = supabase.table("teams").select("team_id").eq("team_transfm_id", transfm_team_id).execute()

        json_response = curr_team_id.data
        if json_response:  # Check if data exists
            team_id = json_response[0]["team_id"]  # Access the first item's team_id
            st.write(f"Extracted team_id: {team_id}")
        else:
            st.write("No data found in the response.")

        for item in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")
            st.write(item['player_name'])
            item["curr_team_id"] = team_id

            try:
                response = supabase.table("players").insert(item).execute()
                st.success(f"Player inserted ")

            except Exception as e:
                st.error(f'Error: {e}')
                #continue

if st.button("Update ALL Players stats for ALL Ligue 1 teams"):
    response = supabase.table("teams").select("team_name, team_id, team_transfm_id, curr_season_url").eq("league_id", 5).execute()

    #st.write(response)

    json_response = response.data
    errors = []
    
    for item in json_response:
        # Format the slug to create a full name
        team_name = item["team_name"]
        team_transfm_id = item["team_transfm_id"]
        url = item["curr_season_url"]

        soup = get_soup(url)
        clean_trs = should_keep_tr(get_page_trs(soup)) 
        final_json = extract_player_jsons(clean_trs, "update")
        #final_json.pop("player_id")
        final_json.pop(0)

        for item2 in final_json:
            #print(f"Name: {item['name']}, Age: {item['age']}")

            player_name = item2['player_name']
            st.write(player_name)
            #item2["curr_team_id"] = team_id

            try:
                response = supabase.table("players").update(item2).eq("player_name", player_name).execute()
                st.success(f"Player updated")

            except Exception as e:
                errors.append(player_name)
                st.error(f'Error: {e}')
                #continue

        st.write(errors)