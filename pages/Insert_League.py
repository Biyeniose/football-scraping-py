import streamlit as st
import sys, random, json, re

st.title("Page for Inserting Teams from a league")
st.write("Make sure the League is already in Supabase and you know the id")
st.write("Use a json file with all Team names and Logo URL")

st.write("After this you can go to Scrape Players page and run the code to Update with Transfermarket IDs and URLs then Scrape players")
