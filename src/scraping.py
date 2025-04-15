import re, requests, sys, json, random, os, re
from bs4 import BeautifulSoup
#from supabase import create_client, Client
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase
import streamlit as st
from datetime import datetime
from constants import ENG_ID, ESP_ID, GER_ID, ITA_ID, FRA_ID, TURKEY_ID, TRANSFM_TEAM_PAGE_URL, TRANSFM_TEAM_URL_HEADER, TRANSFM_HEADER
from datetime import datetime


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

# determine home or away winner
def match_result(score: str) -> str:
    home, away = map(int, score.replace("–", "-").split("-"))  # Normalize dash and split
    if home > away:
        return "h"
    elif away > home:
        return "a"
    else:
        return "d"

def get_clubs_per_league(league_id: int):
    response = supabase.table("teams").select("team_name").eq("league_id", league_id).execute()

    if response.data:
        return response.data  # Return first matching row

    return None

def get_team_info(team_name: str):
    """Search for a team by name first in team_name, then in team_name2."""
    
    # First, search in team_name
    response = (
        supabase
        .from_("teams")
        .select("team_name, team_id, logo_url")
        .eq("team_name", team_name)
        .execute()
    )

    if response.data:
        return response.data[0]  # Return first matching row

    # If not found, search in team_name2
    response = (
        supabase
        .from_("teams")
        .select("team_name, team_id, logo_url")
        .eq("team_name2", team_name)
        .execute()
    )

    if response.data:
        return response.data[0]  # Return first matching row

    return None  # No match found

def get_player_ids(player_name: str):
    response = supabase.table("players").select("player_id, transfm_id").eq("player_name", player_name).execute()

    if response.data:
        return response.data[0]  # Return first matching row

    return None



def get_team_id(team_name: str):
    """Get team id from the team name"""
    
    # First, search in team_name
    response = (
        supabase
        .from_("teams")
        .select("team_id")
        .eq("team_name", team_name)
        .execute()
    )

    if response.data:
        return response.data[0]["team_id"]  # Return first matching row

    # If not found, search in team_name2
    response = (
        supabase
        .from_("teams")
        .select("team_id")
        .eq("team_name2", team_name)
        .execute()
    )

    if response.data:
        return response.data[0]["team_id"]  # Return first matching row

    return None  # No match found

# function that returns soup from given url
def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    }
    
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")
    return soup

def get_player_transfers(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    }
    
    response = requests.get(url, headers=headers)

    return response.json()

def extract_loan_fee(fee_string):
    """
    Extracts the loan fee value from a string if it contains "Loan fee".

    Args:
        fee_string: The string containing the fee information.

    Returns:
        The extracted loan fee value (e.g., "€10.00m") or None if not found.
    """
    if "End of loan" in fee_string:
        return "End of loan", True

    if "Loan fee" in fee_string or "loan transfer" in fee_string:
        match = re.search(r'<i>(.*?)</i>', fee_string) #Handles cases with and without the class attribute
        if match:
            return match.group(1)
        else:
          match = re.search(r'<i class="normaler-text">(.*?)</i>', fee_string) #Handles cases with class attribute.
          if match:
            return match.group(1), True
          else:
            return None, True  # Loan fee found, but value extraction failed
    else:
        return fee_string, False  # "Loan fee" not found

def parse_money_string(money_string):
    """
    Parses a money string (e.g., "€60.00m") and returns the value as a float.

    Args:
        money_string: The money string to parse.

    Returns:
        The numerical value as a float, or None if parsing fails.
    """
    if not isinstance(money_string, str):
      return None

    match = re.match(r'[€\$]([\d.]+)([mkb]?)', money_string) #Handles euro and dollar symbols
    if match:
        value_str = match.group(1)
        multiplier = match.group(2)

        try:
            value = float(value_str)
        except ValueError:
            return None  # Invalid numerical value

        if multiplier == 'm':
            value *= 1000000.0
        elif multiplier == 'k':
            value *= 1000.0
        elif multiplier == 'b':
            value *= 1000000000.0

        return value
    else:
        return None  # Invalid money string format

