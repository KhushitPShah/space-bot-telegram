"""
spaceship.py - Contains classes and methods to simulate spaceship management.
This module handles fuel, oxygen, energy, cargo, weapons, shields, crew, and upgrades.
"""

import random
import logging
import config
import database

logger = logging.getLogger(__name__)


class Spaceship:
    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id
        data = database.get_spaceship(telegram_id)
        if data:
            self.fuel = data["fuel"]
            self.oxygen = data["oxygen"]
            self.energy = data["energy"]
            self.cargo = data["cargo"]
            self.weapons = data["weapons"]
            self.shields = data["shields"]
            self.crew = data["crew"]
        else:
            # Initialize with default values if no record exists
            self.fuel = config.STARTING_FUEL
            self.oxygen = config.STARTING_OXYGEN
            self.energy = config.STARTING_ENERGY
            self.cargo = config.STARTING_CARGO
            self.weapons = config.STARTING_WEAPONS
            self.shields = config.STARTING_SHIELDS
            self.crew = config.STARTING_CREW
            # Create player record with a default username placeholder
            database.add_player(self.telegram_id, "Unknown")

    def save(self):
        """Save the current state of the spaceship to the database."""
        database.update_spaceship(
            self.telegram_id,
            fuel=self.fuel,
            oxygen=self.oxygen,
            energy=self.energy,
            cargo=self.cargo,
            weapons=self.weapons,
            shields=self.shields,
            crew=self.crew
        )
        logger.info(f"Spaceship state saved for user {self.telegram_id}")

    def travel(self, sectors: int):
        """
        Simulate travel to another sector.
        Costs fuel and returns a status message.
        """
        fuel_needed = sectors * config.FUEL_COST_PER_SECTOR
        if self.fuel < fuel_needed:
            logger.info("Not enough fuel to travel.")
            return False, "Not enough fuel to travel."
        self.fuel -= fuel_needed
        self.save()
        logger.info(f"Traveled {sectors} sectors using {fuel_needed} fuel.")
        return True, f"Traveled {sectors} sectors and used {fuel_needed} fuel."

    def upgrade_system(self, system: str):
        """
        Upgrade a specific system on the spaceship.
        Returns the credit cost for the upgrade.
        """
        if system == "engines":
            cost = int((self.fuel + 1) * config.UPGRADE_COST_MULTIPLIER)
            self.fuel += 10
        elif system == "shields":
            cost = int((self.shields + 1) * config.UPGRADE_COST_MULTIPLIER)
            self.shields += 10
        elif system == "weapons":
            cost = int((self.weapons + 1) * config.UPGRADE_COST_MULTIPLIER)
            self.weapons += 5
        else:
            cost = 100
        database.upgrade_spaceship(self.telegram_id, system, new_level=getattr(self, system, 1), cost=cost)
        self.save()
        logger.info(f"Upgraded {system} for {cost} credits.")
        return cost

    def refuel(self, amount: int):
        """Increase fuel level by the given amount."""
        self.fuel += amount
        self.save()
        logger.info(f"Refueled by {amount}. Current fuel: {self.fuel}")
        return self.fuel

    def repair_shields(self, amount: int):
        """Repair or recharge shields."""
        self.shields += amount
        if self.shields > 100:
            self.shields = 100
        self.save()
        logger.info(f"Repaired shields by {amount}. Current shields: {self.shields}")
        return self.shields

    def status_report(self):
        """Return a formatted status report of the spaceship."""
        report = (
            f"Fuel: {self.fuel}\n"
            f"Oxygen: {self.oxygen}\n"
            f"Energy: {self.energy}\n"
            f"Cargo: {self.cargo}\n"
            f"Weapons: {self.weapons}\n"
            f"Shields: {self.shields}\n"
            f"Crew: {self.crew}\n"
        )
        return report


def scan_environment(telegram_id: int):
    """
    Simulate scanning of the space environment.
    Returns a tuple of (result_type, description).
    """
    outcomes = [
        ("resource", "Detected a deposit of rare minerals."),
        ("danger", "Scanners detect abnormal radiation levels."),
        ("mission", "A distress signal indicates a potential mission."),
        ("nothing", "No significant anomalies in the vicinity.")
    ]
    weights = [30, 20, 20, 30]
    result = random.choices(outcomes, weights=weights)[0]
    return result

# Additional spaceship functionalities can be added below.