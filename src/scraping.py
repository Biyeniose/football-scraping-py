import re, requests, sys, json, random, os, re
from bs4 import BeautifulSoup
#from supabase import create_client, Client
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
import streamlit as st
from datetime import datetime
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER


def remove_invisible_characters(text):
    """
    Removes common invisible characters from the given text.
    """
    # List of invisible characters to remove
    invisible_chars = [
        '\u200E',  # Left-to-Right Mark
        '\u200F',  # Right-to-Left Mark
        '\u202A',  # Left-to-Right Embedding
        '\u202B',  # Right-to-Left Embedding
        '\u202C',  # Pop Directional Formatting
        '\u202D',  # Left-to-Right Override
        '\u202E',  # Right-to-Left Override
        '\u2066',  # Left-to-Right Isolate
        '\u2067',  # Right-to-Left Isolate
        '\u2068',  # First Strong Isolate
        '\u2069',  # Pop Directional Isolate
    ]

    # Remove invisible characters
    for char in invisible_chars:
        text = text.replace(char, '')

    return text

# function that returns soup from given url
def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    }
    
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")
    return soup

def get_team_players(team_id, team_page_url, action):
    error_list=[]
    # get the tr elements of each player 
    try:
        # get html of the url 
        soup = get_soup(team_page_url)
        table = soup.find("table", class_="items")
        
        tr1 = table.find_all("tr", class_="odd")
        tr2 = table.find_all("tr", class_="even")
        tr3 = tr1 + tr2

    except Exception as e:
        st.error(f'Error = {e}')

    for i in tr3:
        name = i.find("td", class_="hauptlink").text.strip()
        name2 = i.find("td", class_="hauptlink")
        transfm_url = TRANSFM_HEADER + name2.find("a")['href']

        td_elements = i.find_all('td')

        contract_end = td_elements[-2].text.strip()
        
        foot = td_elements[-5].text.strip()
        date_joined = td_elements[-4].text.strip()
        position = td_elements[4].text.strip()

        date_age = td_elements[5].text.strip()

        mk_value = td_elements[-1].text.strip()
        mk_value = "0.00" if mk_value == "-" else mk_value

        squad_num = td_elements[0].text
        if squad_num == "-":
            squad_num = 0
        else:
            squad_num = int(squad_num)

            
        #squad_num = int(td_elements[0].text)

        # Split the string into date and age
        date_part = date_age.split('(')[0].strip()  # Extract the date part
        age_part = date_age.split('(')[1].strip(')')  # Extract the age part

        # Convert to a datetime object
        date_obj = datetime.strptime(date_part, "%b %d, %Y")

        # Format the date as YYYY-MM-DD
        iso_date = date_obj.strftime("%Y-%m-%d")

        height = td_elements[7].text
        height = "0,00" if height == "-" else height
        
        nations = []
        nation = td_elements[6].find_all("img")
        for j in nation:
            nations.append(j['title'])

        # seperate the nations
        nation1 = nations[0]
        nation2 = nations[1] if len(nations) > 1 else None
        
        try:
            # Date Joined
            # Convert to a datetime object
            joined = datetime.strptime(date_joined, "%b %d, %Y")
            # Format the date as YYYY-MM-DD
            joined_iso_date = joined.strftime("%Y-%m-%d")
        except Exception as e:
            joined = None if contract_end == "" else contract_end
            joined_iso_date = None

        try:
            contr_end = datetime.strptime(contract_end, "%b %d, %Y")
            # Format the date as YYYY-MM-DD
            contract_end_iso_date = contr_end.strftime("%Y-%m-%d")
        except Exception as e:
            contract_end = None if contract_end == "-" else contract_end
            contract_end_iso_date = None

        try:
            # data object
            data = {
                "player_name": name,
                "nation1": nation1,
                "nation2": nation2,
                "player_id": random.randint(10000, 99999),
                "transfm_id": int(transfm_url.split('/')[-1]),
                "transfm_url": transfm_url,
                "dob": iso_date,
                "age": int(age_part),
                "position": position,
                "curr_number": squad_num,
                "curr_team_id": team_id,
                "market_value": extract_numeric_value(mk_value),
                "height": extract_height_value(height),
                "foot": foot,
                "date_joined": joined_iso_date,
                "contract_end": contract_end_iso_date,
                }
        except Exception as e:
            st.error(f'{name}')
            st.error(f'Error = {e}')

        if action == "insert":
            try:
                resp = supabase.table("players").insert(data).execute()
                st.success(f'{name}')
                st.success(resp)
            except Exception as e:
                st.error(f'{name}')
                st.error(f'Error = {e}')

            
        
        else:
            #del data["player_id"]
            data.pop("player_id", None)

            try:
                resp = supabase.table("players").update(data).eq("player_name", name).execute()
                st.success(f'{name}')
                st.success(resp)
            except Exception as e:
                st.error(f'{name}')
                st.error(f'Error = {e}')
        

            


    return None

