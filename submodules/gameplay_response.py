from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import submodules.user_management as um
import submodules.gameplay_management as gm
import submodules.miscellaneous as mc
import os, time, sys, json, re
os.chdir(os.path.realpath(sys.path[0]))
#load config file containing default game stats
with open("./gameplay_config/stats_config.json", "r") as config_file:
    config = json.load(config_file)

def launch_attack(bot, update):
    """
    Function that takes in the attack response from user.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-1-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1, user2 = um.load_user_data([username1, username2])
    #prevent user from executing if status is not 2
    if user1["user_status"] != "2":
        return None
    #switch user status and execute the attack
    um.switch_user_status(user1, user2, "3", "2")
    bot.deleteMessage(chat_id=user1["userid"], message_id=update.callback_query.message.message_id)
    bot.send_message(chat_id=user1["userid"], text="You chose to attack!")
    gm.id_to_player(bot, user1["userid"], "1")
    return None

def repair(bot, update):
    """
    Function that takes in the repair response from user.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-2\S*-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1, user2 = um.load_user_data([username1, username2])
    #prevent user from executing if status is not 2
    if user1["user_status"] != "2":
        return None
    #variable to control actions
    approved_action = []
    #list of possible actions to take depending on button pressed (callback_query.data)
    if "-2-" in data and gm.check_gold(bot, user1["userid"], int(config['castle']['repair_1'])):
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 5, ["100 Gold", "200 Gold", "300 Gold", "Flee", "Back"], ["2.1", "2.2", "2.3", "flee", "reshow_main"])
        bot.editMessageText(chat_id=user1["userid"], message_id=update.callback_query.message.message_id, text="How much do you wish to repair? (1 Gold repairs 1 Health)", reply_markup=reply_markup)
    elif "-2.1-" in data and gm.check_gold(bot, user1["userid"], int(config['castle']['repair_1'])):
        approved_action = ["-2.1-", "You chose to repair <b>100</b> Health with <b>100</b> Gold!"]
    elif "-2.2-" in data and gm.check_gold(bot, user1["userid"], int(config['castle']['repair_2'])):
        approved_action = ["-2.2-", "You chose to repair <b>200</b> Health with <b>200</b> Gold!"]
    elif "-2.3-" in data and gm.check_gold(bot, user1["userid"], int(config['castle']['repair_3'])):
        approved_action = ["-2.3-", "You chose to repair <b>300</b> Health with <b>300</b> Gold!"]
    if approved_action != []:
        um.switch_user_status(user1, user2, "3", "2")
        bot.deleteMessage(chat_id=user1["userid"], message_id=update.callback_query.message.message_id)
        bot.send_message(chat_id=user1["userid"], text=approved_action[1], parse_mode=ParseMode.HTML)
        gm.id_to_player(bot, user1["userid"], approved_action[0][1:4])
    elif "-2-" in data:
        pass
    else:
        bot.send_message(chat_id=user1["userid"], text="You do not have enough gold!")
    return None

