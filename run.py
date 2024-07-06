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


def play_or_edit():
    """
    Gets input from the user whether to play a game or edit a databse
    """
    print('Welcome to Top Trumps. What would you like to do?\n')
    choice = ""
    valid = {'p', 'd', 'i'}
    while choice.lower() not in valid:
        choice = input("P - Play a game of Top Trumps\nD - Edit / View the \
game data\nI - Instructions\n")
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
    print(f'decks {decks}')
    print(f'deck choice {deck_choice}')
    if deck_choice.lower() in decks:
        return deck_choice.lower()
    else:
        print('Invalid choice, please type the deck name correctly.')
        choose_deck(decks)


def get_cards(deck):
    """
    Get the deck data from the chosen google sheet.
    First row is the catgories.
    Second row provides winning criteria for each category (high / low)
    Returns a list of categories, criteria and cards.
    """
    cards = SHEET.worksheet(deck).get_all_values()
    categories = cards.pop(0)
    criteria = cards.pop(0)
    print(criteria)
    return categories, criteria, cards


def shuffle_and_deal(cards):
    """
    Takes a deck of cards in a list, shuffles them and deals them to two
    players. If the number of cards in the deck is odd, the last card is
    removed after the shuffle. 2 lists (hands) of cards are returned, one for
    the player and one for the computer.
    """
    hand_one = []
    hand_two = []
    shuffle(cards)

    if len(cards) % 2 != 0:
        cards.pop()

    for i in range(0, len(cards), 2):
        hand_one.append(cards[i])
        hand_two.append(cards[i+1])

    return hand_one, hand_two


def display_game_state(num1, num2):
    """
    Takes two numbers and displays them in a table, showing the number of cards
    remaining for each player.
    """
    table = PrettyTable()
    table.field_names = ["Player", "Cards Remaining"]
    table.add_rows([
        ["Player", num1],
        ["Computer", num2]
    ])

    print(table)
    input("Press any key to see your next card.\n")


def display_next_card(categories, card):
    """
    Takes two lists as parameters of equal length and displays them in columns.
    Shows the player their next card to be played.
    """
    print("\nHere's your next card..\n")
    table = PrettyTable()
    table.add_column("#", ["", 1, 2, 3, 4, 5, 6])
    table.add_column("Category", categories)
    table.add_column("Player Card", card)
    print(f'{table}\n')


def player_choose_category():
    """
    Asks the user to input a numer 1-6 corresponding to the displayed
    categories. Returns an integer 1-6.
    """
    try:
        cat = int(input('Player, choose the category to play (1-6)\n'))
        if cat > 0 and cat < 7:
            return cat
        else:
            print("Invalid input. Must be an integer 1-6, try again.\n")
            player_choose_category()
    except (ValueError):
        print("That's not even an integer, it must be a number\
        1-6, try again...\n")
        player_choose_category()


def computer_choose_category():
    """
    Return an integer 1 - 6 to indicate the chosen category to display.
    Logic is to return a random selection
    """
    cat = random.randrange(6) + 1
    input("Press any key to see the Computer's chosen category.\n")
    return cat


def create_column(row):
    """
    Takes an integer 1-6 as a parameter and creates a list, which is displayed
    next to the displayed cards showing which category was chosen for this
    comparison.
    """
    column = [""]
    for i in range(1, 7):
        if i == row:
            column.append("<<<<< ?? >>>>>")
        else:
            column.append("")
    return column


def display_both_cards(categories, card_p, card_c, selected):
    """
    Takes 4 lists and displays them all as columns
    Displays the computer card to the user as a column in the table.
    Returns the table.
    """
    table = PrettyTable()
    table.add_column("#", ["", 1, 2, 3, 4, 5, 6])
    table.add_column("Category", categories)
    table.add_column("Player Card", card_p)
    table.add_column("Chosen Category", selected)
    table.add_column("Computer Card", card_c)
    print(f'{table}\n')
    input("Press any key to confirm the winner\n")
    return table


def get_winner(criteria, play, comp, turn):
    """
    Takes the player and computer values for selected category, and winning
    criteria as parameters category. Compares the values and returns the
    result: p (player), c (computer) or t (tie) and True or False for the
    player_turn variable.
    """
    criteria = criteria.lower()
    
    if int(play) > int(comp):
        if criteria == "h":
            return "p", True
        else:
            return "c" , False
    elif int(play) < int(comp):
        if criteria == "h":
            return "c" , False
        else:
            return "p" , True
    else:
        return "t" , True, turn


def process_winner(winner, p_hand, c_hand, held):
    """
    Declares the winner to the terminal and adds the played cards to the bottom
    of their pile. In the event of a tie, the cards are placed into the hold
    list.
    """
    c_card = c_hand.pop(0)
    p_card = p_hand.pop(0)

    match winner:
        case 'c':
            print(f'Computer wins!\n')
            c_hand.append(c_card)
            c_hand.append(p_card)

            for i in range(0, len(held)):
                c_hand.append(held[i])
            held=[]

        case 'p':
            print(f'You win this one!\n')
            p_hand.append(p_card)
            p_hand.append(c_card)

            for i in range(0, len(held)):
                p_hand.append(held[i])
            held=[]

        case 't':
            print(f"It's a tie! Cards are held for the next winner.\n")
            held.append(p_card)
            held.append(c_card)


def end_game_check(p_cards_left, c_cards_left):
    """
    Takes the number of cards remaining in each hand as parameters.
    At least one of the numbers must be zero for the function to be called
    Prints the winner to the terminal and asks user to play again.
    Returns y or n as a string
    """
    if p_cards_left == 0 & c_cards_left == 0:
        print("Game Over! It's a draw.\n") 
    elif p_cards_left == 0:
        print("Oh no! Computer wins! Better luck next time.\n")
    else: 
        print("Congratulations! You win!\n")

    again = input("Play Again? Y/N\n")
    # Validate input!
    return again.lower()


def run_game(deck):
    """
    Runs a game of top trumps with the chosen deck
    """
    player_turn = True
    held_cards = []
    the_end = False
    categories, criteria, all_cards = get_cards(deck)
    
    player_cards, computer_cards = shuffle_and_deal(all_cards)
    
    while the_end == False:

        display_game_state(len(player_cards), len(computer_cards))
        display_next_card(categories, player_cards[0])
        if player_turn is True:
            chosen_category = player_choose_category()
            print(f'You have chosen to play the category: \
{categories[chosen_category]}\n')
        else:
            chosen_category = computer_choose_category()
            print(f'The computer has chosen to play the category: \
{categories[chosen_category]}\n')

        cat_column = create_column(chosen_category)
        show = display_both_cards(categories, player_cards[0], computer_cards[0],
        cat_column)

        num = chosen_category

        winner, player_turn = get_winner(criteria[num], player_cards[0][num],
        computer_cards[0][num], player_turn)

        process_winner(winner, player_cards, computer_cards, held_cards)

        if min(len(player_cards), len(computer_cards)) < 1:
            the_end = True

    play_again = end_game_check(len(player_cards), len(computer_cards))
    return play_again


def main():
    """
    Runs the main program
    """
    option = play_or_edit()
    all_decks = get_decks()
    chosen_deck = choose_deck(all_decks)

    if option == 'p':
        print(f'Chosen deck = {chosen_deck}')
        another_game = run_game(chosen_deck)

    print(another_game)


main()
