"""
battles.py - Implements the turn-based combat system.
This module simulates battles between the player's spaceship and enemies.
"""

import random
import time
import logging
import config
import database

logger = logging.getLogger(__name__)


class Battle:
    def __init__(self, telegram_id: int, enemy_type: str):
        self.telegram_id = telegram_id
        self.enemy_type = enemy_type
        self.turn = 0
        self.player_health = 100
        self.enemy_health = random.randint(50, 120)
        self.battle_over = False
        self.battle_log = []

    def player_attack(self):
        """Simulate player's attack turn."""
        damage = random.randint(10, 30)
        self.enemy_health -= damage
        self.battle_log.append(f"Player attacked {self.enemy_type} for {damage} damage.")
        logger.info(f"Player attacked {self.enemy_type} for {damage} damage.")
        if self.enemy_health <= 0:
            self.enemy_health = 0
            self.battle_over = True
            self.battle_log.append(f"Enemy {self.enemy_type} defeated!")
        return damage

    def enemy_attack(self):
        """Simulate enemy's attack turn."""
        damage = random.randint(5, 25)
        self.player_health -= damage
        self.battle_log.append(f"Enemy {self.enemy_type} attacked for {damage} damage.")
        logger.info(f"Enemy {self.enemy_type} attacked for {damage} damage.")
        if self.player_health <= 0:
            self.player_health = 0
            self.battle_over = True
            self.battle_log.append("Player defeated!")
        return damage

    def execute_turn(self):
        """Execute a full turn (player then enemy)."""
        if self.battle_over:
            return
        self.turn += 1
        self.battle_log.append(f"--- Turn {self.turn} ---")
        self.player_attack()
        if not self.battle_over:
            self.enemy_attack()

    def simulate_battle(self):
        """Simulate the complete battle."""
        while not self.battle_over:
            self.execute_turn()
            time.sleep(0.5)
        result = "win" if self.player_health > 0 else "loss"
        database.add_event_log(self.telegram_id, "battle", "\n".join(self.battle_log))
        logger.info(f"Battle ended with a {result} for user {self.telegram_id}.")
        return result, self.battle_log


def initiate_battle(telegram_id: int, enemy_type: str):
    """Interface function to start a battle."""
    battle = Battle(telegram_id, enemy_type)
    return battle.simulate_battle()