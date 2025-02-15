#!/usr/bin/env python3
"""
main.py - Entry point for the Space Simulation Telegram Game Bot.
This file initializes the Telegram bot, configures command and callback handlers,
sets up the job queue for timed events, and starts the bot's polling loop.
"""

import logging
import sys
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, JobQueue

# Import game modules
import config
import database
import game_commands
import events
import alliance
import crew
import shop
import scanning
import missions

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start_bot():
    """
    The main initialization for the Telegram bot and the game.
    It sets up handlers, job queue events, and kicks off the scheduler.
    """
    updater = Updater(token=config.TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Initialize database, create tables if not exist
    database.init_db()

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", game_commands.start))
    dispatcher.add_handler(CommandHandler("spaceship", game_commands.spaceship_status))
    dispatcher.add_handler(CommandHandler("explore", game_commands.explore))
    dispatcher.add_handler(CommandHandler("shop", shop.shop))
    dispatcher.add_handler(CommandHandler("battle", game_commands.battle))
    dispatcher.add_handler(CommandHandler("crew", crew.crew_status))
    dispatcher.add_handler(CommandHandler("missions", missions.missions))
    dispatcher.add_handler(CommandHandler("upgrade", game_commands.upgrade))
    dispatcher.add_handler(CommandHandler("alliance", alliance.alliance_menu))
    dispatcher.add_handler(CommandHandler("scan", scanning.scan))
    dispatcher.add_handler(CommandHandler("steal", game_commands.steal_resources))

    # Callback queries from inline buttons
    dispatcher.add_handler(CallbackQueryHandler(game_commands.button_handler))
    dispatcher.add_handler(CallbackQueryHandler(alliance.alliance_callback, pattern="^alliance_"))
    dispatcher.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))
    dispatcher.add_handler(CallbackQueryHandler(game_commands.travel_callback, pattern="^travel_"))
    dispatcher.add_handler(CallbackQueryHandler(game_commands.upgrade_callback, pattern="^upgrade_"))
    
    # Set up job queue events
    job_queue: JobQueue = updater.job_queue

    # Random sector events every 2 minutes
    job_queue.run_repeating(events.random_sector_event, interval=120, first=10, context={})
    # Periodic spaceship system updates every minute
    job_queue.run_repeating(game_commands.update_ship_status, interval=60, first=5, context={})
    # Periodic mission timer update every 90 seconds
    job_queue.run_repeating(missions.update_missions, interval=90, first=15, context={})

    logger.info("Bot is starting...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user. Shutting down...")
        sys.exit(0)