"""
alliance.py - Implements alliance functionalities for the Space Simulation Telegram Game Bot.
Players can view existing alliances, create a new alliance, and join one.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import database
import config

logger = logging.getLogger(__name__)

def alliance_menu(update: Update, context: CallbackContext):
    """
    Display the alliance menu with options to view alliances or create an alliance.
    """
    keyboard = [
        [InlineKeyboardButton("View Alliances", callback_data="alliance_view")],
        [InlineKeyboardButton("Create Alliance", callback_data="alliance_create")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Alliance Menu - Choose an option:", reply_markup=reply_markup)

def alliance_callback(update: Update, context: CallbackContext):
    """
    Handle alliance menu callbacks.
    """
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "alliance_view":
        alliances = database.get_alliances()
        if alliances:
            text = "Available Alliances:\n"
            for alliance in alliances:
                text += f"- {alliance['alliance_name']} (ID: {alliance['id']})\n"
        else:
            text = "No alliances available at the moment."
        query.edit_message_text(text)
    elif data == "alliance_create":
        # For simplicity, automatically create an alliance with a generated name.
        alliance_name = f"Alliance_{query.from_user.username or query.from_user.first_name}"
        alliance_id = database.create_alliance(alliance_name)
        # The creator automatically joins the newly created alliance.
        database.join_alliance(query.from_user.id, alliance_id)
        text = f"Alliance '{alliance_name}' created and you have joined it!"
        query.edit_message_text(text)
    else:
        query.edit_message_text("Unknown alliance action.")