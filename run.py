# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('top_trumps')

#golfers = SHEET.worksheet('golfers')

#data = golfers.get_all_values()

#print(data)

def play_or_edit():
    """
    Gets input from the user whether to play a game or edit a databse
    """
    print('Welcome to Top Trumps. What would you like to do?\n')
    choice = ""
    valid = {'p', 'd', 'i'}
    while choice.lower() not in valid:
        choice = input("P - Play a game of Top Trumps\nD - Edit / View the game data\nI - Instructions\n")
        if choice.lower() in valid:
            return choice.lower()
        else:
            print(f"Invalid input, please choose either 'P', 'D' or 'I'")

            
def get_decks():
    """
    Pulls the list of worksheet names from the workbook.
    Displays them to the user as a list of available game decks.
    Returns a list of game decks.
    """    
    decks = []
    print(f'Available decks:\n')
    for sh in SHEET.worksheets():
        decks.append(sh.title)
        print(f'{sh.title}')
    return decks
    
def main():
    """
    Runs the main program
    """
    option = play_or_edit()
    all_decks = get_decks()
    ##deck = choose_deck()


main()