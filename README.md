<p align="center">
  <img src="https://i.imgur.com/acZQy2c.jpg" />
  <h1 align="center">Age of Empire (Telegram Version)</h1>
</p>

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Team](#team)
* [Contributing](#contributing)
* [Others](#others)

### Introduction
5 months ago, I picked up python and did my very first personal project, [Age Of Empire](https://github.com/tjtanjin/age_of_empire), a turn based game on the terminal. Now, 5 months later, I am integrating this game into a telegram bot so that it can be available for play online! The bot is currently live here:
```
https://t.me/ageofempire_bot
```

### Features
Age of Empire (Telegram Version) currently supports only the Player versus Player gamemode. To begin a war, players need to know the telegram handle of the opponent they wish to challenge. They will then issue a request for war with the /war command. A /banish and /unbanish command has also been implemented as a means for players to block those who keep spamming war requests. Majority of the actions taken when a match is active is through intuitive buttons so the game is very simple to get into!

In addition to the above commands, administrators also have access to the /reset command which as the command implies, will forcibly reset and remove a user from current games.

### Technologies
Technologies used by Age of Empire (Telegram Version) are as below:
##### Done with:

<p align="center">
  <img height="150" width="150" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png"/>
</p>
<p align="center">
Python
</p>

##### Deployed on:
<p align="center">
  <img height="150" width="150" src="https://pbs.twimg.com/profile_images/1089877713408557056/aO_IAlp__400x400.jpg" />
</p>
<p align="center">
Upcloud
</p>

##### Project Repository
```
https://github.com/tjtanjin/telegram_aoe
```

### Setup
The following section will guide you through setting up your own telegram version of Age of Empire (telegram account required).
* First, head over to [BotFather](https://t.me/BotFather) and create your own telegram bot with the /newbot command. After choosing an appropriate name and telegram handle for your bot, note down the bot token provided to you.
* Next, cd to the directory of where you wish to store the project and clone this repository. An example is provided below:
```
$ cd /home/user/exampleuser/projects/
$ git clone https://github.com/tjtanjin/telegram_aoe.git
```
* Following which, create a token folder and within it, create a token.json file, saving the token you received from [BotFather](https://t.me/BotFather) as a value to the key "token" as shown below:
```
{"token": "your bot token here"}
```
* Next, create two empty folders (userid & userinfo) in the base directory of the project:
```
$ mkdir userid
$ mkdir userinfo
```
* Finally, from the base directory of the project, execute the following command and the terminal should print "Running..." if everything has been setup correctly!
```
$ python3 main.py
```
* If you wish to host your telegram bot online 24/7, do checkout the guide [here](https://gist.github.com/tjtanjin/ce560069506e3b6f4d70e570120249ed).

### Team
* [Tan Jin](https://github.com/tjtanjin)

### Contributing
If you have code to contribute to the project, open a pull request and describe clearly the changes and what they are intended to do (enhancement, bug fixes etc). Alternatively, you may simply raise bugs or suggestions by opening an issue.

### Others
#### General design
Users are identified primarily by their telegram username but userid is also used to ensure that even if users change their telegram username, other players cannot take over their account. At any point in time, users are set to one of the four statuses below:
  1. Status 0 - Free to fight
  2. Status 1 - Has a pending request for fight
  3. Status 2 - In a fight, and is the player's turn
  4. Status 3 - In a fight, and is the other player's turn
Certain user actions are bound to their statuses. Ideally, every action should be tied to specific status/statuses so more work will be done here.
When players enter a battle, two instances are created to hold the user game data as they fight against each other (this design is likely to be changed soon to allow multiple matches to run concurrently). In this simple turn based battle, players take turn to fight each other until one of their castle health reaches 0.

#### Submodules breakdown
The following are the 5 submodule files and their explanations can be found further below:
  1. User Management
  2. User Response
  3. Gameplay Management
  4. Gameplay Response
  5. Miscellaneous
  
##### User Management
The user management file, as its name implies contains all the functions that handles user behaviour such as creating new users, saving user data and switching user statuses. User inputs do not directly interact with this file but rather, go through the user response file.

##### User Response
The user response file contains the functions that take in every command executed by the user in the chat with the bot such as /war, /fight and /banish. The functions here process the response and decide on the most appropriate action to take based on the user request.

##### Gameplay Management
The gameplay management file contains the gameplay logic. The functions here are responsible for deciding which player's turn it is and for executing the actions of the game and updating the game data. They are primarily directed by the input in the gameplay response file.

##### Gameplay Response
The gameplay response file contains the function that take in every button pressed by the user in the chat with the bot such as attack, repair or hire. The functions here process the callback data from the button and decide on the most appropriate action to take based on the user choice.

##### Miscellaneous
The miscellaneous file contains non-app logic influencing codes such as providing the layout for the buttons.

For any questions regarding the implementation of the project, please drop an email to: cjtanjin@gmail.com.
