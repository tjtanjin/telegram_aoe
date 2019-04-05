from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """
    Function to build the menu buttons to show users.
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def show_user_options(username1, username2, n_cols, text, callback_tag):
    """
    Function that takes in button text and callback data to generate the view.
    """
    try:
        button_list = []
        for i in range(0,n_cols):
            button_list.append(InlineKeyboardButton(text[i], callback_data="-" + callback_tag[i] + "-" + username1 + "-" + username2))
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=n_cols))
        return reply_markup
    except Exception as ex:
        print(ex)