def get_team_players(team_id, team_page_url, action):
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

    
    try:
            
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
                    "player_id": random.randint(1000000, 9999999),
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

    except Exception as e:
        st.error(f'Error = {e}')
        

    return None

def convert_to_minutes(time_string):
    """
    Converts a time string in the format "X.XXX'" to minutes (float).

    Args:
        time_string (str): The time string to convert.

    Returns:
        float: The time in minutes, or None if the input is invalid.
    """
    try:
        if "'" in time_string:
            minutes = time_string.replace("'", "")
            minutes2 = float(minutes.replace(".", ""))
            return minutes2
        
        elif time_string == "-":
            return 0
        else:
            return None  # Invalid format
    except ValueError:
        return None  # Invalid number format

def handle_table_blank(input_string):
    if input_string == "-" or input_string == "Not used during this season" or input_string == "Not in squad during this season":
        return 0
    else:
        return int(input_string)

def get_ids_stats_url(league_id):
    teams = supabase.table("teams").select("team_id, transfm_stats_url, transfm_bio_url").eq("league_id", league_id).execute()

    data = []

    for i in teams.data:
        team_id = i["team_id"]
        transfm_stats_url= i["transfm_stats_url"]
        transfm_bio_url= i["transfm_bio_url"]

        temp = {
            "team_id": team_id,
            "transfm_stats_url": transfm_stats_url,
            "transfm_bio_url": transfm_bio_url
        }

        data.append(temp)

        

    return data

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

def change_transfm_url(original_url, data_type):
    """
    Transforms the URL by replacing 'spielplan' with 'kader' and appending '/plus/1'.

    Args:
        original_url (str): The original URL (e.g., "https://www.transfermarkt.com/manchester-city/spielplan/verein/281/saison_id/2024").

    Returns:
        str: The transformed URL.
    """
    # Replace 'spielplan' with 'kader'
    if data_type == "current_stats":
        match = re.search(r"https://www.transfermarkt.com/([^/]+)/spielplan/verein/(\d+)/saison_id/(\d+)", original_url)
        if match:
            club_name_url = match.group(1)
            verein_id = match.group(2)
            saison_id = match.group(3)

            # Replace hyphens with spaces and capitalize words
            club_name_words = club_name_url.replace("-", " ").split()
            club_name_title = "-".join(word.capitalize() for word in club_name_words)

            new_url = f"https://www.transfermarkt.com/{club_name_title}/leistungsdaten/verein/{verein_id}/reldata/%26{saison_id}/plus/1"
            return new_url
        else:
            return ""
    elif data_type == "bio_page":
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

        #a_tag = tds[1].find('img')['src'].replace("tiny", "big")


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
            "transfm_stats_url": change_transfm_url(transfm_season_url ,"current_stats"),
            "transfm_bio_url": change_transfm_url(transfm_season_url, "bio_page"),
            #"logo_url": a_tag,
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

# function that takes in a League URL from Transfm and updates all the Team detials of the league
def insert_other_teams_with_logos(league_transfm_url, league_id):
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

        #a_tag = tds[1].find('a')
        a_tag = tds[1].find('img')['src'].replace("tiny", "big")

        gp = tds[3].text
        gd = tds[4].text
        points = tds[5].text

        transfm_season_url = url_header + tds[1].find('a')['href']

        team_transfm_id = re.search(r'verein/(\d+)/', transfm_season_url).group(1)

        data = {
            "team_id": random.randint(100000, 999999),
            "team_name": team_short_name,
            "team_name2": team_name,
            "curr_league_rank": int(rank),
            "curr_league_gp": int(gp),
            "curr_league_points": int(points),
            "curr_league_gd": int(gd),
            "transfm_season_url": transfm_season_url,
            "transfm_id": int(team_transfm_id),
            "transfm_stats_url": change_transfm_url(transfm_season_url ,"current_stats"),
            "transfm_bio_url": change_transfm_url(transfm_season_url, "bio_page"),
            "logo_url": a_tag,
            "league_id": league_id,
        }

        st.write(data)

        # update teams table for Prem
        try:
            resp = supabase.table("teams").insert(data).execute()
            
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

