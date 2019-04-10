from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from submodules import user_management as um
from submodules import miscellaneous as mc
import random, time, threading, json, redis
#connect to redis db
game_client = redis.Redis(host='localhost', decode_responses=True)
#load config file containing default game stats
with open("./gameplay_config/stats_config.json", "r") as config_file:
    config = json.load(config_file)

#main class used to hold user values during battle
class Empire():
    def __init__(self):
        self.civilization = "" #name of empire
        self.username = ""
        self.userid = ""
        self.castle = {'current_castle_health': '', 'max_castle_health': '', 'repair_1': '', 'repair_2': '', 'repair_3': ''} #castle properties
        self.gold = {'amount': ''} #current/starting gold (no max, increases by 100 every turn)
        self.soldier = {'price': '', 'num': '', 'attack': '', 'armor': 4, 'desc': "A light infantry unit with weak attack"} #soldier properties
        self.warrior = {'price': '', 'num': '', 'attack': '', 'armor': 5, 'desc': "A toughened soldier with moderate attack"} #warrior properties
        self.knight = {'price': '', 'num': '', 'attack': '', 'armor': 7, 'desc': "A heavily armored unit with strong attack"} #knight properties

def gameover(bot, cplayer, nplayer):
    """
    Function that executes during gameover.
    Args:
        bot: from telegram bot
        cplayer: current player(player that won)
        nplayer: next player(player that lost)
    """
    #display quit button after game
    cplayer_reply_markup = mc.show_user_options(cplayer.username, nplayer.username, 1, ["Quit"], ["quit"])
    nplayer_reply_markup = mc.show_user_options(nplayer.username, cplayer.username, 1, ["Quit"], ["quit"])
    bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/WKBAB3YpXPVDO/giphy.gif?cid=790b76115ca4d7867156474432c0afef", caption="You lost! The <b>" + nplayer.civilization + "</b> are victorious!", reply_markup=cplayer_reply_markup, parse_mode=ParseMode.HTML)
    bot.sendDocument(chat_id=nplayer.userid, document="https://media1.giphy.com/media/Yb9lErqzrRr3O/giphy.gif?cid=790b76115ca4de1069482e65775e3b6e", caption="You are victorious!", reply_markup=nplayer_reply_markup)
    return None

