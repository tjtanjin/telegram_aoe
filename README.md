# About Telegram Age Of Empire
5 months ago, I picked up python and did my very first personal project - Age Of Empire (https://github.com/tjtanjin/age_of_empire), a turn based game on the terminal. Now, 5 months later, I am integrating this game into a telegram bot so that it can be available for play online! Note that there is still a lot of work to be done and due to an oversight on my part, the bot is currently unable to support multiple matches. I am still looking for a workaround so hopefully I'll be able to have multiple matches soon!
## General design
Users are identified primarily by their telegram username but userid is also used to ensure that even if users change their telegram username, other players cannot take over their account. At any point in time, users are set to one of the four statuses below:
  1. Status 0 - Free to fight
  2. Status 1 - Has a pending request for fight
  3. Status 2 - In a fight, and is the player's turn
  4. Status 3 - In a fight, and is the other player's turn
Certain user actions are bound to their statuses. Ideally, every action should be tied to specific status/statuses so more work will be done here.
When players enter a battle, two instances are created to hold the user game data as they fight against each other (this design is likely to be changed soon to allow multiple matches to run concurrently). In this simple turn based battle, players take turn to fight each other until one of their castle health reaches 0.
## Submodules breakdown
There following are the 5 submodule files and their explanations can be found further below:
  1. User Management
  2. User Response
  3. Gameplay Management
  4. Gameplay Response
  5. Miscellaneous
### User Management
The user management file, as its name implies contains all the functions that handles user behaviour such as creating new users, saving user data and switching user statuses. User inputs do not directly interact with this file but rather, go through the user response file.
### User Response
The user response file contains the functions that take in every command executed by the user in the chat with the bot such as /war, /fight and /banish. The functions here process the response and decide on the most appropriate action to take based on the user request.
### Gameplay Management
The gameplay management file contains the gameplay logic. The functions here are responsible for deciding which player's turn it is and for executing the actions of the game and updating the game data. They are primarily directed by the input in the gameplay response file.
### Gameplay Response
The gameplay response file contains the function that take in every button pressed by the user in the chat with the bot such as attack, repair or hire. The functions here process the callback data from the button and decide on the most appropriate action to take based on the user choice.
## Upcoming Work
As mentioned earlier, the bot is only able to run one game at a time which defeats the purpose of putting it on telegram as a multiplayer game. I have a rough idea of how this might be fixed but am still exploring possible options. If anyone has suggestions or inputs, I'll appreciate if you can reach out to me. Thank you for reading!

Update: Redis db has been used to hold game data so multiple matches can go on at once! However, telegram are handling the requests individually resulting in slow response times. Will be visiting the documentation to see what can be done!