def update_player_stats(league_id):
    # get the IDS and Transfm URL of a League's Temas
    team_ids = get_ids_stats_url(league_id)

    for i in team_ids:
        team_id = i["team_id"]
        transfm_stats_url= i["transfm_stats_url"]
        transfm_bio_url= i["transfm_bio_url"]
        
        st.write(transfm_stats_url)

        try:
            soup = get_soup(transfm_stats_url)
            # get the table of data
            table = soup.find("table", class_="items")
            tr1 = table.find_all("tr", class_="odd")
            tr2 = table.find_all("tr", class_="even")
            tr3 = tr1 + tr2

            for i in tr3:
                player_trfm_link = TRANSFM_HEADER + i.find("td", class_="hauptlink").find("a")['href']

                name = i.find("table", class_="inline-table").find("span").text
                
                st.write(f'Name = {name}')

                # get the tds of all data
                tds = i.find_all("td", class_="zentriert")

                num_in_squad = handle_table_blank(tds[3].text)
                matches_played = handle_table_blank(tds[4].text)

                goals = tds[5].text
                goals = handle_table_blank(goals)

                assists = handle_table_blank(tds[6].text)
              
                yellows = handle_table_blank(tds[7].text)
                yellows2 = handle_table_blank(tds[8].text)

                reds = handle_table_blank(tds[9].text)
                subbed_on = handle_table_blank(tds[10].text)
                subbed_off = handle_table_blank(tds[11].text)

                # minutes
                minutes_td = i.find_all('td')
                minutes = convert_to_minutes(minutes_td[-1].text)
                minutes = handle_table_blank(minutes)

                now = datetime.now().isoformat()

                data = {
                    "player_name": name,
                    "transfm_url": player_trfm_link,
                    "curr_in_squad": num_in_squad,
                    "curr_gp": matches_played,
                    "curr_goals": goals,
                    "curr_minutes": minutes,
                    "curr_assists": assists,
                    "curr_ga": goals + assists,
                    "curr_subon": subbed_on,
                    "curr_suboff": subbed_off,
                    "yellows": yellows,
                    "yellow_2": yellows2,
                    "reds": reds,
                    "last_updated": now,
                }
                st.write(data)
                # for loan maybe create a second row for players on loan with id = id54321, would have to add it for scraping players

                try:
                    response = supabase.table("players").update(data).eq("player_name", name).execute()
                    st.success(response)
                except Exception as e:
                    st.error(f'Error = {e}')

                
                st.write("---------")

        except Exception as e:
            st.error(f'Error = {e}')


def update_team_nation_ids(league_id: int):
    """
    Updates the nation_id of teams in a league based on the country name.

    Args:
        supabase_client: The Supabase client object.
        league_id: The ID of the league to update.
    """
    try:
        resp1 = supabase.table("leagues").select("country").eq("league_id", league_id).execute()
        # 3. Update the nation_id of all teams in the league
        #update_response = supabase.table("teams").update({"nation_id": 5838}).eq("league_id", league_id).execute()
        nation = resp1.data[0]["country"]

        resp2 = supabase.table("teams").select("team_id").eq("team_name", nation).execute()

        nation_id = resp2.data[0]["team_id"]

        update_response = supabase.table("teams").update({"nation_id": nation_id}).eq("league_id", league_id).execute()

        st.write(update_response)

    except Exception as e:
        st.write(f"An error occurred: {e}")


endings = ["U23", "U20", "U21", "U18", "U17", "U19", "U16", "U-15", "U15", "Yth", "Yth.", "Youth", "Aca", "Academy", "Yout", "B", "II", "Sub-17", "Sub-15", "CF You"]


def update_leagues_youth_teams(team_name: str):
    try:
        resp1 = supabase.table("teams").select("logo_url, nation_id").eq("team_name", team_name).execute()
        logo = resp1.data[0]["logo_url"]

        nation_id = resp1.data[0]["nation_id"]

        for j in endings:
            new_name = team_name + " " + j
            #st.write(new_name)

            data = {
                # BE CAREFUL WHEN UNCOMENTING FOR UPDATING
                #"team_id": random.randint(100000, 999999),
                "team_name": new_name,
                "logo_url": logo,
                "league_id": 1111,
                "nation_id": nation_id,
            }


            st.write(data)


            #response = supabase.table("teams").insert()
            try:
                #resp = supabase.table("teams").insert(data).execute()
                resp = supabase.table("teams").update(data).eq("team_name", new_name).execute()

                st.write(resp)
            except Exception as e:
                    st.error(f'{new_name}')
                    st.error(f'Error = {e}')

    except Exception as e:
        st.error(f'Error = {e}')


