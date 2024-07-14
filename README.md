# Top Trumps

View the live app [here](https://top-trumps1-6a9a12a49bdc.herokuapp.com/)

This app provides users with a fun online game to play in the python console and allows the user to edit all of the game data.

The app is targeted to people who enjoy a fast and interesting game, especially those who are already familiar with Top Trumps.

## User Expectations

- The app should be easy to navigate and all game information displayed intelligently.
- The user should be able to edit the card data used in the game.
- The app should be fully tested and run without bugs.

## Flow Charts

The main menu gives the user the choice to either play a game, or edit the data. The flow of each branch of the app is displayed below.

### Gameplay Flow
- ![Gameplay flow image](readme-images/flow1.png)

### Data Editing Flow
- ![Data editing flow image](readme-images\flow2.png)

## Features

- __Main Menu__
  - The app starts with a welcome message and immediately presents the user with the main game options. Play, Edit or View instructions.
- ![Data editing flow image](readme-images/welcome-menu.png)

- __Instructions__
  - From the Main Menu the user can choose to view the instructions, printed to the terminal.
For readability reasons, the instructions are split into sections and the user must press any key to move to the next page.
- ![instructions displayed in the terminal](readme-images/instructions.png)

- __Choose Deck__
  - The game data is stored in a Google sheets document and the user is presented with a list of decks to use. Each worksheet represents a deck of cards.
- ![Google sheets data](readme-images/worksheet.png)
The data is pulled from the worksheets and presented to the user in the terminal.
- ![User asked to choose deck](readme-images/choose-deck.png)

- __Game State__
The terminal displays the number of cards each player has in their hand at the start of each round. This shows the user who is winning the game. I used the PrettyTable library to present this information to the user in a clear way.
- ![Game state](readme-images/game-state.png)

- __Card Display__
  - I chose to use the PrettyTable library as a way of displaying the card information to the user in the terminal. This allows the card data to be viewed in a convenient way, with the categories and card data clearly separated. First the player’s card is shown to the player, and then the computer’s card is shown together so the comparison can be made.
- ![Show player card](readme-images/player-card.png)
- ![Card comparison](readme-images/comparison.png)

- __Editing__
 - With the chosen deck, a list of all cards is displayed to the user in the terminal before the editing options are given. This confirms to the user which cards are available in the deck. 
- ![Edit Menu](readme-images/edit-menu.png)

## Technologies Used
 
Python: Used for all program code.
GitHub: Used to store the code online, version control and for deployment.
Gitpod: Used for development as a cloud IDE.
Heroku: Used to deploy the project.
Smartdraw: Used to create flowcharts for the Readme file  (https://app.smartdraw.com/)
CI - Python Linter: Used to validate Python code. (https://pep8ci.herokuapp.com/)
