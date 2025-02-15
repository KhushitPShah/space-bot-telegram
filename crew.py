"""
crew.py - Implements crew management functionalities.
Handles viewing, recruiting, and managing crew members.
"""

import random
import logging
from telegram import Update
from telegram.ext import CallbackContext

import config
import database

logger = logging.getLogger(__name__)


def crew_status(update: Update, context: CallbackContext):
    """Handle the /crew command to display current crew members."""
    user = update.effective_user
    crew_list = database.get_crew(user.id)
    if not crew_list:
        update.message.reply_text("You have no crew members. Use /recruit to add one.")
    else:
        text = "Crew Members:\n"
        for member in crew_list:
            text += f"- {member['name']} (Skill: {member['skill']}, Level: {member['level']})\n"
        update.message.reply_text(text)


def recruit_crew(update: Update, context: CallbackContext):
    """Handle a command to recruit a new crew member (not directly registered in /start)."""
    user = update.effective_user
    names = ["Alex", "Sam", "Jordan", "Casey", "Riley"]
    name = random.choice(names)
    skill = random.choice(config.CREW_SKILLS)
    database.add_crew_member(user.id, name, skill)
    update.message.reply_text(f"Recruited {name} with skill {skill}!")
    logger.info(f"Recruited crew member {name} with skill {skill} for user {user.id}.")