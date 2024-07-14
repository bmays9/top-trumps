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
    Gets input from the user whether to play a game or edit a database
    Returns the choice in lower case
    """
    print('\n\n*** WELCOME TO TOP TRUMPS ***\n')
    print('A fun and challenging version of the classic game for 1 player.\n')
    print('What would you like to do?\n')
    choice = ""
    valid = {'p', 'e', 'i'}
    while choice.lower() not in valid:
        choice = input("P - Play a game of Top Trumps\nE - Edit / View the \
game data\nI - Instructions\n\nEnter choice:\n")
        if choice.lower() in valid:
            return choice.lower()
        else:
            print(f"Invalid input, please choose either 'P', 'E' or 'I'")


def get_decks():
    """
    Pull the list of worksheet names from the workbook.
    Displays them to the user as a list of available game decks.
    Returns a list of game decks.
    """
    decks = []
    print(f'\nAvailable decks:\n')
    for sh in SHEET.worksheets():
        decks.append(sh.title)
        print(f'{sh.title}')
    return decks


def choose_deck(decks):
    """
    Takes one parameter which is a list of deck names.
    Prompt the user to select which deck to use and validates against the list
    Returns the validated choice
    """
    deck_choice = ""
    while deck_choice.lower() not in decks:
        deck_choice = input("\nWhich deck to use? (type the full name)\n")

        if deck_choice.lower() in decks:
            return deck_choice.lower()
        else:
            print('Invalid choice, please type the deck name correctly.')


def get_cards(deck):
    """
    Takes one parameter which is the name of the deck.
    Get the deck data from the chosen google sheet.
    First row is the catgories.
    Second row provides winning criteria for each category (high / low)
    Returns a list of categories, criteria and cards.
    """
    cards = SHEET.worksheet(deck).get_all_values()
    categories = cards.pop(0)
    criteria = cards.pop(0)
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
    Takes two lists as parameters of equal length (6) and displays them in
    columns.
    card = players next card and this prints it to the terminal
    """
    print("\nHere's your card..\n")
    table = PrettyTable()
    table.add_column("#", ["", 1, 2, 3, 4, 5, 6])
    table.add_column("Category", categories)
    table.add_column("Player Card", card)
    print(f'{table}\n')


def player_choose_category():
    """
    Asks the user to input a number 1-6 corresponding to the displayed
    categories. Returns the validated integer value.
    """
    valid = ["1", "2", "3", "4", "5", "6"]
    cat = ""
    while True:
        cat = input('Player, choose the category to play (1-6)\n')
        if cat in valid:
            return int(cat)
        else:
            print("Invalid input. Must be an integer 1-6, try again.\n")


def computer_choose_category():
    """
    Return an integer 1 - 6 to indicate the chosen category to play.
    Logic is to return a random selection.
    """
    cat = random.randrange(6) + 1
    input("Press any key to see the Computer's chosen category.\n")
    return cat