def load_game_stats(username1, username2):
    """
    Function that loads the current game stats for the battle.
    Args:
        username1: first player's username
        username2: second player's username
    """
    user1 = Empire()
    user2 = Empire()
    user1.civilization = game_client.get(username1 + "_civilization")
    user1.username = game_client.get(username1 + "_username")
    user1.userid = game_client.get(username1 + "_userid")
    user1.castle["max_castle_health"] = int(game_client.hgetall(username1 + "_castle")["max_castle_health"])
    user1.castle["current_castle_health"] = int(game_client.hgetall(username1 + "_castle")["current_castle_health"])
    user1.castle["repair_1"] = int(game_client.hgetall(username1 + "_castle")["repair_1"])
    user1.castle["repair_2"] = int(game_client.hgetall(username1 + "_castle")["repair_2"])
    user1.castle["repair_3"] = int(game_client.hgetall(username1 + "_castle")["repair_3"])
    user1.gold["amount"] = int(game_client.hgetall(username1 + "_gold")["amount"])
    user1.soldier["attack"] = int(game_client.hgetall(username1 + "_soldier")["attack"])
    user1.soldier["price"] = int(game_client.hgetall(username1 + "_soldier")["price"])
    user1.soldier["num"] = int(game_client.hgetall(username1 + "_soldier")["num"])
    user1.warrior["attack"] = int(game_client.hgetall(username1 + "_warrior")["attack"])
    user1.warrior["price"] = int(game_client.hgetall(username1 + "_warrior")["price"])
    user1.warrior["num"] = int(game_client.hgetall(username1 + "_warrior")["num"])
    user1.knight["attack"] = int(game_client.hgetall(username1 + "_knight")["attack"])
    user1.knight["price"] = int(game_client.hgetall(username1 + "_knight")["price"])
    user1.knight["num"] = int(game_client.hgetall(username1 + "_knight")["num"])
    user2.civilization = game_client.get(username2 + "_civilization")
    user2.username = game_client.get(username2 + "_username")
    user2.userid = game_client.get(username2 + "_userid")
    user2.castle["max_castle_health"] = int(game_client.hgetall(username2 + "_castle")["max_castle_health"])
    user2.castle["current_castle_health"] = int(game_client.hgetall(username2 + "_castle")["current_castle_health"])
    user2.castle["repair_1"] = int(game_client.hgetall(username2 + "_castle")["repair_1"])
    user2.castle["repair_2"] = int(game_client.hgetall(username2 + "_castle")["repair_2"])
    user2.castle["repair_3"] = int(game_client.hgetall(username2 + "_castle")["repair_3"])
    user2.gold["amount"] = int(game_client.hgetall(username2 + "_gold")["amount"])
    user2.soldier["attack"] = int(game_client.hgetall(username2 + "_soldier")["attack"])
    user2.soldier["price"] = int(game_client.hgetall(username2 + "_soldier")["price"])
    user2.soldier["num"] = int(game_client.hgetall(username2 + "_soldier")["num"])
    user2.warrior["attack"] = int(game_client.hgetall(username2 + "_warrior")["attack"])
    user2.warrior["price"] = int(game_client.hgetall(username2 + "_warrior")["price"])
    user2.warrior["num"] = int(game_client.hgetall(username2 + "_warrior")["num"])
    user2.knight["attack"] = int(game_client.hgetall(username2 + "_knight")["attack"])
    user2.knight["price"] = int(game_client.hgetall(username2 + "_knight")["price"])
    user2.knight["num"] = int(game_client.hgetall(username2 + "_knight")["num"])
    return user1, user2

def save_game_stats(user1, user2):
    """
    Function that saves the current state of the battle.
    Args:
        user1: first user
        user2: second user
    """
    game_client.hmset(str(user1.username) + "_castle", user1.castle)
    game_client.hmset(str(user1.username) + "_gold", user1.gold)
    game_client.hmset(str(user1.username) + "_soldier", user1.soldier)
    game_client.hmset(str(user1.username) + "_warrior", user1.warrior)
    game_client.hmset(str(user1.username) + "_knight", user1.knight)
    game_client.hmset(str(user2.username) + "_castle", user2.castle)
    game_client.hmset(str(user2.username) + "_gold", user2.gold)
    game_client.hmset(str(user2.username) + "_soldier", user2.soldier)
    game_client.hmset(str(user2.username) + "_warrior", user2.warrior)
    game_client.hmset(str(user2.username) + "_knight", user2.knight)

def check_gold(bot, username, gold):
    """
    Function that checks for user's gold.
    Args:
        bot: from telegram bot
        username: userid of the user to check for
        gold: amount of gold to check
    """
    if int(game_client.hgetall(username + "_gold")["amount"]) >= gold:
        return True
    else:
        return False