def insert_leagues_youth_teams(team_name: str):
    try:
        resp1 = supabase.table("teams").select("logo_url, nation_id").eq("team_name", team_name).execute()
        logo = resp1.data[0]["logo_url"]

        nation_id = resp1.data[0]["nation_id"]

        for j in endings:
            new_name = team_name + " " + j
            #st.write(new_name)

            data = {
                # BE CAREFUL WHEN UNCOMENTING FOR UPDATING
                "team_id": random.randint(100000, 999999),
                "team_name": new_name,
                "logo_url": logo,
                "league_id": 1111,
                "nation_id": nation_id,
            }

            st.write(data)

            #response = supabase.table("teams").insert()
            try:
                resp = supabase.table("teams").insert(data).execute()
                #resp = supabase.table("teams").update(data).eq("team_name", new_name).execute()

                st.write(resp)
            except Exception as e:
                    st.error(f'{new_name}')
                    st.error(f'Error = {e}')

    except Exception as e:
        st.error(f'Error = {e}')



def save_player_transfers_byname(name: str):

    ids = get_player_ids(name)
    player_id = ids["player_id"]
    transfm_id = ids["transfm_id"]


    #id = "659459"
    url = f"https://www.transfermarkt.us/ceapi/transferHistory/list/{transfm_id}"
    resp = get_player_transfers(url)["transfers"]

    for i in resp:
        from_club = i["from"]["clubName"]
        from_id = get_team_id(from_club)


        to_club = i["to"]["clubName"]
        to_id = get_team_id(to_club)

        transf_date = i["dateUnformatted"]
        season = i["season"]

        value = i["marketValue"]
        value_val = parse_money_string(value)


        fee, isLoan = extract_loan_fee(i["fee"])
        fee_val = parse_money_string(fee)

        if from_id is None:
            from_id = random.randint(10000, 99999)
            from_url = i["from"]["clubEmblem-1x"].replace("tiny", "big")

            data_2 = {
                "team_name": from_club,
                "team_id": from_id,
                "logo_url": from_url
            }

            try:
                resp1 = supabase.table("teams").insert(data_2).execute()
                st.write(resp1)
            except Exception as e:
                st.error(f'Error = {e}')
        
        if to_id is None:
            to_id = random.randint(10000, 99999)
            to_url = i["to"]["clubEmblem-1x"].replace("tiny", "big")

            data_2 = {
                "team_name": to_club,
                "team_id": to_id,
                "logo_url": to_url
            }

            try:
                resp1 = supabase.table("teams").insert(data_2).execute()
                st.write(resp1)
            except Exception as e:
                st.error(f'Error = {e}')


        from_id = get_team_id(from_club)
        to_id = get_team_id(to_club)

        st.write(f"{from_club} ({from_id}) to {to_club} ({to_id})")
        
        #st.write(f"From: {from_club}")
        #st.write(f"To: {to_club}")
        st.write(f"Date: {transf_date}")
        st.write(f"Season: {season}")
        #st.write(f"Fee: {fee}")
        st.write(f"Fee: {fee_val}")
        #st.write(f"Value: {value}")
        st.write(f"Value: {value_val}")

        st.write(f"Is Loan: {isLoan}")
        #st.write(i)

        data ={
            "transfer_id": random.randint(1000000, 9999999),
            "player_id": player_id,
            "from_team_id": from_id,
            "to_team_id": to_id,
            "isLoan": isLoan,
            "fee": fee_val,
            "value": value_val,
            "date": transf_date,
            "season": season,
        }
        #st.write(data)
        
        try:
            resp = supabase.table("transfers").insert(data).execute()
            st.write(resp)
        except Exception as e:
                st.error(f'{from_club}')
                st.error(f'{to_club}')
                st.error(f'Error = {e}')
    
        st.write("----------------------")


