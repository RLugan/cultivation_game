"""
Cultivation Encounters System with Smart Encounter Manager and Reward Generation
Updated to include the missing generate_encounter_reward function
"""

import random
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

class EncounterType(Enum):
    BOTTLENECK = "bottleneck"
    INSIGHT = "insight"
    ANOMALY = "anomaly"
    TECHNIQUE = "technique"

class SmartEncounterManager:
    """Manages cultivation encounters with smart frequency control and variety enforcement"""
    
    def __init__(self):
        self.last_encounter_session = 0
        self.sessions_since_encounter = 0
        self.recent_encounter_types = []
        self.drought_sessions = 0
        self.base_chance = 0.06  # 6% base encounter rate
        
        # Encounter definitions
        self.encounters = {
            EncounterType.BOTTLENECK: self._get_bottleneck_encounters(),
            EncounterType.INSIGHT: self._get_insight_encounters(),
            EncounterType.ANOMALY: self._get_anomaly_encounters(),
            EncounterType.TECHNIQUE: self._get_technique_encounters()
        }
    
    def _get_bottleneck_encounters(self) -> List[Dict]:
        """Get bottleneck encounter definitions"""
        return [
            {
                "name": "Qi Stagnation",
                "description": "Your qi flow becomes sluggish and inefficient",
                "rarity": "common",
                "ongoing_effect": {
                    "name": "Qi Stagnation",
                    "type": "negative",
                    "description": "Cultivation speed reduced by 15%",
                    "exp_multiplier": 0.85,
                    "remaining_duration": None  # Permanent until cured
                }
            },
            {
                "name": "Meridian Blockage",
                "description": "Impurities block your meridian pathways",
                "rarity": "common",
                "ongoing_effect": {
                    "name": "Meridian Blockage",
                    "type": "negative",
                    "description": "Cultivation efficiency reduced by 20%",
                    "exp_multiplier": 0.80,
                    "remaining_duration": None
                }
            },
            {
                "name": "Foundation Cracks",
                "description": "Your cultivation foundation develops dangerous fissures",
                "rarity": "uncommon",
                "ongoing_effect": {
                    "name": "Foundation Cracks",
                    "type": "negative",
                    "description": "All cultivation progress reduced by 25%",
                    "exp_multiplier": 0.75,
                    "remaining_duration": None
                }
            },
            {
                "name": "Cultivation Deviation",
                "description": "Your cultivation method goes astray",
                "rarity": "rare",
                "ongoing_effect": {
                    "name": "Cultivation Deviation",
                    "type": "negative",
                    "description": "Severe cultivation penalties until corrected",
                    "exp_multiplier": 0.60,
                    "remaining_duration": None
                }
            },
            {
                "name": "Heart Demon",
                "description": "A powerful heart demon manifests from your doubts",
                "rarity": "very_rare",
                "ongoing_effect": {
                    "name": "Heart Demon",
                    "type": "negative",
                    "description": "Major cultivation obstruction affecting all progress",
                    "exp_multiplier": 0.50,
                    "remaining_duration": None
                }
            }
        ]
    
    def _get_insight_encounters(self) -> List[Dict]:
        """Get insight encounter definitions"""
        return [
            {
                "name": "Dao Comprehension",
                "description": "You gain understanding of the universal dao",
                "rarity": "common",
                "rewards": {
                    "experience": 25,
                    "philosophy": {"wisdom": 2, "balance": 1}
                }
            },
            {
                "name": "Elemental Resonance",
                "description": "You feel a deep connection with elemental forces",
                "rarity": "common",
                "rewards": {
                    "experience": 20,
                    "elemental": self._random_elemental_boost(15, 25)
                }
            },
            {
                "name": "Foundation Enlightenment",
                "description": "Your cultivation foundation becomes more stable",
                "rarity": "uncommon",
                "rewards": {
                    "experience": 30,
                    "foundation": 5,
                    "philosophy": {"balance": 2}
                }
            },
            {
                "name": "Heavenly Insight",
                "description": "The heavens grant you profound understanding",
                "rarity": "rare",
                "rewards": {
                    "experience": 50,
                    "philosophy": {"wisdom": 5, "balance": 3}
                },
                "ongoing_effect": {
                    "name": "Enlightenment",
                    "type": "positive",
                    "description": "Cultivation speed increased by 25% for next 10 sessions",
                    "exp_multiplier": 1.25,
                    "remaining_duration": 10
                }
            },
            {
                "name": "Cosmic Revelation",
                "description": "You glimpse the true nature of reality",
                "rarity": "very_rare",
                "rewards": {
                    "experience": 100,
                    "philosophy": {"wisdom": 10, "balance": 5, "nature": 3}
                },
                "ongoing_effect": {
                    "name": "Cosmic Understanding",
                    "type": "positive",
                    "description": "Massive cultivation boost for next 15 sessions",
                    "exp_multiplier": 1.50,
                    "remaining_duration": 15
                }
            }
        ]
    
    def _get_anomaly_encounters(self) -> List[Dict]:
        """Get anomaly encounter definitions"""
        return [
            {
                "name": "Qi Turbulence",
                "description": "Chaotic qi energies disrupt your cultivation",
                "rarity": "common",
                "ongoing_effect": {
                    "name": "Chaotic Qi",
                    "type": "negative",
                    "description": "Unstable qi causes cultivation fluctuations",
                    "exp_multiplier": 0.90,
                    "remaining_duration": 5
                }
            },
            {
                "name": "Elemental Storm",
                "description": "Conflicting elemental energies create chaos",
                "rarity": "uncommon",
                "ongoing_effect": {
                    "name": "Elemental Imbalance",
                    "type": "negative",
                    "description": "Elemental confusion reduces cultivation efficiency",
                    "exp_multiplier": 0.85,
                    "remaining_duration": 8
                }
            },
            {
                "name": "Spatial Rift",
                "description": "A tear in space affects local qi flow",
                "rarity": "rare",
                "rewards": {
                    "experience": -20  # Negative experience
                },
                "ongoing_effect": {
                    "name": "Spiritual Corruption",
                    "type": "negative",
                    "description": "Corrupted spiritual energy impedes progress",
                    "exp_multiplier": 0.70,
                    "remaining_duration": None
                }
            },
            {
                "name": "Dao Fluctuation",
                "description": "The fundamental laws of reality shift briefly",
                "rarity": "very_rare",
                "ongoing_effect": {
                    "name": "Dao Confusion",
                    "type": "negative",
                    "description": "Reality confusion severely hampers cultivation",
                    "exp_multiplier": 0.60,
                    "remaining_duration": None
                }
            },
            {
                "name": "Void Incursion",
                "description": "Void energy seeps into reality",
                "rarity": "legendary",
                "ongoing_effect": {
                    "name": "Void Taint",
                    "type": "negative",
                    "description": "Void corruption threatens your very existence",
                    "exp_multiplier": 0.40,
                    "remaining_duration": None
                }
            }
        ]
    
    def _get_technique_encounters(self) -> List[Dict]:
        """Get technique encounter definitions"""
        return [
            {
                "name": "Ancient Manual",
                "description": "You discover a fragment of an ancient cultivation manual",
                "rarity": "common",
                "rewards": {
                    "experience": 35,
                    "philosophy": {"wisdom": 1, "power": 1}
                }
            },
            {
                "name": "Technique Inspiration",
                "description": "A flash of inspiration improves your technique",
                "rarity": "common",
                "rewards": {
                    "experience": 30,
                    "elemental": self._random_elemental_boost(10, 20)
                }
            },
            {
                "name": "Master's Echo",
                "description": "You sense the lingering presence of a cultivation master",
                "rarity": "uncommon",
                "rewards": {
                    "experience": 45,
                    "philosophy": {"wisdom": 3, "balance": 2}
                },
                "ongoing_effect": {
                    "name": "Master's Guidance",
                    "type": "positive",
                    "description": "Enhanced learning for next 8 sessions",
                    "exp_multiplier": 1.20,
                    "remaining_duration": 8
                }
            },
            {
                "name": "Technique Breakthrough",
                "description": "You achieve a major breakthrough in your cultivation technique",
                "rarity": "rare",
                "rewards": {
                    "experience": 60,
                    "elemental": self._random_elemental_boost(20, 40),
                    "philosophy": {"power": 3, "wisdom": 2}
                }
            },
            {
                "name": "Forbidden Technique",
                "description": "You accidentally practice a dangerous forbidden technique",
                "rarity": "rare",
                "rewards": {
                    "experience": 80,
                    "philosophy": {"power": 5}
                },
                "ongoing_effect": {
                    "name": "Technique Backlash",
                    "type": "negative",
                    "description": "Forbidden technique causes cultivation instability",
                    "exp_multiplier": 0.95,
                    "remaining_duration": 12
                }
            },
            {
                "name": "Legendary Inheritance",
                "description": "You inherit the technique of a legendary cultivator",
                "rarity": "legendary",
                "rewards": {
                    "experience": 150,
                    "elemental": self._random_elemental_boost(40, 80),
                    "philosophy": {"power": 8, "wisdom": 5, "balance": 3}
                },
                "ongoing_effect": {
                    "name": "Legendary Mastery",
                    "type": "positive",
                    "description": "Legendary techniques grant permanent cultivation bonus",
                    "exp_multiplier": 1.15,
                    "remaining_duration": None
                }
            }
        ]
    
    def _random_elemental_boost(self, min_total: int, max_total: int) -> Dict[str, int]:
        """Generate random elemental affinity boosts"""
        elements = ["fire", "water", "earth", "air", "lightning", "ice", "nature", "light", "shadow"]
        total_points = random.randint(min_total, max_total)
        
        # Randomly distribute points among 1-3 elements
        num_elements = random.randint(1, min(3, len(elements)))
        chosen_elements = random.sample(elements, num_elements)
        
        boost = {}
        remaining_points = total_points
        
        for i, element in enumerate(chosen_elements):
            if i == len(chosen_elements) - 1:
                # Last element gets all remaining points
                boost[element] = remaining_points
            else:
                # Distribute points randomly
                points = random.randint(1, max(1, remaining_points - (len(chosen_elements) - i - 1)))
                boost[element] = points
                remaining_points -= points
        
        return boost
    
    def _calculate_encounter_chance(self, current_session: int) -> float:
        """Calculate encounter chance with drought protection"""
        base_chance = self.base_chance
        
        # Drought protection - increase chance if no encounters for a while
        if self.sessions_since_encounter >= 15:
            drought_bonus = min(0.3, (self.sessions_since_encounter - 15) * 0.02)
            base_chance += drought_bonus
        
        return min(base_chance, 0.4)  # Cap at 40%
    
    def _select_encounter_type(self) -> EncounterType:
        """Select encounter type with variety enforcement"""
        available_types = list(EncounterType)
        
        # Avoid recent types if possible
        if len(self.recent_encounter_types) >= 2:
            recent_set = set(self.recent_encounter_types[-2:])
            non_recent = [t for t in available_types if t not in recent_set]
            if non_recent:
                available_types = non_recent
        
        weights = {
            EncounterType.INSIGHT: 40,
            EncounterType.TECHNIQUE: 30,
            EncounterType.BOTTLENECK: 20,
            EncounterType.ANOMALY: 10
        }
        
        return random.choices(available_types, 
                            weights=[weights[t] for t in available_types])[0]
    
    def _select_encounter(self, encounter_type: EncounterType, player_realm: str) -> Dict:
        """Select specific encounter based on type and realm"""
        encounters = self.encounters[encounter_type]
        
        # Filter by rarity based on realm
        realm_rarities = {
            "Qi Gathering": ["common", "uncommon"],
            "Foundation Building": ["common", "uncommon", "rare"],
            "Core Formation": ["common", "uncommon", "rare", "very_rare"],
            "Nascent Soul": ["uncommon", "rare", "very_rare", "legendary"],
            "Soul Transformation": ["rare", "very_rare", "legendary"]
        }
        
        allowed_rarities = realm_rarities.get(player_realm, ["common", "uncommon"])
        filtered_encounters = [e for e in encounters if e["rarity"] in allowed_rarities]
        
        if not filtered_encounters:
            filtered_encounters = encounters
        
        # Weight by rarity (rarer = less likely)
        rarity_weights = {
            "common": 50,
            "uncommon": 30,
            "rare": 15,
            "very_rare": 4,
            "legendary": 1
        }
        
        weights = [rarity_weights.get(e["rarity"], 25) for e in filtered_encounters]
        return random.choices(filtered_encounters, weights=weights)[0]
    
    def process_encounter(self, player_realm: str, player_level: int, 
                         ongoing_effects: List[Dict], current_session: int = None) -> Optional[Tuple[str, Dict]]:
        """Process potential encounter for this cultivation session"""
        if current_session is None:
            current_session = getattr(self, '_session_counter', 0)
            self._session_counter = current_session + 1
        
        self.sessions_since_encounter += 1
        
        # Calculate encounter chance
        encounter_chance = self._calculate_encounter_chance(current_session)
        
        if random.random() < encounter_chance:
            # Select encounter
            encounter_type = self._select_encounter_type()
            encounter = self._select_encounter(encounter_type, player_realm)
            
            # Update tracking
            self.last_encounter_session = current_session
            self.sessions_since_encounter = 0
            self.recent_encounter_types.append(encounter_type)
            if len(self.recent_encounter_types) > 5:
                self.recent_encounter_types.pop(0)
            
            return encounter_type.value, encounter
        
        return None


