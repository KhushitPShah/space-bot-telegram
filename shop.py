"""
shop.py - Implements a dynamic shop and black market for the Space Simulation Telegram Game Bot.
Players can purchase various items or upgrades from the shop.
This implementation includes at least 30 different items and an additional way to earn money via trading commodities.
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import config
import database  # Assuming database operations for purchasing/updating credits will be implemented accordingly

logger = logging.getLogger(__name__)

# Define at least 30 shop items as a list of dictionaries.
SHOP_ITEMS = [
    {"id": 1, "name": "Fuel Pack", "price": 10, "description": "Refuel your spaceship with extra fuel."},
    {"id": 2, "name": "Oxygen Tank", "price": 12, "description": "Increase your oxygen reserves."},
    {"id": 3, "name": "Energy Cell", "price": 8, "description": "Boost your energy levels."},
    {"id": 4, "name": "Cargo Module", "price": 25, "description": "Expand your cargo capacity."},
    {"id": 5, "name": "Laser Cannon", "price": 50, "description": "Enhance your offensive capabilities."},
    {"id": 6, "name": "Shield Booster", "price": 45, "description": "Strengthen your shields."},
    {"id": 7, "name": "Navigation System", "price": 35, "description": "Improve your travel accuracy."},
    {"id": 8, "name": "Engine Tuner", "price": 40, "description": "Upgrade your engine efficiency."},
    {"id": 9, "name": "Crew Quarters", "price": 30, "description": "Increase crew capacity."},
    {"id": 10, "name": "Medical Kit", "price": 15, "description": "Heal injured crew members."},
    {"id": 11, "name": "Repair Drone", "price": 60, "description": "Automate ship repairs during battle."},
    {"id": 12, "name": "Cargo Securing Kit", "price": 20, "description": "Prevent cargo loss during turbulence."},
    {"id": 13, "name": "Advanced Sensors", "price": 55, "description": "Better detection of resources and threats."},
    {"id": 14, "name": "Quantum Drive", "price": 80, "description": "Speed up your travel between sectors."},
    {"id": 15, "name": "Stealth Module", "price": 70, "description": "Enhance your ship's evasion capabilities."},
    {"id": 16, "name": "Auto-Pilot System", "price": 65, "description": "Reduce errors in manual navigation."},
    {"id": 17, "name": "Resource Scanner", "price": 50, "description": "Improve scan accuracy for resources."},
    {"id": 18, "name": "Alien Translator", "price": 45, "description": "Communicate with unknown species."},
    {"id": 19, "name": "Battle AI", "price": 85, "description": "Get tactical assistance in battle."},
    {"id": 20, "name": "Hull Plating", "price": 90, "description": "Increase your ship's durability."},
    {"id": 21, "name": "Black Market Guide", "price": 40, "description": "Discover hidden deals in the galaxy."},
    {"id": 22, "name": "Crypto Credits", "price": 100, "description": "Buy premium currency for exclusive items."},
    {"id": 23, "name": "Planetary Map", "price": 30, "description": "Unveil secret locations in space."},
    {"id": 24, "name": "Disaster Sensor", "price": 35, "description": "Predict upcoming space disasters."},
    {"id": 25, "name": "Mission Briefcase", "price": 55, "description": "Unlock exclusive missions and rewards."},
    {"id": 26, "name": "Solar Panels", "price": 25, "description": "Increase energy regeneration on the go."},
    {"id": 27, "name": "Warp Stabilizer", "price": 75, "description": "Stabilize warp drive for longer jumps."},
    {"id": 28, "name": "Resource Converter", "price": 65, "description": "Convert lower-grade resources into valuable ones."},
    {"id": 29, "name": "Crew Booster", "price": 45, "description": "Improve crew efficiency temporarily."},
    {"id": 30, "name": "Experimental Tech", "price": 95, "description": "A mysterious device of unknown benefits."},
]

def shop(update: Update, context: CallbackContext):
    """
    Display the shop menu with inline buttons for each shop item.
    Items are organized in rows with 3 items per row.
    Additionally, include an extra option "Trade Commodities" to earn money.
    """
    keyboard = []
    row = []
    for index, item in enumerate(SHOP_ITEMS):
        button = InlineKeyboardButton(item["name"], callback_data=f"shop_item_{item['id']}")
        row.append(button)
        if (index + 1) % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    # Add an extra row for trading commodities, which represents an alternative way to earn credits.
    trade_button = [InlineKeyboardButton("Trade Commodities", callback_data="shop_trade")]
    keyboard.append(trade_button)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Welcome to the Galactic Shop! Select an item to purchase or choose an option to earn money:",
        reply_markup=reply_markup
    )

def shop_callback(update: Update, context: CallbackContext):
    """
    Handle callback queries for shop items and trading commodities.
    Distinguishes between item purchases and the trade action.
    """
    query = update.callback_query
    query.answer()
    data = query.data

    # If the trade option is selected
    if data == "shop_trade":
        # Simulate a random trading outcome to earn credits.
        earnings = random.randint(5, 50)
        # In a complete implementation, update the player's credits via the database.
        # e.g., database.update_credits(query.from_user.id, earnings)
        message = f"You successfully traded commodities and earned {earnings} credits!"
        logger.info(f"User {query.from_user.id} earned {earnings} credits through trading.")
        query.edit_message_text(message)
        return

    # Otherwise, handle shop item purchase requests.
    try:
        parts = data.split("_")
        if len(parts) != 3 or parts[0] != "shop" or parts[1] != "item":
            query.edit_message_text("Invalid shop command received.")
            return
        item_id = int(parts[2])
    except (ValueError, IndexError):
        query.edit_message_text("Error processing the selected item.")
        return

    # Look up the shop item by its ID.
    item = next((itm for itm in SHOP_ITEMS if itm["id"] == item_id), None)
    if not item:
        query.edit_message_text("Selected item not found.")
        return

    # Simulate a purchase.
    # In a real application, you would verify sufficient credits and update the player’s inventory.
    purchase_successful = True  # Dummy logic for this demonstration.

    if purchase_successful:
        message = (
            f"Purchase successful!\nYou bought: {item['name']}\n"
            f"Price: {item['price']} credits\nDescription: {item['description']}"
        )
        # Optionally record the purchase in the database:
        # database.purchase_item(query.from_user.id, item)
        logger.info(f"User {query.from_user.id} purchased {item['name']} for {item['price']} credits.")
    else:
        message = "Purchase failed! You do not have enough credits."

    query.edit_message_text(message)

if __name__ == '__main__':
    # For direct testing purposes only.
    # In the full bot, these functions would be called via the bot's command and callback handlers.
    print("This module is meant to be imported into the Telegram bot framework.")