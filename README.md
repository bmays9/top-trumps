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

## Testing
 
### Validator Testing
 
I used Code Institute’s Python Linter to validate the Python code. There is one remaining error which I have decide to leave unchanged. The While loop controls the game while both players have cards and the loop exits when one player has no cards. The program works without error so I decided not to change the code here.
- ![Edit Menu](readme-images/edit-menu.png)

### Manual Testing

<table>
<thead>
  <tr>
    <th>Test Case</th>
    <th>Actual Result</th>
    <th>Pass / Fail</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Application loads without any error messages</td>
    <td>No error messages</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Main Menu is displayed and awaits user input.</td>
    <td>Welcome message and main menu are displayed and the terminal is waiting for user input</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Main menu input is validated correctly</td>
    <td>Incorrect input is relayed to the user and prompted to enter again</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Main menu accepts both upper and lowercase valid characters</td>
    <td>All values I, i, p, P, e, E are accepted</td>
    <td>Pass</td>
  </tr>  
  <tr>
    <td>Players are dealt the same number of cards when the deck has an odd number of cards</td>
    <td>A deck was created with an odd number of cards, and the last card was removed after the shuffle. Players were dealt equal number of cards.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Player is able to choose category</td>
    <td>Input is correctly validated and only values 1-6 are possible</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Computer chooses a category at random</td>
    <td>All category values have been observed as computer selections.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Winner of the round is correctly determined</td>
    <td>Testing succesful with both High and Low value winning criteria. Correct result is printed to the terminal. </td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Winner gets the cards and chooses the next category</td>
    <td>Tested for both player and computer wins. Cards are added to the bottom of the hand.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>In a tied round neither player gets the cards</td>
    <td>Created many cards with the same values to test this extensively. Game state correctly displays the number of cards held after a tie.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>The next winner after a tied round gets the previously held cards</td>
    <td>The right cards are held, and then after an eventual winner are assigned correctly to the winner.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>When one player has no cards left, the game ends and a winner declared</td>
    <td>The right winner is declared when one player has no cards left to play</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>Editing Menu input options are validated correctly</td>
    <td>Only expected values in upper or lower case are accepted as input.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>When Adding card, new details are validated correctly</td>
    <td>Any deviation from the required format results in an error displayed to the user, and they are prompted to re-enter.</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>When Editing a card, the new details are validated correctly</td>
    <td>Any deviation from the required format results in an error displayed to the user, and they are prompted to re-enter</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>When deleting a record, user confirmation is required</td>
    <td>Only entering a Y or y confirms the deletion. Any other key returns to the menu</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>After any card edit action, the worksheet is updated correctly</td>
    <td>All worksheets are updated correctly after a user action to add, delete or edit a card</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>After any card edit, the user is presented with an updated list of card names</td>
    <td>The list of card names is retrieved from the worksheet after an edit, and printed to the terminal</td>
    <td>Pass</td>
  </tr>
  <tr>
    <td>After editing, the user can return to the main menu</td>
    <td></td>
    <td>Pass</td>
  </tr>
  </tbody>
  </table>


