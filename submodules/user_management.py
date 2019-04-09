from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from submodules import gameplay_management as gm
import os, time, json, random
#load config file containing default game stats (for use in auto response for AFK players)
with open("./gameplay_config/stats_config.json", "r") as config_file:
    config = json.load(config_file)

def create_user(userid, username):
    """
    Function to create a user.
    Args:
        userid: userid of the new user
        username: username of the new user
    """
    #set default values and save to userinfo folder
    #The userid folder stores a mapping of userid to registered username in case a player changes username in future
    new_info = {"username":username, "userid":userid, "user_status":"O", "user_group":"normal", "block_list":[]}
    new_id = {"username": username}
    with open("./userinfo/" + username + ".json", 'w+') as info_file:
        json.dump(new_info, info_file)
    with open("./userid/" + userid + ".json", 'w+') as id_file:
        json.dump(new_id, id_file)
    return None

def load_user_data(usernames):
    """
    Function to load user data.
    Args:
        usernames: list of usernames of users to be loaded
    """
    user_list = []
    for username in usernames:
        with open("./userinfo/" + username + ".json", 'r') as file:
            user = json.load(file)
            user_list.append(user)
    if len(usernames) == 1:
        return user_list[0]
    else:
        return user_list

def save_user_data(users):
    """
    Function to save user data.
    Args:
        users: list of users to be saved
    """
    for user in users:
        with open("./userinfo/" + user["username"] + ".json", 'w+') as file:
            json.dump(user, file)

def validate_user(bot, update, userid, username, registration=False):
    """
    Function to validate existing user.
    Args:
        bot: from telegram bot
        update: from telegram update
        userid: userid of user
        username: username of user
        registration: trigger opposite behaviour for registration (user should not exist)
    """
    #load user data if user exist
    if check_exist_user("./userinfo/" + username + ".json"):
        with open("./userinfo/" + username + ".json", 'r') as file:
            user = json.load(file)
    else:
        if registration == False:
            bot.send_message(chat_id=userid, text="Please register your account with the <b>/war</b> command.", parse_mode=ParseMode.HTML)
        if registration == True:
            bot.send_message(chat_id=userid, text="Welcome to Age of Empires, " + username)
        return False
    #make sure current userid match registered userid (prevent users changing username to take over old accounts)
    if user["userid"] == str(userid):
        if registration == True:
            bot.send_message(chat_id=userid, text="The username <b>" + username + "</b> is already registered!", parse_mode=ParseMode.HTML)
        return True
    else:
        if registration == False:
            bot.send_message(chat_id=userid, text="Please register your account with the <b>/war</b> command.", parse_mode=ParseMode.HTML)
        if registration == True:
            bot.send_message(chat_id=userid, text="Welcome to Age of Empires, " + username)
        return False

def check_exist_user(path):
    """
    Function to check if user exist.
    Args:
        path: path to the supposed user's folder
    """
    #checks if user exist by looking for file with user's username
    if not os.path.isfile(path): 
        return False
    directory, filename = os.path.split(path)
    return filename in os.listdir(directory)

def switch_user_status(user1, user2, user1_status, user2_status):
    """
    Function to switch user status (mainly for use in battle when users alternate between 2 and 3).
    Args
        user1: first user
        user2: second user
        user1_status: user1 status to switch to
        user2_status: user2 status to switch to
    """
    user1["user_status"], user2["user_status"] = user1_status, user2_status
    save_user_data([user1, user2])

