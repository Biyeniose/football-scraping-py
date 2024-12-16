# src/supabase/insert_functions.py
from init_supabase import supabase
import requests


def insert_player(player_data):
    """
    Inserts a player record into the players table in Supabase.

    Parameters:
        player_data (dict): A dictionary with player details, e.g., {'name': 'John Doe', 'position': 'Forward', 'goals': 10}
    """
    response = supabase.table("players").insert(player_data).execute()
    
    # Check for success or failure based on the response structure
    if response.data:
        return {"success": True, "data": response.data}
    elif response.error.code:
        return {"success": False, "message": [response.error.code, response.error.name]}
    else:
        return {"success": False, "message": "Unknown error occurred"}
    

def get_gb(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        # Print the result
        #print("Data retrieved successfully:")
        return(data)
    else:
        err_msg = f"Failed to retrieve data. Status code: {response.status_code}"
        return err_msg 
        #print(f"Failed to retrieve data. Status code: {response.status_code}")

