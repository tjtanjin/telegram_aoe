from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from submodules import user_response as ur
from submodules import gameplay_response as gr
import requests, os, sys, json, re
os.chdir(os.path.realpath(sys.path[0]))

#open file to read in token
with open("./token/token.json") as token_file:
    token_file = json.load(token_file)

def main():
    updater = Updater(token_file["token"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('war',ur.welcome_user))
    dp.add_handler(CommandHandler('fight',ur.initiate_fight_user, pass_args=True))
    dp.add_handler(CommandHandler('banish',ur.banish_user, pass_args=True))
    dp.add_handler(CommandHandler('unbanish',ur.unbanish_user, pass_args=True))
    dp.add_handler(CommandHandler('reset',ur.reset_user, pass_args=True))
    dp.add_handler(CallbackQueryHandler(gr.accept_fight, pattern='-accept-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.decline_fight, pattern='-decline-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.launch_attack, pattern='-1-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.repair, pattern='-2\S*-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.hire, pattern='-3\S*-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.flee, pattern='-flee-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.reshow_main_options, pattern='-reshow_main-(\S+)-(\S+)'))
    dp.add_handler(CallbackQueryHandler(gr.quit, pattern='-quit-(\S+)-(\S+)'))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