def display(bot, username1, username2, display_status_only=False):
    """
    Function that displays and stats and prompt users every turn.
    Args:
        bot: from telegram bot
        username1: usernane of current player
        username2: username of next player
        display_status_only: if true, will only show status(used at end of turn to reflect user actions)
    """
    cplayer, nplayer = load_game_stats(username1, username2)
    if display_status_only is False:
        cplayer.gold['amount'] += 100
    html_display = """Status\n
    <b>---------------- Castle ----------------</b>\n
    {} Castle Health: {}\n
    {} Castle Health: {}\n
    <b>---------------- Income ---------------</b>\n
    Gold {} | +100 Every Turn\n
    <b>---------------- Units ------------------</b>\n
    Soldier(s): {}\n
    Warriors(s): {}\n
    Knight(s): {}\n
    <b>------------------------------------------</b>\n
    """.format(cplayer.civilization, cplayer.castle['current_castle_health'], nplayer.civilization, nplayer.castle['current_castle_health'], cplayer.gold['amount'], cplayer.soldier['num'], cplayer.warrior['num'], cplayer.knight['num'])
    bot.send_message(chat_id=cplayer.userid, text=html_display, parse_mode=ParseMode.HTML)
    if display_status_only is True:
        return None
    #if any side's health is 0, game is over
    if cplayer.castle['current_castle_health'] <= 0:
        gameover(bot, cplayer, nplayer)
        return None
    if nplayer.castle['current_castle_health'] <= 0:
        gameover(bot, nplayer, cplayer)
        return None
    reply_markup = mc.show_user_options(cplayer.username, nplayer.username, 4, ["Attack", "Repair", "Hire", "Flee"], ["1", "2", "3", "flee"])
    user_choose = bot.send_message(chat_id=cplayer.userid, text="What will you do?", reply_markup=reply_markup)
    #start a new thread to enforce 30 second timeout for user choice
    threading.Thread(target=um.choice_timeout_user, args=(bot, cplayer.username, nplayer.username, user_choose.message_id, 0.5)).start()
    bot.send_message(chat_id=nplayer.userid, text="<b>{}</b> are thinking...".format(cplayer.civilization), parse_mode=ParseMode.HTML)
    save_game_stats(cplayer, nplayer)
    return None

def flee(bot, username1, username2):
    """
    Function that handles user quitting halfway through the battle.
    Args:
        bot: from telegram bot
        username1: current player(player who flee)
        username2: next player
    """
    cplayer, nplayer = load_game_stats(username1, username2)
    bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/l2Sqc3POpzkj5r8SQ/giphy.gif?cid=790b76115ca4d58d486d6c6d735969b0", caption="You have fled the war in defeat!")
    bot.sendDocument(chat_id=nplayer.userid, document="https://media3.giphy.com/media/l2Sqc3POpzkj5r8SQ/giphy.gif?cid=790b76115ca4d58d486d6c6d735969b0", caption="<b>{}</b> has fled the war in defeat!".format(cplayer.civilization), parse_mode=ParseMode.HTML)
    cplayer.castle['current_castle_health'] = 0
    save_game_stats(cplayer, nplayer)
    display(bot, username1, username2, display_status_only=True)
    display(bot, username2, username1)
    return None

