"""
database.py - Database interface for the Space Simulation Telegram Game Bot.
This module uses SQLite to store and retrieve persistent player and game data.
"""

import sqlite3
import threading
import logging
import config

logger = logging.getLogger(__name__)
database_lock = threading.Lock()


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(config.DATABASE_FILENAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with all required tables."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()

        # Players table for user basic info
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            spaceship_level INTEGER DEFAULT 1,
            credits INTEGER DEFAULT ?
        )
        """, (config.STARTING_CREDITS,))

        # Spaceship table with current stats
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS spaceship (
            telegram_id INTEGER PRIMARY KEY,
            fuel INTEGER,
            oxygen INTEGER,
            energy INTEGER,
            cargo INTEGER,
            weapons INTEGER,
            shields INTEGER,
            crew INTEGER,
            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(telegram_id) REFERENCES players(telegram_id)
        )
        """)

        # Crew table: each crew member record
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crew (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            name TEXT,
            skill TEXT,
            level INTEGER DEFAULT 1,
            FOREIGN KEY(telegram_id) REFERENCES players(telegram_id)
        )
        """)

        # Missions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            description TEXT,
            reward INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            time_limit INTEGER,
            FOREIGN KEY(telegram_id) REFERENCES players(telegram_id)
        )
        """)

        # Upgrades table to log upgrade history
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS upgrades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            type TEXT,
            level INTEGER,
            cost INTEGER,
            upgraded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(telegram_id) REFERENCES players(telegram_id)
        )
        """)

        # Event logs table for battles, encounters, etc.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            event_type TEXT,
            event_details TEXT,
            event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Alliances table: basic alliance matchmaking without ranking
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alliances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alliance_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Alliance membership linking players to alliances
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alliance_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            alliance_id INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(telegram_id) REFERENCES players(telegram_id),
            FOREIGN KEY(alliance_id) REFERENCES alliances(id)
        )
        """)

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully.")


def add_player(telegram_id: int, username: str):
    """Insert a new player and initialize default spaceship details."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO players (telegram_id, username) VALUES (?, ?)",
                       (telegram_id, username))
        conn.commit()

        # Initialize spaceship if not already set up
        cursor.execute("SELECT telegram_id FROM spaceship WHERE telegram_id = ?", (telegram_id,))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO spaceship (telegram_id, fuel, oxygen, energy, cargo, weapons, shields, crew)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (telegram_id, config.STARTING_FUEL, config.STARTING_OXYGEN,
                  config.STARTING_ENERGY, config.STARTING_CARGO, config.STARTING_WEAPONS,
                  config.STARTING_SHIELDS, config.STARTING_CREW))
            conn.commit()
        conn.close()


def get_spaceship(telegram_id: int):
    """Retrieve a player's spaceship details."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM spaceship WHERE telegram_id = ?", (telegram_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


def update_spaceship(telegram_id: int, **kwargs):
    """Update spaceship fields (fuel, oxygen, etc.) for the given player."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        fields = []
        params = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            params.append(value)
        params.append(telegram_id)
        query = f"UPDATE spaceship SET {', '.join(fields)}, last_update = CURRENT_TIMESTAMP WHERE telegram_id = ?"
        cursor.execute(query, tuple(params))
        conn.commit()
        conn.close()


def add_event_log(telegram_id: int, event_type: str, details: str):
    """Insert a log entry for an event (battle, discovery, etc.)."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO event_logs (telegram_id, event_type, event_details)
        VALUES (?, ?, ?)
        """, (telegram_id, event_type, details))
        conn.commit()
        conn.close()


def add_crew_member(telegram_id: int, name: str, skill: str):
    """Add a new crew member to the player's crew."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO crew (telegram_id, name, skill)
        VALUES (?, ?, ?)
        """, (telegram_id, name, skill))
        conn.commit()
        conn.close()


def get_crew(telegram_id: int):
    """Retrieve all crew members for the given player."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crew WHERE telegram_id = ?", (telegram_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]


def add_mission(telegram_id: int, description: str, reward: int, time_limit: int):
    """Insert a new mission for the player."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO missions (telegram_id, description, reward, status, time_limit)
        VALUES (?, ?, ?, 'active', ?)
        """, (telegram_id, description, reward, time_limit))
        conn.commit()
        conn.close()


def get_active_missions(telegram_id: int):
    """Retrieve active missions for the player."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM missions WHERE telegram_id = ? AND status = 'active'", (telegram_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]


def complete_mission(mission_id: int):
    """Mark a mission as completed."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE missions SET status = 'completed' WHERE id = ?", (mission_id,))
        conn.commit()
        conn.close()


def upgrade_spaceship(telegram_id: int, upgrade_type: str, new_level: int, cost: int):
    """Record an upgrade in the database and update player's spaceship level."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO upgrades (telegram_id, type, level, cost)
        VALUES (?, ?, ?, ?)
        """, (telegram_id, upgrade_type, new_level, cost))
        cursor.execute("""
        UPDATE players SET spaceship_level = ?
        WHERE telegram_id = ?
        """, (new_level, telegram_id))
        conn.commit()
        conn.close()


def join_alliance(telegram_id: int, alliance_id: int):
    """Add a player to an alliance."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO alliance_members (telegram_id, alliance_id)
        VALUES (?, ?)
        """, (telegram_id, alliance_id))
        conn.commit()
        conn.close()


def create_alliance(alliance_name: str) -> int:
    """Create a new alliance and return its new ID."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO alliances (alliance_name)
        VALUES (?)
        """, (alliance_name,))
        conn.commit()
        alliance_id = cursor.lastrowid
        conn.close()
        return alliance_id


def get_alliances():
    """Retrieve all alliances."""
    with database_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alliances")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]