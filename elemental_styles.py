# elemental_styles.py

# Original system for backward compatibility
ELEMENTAL_STYLES = {
    "Flame": {
        "qi_gain_multiplier": 1.5,
        "breakthrough_chance_modifier": -0.10,
        "description": "Volatile power. High Qi gain, harder breakthroughs."
    },
    "Ice": {
        "qi_gain_multiplier": 0.8,
        "breakthrough_chance_modifier": 0.20,
        "description": "Stable and slow. Easier breakthroughs, less Qi."
    },
    "Lightning": {
        "qi_gain_multiplier": 1.0,
        "breakthrough_chance_modifier": 0.30,
        "description": "High risk/reward cultivation."
    },
    "Earth": {
        "qi_gain_multiplier": 1.25,
        "breakthrough_chance_modifier": 0.10,
        "description": "Balanced and steady growth."
    },
    "Wind": {
        "qi_gain_multiplier": 1.4,
        "breakthrough_chance_modifier": 0.0,
        "description": "Random cultivation bonuses."
    },
    "Chaos": {
        "qi_gain_multiplier": 0.0,  # Handled dynamically
        "breakthrough_chance_modifier": 0.0,
        "description": "Completely unpredictable cultivation style."
    },
    "Time": {
        "qi_gain_multiplier": 1.0,
        "breakthrough_chance_modifier": 0.0,
        "extra_sessions_per_turn": 1,
        "description": "Cultivate multiple times per turn."
    },
    "Void": {
        "qi_gain_multiplier": 2.0,
        "breakthrough_chance_modifier": -0.50,
        "description": "Extreme gains and extreme risk."
    }
}

# New system for Phase 2 encounter system
ELEMENTAL_AFFINITIES = {
    "neutral": {
        "name": "Neutral",
        "symbol": "⚪",
        "description": "Balanced cultivation with no specialization",
        "qi_gain_multiplier": 1.0,
        "breakthrough_chance_modifier": 0.0
    },
    "flame": {
        "name": "Flame",
        "symbol": "🔥",
        "description": "Volatile power. High Qi gain, harder breakthroughs",
        "qi_gain_multiplier": 1.5,
        "breakthrough_chance_modifier": -0.10
    },
    "ice": {
        "name": "Ice",
        "symbol": "❄️",
        "description": "Stable and slow. Easier breakthroughs, less Qi",
        "qi_gain_multiplier": 0.8,
        "breakthrough_chance_modifier": 0.20
    },
    "lightning": {
        "name": "Lightning",
        "symbol": "⚡",
        "description": "High risk/reward cultivation",
        "qi_gain_multiplier": 1.0,
        "breakthrough_chance_modifier": 0.30
    },
    "earth": {
        "name": "Earth",
        "symbol": "⛰️",
        "description": "Balanced and steady growth",
        "qi_gain_multiplier": 1.25,
        "breakthrough_chance_modifier": 0.10
    },
    "wind": {
        "name": "Wind",
        "symbol": "💨",
        "description": "Swift and unpredictable cultivation",
        "qi_gain_multiplier": 1.4,
        "breakthrough_chance_modifier": 0.0
    },
    "chaos": {
        "name": "Chaos",
        "symbol": "🌀",
        "description": "Completely unpredictable cultivation style",
        "qi_gain_multiplier": 0.0,  # Handled dynamically
        "breakthrough_chance_modifier": 0.0
    },
    "time": {
        "name": "Time",
        "symbol": "⏰",
        "description": "Manipulate time to cultivate more efficiently",
        "qi_gain_multiplier": 1.0,
        "breakthrough_chance_modifier": 0.0,
        "extra_sessions_per_turn": 1
    },
    "void": {
        "name": "Void",
        "symbol": "🕳️",
        "description": "Extreme gains and extreme risk",
        "qi_gain_multiplier": 2.0,
        "breakthrough_chance_modifier": -0.50
    }
}

def get_affinity_info(affinity):
    """Get affinity information for the new system"""
    return ELEMENTAL_AFFINITIES.get(affinity, ELEMENTAL_AFFINITIES["neutral"])

def get_style_info(style):
    """Get style information for the old system (backward compatibility)"""
    return ELEMENTAL_STYLES.get(style, ELEMENTAL_STYLES["Earth"])