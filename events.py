"""
events.py - Defines random events occurring during space exploration.
These events include battles, discoveries, disasters, and mission triggers.
"""

import random
import logging
import config
import database
from spaceship import Spaceship

logger = logging.getLogger(__name__)


def random_sector_event(context):
    """
    Scheduled function for random sector events.
    Triggers for each active player.
    """
    telegram_ids = get_active_telegram_ids()
    for tid in telegram_ids:
        event_type, description = get_random_event()
        database.add_event_log(tid, event_type, description)
        logger.info(f"Random event for user {tid}: {description}")
    return


def get_active_telegram_ids():
    """
    Retrieve active players.
    For demo purposes, this returns a fixed list.
    """
    return [111111, 222222, 333333]


def get_random_event():
    """
    Select a random event based on weights.
    Returns a tuple: (event_type, description)
    """
    r = random.randint(1, 100)
    cumulative = 0
    event = "nothing"
    for key, prob in config.EVENT_PROBABILITIES.items():
        cumulative += prob
        if r <= cumulative:
            event = key
            break

    if event == "nothing":
        return "info", "The sector is quiet. Nothing happens."
    elif event == "enemy_encounter":
        enemy = random.choice(["pirates", "alien fighters", "bounty hunters"])
        return "battle", f"Ambushed by {enemy} in deep space!"
    elif event == "space_disaster":
        disaster = random.choice(["asteroid field", "black hole", "system failure"])
        return "disaster", f"A {disaster} suddenly affects your ship!"
    elif event == "resource_find":
        resource = random.choice(["rare minerals", "volatile gases", "alien artifacts"])
        return "resource", f"Discovered {resource} drifting in space."
    elif event == "mission_offer":
        return "mission", "A distress signal offers a new mission opportunity."
    else:
        return "unknown", "An inexplicable phenomenon occurs."


def extra_event_condition(index: int):
    """
    Additional conditions (30+ unique events) affecting gameplay.
    """
    conditions = [
        "ion storm", "solar flare", "quantum anomaly", "wormhole disturbance",
        "time dilation field", "gravitational wave", "neutron star proximity",
        "space debris field", "frozen nebula", "plasma surge", "magnetic disruption",
        "radiation burst", "cosmic ray shower", "extragalactic signal", "virtual mirage",
        "subspace echo", "dark matter condensation", "cosmic string interference",
        "orbital decay", "comet tail passage", "electromagnetic pulse", "stellar winds",
        "volcanic activity on a moon", "cryo-cloud formation", "metamorphic signal",
        "lost satellite", "computational glitch", "pirate misinformation", "anomalous reading",
        "haunted void"
    ]
    return conditions[index % len(conditions)]