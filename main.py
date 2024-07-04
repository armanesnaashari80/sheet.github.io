import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("C:/Users/Alijenab/PycharmProjects/pythonProject15/booming-voice-427922-g9-2639ea16e492.json", scopes=scope)
client = gspread.authorize(creds)

sheet_url = "https://docs.google.com/spreadsheets/d/1zs_jjSotWm0Xb09NfVzamGEpzJkX-Gw1FEKBNtuju_0/edit?usp=sharing"
sheet = client.open_by_url(sheet_url).sheet1

def get_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def add_data_to_sheet(data):
    sheet.append_row(data)

def update_data_in_sheet(row_index, data):
    for col, value in enumerate(data, start=1):
        sheet.update_cell(row_index + 2, col, value)

def delete_data_in_sheet(row_index):
    sheet.delete_rows(row_index + 2)

st.set_page_config(
    page_title="My Google Sheet",
    page_icon="📈📉",
    layout="wide",
)

st.markdown("""
    <style>
        .main {
            background-color: #000000;
            color: #FFFFFF;
        }
        h1, h2 {
            color: #FFD700;
        }
        .stButton button {
            background-color: #FFD700;
            color: #000000;
        }
        .stTextInput input {
            border: 2px solid #FFD700;
            padding: 10px;
            border-radius: 5px;
            background-color: #333333;
            color: white;
        }
        .stDataFrame {
            background-color: white;
            color: black;
        }
        .css-1cpxqw2 a {
            color: #FFD700;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📈 My Google Sheet 📉")

st.header("⬇ My Data ⬇")
data = get_data()
st.dataframe(data, width=1000, height=400)

st.header("➕ Add New Data")
with st.form(key='add_data_form'):
    new_data = {}
    columns = data.columns
    for column in columns:
        new_data[column] = st.text_input(f"Enter {column}", "")

    submit_button = st.form_submit_button(label='Add Data')

if submit_button:
    if any(new_data.values()):
        add_data_to_sheet(list(new_data.values()))
        st.success("Data added successfully")
        st.experimental_rerun()
    else:
        st.error("Please fill in at least one field.")

data = get_data()
st.header("📄 Updated Data")
st.dataframe(data, width=1000, height=400)

st.header("✏️ Edit Data")
selected_row = st.number_input("Enter the row number to edit", min_value=1, max_value=len(data))
if selected_row:
    with st.form(key='edit_data_form'):
        row_data = data.iloc[selected_row-1].to_dict()
        new_data = {}
        for column, value in row_data.items():
            new_data[column] = st.text_input(f"Enter new {column}", value)

        update_button = st.form_submit_button(label='Update Data')

    if update_button:
        if any(new_data.values()):
            update_data_in_sheet(selected_row, list(new_data.values()))
            st.success("Data updated successfully")
            st.experimental_rerun()
        else:
            st.error("Please fill in at least one field.")

    data = get_data()
    st.dataframe(data, width=1000, height=400)

st.header("❌ Delete Data")
delete_row = st.number_input("Enter the row number to delete", min_value=1, max_value=len(data))
delete_button = st.button(label='Delete Data')

if delete_button:
    delete_data_in_sheet(delete_row)
    st.success("Data deleted successfully")
    st.experimental_rerun()

    data = get_data()
    st.dataframe(data, width=1000, height=400)