def transform_url_transfm_all_players(original_url):
    """
    Transforms the URL by replacing 'spielplan' with 'kader' and appending '/plus/1'.

    Args:
        original_url (str): The original URL (e.g., "https://www.transfermarkt.com/manchester-city/spielplan/verein/281/saison_id/2024").

    Returns:
        str: The transformed URL.
    """
    # Replace 'spielplan' with 'kader'
    transformed_url = original_url.replace("spielplan", "kader")

    # Append '/plus/1' to the URL
    transformed_url += "/plus/1"

    return transformed_url



# function that use the .json file to insert teams of a League (more so for when a new season starts)
def insert_league(league_id, file_path):
    # insert the Teams and ImageURLs of the Turkey League
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        teams_data = json.load(file)

    # Loop through each team and image_url
    for team_info in teams_data:
        team = team_info['team']
        image_url = team_info['image_url']

        data = {
            "team_name": team,
            "team_id": random.randint(1000, 9999),
            "league_id": league_id,
            "logo_url": image_url,
        }

        # for each team, insert into supabase
        try:
            response = supabase.table("teams").insert(data).execute()
            st.success(response)
        except Exception as e:
            st.error(team)
            st.error(f'Error = {e}')
    
    return None

def extract_numeric_value(value_str):
    """
    Extracts the numeric value from a string like "€10.00m" and converts it to a float.

    Args:
        value_str (str): The input string (e.g., "€10.00m", "€1.2b", "€500k").

    Returns:
        float: The extracted numeric value.
    """
    # Remove the currency symbol
    cleaned_value = value_str.replace("€", "")

    # Handle suffixes and determine the multiplier
    if cleaned_value.endswith("m"):
        multiplier = 1_000_000  # Millions
        cleaned_value = cleaned_value.replace("m", "")
    elif cleaned_value.endswith("k"):
        multiplier = 1_000  # Thousands
        cleaned_value = cleaned_value.replace("k", "")
    elif cleaned_value.endswith("b"):
        multiplier = 1_000_000_000  # Billions
        cleaned_value = cleaned_value.replace("b", "")
    else:
        multiplier = 1  # No suffix

    # Convert to float and apply the multiplier
    return float(cleaned_value) * multiplier

def extract_height_value(height_str):
    """
    Extracts the numeric value from a height string like "1,88m" and converts it to a float.

    Args:
        height_str (str): The input string (e.g., "1,88m").

    Returns:
        float: The extracted height value.
    """
    # Remove the 'm' suffix
    cleaned_value = height_str.replace("m", "")

    # Replace comma with period to handle decimal separator
    cleaned_value = cleaned_value.replace(",", ".")

    # Convert to float
    return float(cleaned_value)

# function that takes in a League URL from Transfm and updates all the Team detials of the league
def update_league(league_transfm_url):
    # get html of the url 
    soup = get_soup(league_transfm_url)

    url_header = "https://www.transfermarkt.com"

    # main table element of the teams 
    table = soup.find_all("table", class_="items")

    # get the 20 trs (rows) of the teams
    trs = table[2].find_all("tr")

    # lo0p through each team row
    for i in trs[1:]:
        tds = i.find_all("td")

        rank = tds[0].text
        team_short_name = tds[2].text.strip()
        team_name = tds[2].find('a')['title']

        gp = tds[3].text
        gd = tds[4].text
        points = tds[5].text

        transfm_season_url = url_header + tds[1].find('a')['href']

        team_transfm_id = re.search(r'verein/(\d+)/', transfm_season_url).group(1)

        data = {
            "team_name": team_short_name,
            "team_name2": team_name,
            "curr_league_rank": int(rank),
            "curr_league_gp": int(gp),
            "curr_league_points": int(points),
            "curr_league_gd": int(gd),
            "transfm_season_url": transfm_season_url,
            "transfm_id": int(team_transfm_id),
        }

        st.write(data)

        # update teams table for Prem
        try:
            resp = supabase.table("teams").update(data).eq("team_name", team_short_name).execute()
            
            st.write(f"Team {team_short_name}")
            st.success(resp)
        except Exception as e:
            st.error(f'Team = {team_short_name}')
            st.error(f'Error: {e}')
            continue

        st.write("-------")
    
    return None