def attack(bot, username1, username2):
    """
    Function that handles attack action.
    Args:
        bot: from telegram bot
        username1: current player attacking
        username2: next player receiving the attack
    """
    cplayer, nplayer = load_game_stats(username1, username2)
    cplayer_attack_strength = cplayer.soldier['attack'] * cplayer.soldier['num'] + cplayer.warrior['attack'] * cplayer.warrior['num'] + cplayer.knight['attack'] * cplayer.knight['num'] #summing up for attack strength
    cplayer_message_1 = bot.send_message(chat_id=cplayer.userid, text="Preparing forces...\nAttack Strength: <b>{}</b>".format(cplayer_attack_strength), parse_mode=ParseMode.HTML)
    nplayer_message_1 = bot.send_message(chat_id=nplayer.userid, text="<b>{}</b> preparing forces...\nAttack Strength: <b>{}</b>".format(cplayer.civilization, cplayer_attack_strength), parse_mode=ParseMode.HTML)
    time.sleep(2)
    cplayer_message_2 = bot.editMessageText(chat_id=cplayer.userid, message_id=cplayer_message_1.message_id, text="Launching attack...", parse_mode=ParseMode.HTML)
    nplayer_message_2 = bot.editMessageText(chat_id=nplayer.userid, message_id=nplayer_message_1.message_id, text="<b>{}</b> launching attack...".format(cplayer.civilization), parse_mode=ParseMode.HTML)
    time.sleep(3) #simulate loading time #simulate loading time
    luck = random.randint(1,10) #determine 70/30 success/failure of attack
    if luck < 8: #execute if attack successful
        nplayer.castle['current_castle_health'] = nplayer.castle['current_castle_health'] - cplayer_attack_strength #subtract defending castle's health
        if nplayer.castle['current_castle_health'] < 0: #ensure castle health cannot be negative
            nplayer.castle['current_castle_health'] = 0
        s_luck = random.randint(0, cplayer.soldier['num']//4) #randomly give casualty to the attacker
        w_luck = random.randint(0, cplayer.warrior['num']//6) #randomly give casualty to the attacker
        k_luck = random.randint(0, cplayer.knight['num']//8) #randomly give casualty to the attacker
        g_luck = random.randint(100,200) #randomly loot gold
        cplayer.soldier['num'] = cplayer.soldier['num'] - s_luck #subtract casualty from initial amount
        cplayer.warrior['num'] = cplayer.warrior['num'] - w_luck #subtract casualty from initial amount
        cplayer.knight['num'] = cplayer.knight['num'] - k_luck #subtract casualty from initial amount
        cplayer.gold['amount'] = cplayer.gold['amount'] + g_luck #add gold to attacker
        nplayer.gold['amount'] = nplayer.gold['amount'] - g_luck #subtract gold from defender
        if nplayer.gold['amount'] < 0: #ensure gold cannot be negative
            disparity = -(nplayer.gold['amount'])
            nplayer.gold['amount'] = 0
            cplayer.gold['amount'] = cplayer.gold['amount'] - disparity #ensure no "overloot"
            cplayer_message_3 = bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_2.message_id)
            nplayer_message_3 = bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_2.message_id)
            bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/5xtDarIhRgrJrXksdzi/giphy.gif?cid=790b76115ca4d9644255786a679a99da", caption="The attack was a success!\n- You plundered all their gold!\n- <b>{}</b> Castle took <b>{}</b> damage!\n- <b>{}</b> soldiers, <b>{}</b> warriors and <b>{}</b> knights were lost!".format(nplayer.civilization, cplayer_attack_strength, s_luck, w_luck, k_luck), parse_mode=ParseMode.HTML)
            bot.sendDocument(chat_id=nplayer.userid, document="https://media3.giphy.com/media/5xtDarIhRgrJrXksdzi/giphy.gif?cid=790b76115ca4d9644255786a679a99da", caption="<b>{}</b> attack was a success!\n- They plundered all your gold!\n-Your castle took <b>{}</b> damage!".format(cplayer.civilization, cplayer_attack_strength), parse_mode=ParseMode.HTML)
        if nplayer.gold['amount'] > 0:
            cplayer_message_3 = bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_2.message_id)
            nplayer_message_3 = bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_2.message_id)
            bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/5xtDarIhRgrJrXksdzi/giphy.gif?cid=790b76115ca4d9644255786a679a99da", caption="The attack was a success!\n- You plundered <b>{}</b> gold!\n- <b>{}</b> Castle took <b>{}</b> damage!\n- <b>{}</b> soldiers, <b>{}</b> warriors and <b>{}</b> knights were lost!".format(g_luck, nplayer.civilization, cplayer_attack_strength, s_luck, w_luck, k_luck), parse_mode=ParseMode.HTML)
            bot.sendDocument(chat_id=nplayer.userid, document="https://media3.giphy.com/media/5xtDarIhRgrJrXksdzi/giphy.gif?cid=790b76115ca4d9644255786a679a99da", caption="<b>{}</b> attack was a success!\n- They plundered <b>{}</b> gold!\n- Your castle took <b>{}</b> damage!".format(cplayer.civilization, g_luck, cplayer_attack_strength), parse_mode=ParseMode.HTML)
    else: #execute if attack failed
        s_luck = random.randint(0, cplayer.soldier['num']//3) #randomly give casualty to the attacker (Higher casualty rate than successful attack)
        w_luck = random.randint(0, cplayer.warrior['num']//4) #randomly give casualty to the attacker (Higher casualty rate than successful attack)
        k_luck = random.randint(0, cplayer.knight['num']//6) #randomly give casualty to the attacker (Higher casualty rate than successful attack)
        cplayer.soldier['num'] = cplayer.soldier['num'] - s_luck #subtract casualty from initial amount
        cplayer.warrior['num'] = cplayer.warrior['num'] - w_luck #subtract casualty from initial amount
        cplayer.knight['num'] = cplayer.knight['num'] - k_luck #subtract casualty from initial amount
        cplayer_message_3 = bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_2.message_id)
        nplayer_message_3 = bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_2.message_id)
        bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/3og0IPizf4zPR6VMt2/giphy.gif?cid=790b76115ca4daab6445336536f05214", caption="The attack was repelled!\n- <b>{}</b> soldiers, <b>{}</b> warriors and <b>{}</b> knights were lost!".format(s_luck, w_luck, k_luck), parse_mode=ParseMode.HTML)
        bot.sendDocument(chat_id=nplayer.userid, document="https://media3.giphy.com/media/3og0IPizf4zPR6VMt2/giphy.gif?cid=790b76115ca4daab6445336536f05214", caption="You repelled their attack!")
    save_game_stats(cplayer, nplayer)
    display(bot, username1, username2, display_status_only=True)
    display(bot, username2, username1)
    return None

def repair(bot, username1, username2, type):
    """
    Function that handles repair action.
    Args
        bot: from telegram bot
        username1: current player repairing
        username2: next player waiting
        type: type of repair to carry out (100, 200 or 300)
    """
    cplayer, nplayer = load_game_stats(username1, username2)
    if type == "2.1":
        repair = cplayer.castle['repair_1']
        cplayer.castle['current_castle_health'] = cplayer.castle['current_castle_health'] + repair
        cplayer.gold['amount'] = cplayer.gold['amount'] - repair #subtract 100 gold
    elif type == "2.2":
        repair = cplayer.castle['repair_2']
        cplayer.castle['current_castle_health'] = cplayer.castle['current_castle_health'] + repair
        cplayer.gold['amount'] = cplayer.gold['amount'] - repair #subtract 200 gold
    elif type == "2.3":
        repair = cplayer.castle['repair_3']
        cplayer.castle['current_castle_health'] = cplayer.castle['current_castle_health'] + repair
        cplayer.gold['amount'] = cplayer.gold['amount'] - repair #subtract 300 gold
    cplayer_message_1 = bot.send_message(chat_id=cplayer.userid, text="Repairing castle...")
    nplayer_message_1 = bot.send_message(chat_id=nplayer.userid, text="<b>{}</b> repairing castle...".format(cplayer.civilization), parse_mode=ParseMode.HTML)
    time.sleep(3) #simulate loading time
    if cplayer.castle['current_castle_health'] > cplayer.castle['max_castle_health']: #ensure castle health does not exceed max health, set castle health to max and refund gold if so
        gold_refund = cplayer.castle['current_castle_health'] - cplayer.castle['max_castle_health']
        cplayer.castle['current_castle_health'] = cplayer.castle['max_castle_health']
        cplayer.gold['amount'] = cplayer.gold['amount'] + gold_refund
        cplayer_message_2 = bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_1.message_id)
        nplayer_message_2 = bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_1.message_id)
        bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/LJS5HXOM6HX0c/giphy.gif?cid=790b76115ca4db8779506d4f32b09353", caption="Your castle is already at full health! Extra <b>{}</b> gold returned!".format(gold_refund), parse_mode=ParseMode.HTML)
        bot.sendDocument(chat_id=nplayer.userid, document="https://media3.giphy.com/media/LJS5HXOM6HX0c/giphy.gif?cid=790b76115ca4db8779506d4f32b09353", caption="<b>{}</b> castle is already at full health! Extra <b>{}</b> gold returned!".format(cplayer.civilization, gold_refund), parse_mode=ParseMode.HTML)
    elif cplayer.castle['current_castle_health'] <= cplayer.castle['max_castle_health']:
        cplayer_message_2 = bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_1.message_id)
        nplayer_message_2 = bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_1.message_id)
        bot.sendDocument(chat_id=cplayer.userid, document="https://media3.giphy.com/media/LJS5HXOM6HX0c/giphy.gif?cid=790b76115ca4db8779506d4f32b09353", caption="Your castle has repaired <b>{}</b> health!".format(repair), parse_mode=ParseMode.HTML)
        bot.sendDocument(chat_id=nplayer.userid, document="https://media3.giphy.com/media/LJS5HXOM6HX0c/giphy.gif?cid=790b76115ca4db8779506d4f32b09353", caption="<b>{}</b> castle has repaired <b>{}</b> health!".format(cplayer.civilization, repair), parse_mode=ParseMode.HTML)
    save_game_stats(cplayer, nplayer)
    display(bot, username1, username2, display_status_only=True)
    display(bot, username2, username1)
    return None

