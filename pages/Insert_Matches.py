import streamlit as st
import sys, random, json, re, os
sys.path.append("src")
from src.init_supabase import supabase
from scraping import get_soup, match_result, get_team_info


st.title("Insert matches")

wiki_url = "https://en.wikipedia.org/wiki/2024%E2%80%9325_Premier_League"

st.subheader("EPL Matches")

team_names =[]
if st.button("Button for inserting EPL matches"):
    soup = get_soup(wiki_url)

    table = soup.find("table", class_="wikitable plainrowheaders")
    trs = table.find_all('tr')

    #st.write(trs)
    for i in trs[1:]:
        team_name = i.find('th').text
        team_names.append(team_name)

    for i in trs[1:]:
        team_name = i.find('th').text.strip()

        home_team_data = get_team_info(team_name)


        st.write(home_team_data["team_name"])

        tds = i.find_all("td")

        for j, k in enumerate(tds, start=0):  # start=1 to count from 1
            score = k.text.strip()
            if score in ("", " ", "—", "a"):
               continue 

            st.write(score)

            opponent = team_names[j]
            st.write(f"Oppenent = {opponent}")

            away_team_data = get_team_info(opponent.strip())
            #st.write(data)
            st.write(f"Oppenent ID = {away_team_data["team_id"]}")


            data = {
                "league_id": 2,
                "year": "2024-01-01",
                "home_team": home_team_data["team_name"],
                "home_id": home_team_data["team_id"],
                "home_logo": home_team_data["logo_url"],
                "away_team": away_team_data["team_name"],
                "away_id": away_team_data["team_id"],
                "away_logo": away_team_data["logo_url"],
                "home_goals": int(score[0]),
                "away_goals": int(score[2]),
                "result": match_result(score=score)
            }

            #st.write(data)

            response = (
                supabase.table("matches")
                .insert(data)
                .execute()
            )

            st.write(response)




    