# FOR THE SAKE OF FIXING THE PLAYERS W/o RETIRED
def update_team_past_players(team_name: str):
    year = 2023

    resp1 = supabase.table("teams").select("transfm_bio_url").eq("team_name", team_name).execute()

    stats_url = resp1.data[0]["transfm_bio_url"]

    resp2 = supabase.table("teams").select("team_id").eq("team_name", team_name).execute()
    team_id = resp2.data[0]["team_id"]

    while year > 2004:
        edit_year = f'{str(year)}'

        new_stats_url = stats_url.replace('2024', edit_year)

        st.write(new_stats_url)

        try:
            soup = get_soup(new_stats_url)
            trs = get_page_trs(soup)

            #st.write(trs)

            for i in trs:

                # all the tds with data
                tds = i.find_all('td')

                squad_num = i.find('td').text

                # check if there is a number
                match = re.search(r'\d', squad_num)
                if not match:
                    continue

                # current club
                curr_club = tds[7].find('img')['title']

                # retired
                isRetired = False

                # player id
                player_id = tds[1].find('a')['href']

                # position
                position = tds[4].text.strip()



                parts = player_id.split('/')
                if parts:
                    last_part = parts[-1]
                    if last_part.isdigit():
                        player_id = last_part
                    else:
                        player_id = None
                else:
                    player_id = None
            
                # player name
                name = tds[1].find('img')['title']
                #name = tds[1].find('a')['title']
                #name = tds[1].find('span').text
                if name == "":
                    name2 = tds[1].find_all('img')
                    name = name2[-1]['alt']

                # season
                s1 = abs(year) % 100
                s2 = s1 + 1
                season = str(s1)+"/"+str(s2)

                
                # foot
                foot = tds[9].text

                # dob
                date_age = tds[5].text.strip()
                # Split the string into date and age
                date_part = date_age.split('(')[0].strip()  # Extract the date part

                # Convert to a datetime object
                date_obj = datetime.strptime(date_part, "%b %d, %Y")

                # Format the date as YYYY-MM-DD
                iso_date = date_obj.strftime("%Y-%m-%d")


                # get the nations
                nations = []
                nation = tds[6].find_all("img")
                for j in nation:
                    nations.append(j['title'])

                # seperate the nations
                nation1 = nations[0]
                nation2 = nations[1] if len(nations) > 1 else None

                #st.write(curr_club)
                #st.write(season)



                #st.write(name)
                #st.write(season)
#
                #st.write(position)
                #st.write(f'{nation1} and {nation2}')
#
                #st.write(player_id)
                #st.write(foot)
                #st.write(iso_date)
#
                #st.write(squad_num)
                #st.write(curr_club)
                if curr_club == "Retired":
                    isRetired = True
                    #st.write("RETIRED")
                #st.write(isRetired)

                data = {
                    "isRetired": isRetired,
                    #"player_name": name,
                    "position": position,
                    "nation1": nation1,
                    "nation2": nation2,
                    "foot": foot,
                    "dob": iso_date,
                    "transfm_id": int(player_id),
                }

                #st.write(tds)
                #st.write(data)
                
                try:
                    resp = supabase.table("players").update(data).eq("player_name", name).execute()
                    st.write(resp)
                except Exception as e:
                    st.error(f'Error = {e}')
                
                #year_int = int(year_string)
                #date_object = datetime(year, 1, 1).isoformat()

                resp3 = supabase.table("players").select("player_id").eq("player_name", name).execute()

                player_id = resp3.data[0]["player_id"]
    
                st.write("--------------------")

            #st.write(trs)
        except Exception as e:
            st.error({e})

        year = year - 1




