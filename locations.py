"""
Cultivation Game - Location System (Integrated with Enhanced Player System)
Handles different cultivation areas with unique encounters and rewards
Compatible with existing SmartEncounterManager and SpiritStoneManager
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

class LocationType(Enum):
    PEACEFUL = "peaceful"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    RUINS = "ruins"

@dataclass
class LocationInfo:
    name: str
    description: str
    unlock_realm: str  # Realm name required to unlock
    unlock_level: int   # Level required to unlock
    spirit_stone_multiplier: float  # Multiplier for spirit stone rewards
    encounter_difficulty: float  # Affects encounter frequency/severity
    special_features: List[str]
    unlock_description: str
    philosophy_bonuses: Dict[str, float]  # Philosophy bonuses for cultivation
    elemental_affinities: List[str]  # Elements that are enhanced here

class LocationManager:
    def __init__(self):
        self.locations = self._initialize_locations()
        self.current_location = LocationType.PEACEFUL
        
    def _initialize_locations(self) -> Dict[LocationType, LocationInfo]:
        return {
            LocationType.PEACEFUL: LocationInfo(
                name="🌸 Peaceful Valley",
                description="A serene valley where spiritual energy flows gently. Perfect for beginners to cultivate in safety.",
                unlock_realm="Body Tempering",
                unlock_level=1,
                spirit_stone_multiplier=1.0,
                encounter_difficulty=0.8,
                special_features=["Healing Springs", "Gentle Qi Flow", "Protected by Ancient Wards"],
                unlock_description="Your starting sanctuary for cultivation.",
                philosophy_bonuses={"balance": 0.05, "nature": 0.03},
                elemental_affinities=["nature", "light"]
            ),
            
            LocationType.FOREST: LocationInfo(
                name="🌲 Whispering Forest",
                description="Ancient woods where the trees themselves have gained wisdom. Mysterious encounters await among the shadows.",
                unlock_realm="Foundation Building",
                unlock_level=15,
                spirit_stone_multiplier=1.3,
                encounter_difficulty=1.2,
                special_features=["Spirit Beasts", "Ancient Tree Wisdom", "Hidden Treasures"],
                unlock_description="The forest calls to those who have proven their foundation.",
                philosophy_bonuses={"nature": 0.10, "balance": 0.05},
                elemental_affinities=["nature", "earth", "shadow"]
            ),
            
            LocationType.MOUNTAIN: LocationInfo(
                name="⛰️ Dragon's Peak",
                description="A towering mountain where dragons once roamed. The thin air and intense qi make cultivation dangerous but rewarding.",
                unlock_realm="Core Formation",
                unlock_level=35,
                spirit_stone_multiplier=1.8,
                encounter_difficulty=1.5,
                special_features=["Dragon Veins", "Intense Qi Storms", "Legendary Artifacts"],
                unlock_description="Only those with solid cultivation dare ascend the peak where legends were born.",
                philosophy_bonuses={"destruction": 0.10, "fire": 0.05},
                elemental_affinities=["lightning", "fire", "air"]
            ),
            
            LocationType.RUINS: LocationInfo(
                name="🏛️ Ancient Ruins",
                description="Remnants of a lost civilization where immortals once walked. Immense power and terrible danger lie hidden in the stones.",
                unlock_realm="Nascent Soul",
                unlock_level=70,
                spirit_stone_multiplier=2.5,
                encounter_difficulty=2.0,
                special_features=["Immortal Artifacts", "Ancient Formations", "Lost Techniques"],
                unlock_description="The ruins whisper secrets to those who have transcended mortal limitations.",
                philosophy_bonuses={"sword": 0.15, "destruction": 0.08},
                elemental_affinities=["light", "shadow", "lightning"]
            )
        }
    
    def get_available_locations(self, player_realm: str, player_stage: int) -> List[LocationType]:
        """Get all locations the player can access based on realm and stage"""
        available = []
        realm_order = ["Body Tempering", "Qi Gathering", "Foundation Building", "Core Formation", "Nascent Soul", "Soul Transformation", "Void Refinement"]
        
        try:
            player_realm_index = realm_order.index(player_realm)
        except ValueError:
            # Unknown realm, assume highest
            player_realm_index = len(realm_order) - 1
        
        for location_type, info in self.locations.items():
            try:
                required_realm_index = realm_order.index(info.unlock_realm)
                if (player_realm_index > required_realm_index or 
                    (player_realm_index == required_realm_index and player_stage >= info.unlock_level)):
                    available.append(location_type)
            except ValueError:
                # Unknown required realm, skip
                continue
        
        return available
    
    def get_location_info(self, location_type: LocationType) -> LocationInfo:
        """Get detailed information about a location"""
        return self.locations[location_type]
    
    def can_access_location(self, location_type: LocationType, player_realm: str, player_stage: int) -> bool:
        """Check if player can access a specific location"""
        info = self.locations[location_type]
        realm_order = ["Body Tempering", "Qi Gathering", "Foundation Building", "Core Formation", "Nascent Soul", "Soul Transformation", "Void Refinement"]
        
        try:
            player_realm_index = realm_order.index(player_realm)
            required_realm_index = realm_order.index(info.unlock_realm)
            
            return (player_realm_index > required_realm_index or 
                    (player_realm_index == required_realm_index and player_stage >= info.unlock_level))
        except ValueError:
            return False
    
    def get_cultivation_bonuses(self, location_type: LocationType, player) -> Dict[str, float]:
        """Get cultivation bonuses for the player at this location"""
        location_info = self.locations[location_type]
        bonuses = {}
        
        # Philosophy bonuses (now using dao_comprehension instead of philosophy)
        for philosophy, bonus in location_info.philosophy_bonuses.items():
            # Use dao_comprehension instead of philosophy
            current_dao = player.dao_comprehension.get(philosophy, 0)
            # Bonus scales with existing dao comprehension
            actual_bonus = bonus * (1 + current_dao * 0.1)
            bonuses[f"{philosophy}_dao"] = actual_bonus
        
        # Elemental affinity bonuses
        for element in location_info.elemental_affinities:
            current_affinity = player.elemental_affinities.get(element, 0)
            # Small bonus for cultivating in aligned environment
            if current_affinity > 0:
                bonuses[f"{element}_element"] = 0.02 * current_affinity
        
        return bonuses
    
    def modify_encounter_for_location(self, location_type: LocationType, encounter_result):
        """Modify encounter based on location characteristics"""
        if not encounter_result:
            return encounter_result
        
        location_info = self.locations[location_type]
        encounter_type, encounter_data = encounter_result
        
        # Create a copy to avoid modifying the original
        modified_data = encounter_data.copy()
        
        # Add location-specific flavor to encounter descriptions
        location_flavors = {
            LocationType.PEACEFUL: [
                "The valley's peaceful energy guides this encounter.",
                "Ancient protective wards influence the outcome.",
                "The gentle qi flow shapes this experience."
            ],
            LocationType.FOREST: [
                "The whispering trees seem to orchestrate this event.",
                "Forest spirits observe from the shadows.",
                "Ancient woodland magic influences this encounter."
            ],
            LocationType.MOUNTAIN: [
                "Dragon energies surge through this encounter.",
                "The mountain's fierce qi amplifies the experience.",
                "Echoes of ancient dragon roars accompany this event."
            ],
            LocationType.RUINS: [
                "Immortal remnants stir with ancient power.",
                "The ruins' accumulated wisdom affects this encounter.",
                "Ghostly memories of past immortals influence the outcome."
            ]
        }
        
        if location_type in location_flavors:
            flavor = random.choice(location_flavors[location_type])
            if 'description' in modified_data:
                modified_data['description'] += f" {flavor}"
            else:
                modified_data['description'] = flavor
        
        # Adjust encounter intensity based on location difficulty
        if location_info.encounter_difficulty > 1.0 and encounter_type in ['positive', 'negative']:
            # More intense encounters in dangerous locations
            if 'rarity' in modified_data:
                rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']
                current_index = rarities.index(modified_data['rarity'])
                # Small chance to upgrade rarity in dangerous locations
                if random.random() < (location_info.encounter_difficulty - 1.0) * 0.3:
                    new_index = min(current_index + 1, len(rarities) - 1)
                    modified_data['rarity'] = rarities[new_index]
        
        return encounter_type, modified_data
    
    def get_spirit_stone_multiplier(self, location_type: LocationType) -> float:
        """Get spirit stone reward multiplier for location"""
        return self.locations[location_type].spirit_stone_multiplier
    
    def get_encounter_difficulty(self, location_type: LocationType) -> float:
        """Get encounter difficulty multiplier for location"""
        return self.locations[location_type].encounter_difficulty
    
    def set_current_location(self, location_type: LocationType):
        """Set the current cultivation location"""
        self.current_location = location_type
    
    def get_current_location(self) -> LocationType:
        """Get the current cultivation location"""
        return self.current_location
    
    def display_location_menu(self, available_locations: List[LocationType]) -> str:
        """Generate location selection menu"""
        menu_text = "\n" + "="*60 + "\n"
        menu_text += "🌍 **CULTIVATION LOCATIONS** 🌍\n"
        menu_text += "="*60 + "\n\n"
        
        for i, location_type in enumerate(available_locations, 1):
            info = self.locations[location_type]
            current_marker = "👈 CURRENT" if location_type == self.current_location else ""
            
            menu_text += f"{i}. {info.name} {current_marker}\n"
            menu_text += f"   {info.description}\n"
            menu_text += f"   🔸 Spirit Stone Bonus: {info.spirit_stone_multiplier:.1f}x\n"
            menu_text += f"   ⚔️ Encounter Risk: {info.encounter_difficulty:.1f}x\n"
            menu_text += f"   📚 Dao Bonuses: {', '.join(f'+{v:.1%} {k}' for k, v in info.philosophy_bonuses.items())}\n"
            menu_text += f"   🌟 Elemental Affinities: {', '.join(info.elemental_affinities)}\n"
            menu_text += f"   ✨ Features: {', '.join(info.special_features)}\n\n"
        
        menu_text += f"{len(available_locations) + 1}. 🔙 Return to Main Menu\n"
        menu_text += "="*60 + "\n"
        
        return menu_text
    
    def display_location_unlock_message(self, location_type: LocationType) -> str:
        """Display message when new location is unlocked"""
        info = self.locations[location_type]
        message = f"\n{'='*60}\n"
        message += f"🌟 **NEW LOCATION UNLOCKED!** 🌟\n"
        message += f"{'='*60}\n\n"
        message += f"{info.name}\n"
        message += f"{info.unlock_description}\n\n"
        message += f"🔸 Spirit Stone Bonus: {info.spirit_stone_multiplier:.1f}x\n"
        message += f"⚔️ Encounter Risk: {info.encounter_difficulty:.1f}x\n"
        message += f"📚 Dao Bonuses: {', '.join(f'+{v:.1%} {k}' for k, v in info.philosophy_bonuses.items())}\n"
        message += f"🌟 Elemental Affinities: {', '.join(info.elemental_affinities)}\n"
        message += f"✨ Special Features: {', '.join(info.special_features)}\n"
        message += f"{'='*60}\n"
        
        return message
    
    def get_location_status_display(self, location_type: LocationType, player) -> str:
        """Get status display showing current location and bonuses"""
        info = self.locations[location_type]
        bonuses = self.get_cultivation_bonuses(location_type, player)
        
        status = f"📍 Current Location: {info.name}\n"
        status += f"   {info.description}\n"
        
        if bonuses:
            status += f"   🌟 Active Bonuses:\n"
            for bonus_name, bonus_value in bonuses.items():
                if bonus_value > 0:
                    status += f"      • {bonus_name}: +{bonus_value:.1%}\n"
        
        return status