def connect_users(bot, user1, user2, message_id, minutes):
    """
    Function to enforce timeout request when 2 users are pending request.
    Args:
        bot: from telegram bot
        user1: first user
        user2: second user
        message_id: message_id of query to user
        minutes: timeout duration
    """
    seconds = minutes * 60
    start = time.time()
    elapsed = 0
    mtime1 = os.stat("./userinfo/"+ user1["username"] +".json").st_mtime
    user1mtime = mtime1
    while user1mtime == mtime1:
        elapsed = time.time() - start
        mtime1 = os.stat("./userinfo/"+ user1["username"] +".json").st_mtime
        if round(elapsed, 4) == round(seconds, 4):
            #if timeout, switch user statuses back to 0 from 1
            user1["user_status"], user2["user_status"] = "0", "0"
            save_user_data([user1, user2])
            bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> is unavailable for war!", parse_mode=ParseMode.HTML)
            bot.deleteMessage(chat_id=user2["userid"], message_id=message_id)
            bot.send_message(chat_id=user2["userid"], text="You missed a battle request from <b>" + user1["username"] + "</b>!", parse_mode=ParseMode.HTML)
    return None

def choice_timeout_user(bot, username1, username2, message_id, minutes):
    """
    Function to enforce timeout between player turns.
    Args:
        bot: from telegram bot
        username1: first username
        username2: second username
        message_id: message_id of query to user
        minutes: timeout duration
    """
    seconds = minutes * 60
    start = time.time()
    elapsed = 0
    user1, user2 = load_user_data([username1, username2])
    mtime1 = os.stat("./userinfo/"+ user1["username"] +".json").st_mtime
    user1mtime = mtime1
    while user1mtime == mtime1:
        elapsed = time.time() - start
        mtime1 = os.stat("./userinfo/"+ user1["username"] +".json").st_mtime
        #reminder at halfway mark
        if round(elapsed, 4) == round(seconds/2, 4):
            bot.send_message(chat_id=user1["userid"], text="You have <b>" + str(round(seconds/2)) + "</b> seconds left to make your choice!", parse_mode=ParseMode.HTML)
        #if no response, automatically random a response for AFK user
        if round(elapsed, 4) == round(seconds, 4):
            user1["user_status"], user2["user_status"] = "3", "2"
            save_user_data([user1, user2])
            bot.deleteMessage(chat_id=user1["userid"], message_id=message_id)
            bot.send_message(chat_id=user1["userid"], text="Time's up! An action was randomly chosen for you.")
            auto_action(bot, user1, user2)
    return None

def auto_action(bot, user1, user2):
    """
    Function to automatically choose an action for AFK users.
    Args:
        bot: from telegram bot
        user1: user that is AFK
    """
    choice = random.randint(0,22)
    if choice >= 0 and choice <= 1 and gm.check_gold(bot, user1["username"], int(config['castle']['repair_1'])):
        gm.repair(bot, user1["username"], user2["username"], "2.1")
    elif choice >= 2 and choice <= 3 and gm.check_gold(bot, user1["username"], int(config['castle']['repair_2'])):
        gm.repair(bot, user1["username"], user2["username"], "2.2")
    elif choice >= 4 and choice <= 5 and gm.check_gold(bot, user1["username"], int(config['castle']['repair_3'])):
        gm.repair(bot, user1["username"], user2["username"], "2.3")
    elif choice >= 6 and choice <= 7 and gm.check_gold(bot, user1["username"], 5*int(config['soldier']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.1.1")
    elif choice == 8 and gm.check_gold(bot, user1["username"], 10*int(config['soldier']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.1.2")
    elif choice == 9 and gm.check_gold(bot, user1["username"], 15*int(config['soldier']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.1.3")
    elif choice >= 10 and choice <= 11 and gm.check_gold(bot, user1["username"], 5*int(config['warrior']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.2.1")
    elif choice == 12 and gm.check_gold(bot, user1["username"], 10*int(config['warrior']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.2.2")
    elif choice == 13 and gm.check_gold(bot, user1["username"], 15*int(config['warrior']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.2.3")
    elif choice >= 14 and choice <= 15 and gm.check_gold(bot, user1["username"], 5*int(config['knight']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.3.1")
    elif choice == 16 and gm.check_gold(bot, user1["username"], 10*int(config['knight']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.3.2")
    elif choice == 17 and gm.check_gold(bot, user1["username"], 15*int(config['knight']['price'])):
        gm.hire(bot, user1["username"], user2["username"], "3.3.3")
    else:
        gm.attack(bot, user1["username"], user2["username"])
    return None