def insert_team_past_players(team_name: str):
    year = 2023

    resp1 = supabase.table("teams").select("transfm_bio_url").eq("team_name", team_name).execute()

    stats_url = resp1.data[0]["transfm_bio_url"]

    resp2 = supabase.table("teams").select("team_id").eq("team_name", team_name).execute()
    team_id = resp2.data[0]["team_id"]

    while year > 2004:
        edit_year = f'{str(year)}'

        new_stats_url = stats_url.replace('2024', edit_year)

        st.write(new_stats_url)

        try:
            soup = get_soup(new_stats_url)
            trs = get_page_trs(soup)

            #st.write(trs)

            for i in trs:

                # all the tds with data
                tds = i.find_all('td')

                squad_num = i.find('td').text

                # check if there is a number
                match = re.search(r'\d', squad_num)
                if not match:
                    continue

                # current club
                curr_club = tds[7].find('img')['title']

                # retired
                isRetired = False

                # player id
                player_id = tds[1].find('a')['href']

                # position
                position = tds[4].text.strip()



                parts = player_id.split('/')
                if parts:
                    last_part = parts[-1]
                    if last_part.isdigit():
                        player_id = last_part
                    else:
                        player_id = None
                else:
                    player_id = None
            
                # player name
                name = tds[1].find('img')['title']
                #name = tds[1].find('a')['title']
                #name = tds[1].find('span').text
                if name == "":
                    name2 = tds[1].find_all('img')
                    name = name2[-1]['alt']

                # season
                s1 = abs(year) % 100
                s2 = s1 + 1
                season = str(s1)+"/"+str(s2)

                
                # foot
                foot = tds[9].text

                # dob
                date_age = tds[5].text.strip()
                # Split the string into date and age
                date_part = date_age.split('(')[0].strip()  # Extract the date part

                # Convert to a datetime object
                date_obj = datetime.strptime(date_part, "%b %d, %Y")

                # Format the date as YYYY-MM-DD
                iso_date = date_obj.strftime("%Y-%m-%d")


                # get the nations
                nations = []
                nation = tds[6].find_all("img")
                for j in nation:
                    nations.append(j['title'])

                # seperate the nations
                nation1 = nations[0]
                nation2 = nations[1] if len(nations) > 1 else None

                #st.write(curr_club)
                #st.write(season)



                #st.write(name)
                #st.write(season)
#
                #st.write(position)
                #st.write(f'{nation1} and {nation2}')
#
                #st.write(player_id)
                #st.write(foot)
                #st.write(iso_date)
#
                #st.write(squad_num)
                #st.write(curr_club)
                if curr_club == "Retired":
                    isRetired = True
                    #st.write("RETIRED")
                #st.write(isRetired)

                data = {
                    "player_id": random.randint(1000000, 9999999),
                    "isRetired": isRetired,
                    "player_name": name,
                    "position": position,
                    "nation1": nation1,
                    "nation2": nation2,
                    "foot": foot,
                    "dob": iso_date,
                    "transfm_id": int(player_id),
                }

                #st.write(tds)
                #st.write(data)
                
                try:
                    resp = supabase.table("players").insert(data).execute()
                    st.write(resp)
                except Exception as e:
                    st.error(f'Error = {e}')
                
                #year_int = int(year_string)
                #date_object = datetime(year, 1, 1).isoformat()


                #st.write(data2)"
                
    
                st.write("--------------------")

            #st.write(trs)
        except Exception as e:
            st.error({e})

        year = year - 1