def create_column(row):
    """
    Takes an integer 1-6 as a parameter and creates a list. The number
    reflects the chosen category, which is printed next to the displayed
    cards in the terminal.
    Returns a list of strings, with only one value.
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
    Takes 4 lists and displays them all as columns.
    caatgories is the list of categories on the card.
    card_p is the player's card
    card_c is the computers's card
    selected is the list
    Function displays the computer card to the user as a column in
    the table and returns the table.
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


def get_winner(criteria, play, comp, p_turn):
    """
    Takes four variables as arguments
    criteria - "h" or "l" to control if the highest or lowest number wins
    play - the player's card value for the selected category
    comp - the computer's card value for the selected category
    p_turn - True or False indicating whether it was the player's choice.
    The function compares the values and returns the result:
    "p" (player), "c" (computer) or "t" (tie) and True or False for the
    player_turn variable.
    """
    criteria = criteria.lower()

    if int(play) > int(comp):
        if criteria == "h":
            return "p", True
        else:
            return "c", False
    elif int(play) < int(comp):
        if criteria == "h":
            return "c", False
        else:
            return "p", True
    else:
        return "t", p_turn


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
            held = []

        case 'p':
            print(f'You win this one!\n')
            p_hand.append(p_card)
            p_hand.append(c_card)

            for i in range(0, len(held)):
                p_hand.append(held[i])
            held = []

        case 't':
            print(f"It's a tie! Cards are held for the next winner.\n")
            held.append(p_card)
            held.append(c_card)

    return held


def end_game_check(p_cards_left, c_cards_left):
    """
    Takes the number of cards remaining in each hand as parameters.
    At least one of the numbers must be zero for the function to be called
    Prints the winner to the terminal and asks user to play again.
    Returns y or n as a string
    """
    if p_cards_left == 0 and c_cards_left == 0:
        print("Game Over! It's a draw.\n")
    elif p_cards_left == 0:
        print("Oh no! Computer wins! Better luck next time.\n")
    else:
        print("Congratulations! You win this game!\n")

    print('Enter "Y" to play again with the same deck,')
    print('"M" to return to the main menu, or')
    print('"Q" to quit.')
    again = input("\nPlease choose:\n")

    return again.lower()


def get_all_names(deck):
    '''
    Pulls the list of card names from the spreadsheet.
    Card names are in Column A from Row 3 onwards.
    Returns the list of names.
    '''
    names = SHEET.worksheet(deck).col_values(1)
    names.pop(0)
    names.pop(0)
    return names


def display_all_names(names):
    """
    Takes a list of names and prints them in a table.
    Table Rows are numbered.
    """
    print("\nHere's the list of cards in the deck:\n")
    row_num = [i for i in range(1, len(names)+1)]
    table = PrettyTable()
    table.add_column("No.", row_num)
    table.add_column("Names", names)
    print(f'{table}\n')


def get_edit_type():
    """
    Asks the user to input how they want to edit the data.
    Returns their validated choice.
    """

    valid = ["a", "e", "d", "m"]
    choice = ""
    while True:
        print('Do you want to (E)dit (A)dd or (D)elete a record?')
        choice = input('Or return to the game (M)enu?\n')

        if choice.lower() in valid:
            return choice.lower()
        else:
            print("Invalid input. You must choose A, E, D or M")


def add_card(deck, names, cats):
    """
    Takes 3 arguments and allows user to add a card to the deck.
    deck is the deck name (worksheet name)
    names is a list of card names in the deck
    cats is a list of categories for that deck.
    User is prompted to enter a new card name and validates against
    duplicates.
    """
    names_lower = []
    new_card = []
    for x in names:
        names_lower.append(x.lower())

    print("Enter a new card name, (card must not already exist)")
    print("Max length = 20")

    while True:
        new_name = input("Name:\n")
        new_name_lower = new_name.lower()

        if validate_name(new_name_lower, names_lower):
            print("New card name accepted.\n")
            break

    new_card.append(new_name)
    print(f'Please enter the data for {new_name}\n')

    new_values = get_new_card_data(cats)

    for x in new_values:
        new_card.append(x)

    add_to_deck(new_card, deck)


def validate_name(new, existing):
    """
    Validates user input (new) as a string and compares against the
    'existing' list of names in the deck.
    Returns True if valid and unique input
    """
    if len(new) > 20:
        print("Name is too long, try again")
        return False

    if new in existing:
        print("Card already exists. Enter a new name or 'Quit' to exit\n")
        return False

    return True


def validate_data(data):
    """
    Takes a list 'data' as a variable. Converst all string values to
    integers. Raises a ValueError if strings cannot be converted to
    integers, or if there aren't exactly 6 numbers.
    Credit to CodeInstitute LoveSandwiches exercise for the
    basis of this code.
    """

    try:
        [int(value) for value in data]
        if len(data) != 6:
            raise ValueError(
                f"Exactly 6 numbers are required, you only entered \
{len(data)}."
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def add_to_deck(card, deck):
    """
    Takes 2 arguments. 'card' is a list containing the new card details
    'deck' is the name of the deck / worksheet where it will be added
    """
    print("Updating card deck..\n")
    this_sheet = SHEET.worksheet(deck)
    this_sheet.append_row(card)
    print("Card has been added to the deck.\n")


def update_deck(card, deck, card_number):
    """
    Takes 3 arguments
    'card' is a list containing the new card details
    'deck' is the name of the card deck / worksheet
    card_number is the number of the card within the deck.
    This is necessary information to update a row in the worksheet

    """
    print("Updating card deck with new data..\n")
    this_sheet = SHEET.worksheet(deck)
    row_num = card_number + 2
    this_sheet.update([card], f'A{row_num}:G{row_num}')
    print("Update complete.\n")


def get_card_number(names):
    """
    Takes one parameter which is a list of names in the deck.
    This is used to validate the input.
    Prompts the user to choose a card number to edit or delete,
    and returns the card number and the name of the card.
    """
    while True:
        card_num = int(input('Which card number?\n'))
        if card_num > 0 and card_num < len(names) + 1:
            name = names[card_num - 1]
            print(f"You have chosen card: {name}\n")
            break
        else:
            print("Invalid input. Please select a valid number.\n")

    return card_num, name


def edit_card(deck, names, cats):
    """
    Runs the edit card process
    """
    card_num, name_to_edit = get_card_number(names)
    new_row_data = [name_to_edit]
    card = get_card_data(deck, card_num)
    display_next_card(cats, card)
    new_values = get_new_card_data(cats)
    for num in new_values:
        new_row_data.append(num)
    print(new_row_data)
    update_deck(new_row_data, deck, card_num)


def get_card_data(deck, card):
    '''
    Pulls the card data from the spreadsheet
    First card is on row three, so the + 2 is required.
    '''
    card_data = SHEET.worksheet(deck).row_values(card + 2)
    return card_data


def get_new_card_data(categories):
    """
    Cats is the list of categories
    Takes input from the user for new card data.
    Format is 6 integers, separated by commas.
    Returns a list of 6 integers.
    """
    while True:
        print("Enter the data for each category, in order.")
        print("Data will be six numbers, separated by a comma.")
        print("Example: 1111, 2222, 3333333, 444, 55, 6")
        print("The categories are:\n")

        for cat in range(1, 7):

            print(categories[cat])

        new_data = input("\nEnter data: \n")
        new_values = new_data.split(",")
        check = validate_data(new_values)

        if check:
            print("\nData is valid - card accepted\n")
            break

    return new_values


def delete_card(deck, names):
    """
    Receives the deck name and the list of (card) names as arguments.
    Deletes a card from the deck by removing the row from the worksheet
    """
    card_num, name = get_card_number(names)
    print("\nAre you sure you want to delete?\n")
    confirm = input('Enter "Y" to confirm\n')
    if confirm.lower() == "y":
        print("delete(card)")
        remove_card_from_deck(card_num, deck)
    else:
        print("Card not deleted and remains in the deck")


def remove_card_from_deck(card_number, deck):
    """
    Deletes the card_number from the worksheet identified by
    deck parameter. Actual row in the worksheet is card number + 2
    """
    print("\nDeleting card from deck...")
    row_num = card_number + 2
    this_sheet = SHEET.worksheet(deck)
    this_sheet.delete_rows(row_num)
    print("Card has been removed\n")


def instructions():
    """
    Prints the game instructions to the terminal and returns to the menu.
    """
    print("\n-- Top Trumps Instructions --\n")
    print("Top Trumps is a card based game where the aim of the game is to")
    print("hold all of the cards.")
    print("The game ends when one player has no more cards to play.")

    print("\n-- Main Menu --\n")

    print("Here you choose whether you want to Play a game or Edit the cards")
    print("used in the game. The edit menu, you will have the option to add")
    print("a new card, edit or remove any card in the available decks.")

    input("\nPress any key to continue..\n")

    print("\n-- Playing The Game --\n")

    print("Firstly you will need to choose a deck of cards to play with.")
    print("Enter the deck name exactly as it is written in the list.")

    print("Cards are shuffled and dealt equally between you and the")
    print("computer. As the player you always choose the first category.")
    print("The aim of each round is to have a better score in that category")
    print("than the computer's card.")
    print("Each player has to play the next card at the top of their hand")
    print("you are forced to play the cards in order.")
    print("With most categories it is the highest number that wins the round,")
    print("but with a few exceptions. e.g Ranking - being ranked number 1")
    print("wins over someone ranked 20 (lowest number wins).")
    print("The winner of each round collects both cards and they are added to")
    print("the bottom of their hand. The winning player also chooses the")
    print("category in the next round.\nThe number of cards in each player's")
    print("hand is displayed at the end of each round.")
    print("In the event of a tied round, the cards are held and are given to")
    print("the winner of the next round.")
    print("The game ends when one player has no cards left to play.")
    print("The player with all the cards wins.")

    input("\nPress any key to continue..\n")

    print("\n-- Editing --\n")
    print("Here you can Add, Remove or Edit any card in any database.")
    print("Follow the on-screen instructions that will guide you through")
    print("each process.")
    print("Why not add yourself as a card in the 'peoples' deck and give")
    print("yourself whatever score you wish in each category - there are no")
    print("suggested ranges!\n")

    input("\nPress any key to go back to the menu.\n")


def edit_data(deck):
    """
    Runs the program for editing the spreadsheet data.
    Function takes one parameter containing the deck name.
    """
    print(f'You have chosen to edit the database: {deck}\n')
    editing = True

    categories, criteria, all_cards = get_cards(deck)

    while editing:
        all_names = get_all_names(deck)
        display_all_names(all_names)
        edit_type = get_edit_type()
        match edit_type:
            case 'a':
                print("\nYou have chosen to add a card.")
                add_card(deck, all_names, categories)

            case 'e':
                print("\nYou have chosen to edit a card..\n")
                edit_card(deck, all_names, categories)

            case 'd':
                print("\nYou have chosen to delete a card..\n")
                delete_card(deck, all_names)

            case 'm':
                print("Back to the menu\n")
                editing = False


def run_game(deck):
    """
    Runs a game of top trumps with the chosen deck.
    Function takes one parameter containing the deck name.
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
            print(f'You have chosen to play the category:')
            print(f'{categories[chosen_category]}\n')
        else:
            chosen_category = computer_choose_category()
            print(f'The computer has chosen to play the category:')
            print(f'{categories[chosen_category]}\n')

        cat_column = create_column(chosen_category)
        show = display_both_cards(
            categories, player_cards[0], computer_cards[0], cat_column)

        num = chosen_category

        winner, player_turn = get_winner(
            criteria[num], player_cards[0][num],
            computer_cards[0][num], player_turn)

        held_cards = process_winner(
                        winner, player_cards, computer_cards, held_cards)

        if min(len(player_cards), len(computer_cards)) < 1:
            the_end = True

    play_again = end_game_check(len(player_cards), len(computer_cards))
    return play_again.lower()


def main():
    """
    Runs the main program
    """

    option = "i"
    another_game = 'm'

    while option == "i":
        option = play_or_edit()
        if option == "i":
            instructions()

    all_decks = get_decks()
    chosen_deck = choose_deck(all_decks)

    if option == 'p':
        print(
            f"\n{chosen_deck} deck selected. Let's play Top Trumps!\n")
        another_game = run_game(chosen_deck)

    elif option == 'i':
        instructions()

    elif option == 'e':
        edit_data(chosen_deck)
        main()

    if another_game == 'y':
        print(f'\nStarting a new game with deck: {chosen_deck}\n')
        run_game(chosen_deck)

    if another_game == 'm':
        print("\nReturning to Main Menu\n")
        return True

    if another_game == 'q':
        print(f'\n*** THANK YOU FOR PLAYING TOP TRUMPS ***\n')
        print(f"Please visit https://github.com/bmays9 for more games!\n")


back_to_menu = True

while back_to_menu:
    back_to_menu = main()