def hire(bot, username1, username2, type):
    """
    Function that handles hire action.
    Args:
        bot: from telegram bot
        username1: current player hiring
        username2: next player waiting
        type: type of hiring to carry out (soldiers, warriors, knights)
    """
    #determine quantity and type to hire based on type
    cplayer, nplayer = load_game_stats(username1, username2)
    if type[-1] == "1":
        hire_num = 5
    elif type[-1] == "2":
        hire_num = 10
    elif type[-1] == "3":
        hire_num = 15
    if type[0:3] == "3.1":
        cplayer.soldier['num'] += hire_num #Add soldier once hire is successful
        cplayer.gold['amount'] -= hire_num*cplayer.soldier['price'] #Subtract hire price
        cplayer_message_1 = bot.send_message(chat_id=cplayer.userid, text="Hiring <b>{}</b> Soldiers...".format(hire_num), parse_mode=ParseMode.HTML)
        nplayer_message_1 = bot.send_message(chat_id=nplayer.userid, text="<b>{}</b> hiring <b>{}</b> Soldiers...".format(cplayer.civilization, hire_num), parse_mode=ParseMode.HTML)
        time.sleep(3) #simulate loading time
        bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_1.message_id)
        bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_1.message_id)
        bot.sendDocument(chat_id=cplayer.userid, document="https://media.giphy.com/media/3ohs7QZ705ndlrRChy/giphy.gif", caption="You successfully hired <b>{}</b> Soldiers!".format(hire_num), parse_mode=ParseMode.HTML)
        bot.sendDocument(chat_id=nplayer.userid, document="https://media.giphy.com/media/3ohs7QZ705ndlrRChy/giphy.gif", caption="<b>{}</b> successfully hired <b>{}</b> Soldiers!".format(cplayer.civilization, hire_num), parse_mode=ParseMode.HTML)
    elif type[0:3] == "3.2":
        cplayer.warrior['num'] += hire_num #Add soldier once hire is successful
        cplayer.gold['amount'] -= hire_num*cplayer.warrior['price'] #Subtract hire price
        cplayer_message_1 = bot.send_message(chat_id=cplayer.userid, text="Hiring <b>{}</b> Warriors...".format(hire_num), parse_mode=ParseMode.HTML)
        nplayer_message_1 = bot.send_message(chat_id=nplayer.userid, text="<b>{}</b> hiring <b>{}</b> Warriors...".format(cplayer.civilization, hire_num), parse_mode=ParseMode.HTML)
        time.sleep(3) #simulate loading time
        bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_1.message_id)
        bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_1.message_id)
        bot.sendDocument(chat_id=cplayer.userid, document="https://media.giphy.com/media/3ohs7QZ705ndlrRChy/giphy.gif", caption="You successfully hired <b>{}</b> Warriors!".format(hire_num), parse_mode=ParseMode.HTML)
        bot.sendDocument(chat_id=nplayer.userid, document="https://media.giphy.com/media/3ohs7QZ705ndlrRChy/giphy.gif", caption="<b>{}</b> successfully hired <b>{}</b> Warriors!".format(cplayer.civilization, hire_num), parse_mode=ParseMode.HTML)
    elif type[0:3] == "3.3":
        cplayer.knight['num'] += hire_num #Add soldier once hire is successful
        cplayer.gold['amount'] -= hire_num*cplayer.knight['price'] #Subtract hire price
        cplayer_message_1 = bot.send_message(chat_id=cplayer.userid, text="Hiring <b>{}</b> Knights...".format(hire_num), parse_mode=ParseMode.HTML)
        nplayer_message_1 = bot.send_message(chat_id=nplayer.userid, text="<b>{}</b> hiring <b>{}</b> Knights...".format(cplayer.civilization, hire_num), parse_mode=ParseMode.HTML)
        time.sleep(3) #simulate loading time
        bot.deleteMessage(chat_id=cplayer.userid, message_id=cplayer_message_1.message_id)
        bot.deleteMessage(chat_id=nplayer.userid, message_id=nplayer_message_1.message_id)
        bot.sendDocument(chat_id=cplayer.userid, document="https://media.giphy.com/media/3ohs7QZ705ndlrRChy/giphy.gif", caption="You successfully hired <b>{}</b> Knights!".format(hire_num), parse_mode=ParseMode.HTML)
        bot.sendDocument(chat_id=nplayer.userid, document="https://media.giphy.com/media/3ohs7QZ705ndlrRChy/giphy.gif", caption="<b>{}</b> successfully hired <b>{}</b> Knights!".format(cplayer.civilization, hire_num), parse_mode=ParseMode.HTML)
    save_game_stats(cplayer, nplayer)
    display(bot, username1, username2, display_status_only=True)
    display(bot, username2, username1)
    return None

