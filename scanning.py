"""
scanning.py - Implements the scanning functionality for the Space Simulation Telegram Game Bot.
Players can scan space objects and planets to reveal resources, dangers, or mission opportunities.
"""

import logging
from telegram import Update
from telegram.ext import CallbackContext
import spaceship

logger = logging.getLogger(__name__)

def scan(update: Update, context: CallbackContext):
    """
    Handle the /scan command to perform a space environment scan.
    """
    user = update.effective_user
    result_type, description = spaceship.scan_environment(user.id)
    message = f"Scan Result: {description}"
    update.message.reply_text(message)