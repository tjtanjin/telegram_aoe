from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from submodules import user_management as um
from submodules import gameplay_management as gm
from submodules import miscellaneous as mc
import threading

def show_help(update, context):
    """
    Function that list all available commands to user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    userid = str(update.message.chat_id)
    context.bot.send_message(chat_id=userid, text="""Here are the currently available commands:\n
        <b>/war</b> - register your account\n
        <b>/fight &lt;username&gt;</b> - declare war on another registered user\n
        <b>/banish &lt;username&gt;</b> - block that annoying user that keeps spamming you\n
        <b>/unbanish &lt;username&gt;</b> - unblock a banished user\n
        <b>/help</b> - displays the available commands\n 
Have ideas and suggestions for this mini project? Head over to the <a href="https://github.com/tjtanjin/telegram_aoe">Project Repository</a>!""", parse_mode=ParseMode.HTML, disable_web_page_preview=True)

def welcome_user(update, context):
    """
    Function that executes from the /war command. Registers only new users with a telegram username and
    declines existing users from re-registering if they are able to be validated.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    #retrieve username and id user who executed the command
    userid = str(update.message.chat_id)
    username = str(update.message.from_user.username)
    #check eligibility for registration
    if username == "None" or username == None:
        context.bot.send_message(chat_id=userid, text="Sorry, you can only register if you have a telegram username")
        return None
    #if unable to validate user(not existing user), register as new user
    if um.validate_user(update, context, userid, username, registration=True) is False:
        um.create_user(userid, username)
    return None

def banish_user(update, context):
    """
    Function that executes from the /banish command. Adds specified user to the block list if not already blocked.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(update, context, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #prompt usage if no context.args provided
    if context.args == []:
        context.bot.send_message(chat_id=user1["userid"], text='Usage: <b>/banish &lt;username&gt;</b>', parse_mode=ParseMode.HTML)
        return None
    else:
        username2 = context.args[0]
    #check if specified user exist(registered user)
    if um.check_exist_user("./userinfo/" + username2 + ".json") is False:
        context.bot.send_message(chat_id=user1["userid"], text="User cannot be found!")
        return None
    else:
        user2 = um.load_user_data([username2])
    #check if user is already blocked
    if user2["userid"] in user1["block_list"]:
        context.bot.send_message(chat_id=user1["userid"], text="<b>" + username2 + "</b> is already banished!", parse_mode=ParseMode.HTML)
    else:
        #if not blocked, add to block list
        user1["block_list"].append(user2["userid"])
        um.save_user_data([user1])
        context.bot.send_message(chat_id=user1["userid"], text="You have banished <b>" + username2 + "</b>! (To unbanish, use /unbanish)", parse_mode=ParseMode.HTML)
    return None

def unbanish_user(update, context):
    """
    Function that executes from the /unbanish command. Removes specified user from the block list if in block list.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    try:
        #if invalid user, the validate_user function will prompt to register with /war command
        if um.validate_user(update, context, update.message.chat_id, update.message.from_user.username) is False:
            return None
        else:
            #if valid user, load in user data
            user1 = um.load_user_data([update.message.from_user.username])
        #prompt usage if no context.args provided
        if context.args == []:
            context.bot.send_message(chat_id=user1["userid"], text='Usage: <b>/unbanish &lt;username&gt;</b>', parse_mode=ParseMode.HTML)
            return None
        else:
            username2 = context.args[0]
        #check if specified user exist(registered user)
        if um.check_exist_user("./userinfo/" + username2 + ".json") is False:
            context.bot.send_message(chat_id=user1["userid"], text="User cannot be found!")
            return None
        else:
            user2 = um.load_user_data([username2])
        #check if user is blocked
        if user2["userid"] not in user1["block_list"]:
            context.bot.send_message(chat_id=user1["userid"], text="<b>" + username2 + "</b> is not banished!", parse_mode=ParseMode.HTML)
        else:
            #if blocked, unblock the user
            user1["block_list"].remove(user2["userid"])
            um.save_user_data([user1])
            context.bot.send_message(chat_id=user1["userid"], text="You have unbanished <b>" + username2 + "</b>! (To banish, use /banish)", parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(ex)
    return None

def initiate_fight_user(update, context):
    """
    Function that executes from the /fight command. Initiates a battle request against another user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(update, context, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #prompt usage if no context.args provided, else check user current status to make sure eligibility for making request
    if context.args == []:
        context.bot.send_message(chat_id=user1["userid"], text="Usage: <b>/fight &lt;username&gt;</b>", parse_mode=ParseMode.HTML)
        return None
    elif user1["user_status"] == "1":
        context.bot.send_message(chat_id=user1["userid"], text="You already have a pending request!")
        return None
    elif user1["user_status"] == "2" or user1["user_status"] == "3":
        context.bot.send_message(chat_id=user1["userid"], text="You are in the midst of a war!")
        return None
    else:
        username2 = context.args[0]
    #check if specified user exist(registered user)
    if um.check_exist_user("./userinfo/" + username2 + ".json") is False:
        context.bot.send_message(chat_id=user1["userid"], text="User cannot be found!")
        return None
    else:
        user2 = um.load_user_data([username2])
    #refuse the request if specified user has blocked requesting user
    if user1["userid"] in user2["block_list"]:
        context.bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> is unavailable for war!", parse_mode=ParseMode.HTML)
    elif user2["user_status"] == "1":
        context.bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> has a pending request!", parse_mode=ParseMode.HTML)
    elif user2["user_status"] == "2" or user1["user_status"] == "3":  
        context.bot.send_message(chat_id=user1["userid"], text="<b>" + user2["username"] + "</b> is in the midst of a war!", parse_mode=ParseMode.HTML)
    else:
        #switch user statuses to pending and send out battle declaration
        user1["user_status"], user2["user_status"] = "1", "1"
        um.save_user_data([user1, user2])
        reply_markup = mc.show_user_options(user1["username"], user2["username"], 2, ["Yes", "No"], ["accept", "decline"])
        context.bot.send_message(chat_id=user1["userid"], text="Enemy Detected...")
        context.bot.send_message(chat_id=user1["userid"], text="Declaring Battle...")
        declare_war = context.bot.send_message(chat_id=user2["userid"], text="<b>" + user1["username"] + "</b> has declared battle! Are you ready?", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        #start a thread to enforce a 30 second timeout rule
        threading.Thread(target=um.connect_users, args=(context.bot, user1, user2, declare_war.message_id, 0.5)).start()
    return None

def reset_user(update, context):
    """
    Function that executes from the /reset command to reset user state to 0. Only admins have the right to execute this command.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    #if invalid user, the validate_user function will prompt to register with /war command
    if um.validate_user(update, context, update.message.chat_id, update.message.from_user.username) is False:
        return None
    else:
        #if valid user, load in user data
        user1 = um.load_user_data([update.message.from_user.username])
    #only admin users can execute resets
    if user1["user_group"] == "admin":
        user2 = um.load_user_data([context.args[0]])
        user2["user_status"] = "0"
        um.save_user_data([user2])
        context.bot.send_message(chat_id=user1["userid"], text="User reset successful!")
    else:
        context.bot.send_message(chat_id=user1["userid"], text="You do not have the permission!")
    return None