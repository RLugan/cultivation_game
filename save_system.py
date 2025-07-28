"""
Save/Load System for Cultivation Game
Handles automatic saving and loading of player progress
Updated for Enhanced Player System
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import traceback

class SaveSystem:
    """Handles saving and loading game state"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self.save_file = "cultivation_save.json"
        self.backup_file = "cultivation_save_backup.json"
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    
    def get_save_path(self, filename: str) -> str:
        """Get full path for save file"""
        return os.path.join(self.save_directory, filename)
    
    def save_player(self, player) -> bool:
        """
        Save player data to file
        Returns True if successful, False otherwise
        """
        try:
            # Create backup of existing save
            save_path = self.get_save_path(self.save_file)
            backup_path = self.get_save_path(self.backup_file)
            
            if os.path.exists(save_path):
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(save_path, backup_path)
            
            # Convert player to saveable format
            save_data = self._enhanced_player_to_dict(player)
            
            # Add save metadata
            save_data["_save_info"] = {
                "version": "2.0",
                "timestamp": datetime.now().isoformat(),
                "game_phase": "Enhanced Cultivation System"
            }
            
            # Save to file
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            traceback.print_exc()
            return False
    
    def load_player(self) -> Optional[Dict[str, Any]]:
        """
        Load player data from file
        Returns player data dict if successful, None otherwise
        """
        save_path = self.get_save_path(self.save_file)
        backup_path = self.get_save_path(self.backup_file)
        
        # Try to load main save file
        player_data = self._try_load_file(save_path)
        if player_data:
            return player_data
        
        # If main file failed, try backup
        print("Main save file corrupted or missing, trying backup...")
        player_data = self._try_load_file(backup_path)
        if player_data:
            print("Loaded from backup save file.")
            return player_data
        
        return None
    
    def _try_load_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Try to load a specific save file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate save data
            if self._validate_enhanced_save_data(data):
                return data
            else:
                print(f"Invalid save data in {file_path}")
                return None
                
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def _validate_enhanced_save_data(self, data: Dict[str, Any]) -> bool:
        """Validate that save data has required fields for enhanced system"""
        required_fields = [
            "name", "realm", "stage", "experience", 
            "dao_comprehension", "foundation_quality", "elemental_affinities",
            "ongoing_effects", "spirit_stones", "total_encounters"
        ]
        
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return False
        
        return True
    
    def _enhanced_player_to_dict(self, player) -> Dict[str, Any]:
        """Convert enhanced player object to dictionary for saving"""
        from spirit_stones import SpiritStoneGrade
        
        # Convert spirit stone inventory to saveable format
        spirit_stones_data = {}
        for grade in SpiritStoneGrade:
            spirit_stones_data[grade.value] = player.spirit_stones.inventory[grade]
        
        # Convert cultivation history to saveable format
        cultivation_history = []
        for session in player.cultivation_history:
            session_data = session.copy()
            # Convert spirit stones in history
            if "spirit_stones" in session_data and session_data["spirit_stones"]:
                stones_dict = {}
                for grade, amount in session_data["spirit_stones"].items():
                    if hasattr(grade, 'value'):
                        stones_dict[grade.value] = amount
                    else:
                        stones_dict[str(grade)] = amount
                session_data["spirit_stones"] = stones_dict
            cultivation_history.append(session_data)
        
        # Convert last session details
        last_session = None
        if player.last_session_details:
            last_session = player.last_session_details.copy()
            if "spirit_stones" in last_session and last_session["spirit_stones"]:
                stones_dict = {}
                for grade, amount in last_session["spirit_stones"].items():
                    if hasattr(grade, 'value'):
                        stones_dict[grade.value] = amount
                    else:
                        stones_dict[str(grade)] = amount
                last_session["spirit_stones"] = stones_dict
        
        return {
            # Basic info - UPDATED FOR ENHANCED SYSTEM
            "name": player.name,
            "realm": player.realm.value,  # Save realm as string
            "stage": player.stage,        # NEW: stage instead of level
            "experience": player.experience,
            "foundation_quality": player.foundation_quality,
            "foundation_stability": getattr(player, 'foundation_stability', 100),
            
            # Enhanced systems - NEW
            "dao_comprehension": player.dao_comprehension,
            "elemental_affinities": player.elemental_affinities,
            "primary_element": player.primary_element,
            "secondary_elements": getattr(player, 'secondary_elements', []),
            
            # Cultivation progression - NEW
            "cultivation_method": getattr(player, 'cultivation_method', 'balanced'),
            "breakthrough_failures": getattr(player, 'breakthrough_failures', 0),
            "recovery_time": getattr(player, 'recovery_time', 0),
            
            # Effects
            "ongoing_effects": player.ongoing_effects,
            
            # Spirit Stones
            "spirit_stones": spirit_stones_data,
            
            # Statistics
            "total_encounters": player.total_encounters,
            "effects_cured": player.effects_cured,
            "spirit_stones_earned": player.spirit_stones_earned,
            "total_breakthroughs": getattr(player, 'total_breakthroughs', 0),
            "foundation_sessions": getattr(player, 'foundation_sessions', 0),
            
            # History
            "cultivation_history": cultivation_history,
            "last_session_details": last_session,
            
            # Background info (if exists) - Convert to serializable format
            "background": self._serialize_background(getattr(player, 'background', None)),
            "motivation": getattr(player, 'motivation', None),
            
            # Encounter manager state
            "encounter_manager_state": {
                "last_encounter_session": player.encounter_manager.last_encounter_session,
                "sessions_since_encounter": player.encounter_manager.sessions_since_encounter,
                "recent_encounter_types": [t.value for t in player.encounter_manager.recent_encounter_types],
                "drought_sessions": player.encounter_manager.drought_sessions
            }
        }
    
    def dict_to_enhanced_player(self, data: Dict[str, Any]):
        """Convert dictionary back to enhanced player object"""
        from player import EnhancedPlayer
        from spirit_stones import SpiritStoneGrade
        from cultivation_encounters import EncounterType
        from realm_stage_system import CultivationRealm
        
        # Create new enhanced player
        player = EnhancedPlayer(data["name"])
        
        # Restore basic info
        try:
            player.realm = CultivationRealm(data["realm"])
        except (ValueError, KeyError):
            player.realm = CultivationRealm.BODY_TEMPERING
        
        player.stage = data.get("stage", 1)
        player.experience = data.get("experience", 0)
        player.foundation_quality = data.get("foundation_quality", 10)
        player.foundation_stability = data.get("foundation_stability", 100)
        
        # Restore enhanced systems
        player.dao_comprehension = data.get("dao_comprehension", player.dao_comprehension)
        player.elemental_affinities = data.get("elemental_affinities", player.elemental_affinities)
        player.primary_element = data.get("primary_element", None)
        player.secondary_elements = data.get("secondary_elements", [])
        
        # Restore cultivation progression
        player.cultivation_method = data.get("cultivation_method", "balanced")
        player.breakthrough_failures = data.get("breakthrough_failures", 0)
        player.recovery_time = data.get("recovery_time", 0)
        
        # Restore effects
        player.ongoing_effects = data.get("ongoing_effects", [])
        
        # Restore spirit stones
        for grade_name, amount in data.get("spirit_stones", {}).items():
            try:
                grade = SpiritStoneGrade(grade_name)
                player.spirit_stones.inventory[grade] = amount
            except ValueError:
                continue
        
        # Restore statistics
        player.total_encounters = data.get("total_encounters", 0)
        player.effects_cured = data.get("effects_cured", 0)
        player.spirit_stones_earned = data.get("spirit_stones_earned", 0)
        player.total_breakthroughs = data.get("total_breakthroughs", 0)
        player.foundation_sessions = data.get("foundation_sessions", 0)
        
        # Restore background info
        background_data = data.get("background", None)
        if background_data:
            player.background = self._deserialize_background(background_data)
        else:
            player.background = None
        player.motivation = data.get("motivation", None)
        
        # Restore cultivation history
        if "cultivation_history" in data:
            cultivation_history = []
            for session_data in data["cultivation_history"]:
                session = session_data.copy()
                # Convert spirit stones back
                if "spirit_stones" in session and session["spirit_stones"]:
                    stones_dict = {}
                    for grade_name, amount in session["spirit_stones"].items():
                        try:
                            stones_dict[SpiritStoneGrade(grade_name)] = amount
                        except ValueError:
                            continue
                    session["spirit_stones"] = stones_dict
                cultivation_history.append(session)
            player.cultivation_history = cultivation_history
        
        # Restore last session details
        if "last_session_details" in data and data["last_session_details"]:
            last_session = data["last_session_details"].copy()
            if "spirit_stones" in last_session and last_session["spirit_stones"]:
                stones_dict = {}
                for grade_name, amount in last_session["spirit_stones"].items():
                    try:
                        stones_dict[SpiritStoneGrade(grade_name)] = amount
                    except ValueError:
                        continue
                last_session["spirit_stones"] = stones_dict
            player.last_session_details = last_session
        
        # Restore encounter manager state
        if "encounter_manager_state" in data:
            state = data["encounter_manager_state"]
            player.encounter_manager.last_encounter_session = state.get("last_encounter_session", 0)
            player.encounter_manager.sessions_since_encounter = state.get("sessions_since_encounter", 0)
            player.encounter_manager.drought_sessions = state.get("drought_sessions", 0)
            try:
                player.encounter_manager.recent_encounter_types = [
                    EncounterType(t) for t in state.get("recent_encounter_types", [])
                ]
            except (ValueError, KeyError):
                player.encounter_manager.recent_encounter_types = []
        
        return player
    
    def _serialize_background(self, background) -> Optional[Dict[str, Any]]:
        """Convert Background object to serializable dictionary"""
        if background is None:
            return None
        
        try:
            return {
                "name": background.name,
                "title": background.title,
                "description": background.description,
                "story": background.story,
                "starting_bonuses": [
                    {
                        "type": bonus.type,
                        "value": bonus.value,
                        "description": bonus.description
                    } for bonus in background.starting_bonuses
                ],
                "ongoing_effects": [
                    {
                        "type": effect.type,
                        "value": effect.value,
                        "description": effect.description
                    } for effect in background.ongoing_effects
                ]
            }
        except Exception as e:
            print(f"Warning: Could not serialize background: {e}")
            return None
    
    def _deserialize_background(self, background_data: Dict[str, Any]):
        """Convert serialized dictionary back to Background object"""
        try:
            from character_backgrounds import Background, BackgroundBonus
            
            # Recreate background bonuses
            starting_bonuses = []
            for bonus_data in background_data.get("starting_bonuses", []):
                bonus = BackgroundBonus(
                    type=bonus_data["type"],
                    value=bonus_data["value"],
                    description=bonus_data["description"]
                )
                starting_bonuses.append(bonus)
            
            # Recreate ongoing effects
            ongoing_effects = []
            for effect_data in background_data.get("ongoing_effects", []):
                effect = BackgroundBonus(
                    type=effect_data["type"],
                    value=effect_data["value"],
                    description=effect_data["description"]
                )
                ongoing_effects.append(effect)
            
            # Create Background object
            background = Background(
                name=background_data["name"],
                title=background_data["title"],
                description=background_data["description"],
                story=background_data["story"],
                starting_bonuses=starting_bonuses,
                ongoing_effects=ongoing_effects
            )
            
            return background
            
        except Exception as e:
            print(f"Warning: Could not deserialize background: {e}")
            return None

    def save_exists(self) -> bool:
        """Check if a save file exists"""
        save_path = self.get_save_path(self.save_file)
        backup_path = self.get_save_path(self.backup_file)
        return os.path.exists(save_path) or os.path.exists(backup_path)
    
    def get_save_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the save file"""
        data = self.load_player()
        if data and "_save_info" in data:
            return data["_save_info"]
        return None
    
    def delete_save(self) -> bool:
        """Delete save files"""
        try:
            save_path = self.get_save_path(self.save_file)
            backup_path = self.get_save_path(self.backup_file)
            
            if os.path.exists(save_path):
                os.remove(save_path)
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            return True
        except Exception as e:
            print(f"Error deleting save files: {e}")
            return False


# Backward compatibility for old saves
def migrate_old_save_to_enhanced(old_data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate old save format to enhanced format"""
    from realm_stage_system import convert_old_level_to_realm_stage, CultivationRealm
    
    enhanced_data = old_data.copy()
    
    # Convert level to realm/stage if needed
    if "level" in old_data and "realm" not in old_data:
        old_level = old_data["level"]
        realm, stage = convert_old_level_to_realm_stage(old_level)
        enhanced_data["realm"] = realm.value
        enhanced_data["stage"] = stage
        del enhanced_data["level"]  # Remove old level
    
    # Convert philosophy to dao_comprehension if needed
    if "philosophy" in old_data and "dao_comprehension" not in old_data:
        enhanced_data["dao_comprehension"] = old_data["philosophy"]
        del enhanced_data["philosophy"]  # Remove old philosophy
    
    # Add missing enhanced fields with defaults
    if "foundation_stability" not in enhanced_data:
        enhanced_data["foundation_stability"] = 100
    
    if "primary_element" not in enhanced_data:
        enhanced_data["primary_element"] = None
    
    if "secondary_elements" not in enhanced_data:
        enhanced_data["secondary_elements"] = []
    
    if "cultivation_method" not in enhanced_data:
        enhanced_data["cultivation_method"] = "balanced"
    
    if "breakthrough_failures" not in enhanced_data:
        enhanced_data["breakthrough_failures"] = 0
    
    if "recovery_time" not in enhanced_data:
        enhanced_data["recovery_time"] = 0
    
    if "total_breakthroughs" not in enhanced_data:
        enhanced_data["total_breakthroughs"] = 0
    
    if "foundation_sessions" not in enhanced_data:
        enhanced_data["foundation_sessions"] = 0
    
    return enhanced_data


# Example usage
if __name__ == "__main__":
    # Test the save system
    save_system = SaveSystem()
    
    print("=== Enhanced Save System Test ===")
    
    if save_system.save_exists():
        print("Save file exists!")
        save_info = save_system.get_save_info()
        if save_info:
            print(f"Save created: {save_info.get('timestamp', 'Unknown')}")
            print(f"Game version: {save_info.get('game_phase', 'Unknown')}")
    else:
        print("No save file found.")