def start(bot, username1, chat_id1, username2, chat_id2):
    """
    Function executed at the start of battle.
    Args:
        bot: from telegram bot
        username1: username of first player
        chat_id1: userid of first player
        username2: username of second player
        chat_id2: userid of second player
    """
    #set to default all values and assign usernames and userids for mapping purposes
    user1 = Empire()
    user2 = Empire()
    user1.civilization = game_client.set(username1 + "_civilization", "Egyptians")
    user1.username = game_client.set(username1 + "_username", username1)
    user1.userid = game_client.set(username1 + "_userid", chat_id1)
    user1.castle = game_client.hmset(username1 + "_castle", config["castle"])
    user1.gold = game_client.hmset(username1 + "_gold", config["gold"])
    user1.soldier = game_client.hmset(username1 + "_soldier", config["soldier"])
    user1.warrior = game_client.hmset(username1 + "_warrior", config["warrior"])
    user1.knight = game_client.hmset(username1 + "_knight", config["knight"])
    user2.civilization = game_client.set(username2 + "_civilization", "Greeks")
    user2.username = game_client.set(username2 + "_username", username2)
    user2.userid = game_client.set(username2 + "_userid", chat_id2)
    user2.castle = game_client.hmset(username2 + "_castle", config["castle"])
    user2.gold = game_client.hmset(username2 + "_gold", config["gold"])
    user2.soldier = game_client.hmset(username2 + "_soldier", config["soldier"])
    user2.warrior = game_client.hmset(username2 + "_warrior", config["warrior"])
    user2.knight = game_client.hmset(username2 + "_knight", config["knight"])
    display(bot, username2, username1, display_status_only=True)
    display(bot, username1, username2)
    return None