def generate_encounter_reward(encounter_type: str, encounter_data: Dict, player_realm: str) -> Dict[str, Any]:
    """
    Generate rewards for an encounter
    
    Args:
        encounter_type: Type of encounter (bottleneck, insight, anomaly, technique)
        encounter_data: The encounter data dictionary
        player_realm: Current player realm for scaling
        
    Returns:
        Dictionary of rewards to apply to the player
    """
    rewards = {}
    
    # Realm multipliers for scaling rewards
    realm_multipliers = {
        "Qi Gathering": 1.0,
        "Foundation Building": 1.2,
        "Core Formation": 1.5,
        "Nascent Soul": 2.0,
        "Soul Transformation": 2.5,
        "Void Transcendence": 3.0
    }
    
    multiplier = realm_multipliers.get(player_realm, 1.0)
    
    # Process direct rewards from encounter data
    if "rewards" in encounter_data:
        for reward_type, reward_value in encounter_data["rewards"].items():
            if reward_type == "experience":
                # Scale experience with realm
                scaled_exp = int(reward_value * multiplier)
                rewards[reward_type] = scaled_exp
            elif reward_type == "philosophy":
                # Philosophy gains are less affected by realm
                philosophy_multiplier = min(multiplier, 1.5)
                scaled_philosophy = {}
                for phil_type, phil_value in reward_value.items():
                    scaled_philosophy[phil_type] = int(phil_value * philosophy_multiplier)
                rewards[reward_type] = scaled_philosophy
            elif reward_type == "elemental":
                # Elemental affinities scale moderately with realm
                elemental_multiplier = min(multiplier, 2.0)
                scaled_elemental = {}
                for elem_type, elem_value in reward_value.items():
                    scaled_elemental[elem_type] = int(elem_value * elemental_multiplier)
                rewards[reward_type] = scaled_elemental
            elif reward_type == "foundation":
                # Foundation quality scales with realm
                scaled_foundation = int(reward_value * multiplier)
                rewards[reward_type] = scaled_foundation
            else:
                # Other rewards pass through unchanged
                rewards[reward_type] = reward_value
    
    # Process ongoing effects
    if "ongoing_effect" in encounter_data:
        effect = encounter_data["ongoing_effect"].copy()
        
        # Scale effect duration based on realm for temporary effects
        if effect.get("remaining_duration") is not None:
            duration_multiplier = max(0.5, 1.5 - (multiplier - 1.0) * 0.3)
            effect["remaining_duration"] = max(1, int(effect["remaining_duration"] * duration_multiplier))
        
        rewards["ongoing_effect"] = effect
    
    # Add random bonus rewards based on encounter type and realm
    bonus_rewards = _generate_bonus_rewards(encounter_type, player_realm, multiplier)
    for reward_type, reward_value in bonus_rewards.items():
        if reward_type in rewards:
            if isinstance(rewards[reward_type], dict) and isinstance(reward_value, dict):
                # Merge dictionaries (for philosophy/elemental)
                for key, value in reward_value.items():
                    rewards[reward_type][key] = rewards[reward_type].get(key, 0) + value
            elif isinstance(rewards[reward_type], int) and isinstance(reward_value, int):
                # Add integers (for experience/foundation)
                rewards[reward_type] += reward_value
        else:
            rewards[reward_type] = reward_value
    
    return rewards


