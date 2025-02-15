"""
missions.py - Implements mission functionalities for the Space Simulation Telegram Game Bot.
Players can view their active missions, accept new missions, and have missions automatically updated
or completed via periodic background tasks.
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import database
import config

logger = logging.getLogger(__name__)

def missions(update: Update, context: CallbackContext):
    """
    Handle the /missions command.
    Displays the user's active missions. If none exist, provides an option to accept a new mission.
    """
    user = update.effective_user
    active_missions = database.get_active_missions(user.id)
    if not active_missions:
        text = "You have no active missions. Would you like to accept a new mission?"
        keyboard = [
            [InlineKeyboardButton("Accept New Mission", callback_data="mission_accept")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text, reply_markup=reply_markup)
    else:
        text = "Your Active Missions:\n"
        for mission in active_missions:
            text += (
                f"- {mission['description']} (Reward: {mission['reward']} credits, "
                f"Time Limit: {mission['time_limit']} seconds)\n"
            )
        update.message.reply_text(text)

def mission_callback(update: Update, context: CallbackContext):
    """
    Handle callback queries related to missions.
    For example, accepting a new mission.
    """
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "mission_accept":
        # Assign a new mission and notify the user.
        new_mission = assign_new_mission(query.from_user.id)
        message = (
            f"New Mission Accepted!\n"
            f"Description: {new_mission['description']}\n"
            f"Reward: {new_mission['reward']} credits\n"
            f"Time Limit: {new_mission['time_limit']} seconds"
        )
        query.edit_message_text(message)
    else:
        query.edit_message_text("Invalid mission action.")

def assign_new_mission(user_id: int) -> dict:
    """
    Assign a new mission to the specified user.
    Generates a mission with randomized description, reward, and time limit.
    Inserts the mission into the database and returns the newly created mission details.
    """
    mission_descriptions = [
        "Rescue the stranded astronauts.",
        "Collect rare minerals from the asteroid belt.",
        "Investigate a suspicious derelict spacecraft.",
        "Deliver critical supplies to an outer rim colony.",
        "Explore an uncharted nebula for anomalies."
    ]
    description = random.choice(mission_descriptions)
    reward = random.randint(20, 100)
    time_limit = random.randint(60, 300)
    # Insert the mission into the database.
    mission_id = database.add_mission(user_id, description, reward, time_limit)
    mission = {
        "id": mission_id,
        "user_id": user_id,
        "description": description,
        "reward": reward,
        "time_limit": time_limit
    }
    logger.info(f"Assigned new mission {mission_id} to user {user_id}.")
    return mission

def update_missions(context: CallbackContext):
    """
    Periodic job to update mission statuses for active users.
    For each user, this function randomly marks a mission as complete to simulate progress, 
    and if the user has no active missions, a new mission is automatically assigned.
    """
    # In a real application, the list of active users would be dynamically determined.
    active_user_ids = [111111, 222222, 333333]
    
    for user_id in active_user_ids:
        active = database.get_active_missions(user_id)
        if active:
            for mission in active:
                # Random chance to mark a mission complete, simulating mission progress.
                if random.choice([True, False]):
                    database.complete_mission(mission['id'])
                    logger.info(f"Mission {mission['id']} completed for user {user_id}.")
        else:
            # If the user has no active missions, assign a new mission.
            assign_new_mission(user_id)

if __name__ == '__main__':
    print("This module is meant to be imported into the Telegram bot framework.")