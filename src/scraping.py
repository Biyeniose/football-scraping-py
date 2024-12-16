import re, requests, sys, json, random, os, re
from bs4 import BeautifulSoup
#from supabase import create_client, Client
from src.init_supabase import supabase  # Import the supabase client from src/init_supabase

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

# returns an array of trs containing data in the soup element
def get_page_trs(soup):
    # soup = get_soup("https://www.transfermarkt.com/aston-villa/leistungsdaten/verein/405/reldata/%262023/plus/1")
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



