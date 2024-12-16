import streamlit as st

# Set up Streamlit's configuration
st.set_page_config(page_title="Goal Archive Data Entry", layout="centered")

# Main welcome page content
def welcome_page():
    st.title("Welcome to Goal Archive Data Entry")
    st.write("This is a data entry UI for goal-archive.com")

# Display the main page based on selected navigation
if __name__ == "__main__":
    welcome_page()
