# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
from random import shuffle
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('top_trumps')

##player_cards = []
##computer_cards = []

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
    Pull the list of worksheet names from the workbook.
    Displays them to the user as a list of available game decks.
    Returns a list of game decks.
    """    
    decks = []
    print(f'Available decks:\n')
    for sh in SHEET.worksheets():
        decks.append(sh.title)
        print(f'{sh.title}')
    return decks

def choose_deck(decks):
    """
    Prompt the user to select which deck to use and return the choice
    """
    deck_choice = input("Which deck to use?\n")
    if deck_choice.lower() in decks:
        return deck_choice.lower()
    else:
        print('Invalid choice, please type the deck name correctly.')
        choose_deck(decks)


def get_cards(deck):
    """
    Get the deck data from the chosen google sheet. First row is the catgories.
    Returns a list of categories and cards.
    """
    cards = SHEET.worksheet(deck).get_all_values()
    categories = cards.pop(0)
    return categories, cards

def shuffle_and_deal(cards):
    """
    Takes a deck of cards in a list, shuffles them and deals them to two players.
    If the number of cards in the deck is odd, the last card is removed after the shuffle.
    2 lists (hands) of cards are returned, one for the player and one for the computer
    """
    hand_one = []
    hand_two = []
    shuffle(cards)
    
    if len(cards) % 2 != 0:
        cards.pop()
    
    for i in range(0,len(cards),2):
        hand_one.append(cards[i])
        hand_two.append(cards[i+1])

    return hand_one, hand_two

def display_game_state(num1, num2):
    """
    Takes two numbers and displays them in a table, showing the number of cards remaining
    for each player
    """
    table = PrettyTable()
    table.field_names = ["Player", "Cards Remaining"]
    table.add_rows ([
        ["Player", num1],
        ["Computer", num2] 
    ])
    
    print(table)

def display_next_card(categories, card):
    """
    Takes two lists as parameters of equal length and displays them in columns  input Shows the next card in the player's hand to be played.
    """
    table = PrettyTable()
    table.add_column("#", ["",1,2,3,4,5,6])
    table.add_column("Category", categories)
    table.add_column("Player Card", card)
    print (table)

def player_choose_category():
    """
    Asks the user to input a numer 1-6 corresponding to the displayed categories.
    Returns an integer 1-6
    """
    try:
        cat = int(input('Player, choose the category to play (1-6)\n'))
        if cat > 0 and cat < 7:
            return cat
        else: 
            print("Invalid input. Must be a number between 1 and 6, try again\n")
            player_choose_category()
    except (ValueError):
            print("That's not even an integer, it must be an integer between 1 and 6, try again..\n")
            player_choose_category()

def computer_choose_category():
    cat = random.randrange(6) + 1
    return cat

def run_game(deck):
    """
    Runs a game of top trumps with the chosen deck
    """
    player_turn = False 
    categories, all_cards = get_cards(deck)
    ##print(all_cards)
    player_cards, computer_cards = shuffle_and_deal(all_cards)
    ##print(categories)
    ##print(f'P1: {player_cards}')
    ##print(f'P2: {computer_cards}')
    display_game_state(len(player_cards), len(computer_cards))
    display_next_card(categories, player_cards[0])
    if player_turn == True:
        chosen_category = player_choose_category()
        print(f'You have chosen to play the category: {categories[chosen_category]}\n')
    else:
        chosen_category = computer_choose_category()
        print(f'The computer has chosen to play the category: {categories[chosen_category]}\n')

def main():
    """
    Runs the main program
    """
    option = play_or_edit()
    all_decks = get_decks()
    chosen_deck = choose_deck(all_decks)
    
    if option == 'p':
        print(f'Chosen deck = {chosen_deck}')
        run_game(chosen_deck)
        
main()