def insert_team_past_stats(team_name: str):
    year = 2023

    resp1 = supabase.table("teams").select("transfm_stats_url").eq("team_name", team_name).execute()

    stats_url = resp1.data[0]["transfm_stats_url"]

    resp2 = supabase.table("teams").select("team_id").eq("team_name", team_name).execute()
    team_id = resp2.data[0]["team_id"]

    while year > 2004:
        edit_year = f'{str(year)}'

        new_stats_url = stats_url.replace('2024', edit_year)

        st.write(new_stats_url)

        try:
            soup = get_soup(new_stats_url)
            trs = get_page_trs(soup)

            #st.write(trs)

            for i in trs:

                # all the tds with data
                tds = i.find_all('td')

                squad_num = i.find('td').text
                

                # check if there is a number
                match = re.search(r'\d', squad_num)
                if not match:
                    continue

                min = tds[-1].text

                match2 = re.search(r'\d', min)
                if not match2:
                    continue


                # player id
                #player_id = tds[1].find('a')['href']

                # player name
                #name = tds[1].find('a')['title']
                name = tds[1].find('span').text

                
                if name == "":
                    name2 = tds[1].find_all('img')
                    name = name2[-1]['alt']
                

                # minutes
                
                minutes = convert_to_minutes(min)

                # subbed off
                sub_off = tds[-3].text
                match = re.search(r'\d', sub_off)
                if not match:
                    sub_off = 0

                # subbed on
                sub_on = tds[-4].text
                match = re.search(r'\d', sub_on)
                if not match:
                    sub_on = 0

                # red 
                red = tds[-5].text
                match = re.search(r'\d', red)
                if not match:
                    red = 0

                # yellows2 
                yellows2 = tds[-6].text
                match = re.search(r'\d', yellows2)
                if not match:
                    yellows2 = 0

                # yellows 
                yellows = tds[-7].text
                match = re.search(r'\d', yellows)
                if not match:
                    yellows = 0

                # asssists 
                assists = tds[-8].text
                match = re.search(r'\d', assists)
                if not match:
                    assists = 0
                
                # goals 
                goals = tds[-9].text
                match = re.search(r'\d', goals)
                if not match:
                    goals = 0
                
                # gp 
                gp = tds[-10].text
                match = re.search(r'\d', gp)
                if not match:
                    gp = 0


                # season
                s1 = abs(year) % 100
                s2 = s1 + 1
                season = str(s1)+"/"+str(s2)

                #st.write(curr_club)
                #st.write(season)
                now = datetime.now().isoformat()


                

                resp3 = supabase.table("players").select("player_id").eq("player_name", name).execute()

                if resp3.data and len(resp3.data) > 0: # check if the response data is not empty
                    player_id = resp3.data[0]["player_id"]
                else:
                    continue
                #player_id = resp3.data["player_id"]
                
                st.write(name)
                data = {
                    "player_id": player_id,
                    "season": season,
                    "league_id": 9999,
                    "team_id": team_id,
                    "goals": int(goals),
                    "assists": int(assists),
                    "ga": int(goals) + int(assists),
                    "gp": int(gp),
                    "minutes": float(minutes),
                    "yellows": int(yellows),
                    "yellows2": int(yellows2),
                    "reds": int(red),
                    "season_year": year,
                    "squad_number": int(squad_num),
                    "subbed_on": int(sub_on),
                    "subbed_off": int(sub_off),
                    "last_updated": now,
                }

                #st.write(data)
                
                try:
                    resp = supabase.table("player_stats").insert(data).execute()
                    st.write(resp)
                except Exception as e:
                    st.error(f'Error = {e}')
                                
    
                st.write("--------------------")

            #st.write(trs)
        except Exception as e:
            st.error({e})

        year = year - 1