def _generate_bonus_rewards(encounter_type: str, player_realm: str, multiplier: float) -> Dict[str, Any]:
    """Generate random bonus rewards based on encounter type"""
    bonus = {}
    
    # Small chance for bonus experience
    if random.random() < 0.3:
        base_bonus = {
            "bottleneck": 5,
            "insight": 15,
            "anomaly": 8,
            "technique": 12
        }
        bonus_exp = int(base_bonus.get(encounter_type, 10) * multiplier)
        bonus["experience"] = bonus_exp
    
    # Small chance for philosophy bonus
    if random.random() < 0.2:
        philosophy_types = ["balance", "power", "wisdom", "nature"]
        chosen_philosophy = random.choice(philosophy_types)
        philosophy_amount = random.randint(1, max(1, int(2 * multiplier)))
        bonus["philosophy"] = {chosen_philosophy: philosophy_amount}
    
    # Very small chance for foundation bonus (except for bottlenecks)
    if encounter_type != "bottleneck" and random.random() < 0.1:
        foundation_bonus = random.randint(1, max(1, int(3 * multiplier)))
        bonus["foundation"] = foundation_bonus
    
    return bonus


# Example usage and testing
if __name__ == "__main__":
    # Test the encounter system
    manager = SmartEncounterManager()
    
    print("=== Encounter System Test ===")
    
    # Simulate several cultivation sessions
    for session in range(10):
        print(f"\n--- Session {session + 1} ---")
        
        result = manager.process_encounter("Foundation Building", 15, [], session)
        
        if result:
            encounter_type, encounter_data = result
            print(f"Encounter: {encounter_type.title()} - {encounter_data['name']}")
            print(f"Description: {encounter_data['description']}")
            
            # Test reward generation
            rewards = generate_encounter_reward(encounter_type, encounter_data, "Foundation Building")
            if rewards:
                print("Rewards:")
                for reward_type, reward_value in rewards.items():
                    print(f"  {reward_type}: {reward_value}")
        else:
            print("No encounter this session")
    
    print(f"\nTotal encounters: {len(manager.recent_encounter_types)}")
    print(f"Sessions since last encounter: {manager.sessions_since_encounter}")