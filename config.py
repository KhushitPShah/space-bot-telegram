"""
config.py - Configuration file for the Space Simulation Telegram Game Bot.
Set all parameters and secrets needed.
"""

# Telegram bot API token (replace with your own token)
TELEGRAM_API_TOKEN = "YOUR_TELEGRAM_BOT_API_TOKEN"

# SQLite database filename
DATABASE_FILENAME = "space_game.db"

# Starting resources and spaceship stats
STARTING_FUEL = 100
STARTING_OXYGEN = 100
STARTING_ENERGY = 100
STARTING_CARGO = 0
STARTING_WEAPONS = 10
STARTING_SHIELDS = 50
STARTING_CREW = 3
STARTING_CREDITS = 100

# Travel settings: fuel cost per sector and travel time (seconds per sector)
FUEL_COST_PER_SECTOR = 5
TRAVEL_TIME_PER_SECTOR = 30

# Upgrade constants
UPGRADE_COST_MULTIPLIER = 1.5

# Random event probabilities (in percentages)
EVENT_PROBABILITIES = {
    "nothing": 20,
    "enemy_encounter": 20,
    "space_disaster": 10,
    "resource_find": 30,
    "mission_offer": 20,
}

# Battle settings
BATTLE_TURN_TIME = 10  # seconds per turn

# Crew skills available for recruitment
CREW_SKILLS = ["pilot", "engineer", "gunner", "scientist", "medic"]

# Alliance settings
ALLIANCE_JOIN_COST = 50

# Total number of different conditions affecting gameplay (for extended events)
CONDITIONS_COUNT = 30

# Additional miscellaneous constants
SHIP_REPAIR_COST = 20
SHOP_PRICE_MODIFIER = 1.2

# Log file setup (path or file name)
LOG_FILE = "space_game.log"