def update_curr_stats(team_name: str, action: str):
    year = 2024

    resp1 = supabase.table("teams").select("transfm_stats_url").eq("team_name", team_name).execute()

    stats_url = resp1.data[0]["transfm_stats_url"]

    resp2 = supabase.table("teams").select("team_id").eq("team_name", team_name).execute()
    team_id = resp2.data[0]["team_id"]

    while year > 2004:
        #edit_year = f'{str(year)}'

        #new_stats_url = stats_url.replace('2024', edit_year)

        st.write(stats_url)

        try:
            soup = get_soup(stats_url)
            trs = get_page_trs(soup)

            #st.write(trs)

            for i in trs:

                # all the tds with data
                tds = i.find_all('td')

                squad_num = i.find('td').text

                # check if there is a number
                match = re.search(r'\d', squad_num)
                if not match:
                    continue
            
                # player name
                #name = tds[1].find('img')['title']
                #name = tds[1].find('a')['title']
                name = tds[1].find('span').text
                if name == "":
                    name2 = tds[1].find_all('img')
                    name = name2[-1]['alt']

                resp3 = supabase.table("players").select("player_id").eq("player_name", name).execute()

                if resp3.data and len(resp3.data) > 0: # check if the response data is not empty
                    player_id = resp3.data[0]["player_id"]
                else:
                    continue


                
                # minutes
                min = tds[-1].text
                minutes = convert_to_minutes(min)

                # subbed off
                sub_off = tds[-3].text
                match = re.search(r'\d', sub_off)
                if not match:
                    sub_off = 0

                # subbed on
                sub_on = tds[-4].text
                match = re.search(r'\d', sub_on)
                if not match:
                    sub_on = 0

                # red 
                red = tds[-5].text
                match = re.search(r'\d', red)
                if not match:
                    red = 0

                # yellows2 
                yellows2 = tds[-6].text
                match = re.search(r'\d', yellows2)
                if not match:
                    yellows2 = 0

                # yellows 
                yellows = tds[-7].text
                match = re.search(r'\d', yellows)
                if not match:
                    yellows = 0

                # asssists 
                assists = tds[-8].text
                match = re.search(r'\d', assists)
                if not match:
                    assists = 0
                
                # goals 
                goals = tds[-9].text
                match = re.search(r'\d', goals)
                if not match:
                    goals = 0
                
                # gp 
                gp = tds[-10].text
                match = re.search(r'\d', gp)
                if not match:
                    gp = 0

                # season
                s1 = abs(year) % 100
                s2 = s1 + 1
                season = str(s1)+"/"+str(s2)

        
                now = datetime.now().isoformat()

                data = {
                    "player_id": player_id,
                    "season": season,
                    "league_id": 9999,
                    "team_id": team_id,
                    "goals": int(goals),
                    "assists": int(assists),
                    "ga": int(goals) + int(assists),
                    "gp": int(gp),
                    "minutes": float(minutes),
                    "yellows": int(yellows),
                    "yellows2": int(yellows2),
                    "reds": int(red),
                    "season_year": year,
                    "squad_number": int(squad_num),
                    "subbed_on": int(sub_on),
                    "subbed_off": int(sub_off),
                    "last_updated": now,
                }

                #st.write(tds)
                #st.write(data)
                if action == "insert": 
                    try:
                        resp = supabase.table("player_stats").insert(data).execute()
                        st.write(resp)
                    except Exception as e:
                        st.error(f'Error = {e}')
                
                elif action == "update":
                    try:
                        resp = supabase.table("player_stats").upsert(data).execute()
                        st.write(resp)
                    except Exception as e:
                        st.error(f'Error = {e}')

                
                    st.write("--------------------")

            #st.write(trs)
        except Exception as e:
            st.error({e})

        year = year - 1


def update_or_insert_teams_current_players(team_name):
    resp1 = supabase.table("teams").select("transfm_bio_url").eq("team_name", team_name).execute()

    stats_url = resp1.data[0]["transfm_bio_url"]

    resp2 = supabase.table("teams").select("team_id").eq("team_name", team_name).execute()
    team_id = resp2.data[0]["team_id"]

    # get the tr elements of each player 
    soup = get_soup(stats_url)
    table = soup.find("table", class_="items")
    
    tr1 = table.find_all("tr", class_="odd")
    tr2 = table.find_all("tr", class_="even")
    tr3 = tr1 + tr2

    
    try:
            
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

            now = datetime.now().isoformat()
            
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

                resp3 = supabase.table("players").select("player_id").eq("player_name", name).execute()

                if resp3.data and len(resp3.data) > 0: # check if the response data is not empty
                    player_id = resp3.data[0]["player_id"]
                    data = {
                        "player_name": name,
                        "nation1": nation1,
                        "nation2": nation2,
                        "player_id": player_id,
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
                        "last_updated": now,
                        "isRetired": False,
                    }

                    try:
                        resp = supabase.table("players").update(data).eq("player_id", player_id).execute()
                        st.write(f'{name}')
                        st.write(resp)
                    except Exception as e:
                        st.error(f'{name}')
                        st.error(f'Error = {e}')



                else:
                    data = {
                        "player_name": name,
                        "nation1": nation1,
                        "nation2": nation2,
                        "player_id": random.randint(1000000, 9999999),
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
                        "last_updated": now,
                        "isRetired": False,
                    }
                    #continue
                    try:
                        resp = supabase.table("players").insert(data).execute()
                        st.write(resp)
                    except Exception as e:
                        st.error(f'{name}')
                        st.error(f'Error = {e}')

                
            except Exception as e:
                st.error(f'{name}')
                st.error(f'Error = {e}')


    except Exception as e:
        st.error(f'Error = {e}')
        

    return None