# returns an array of trs containing data in the soup element
def get_page_trs(soup):
    # trs = data.find('tr', class_="odd", attrs={"itemprop": "birthDate"}).text
    trs_odd = soup.find_all('tr', class_="odd")
    trs_even = soup.find_all('tr', class_="even")
    return trs_odd + trs_even

def should_keep_tr(trs):
    final_arr = []
    # Iterate over a copy of the ResultSet to avoid modifying the list while iterating
    for tr in trs:
        # Find the first 'td' element and get its text
        squad_num = tr.find('td').text
        
        # Check if the squad number is not "-"
        if squad_num != "-":
            # Remove the 'tr' element from the set
            final_arr.append(tr)
    
    return final_arr

def get_player_id(url):
    # Example URL
    #url = "https://img.a.transfermarkt.technology/portrait/small/183288-1668500175.jpg?lm=1"

    # Regular expression to match digits after "small/"
    pattern = r"small/(\d+)-"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    if match:
        result = match.group(1)  # Extract the first capturing group (digits)
        return result  # Output: 183288
    else:
        return None

def extract_player_jsons(elements_arr, action_type):
    all_players = []
    
    for i in elements_arr:
        countries = []
        
        
        data1 = i.find_all('td')
        number = data1[0].text
        age = data1[5].text
        
        nation = data1[6]
        imgs = nation.find_all('img')
        nations = {}
        for j in imgs:
            im = j['alt']
            src = j['src']
            #nations[im] = src
            #countries.append(im)
            #countries.append(src)
            #print(im)
            countries.append(im)
            #countries.append(nations)
        
        name_temp = data1[2]
        name = name_temp.find('img')['alt']
        photo_url = name_temp.find('img')['src']

        #player_transf_url = data1.find_all('span', class_="hide-for-small")
        player_transf_url = data1[3].find("a")["href"]
        """
        
        for j in data1:
            
            player_transf_url = j.find_all('span', class_="hide-for-small")
            arr1.append(player_transf_url)
        #player_transf_url2 = player_transf_url["title"]
        """

        transfm_id = get_player_id(photo_url)
        #squad_num = data1[0].find('td').text
        squad_num = data1[0].text
        
        # debugging
        st.write(player_transf_url)
        #st.write(data1)


        minutes = data1[17].text.replace(".", "").strip("'") 
        #clean_value = value.strip("'") 
        if minutes in ("-","Not used during this season", "Not in squad during this season"):
            minutes = 0

        
        
        position = data1[4].text
        apps = data1[8].text
        if apps in ("-","Not used during this season", "Not in squad during this season"):
            apps = 0

        try:
            goals = int(data1[9].text)
        except ValueError as e:
            goals = 0
        try:
            assists = int(data1[10].text)
        except ValueError as e:
            assists = 0
            
        g_a = goals + assists
        
        player_id = random.randint(10000, 99999)
        try:
            player_json = {
            "player_id": player_id,
            "player_name": name,
            "curr_number": int(number),     
            "position": position,
            "age": int(age),
            "curr_gp": int(apps),
            "curr_goals": goals,
            "curr_assists": assists,
            "nation": countries,
            "pic_url": photo_url,
            "transfm_id": transfm_id,
            "transfm_url": "https://www.transfermarkt.us"+player_transf_url,
            "curr_number": int(squad_num),
            "curr_minutes": int(minutes),
        }
            if action_type == "insert":
                all_players.append(player_json)
                
            elif action_type == "update":
                player_json = {
                    "player_name": name,
                    "curr_number": int(number),     
                    "position": position,
                    "age": int(age),
                    "curr_gp": int(apps),
                    "curr_goals": goals,
                    "curr_assists": assists,
                    "nation": countries,
                    "pic_url": photo_url,
                    "transfm_id": transfm_id,
                    "transfm_url": "https://www.transfermarkt.us"+player_transf_url,
                    "curr_number": int(squad_num),
                    "curr_minutes": int(minutes),
                }
                all_players.append(player_json)

        except Exception as e:
           
            print(e)
        
    return all_players



