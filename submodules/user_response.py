from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import submodules.user_management as um
import submodules.gameplay_management as gm
import submodules.miscellaneous as mc
import threading

def welcome_user(bot, update):
    """
    Function that executes from the /war command. Registers only new users with a telegram username and
    declines existing users from re-registering if they are able to be validated.
    Args:
        None
    """
    #retrieve username and id user who executed the command
    userid = str(update.message.chat_id)
    username = str(update.message.from_user.username)
    #check eligibility for registration
    if username == "None" or username == None:
        bot.send_message(chat_id=userid, text="Sorry, you can only register if you have a telegram username")
        return None
    #if unable to validate user(not existing user), register as new user
    if um.validate_user(bot, update, userid, username, registration=True) is False:
        um.create_user(userid, username)
    return None

def banish_user(bot, update, args):
    """
    Function that executes from the /banish command. Adds specified user to the block list if not already blocked.
    Args:
        args: Only validates the input at index 0 and ignores any extra inputs.
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(bot, update, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #prompt usage if no args provided
    if args == []:
        bot.send_message(chat_id=user1["userid"], text='Usage: <b>/banish &lt;username&gt;</b>', parse_mode=ParseMode.HTML)
        return None
    else:
        username2 = args[0]
    #check if specified user exist(registered user)
    if um.check_exist_user("./userinfo/" + username2 + ".json") is False:
        bot.send_message(chat_id=user1["userid"], text="User cannot be found!")
        return None
    else:
        user2 = um.load_user_data([username2])
    #check if user is already blocked
    if user2["userid"] in user1["block_list"]:
        bot.send_message(chat_id=user1["userid"], text="<b>" + username2 + "</b> is already banished!", parse_mode=ParseMode.HTML)
    else:
        #if not blocked, add to block list
        user1["block_list"].append(user2["userid"])
        um.save_user_data([user1])
        bot.send_message(chat_id=user1["userid"], text="You have banished <b>" + username2 + "</b>! (To unbanish, use /unbanish)", parse_mode=ParseMode.HTML)
    return None

def unbanish_user(bot, update, args):
    """
    Function that executes from the /unbanish command. Removes specified user from the block list if in block list.
    Args:
        args: Only validates the input at index 0 and ignores any extra inputs.
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(bot, update, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #prompt usage if no args provided
    if args == []:
        bot.send_message(chat_id=user1["userid"], text='Usage: <b>/unbanish &lt;username&gt;</b>', parse_mode=ParseMode.HTML)
        return None
    else:
        username2 = args[0]
    #check if specified user exist(registered user)
    if um.check_exist_user("./userinfo/" + username2 + ".json") is False:
        bot.send_message(chat_id=user1["userid"], text="User cannot be found!")
        return None
    else:
        user2 = um.load_user_data([username2])
    #check if user is blocked
    if user2["userid"] not in user1["block_list"]:
        bot.send_message(chat_id=user1["userid"], text="<b>" + username2 + "</b> is not banished!", parse_mode=ParseMode.HTML)
    else:
        #if blocked, unblock the user
        user1["block_list"].remove(user2["userid"])
        um.save_user_data([user1])
        bot.send_message(chat_id=user1["userid"], text="You have unbanished <b>" + username2 + "</b>! (To banish, use /banish)", parse_mode=ParseMode.HTML)
    return None

def initiate_fight_user(bot, update, args):
    """
    Function that executes from the /fight command. Initiates a battle request against another user.
    Args:
        args: Only validates the input at index 0 and ignores any extra inputs.
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(bot, update, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #prompt usage if no args provided, else check user current status to make sure eligibility for making request
    if args == []:
        bot.send_message(chat_id=user1["userid"], text="Usage: <b>/fight &lt;username&gt;</b>", parse_mode=ParseMode.HTML)
        return None
    elif user1["user_status"] == "1":
        bot.send_message(chat_id=user1["userid"], text="You already have a pending request!")
        return None
    elif user1["user_status"] == "2" or user1["user_status"] == "3":
        bot.send_message(chat_id=user1["userid"], text="You are in the midst of a war!")
        return None
    else:
        username2 = args[0]
    #check if specified user exist(registered user)
    if um.check_exist_user("./userinfo/" + username2 + ".json") is False:
        bot.send_message(chat_id=user1["userid"], text="User cannot be found!")
        return None
    else:
        user2 = um.load_user_data([username2])
    #refuse the request if specified user has blocked requesting user
    if user1["userid"] in user2["block_list"]:
        bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> is unavailable for war!", parse_mode=ParseMode.HTML)
    elif user2["user_status"] == "1":
        bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> has a pending request!", parse_mode=ParseMode.HTML)
    elif user2["user_status"] == "2" or user1["user_status"] == "3":  
        bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> is in the midst of a war!", parse_mode=ParseMode.HTML)
    else:
        #switch user statuses to pending and send out battle declaration
        user1["user_status"], user2["user_status"] = "1", "1"
        um.save_user_data([user1, user2])
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 2, ["Yes", "No"], ["accept", "decline"])
        bot.send_message(chat_id=user1["userid"], text="Enemy Detected...")
        bot.send_message(chat_id=user1["userid"], text="Declaring Battle...")
        declare_war = bot.send_message(chat_id=user2["userid"], text="<b>" + user1["username"] + "</b> has declared battle! Are you ready?", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        #start a thread to enforce a 30 second timeout rule
        threading.Thread(target=um.connect_users, args=(bot, user1, user2, declare_war.message_id, 0.5)).start()
    return None

def reset_user(bot, update, args):
    """
    Function that executes from the /reset command to reset user state to 0. Only admins have the right to execute this command.
    Args:
        args: Only validates the input at index 0 and ignores any extra inputs.
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(bot, update, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #only admin users can execute resets
    if user1["user_group"] == "admin":
        user2 = um.load_user_data([args[0]])
        user2["user_status"] = "0"
        um.save_user_data([user2])
        bot.send_message(chat_id=user1["userid"], text="User reset successful!")
    else:
        bot.send_message(chat_id=user1["userid"], text="You do not have the permission!")
    return None