def hire(bot, update):
    """
    Function that takes in the hire response from user.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-3\S*-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1, user2 = um.load_user_data([username1, username2])
    #prevent user from executing if status is not 2
    if user1["user_status"] != "2":
        return None
    #variable to control actions
    approved_action = []
    #list of possible actions to take depending on button pressed (callback_query.data)
    if "-3-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['soldier']['price'])):
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 5, ["Soldiers", "Warriors", "Knights", "Flee", "Back"], ["3.1", "3.2", "3.3", "flee", "reshow_main"])
        bot.editMessageText(chat_id=user1["userid"], message_id=update.callback_query.message.message_id, text="Which unit do you wish to hire?", reply_markup=reply_markup)
    elif "-3.1-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['soldier']['price'])):
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 5, ["5", "10", "15", "Flee", "Back"], ["3.1.1", "3.1.2", "3.1.3", "flee", "3"])
        bot.editMessageText(chat_id=user1["userid"], message_id=update.callback_query.message.message_id, text="How many Soldiers do you wish to hire? (20 Gold, 5 Attack Damage each)", reply_markup=reply_markup)
    elif "-3.2-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['warrior']['price'])):
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 5, ["5", "10", "15", "Flee", "Back"], ["3.2.1", "3.2.2", "3.2.3", "flee", "3"])
        bot.editMessageText(chat_id=user1["userid"], message_id=update.callback_query.message.message_id, text="How many Warriors do you wish to hire? (50 Gold, 10 Attack Damage each)", reply_markup=reply_markup)
    elif "-3.3-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['knight']['price'])):
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 5, ["5", "10", "15", "Flee", "Back"], ["3.3.1", "3.3.2", "3.3.3", "flee", "3"])
        bot.editMessageText(chat_id=user1["userid"], message_id=update.callback_query.message.message_id, text="How many Knights do you wish to hire? (100 Gold, 20 Attack Damage each)", reply_markup=reply_markup)
    elif "-3.1.1-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['soldier']['price'])):
        approved_action = ["-3.1.1-", "You chose to hire <b>5</b> Soldiers!"]
    elif "-3.1.2-" in data and gm.check_gold(bot, user1["userid"], 10*int(config['soldier']['price'])):
        approved_action = ["-3.1.2-", "You chose to hire <b>10</b> Soldiers!"]
    elif "-3.1.3-" in data and gm.check_gold(bot, user1["userid"], 15*int(config['soldier']['price'])):
        approved_action = ["-3.1.3-", "You chose to hire <b>15</b> Soldiers!"]
    elif "-3.2.1-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['warrior']['price'])):
        approved_action = ["-3.2.1-", "You chose to hire <b>5</b> Warriors!"]
    elif "-3.2.2-" in data and gm.check_gold(bot, user1["userid"], 10*int(config['warrior']['price'])):
        approved_action = ["-3.2.2-", "You chose to hire <b>10</b> Warriors!"]
    elif "-3.2.3-" in data and gm.check_gold(bot, user1["userid"], 15*int(config['warrior']['price'])):
        approved_action = ["-3.2.3-", "You chose to hire <b>15</b> Warriors!"]
    elif "-3.3.1-" in data and gm.check_gold(bot, user1["userid"], 5*int(config['knight']['price'])):
        approved_action = ["-3.3.1-", "You chose to hire <b>5</b> Knights!"]
    elif "-3.3.2-" in data and gm.check_gold(bot, user1["userid"], 10*int(config['knight']['price'])):
        approved_action = ["-3.3.2-", "You chose to hire <b>10</b> Knights!"]
    elif "-3.3.3-" in data and gm.check_gold(bot, user1["userid"], 15*int(config['knight']['price'])):
        approved_action = ["-3.3.3-", "You chose to hire <b>15</b> Knights!"]
    if approved_action != []:
        um.switch_user_status(user1, user2, "3", "2")
        bot.deleteMessage(chat_id=user1["userid"], message_id=update.callback_query.message.message_id)
        bot.send_message(chat_id=user1["userid"], text=approved_action[1], parse_mode=ParseMode.HTML)
        gm.id_to_player(bot, user1["userid"], approved_action[0][1:6])
    elif "-3-" in data or "-3.1-" in data or "-3.2" in data or "-3.3-" in data:
        pass
    else:
        bot.send_message(chat_id=user1["userid"], text="You do not have enough gold!")
    return None

def flee(bot, update):
    """
    Function that takes in the flee response from user.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-flee-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1, user2 = um.load_user_data([username1, username2])
    #prevent user from executing if status is not 2
    if user1["user_status"] != "2":
        return None
    bot.deleteMessage(chat_id=user1["userid"], message_id=update.callback_query.message.message_id)
    gm.id_to_player(bot, user1["userid"], "0")
    return None

def reshow_main_options(bot, update):
    """
    Function that takes in the back response from user to show the main prompt again.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-reshow_main-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1, user2 = um.load_user_data([username1, username2])
    #prevent user from executing if status is not 2
    if user1["user_status"] != "2":
        return None
    reply_markup = mc.show_user_options(user1["username"], user2["username"], 4, ["Attack", "Repair", "Hire", "Flee"], ["1", "2", "3", "flee"])
    bot.editMessageText(chat_id=user1["userid"], message_id=update.callback_query.message.message_id, text="What will you do?", reply_markup=reply_markup)
    return None

def accept_fight(bot, update):
    """
    Function takes in the yes response from user in accepting a fight.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-accept-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1, user2 = um.load_user_data([username1, username2])
    #ensure both users are at status 1 before starting the battle
    if user1["user_status"] == "1" and user2["user_status"] == "1":
        um.switch_user_status(user1, user2, "2", "3")
        bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> accepted your request for war!", parse_mode=ParseMode.HTML)
        bot.send_message(chat_id=user1["userid"], text="Preparing for war...")
        bot.editMessageText(chat_id=user2["userid"], message_id=update.callback_query.message.message_id, text="You accepted the request for war from " + user1["username"] + "!")
        bot.send_message(chat_id=user2["userid"], text="Preparing for war...")
        #starts the battle
        gm.start(bot, user1["username"], user1["userid"], user2["username"], user2["userid"])
    return None

def decline_fight(bot, update):
    """
    Function that takes in no response from user in declining a fight.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and loads user
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    usernames = re.match(r'-decline-(\S+)-(\S+)', data)
    username1, username2 = usernames.group(1), usernames.group(2)
    user1,user2 = um.load_user_data([username1, username2])
    #ensure both users are at status 1 before declining the battle
    if user1["user_status"] == "1" and user2["user_status"] == "1":
        um.switch_user_status(user1, user2, "0", "0")
        bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> declined your request for war!", parse_mode=ParseMode.HTML)
        bot.editMessageText(chat_id=user2["userid"], message_id=update.callback_query.message.message_id, text="You declined the request for war from " + user1["username"] + "!")
    return None

def quit(bot, update):
    """
    Function that takes in quit response at end of match.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    #answer query and load users
    bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    username = re.match(r'-quit-(\S+)-(\S+)', data)
    username = username.group(1)
    user = um.load_user_data([username])
    #set user status to 0
    user["user_status"] = "0"
    um.save_user_data([user])
    bot.edit_message_reply_markup(chat_id=user["userid"], message_id=update.callback_query.message.message_id, reply_markup=None)
    bot.send_message(chat_id=user["userid"], text="Match ended.")
    return None