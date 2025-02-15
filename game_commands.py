"""
game_commands.py - Contains Telegram command and callback handlers for gameplay.
This module interacts with the user via Telegram and calls appropriate engine functions.
"""

import random
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import config
import database
import spaceship
import battles

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Handle the /start command: welcome the user and initialize game data."""
    user = update.effective_user
    database.add_player(user.id, user.username or "Player")
    welcome = (
        f"Welcome, {user.first_name}! Your deep space adventure is about to begin.\n"
        "Use the commands and buttons to manage your ship, explore, battle, upgrade, and more.\n\n"
        "Commands:\n"
        "/spaceship - View your ship status\n"
        "/explore - Travel to a new sector\n"
        "/shop - Enter the shop/black market\n"
        "/battle - Initiate a battle\n"
        "/crew - Manage your crew\n"
        "/missions - View missions\n"
        "/upgrade - Upgrade ship systems\n"
        "/alliance - Join alliances\n"
        "/scan - Scan for resources and missions\n"
        "/steal - Attempt to steal resources"
    )
    update.message.reply_text(welcome)


def spaceship_status(update: Update, context: CallbackContext):
    """Handle the /spaceship command to show the current ship status."""
    user = update.effective_user
    ship = spaceship.Spaceship(user.id)
    update.message.reply_text("Spaceship Status:\n" + ship.status_report())


def explore(update: Update, context: CallbackContext):
    """Handle the /explore command to initiate travel with inline sector buttons."""
    keyboard = [
        [InlineKeyboardButton("1 Sector", callback_data="travel_1"),
         InlineKeyboardButton("2 Sectors", callback_data="travel_2")],
        [InlineKeyboardButton("3 Sectors", callback_data="travel_3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose how many sectors to travel:", reply_markup=reply_markup)


def battle(update: Update, context: CallbackContext):
    """Handle the /battle command to start a combat encounter."""
    user = update.effective_user
    enemy = random.choice(["pirates", "alien fighters", "bounty hunters"])
    update.message.reply_text(f"Encountered {enemy}! Battle commencing...")
    result, log = battles.initiate_battle(user.id, enemy)
    outcome = "\n".join(log) + f"\nBattle result: {result.upper()}"
    update.message.reply_text(outcome)


def steal_resources(update: Update, context: CallbackContext):
    """
    Handle the /steal command to perform a risk-reward resource theft.
    For demo purposes, success is randomized.
    """
    user = update.effective_user
    chance = random.randint(1, 100)
    if chance > 50:
        update.message.reply_text("Steal attempt succeeded! You snatched some resources.")
        database.add_event_log(user.id, "steal", "Successfully stole resources.")
    else:
        update.message.reply_text("Steal attempt failed! You encountered resistance.")
        database.add_event_log(user.id, "steal", "Steal attempt failed.")
    

def upgrade(update: Update, context: CallbackContext):
    """Handle the /upgrade command to show system upgrade options."""
    keyboard = [
        [InlineKeyboardButton("Engines", callback_data="upgrade_engines"),
         InlineKeyboardButton("Shields", callback_data="upgrade_shields")],
        [InlineKeyboardButton("Weapons", callback_data="upgrade_weapons")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select a system to upgrade:", reply_markup=reply_markup)


def button_handler(update: Update, context: CallbackContext):
    """
    General handler for inline button callback queries not handled by other modules.
    Delegates travel and upgrade requests.
    """
    query = update.callback_query
    query.answer()
    data = query.data

    if data.startswith("travel_"):
        travel_callback(update, context)
    elif data.startswith("upgrade_"):
        upgrade_callback(update, context)
    else:
        query.edit_message_text("Unknown action.")


def travel_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    sectors = int(query.data.split("_")[1])
    user_id = query.from_user.id
    ship = spaceship.Spaceship(user_id)
    success, msg = ship.travel(sectors)
    query.edit_message_text(msg)


def upgrade_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    system = query.data.split("_")[1]
    user_id = query.from_user.id
    ship = spaceship.Spaceship(user_id)
    cost = ship.upgrade_system(system)
    query.edit_message_text(f"Upgraded {system}. It cost {cost} credits.")


def update_ship_status(context: CallbackContext):
    """
    Periodic job to update spaceship systems (simulate regeneration or repairs).
    """
    # For a real implementation, iterate through all active players.
    for tid in [111111, 222222, 333333]:
        ship = spaceship.Spaceship(tid)
        # Regenerate energy & oxygen moderately.
        ship.energy = min(ship.energy + 2, 100)
        ship.oxygen = min(ship.oxygen + 1, 100)
        ship.save()