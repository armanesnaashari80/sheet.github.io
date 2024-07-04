import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Replace 'credentials.json' with the path to your JSON credentials file
credentials = ServiceAccountCredentials.from_json_keyfile_name('booming-voice-427922-g9-2e055ec58a87', scope)
client = gspread.authorize(credentials)

# Now 'client' can be used to interact with Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1zs_jjSotWm0Xb09NfVzamGEpzJkX-Gw1FEKBNtuju_0/edit?usp=sharing"
sheet = client.open_by_url(sheet_url).sheet1

# Example: Print the title of the first sheet
print(sheet.title)
