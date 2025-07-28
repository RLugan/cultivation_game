"""
Location Integration Helper
Bridges your advanced player system with the new location system
"""

from typing import Dict, Any, Optional
from locations import LocationManager, LocationType
from spirit_stones import generate_spirit_stone_reward, format_spirit_stone_reward

class LocationIntegrationHelper:
    """Helps integrate location bonuses with your existing advanced systems"""
    
    def __init__(self, location_manager: LocationManager):
        self.location_manager = location_manager
    
    def apply_location_cultivation_bonuses(self, player, current_location: LocationType, 
                                         is_batch: bool = False) -> Dict[str, float]:
        """
        Apply location bonuses to player during cultivation
        Returns dict of bonuses applied for display
        """
        bonuses_applied = {}
        location_bonuses = self.location_manager.get_cultivation_bonuses(current_location, player)
        
        # Multiplier for batch cultivation (reduced to prevent overpowering)
        multiplier = 0.3 if is_batch else 1.0
        
        for bonus_name, bonus_value in location_bonuses.items():
            if bonus_value > 0:
                actual_bonus = bonus_value * multiplier
                bonuses_applied[bonus_name] = actual_bonus
                
                # Apply philosophy bonuses
                if 'philosophy' in bonus_name:
                    phil_type = bonus_name.split('_')[0]
                    if phil_type in player.philosophy:
                        player.philosophy[phil_type] += actual_bonus
                
                # Apply elemental bonuses
                elif 'element' in bonus_name:
                    elem_type = bonus_name.split('_')[0]
                    if elem_type in player.elemental_affinities:
                        player.elemental_affinities[elem_type] += actual_bonus * 0.5
        
        return bonuses_applied
    
    def apply_location_spirit_stone_bonus(self, player, current_location: LocationType, 
                                        sessions: int = 1) -> Optional[Dict]:
        """
        Apply location-based spirit stone bonuses
        Returns dict of bonus stones for display
        """
        stone_multiplier = self.location_manager.get_spirit_stone_multiplier(current_location)
        
        if stone_multiplier <= 1.0:
            return None
        
        # Generate base reward and apply location multiplier
        base_reward = generate_spirit_stone_reward(player.realm)
        if not base_reward:
            return None
        
        bonus_stones = {}
        bonus_multiplier = (stone_multiplier - 1.0) * 0.5  # 50% of the bonus to avoid overpowering
        
        for grade, amount in base_reward.items():
            bonus_amount = max(1, int(amount * sessions * bonus_multiplier))
            if bonus_amount > 0:
                player.spirit_stones.add_stones(grade, bonus_amount)
                bonus_stones[grade] = bonus_amount
        
        return bonus_stones if bonus_stones else None
    
    def enhance_encounter_with_location(self, encounter_result, current_location: LocationType):
        """
        Add location flavor to encounters from your SmartEncounterManager
        Works with your existing encounter system
        """
        if not encounter_result:
            return encounter_result
        
        encounter_type, encounter_data = encounter_result
        
        # Add location-specific flavor text
        location_flavors = self._get_location_flavor_texts(current_location)
        
        if location_flavors and 'description' in encounter_data:
            # Append location flavor to existing description
            flavor = location_flavors[encounter_type] if encounter_type in location_flavors else location_flavors.get('default', '')
            if flavor:
                encounter_data['description'] += f" {flavor}"
        
        return encounter_type, encounter_data
    
    def _get_location_flavor_texts(self, location_type: LocationType) -> Dict[str, str]:
        """Get location-specific flavor texts for encounters"""
        flavors = {
            LocationType.PEACEFUL: {
                'insight': "The valley's peaceful energy guides your understanding.",
                'technique': "Ancient protective wards enhance your practice.",
                'bottleneck': "The gentle environment softens the spiritual obstacle.",
                'anomaly': "The valley's protection minimizes the disturbance.",
                'default': "The peaceful valley's energy influences this experience."
            },
            LocationType.FOREST: {
                'insight': "The whispering trees share their ancient wisdom.",
                'technique': "Forest spirits observe and approve of your progress.",
                'bottleneck': "Wild energies make the spiritual barrier more chaotic.",
                'anomaly': "The forest's untamed power amplifies the disturbance.",
                'default': "The mysterious forest shapes this encounter."
            },
            LocationType.MOUNTAIN: {
                'insight': "Dragon energies surge through your enlightenment.",
                'technique': "The mountain's fierce qi tests your resolve.",
                'bottleneck': "Dragon veins make the spiritual obstacle more formidable.",
                'anomaly': "The mountain's raw power intensifies the chaos.",
                'default': "The mighty peak's energy dominates this experience."
            },
            LocationType.RUINS: {
                'insight': "Immortal wisdom from ages past flows through you.",
                'technique': "Ancient formations recognize your cultivation efforts.",
                'bottleneck': "Residual immortal power makes the obstacle more complex.",
                'anomaly': "Chaotic immortal energies create unprecedented effects.",
                'default': "The ruins' accumulated power influences this encounter."
            }
        }
        
        return flavors.get(location_type, {})
    
    def get_location_compatibility_report(self, player, current_location: LocationType) -> str:
        """
        Generate a compatibility report for the player at the current location
        """
        location_info = self.location_manager.get_location_info(current_location)
        bonuses = self.location_manager.get_cultivation_bonuses(current_location, player)
        
        report = f"📍 **{location_info.name} Compatibility Report**\n"
        report += f"{'='*50}\n"
        
        # Basic location info
        report += f"🌿 {location_info.description}\n\n"
        
        # Active bonuses
        if bonuses:
            report += "🌟 **Active Bonuses:**\n"
            for bonus_name, bonus_value in bonuses.items():
                if bonus_value > 0:
                    report += f"   • {bonus_name}: +{bonus_value:.1%}\n"
        else:
            report += "🌟 **Active Bonuses:** None (develop matching affinities for bonuses)\n"
        
        # Philosophy alignment
        report += f"\n📚 **Philosophy Alignment:**\n"
        for philosophy, base_bonus in location_info.philosophy_bonuses.items():
            current_value = player.philosophy.get(philosophy, 0)
            actual_bonus = base_bonus * (1 + current_value * 0.1)
            status = "Strong" if current_value > 5 else "Developing" if current_value > 0 else "Untapped"
            report += f"   • {philosophy.title()}: {status} ({actual_bonus:.1%} bonus)\n"
        
        # Elemental alignment
        report += f"\n🌟 **Elemental Alignment:**\n"
        for element in location_info.elemental_affinities:
            current_affinity = player.elemental_affinities.get(element, 0)
            if current_affinity > 0:
                bonus = 0.02 * current_affinity
                report += f"   • {element.title()}: Active ({bonus:.1%} bonus)\n"
            else:
                report += f"   • {element.title()}: Potential (develop for bonuses)\n"
        
        # Recommendations
        report += f"\n💡 **Recommendations:**\n"
        
        # Check if player has good alignment
        total_active_bonuses = sum(1 for _, v in bonuses.items() if v > 0)
        if total_active_bonuses >= 3:
            report += "   • Excellent location match! Continue cultivating here.\n"
        elif total_active_bonuses >= 1:
            report += "   • Good location synergy. Consider developing more aligned affinities.\n"
        else:
            report += "   • Limited synergy. Focus on developing aligned philosophy/elements.\n"
        
        # Spirit stone bonus
        stone_multiplier = self.location_manager.get_spirit_stone_multiplier(current_location)
        if stone_multiplier > 1.0:
            report += f"   • Great for spirit stone farming ({stone_multiplier:.1f}x multiplier).\n"
        
        # Risk assessment
        difficulty = self.location_manager.get_encounter_difficulty(current_location)
        if difficulty > 1.5:
            report += f"   • High risk area - ensure you can handle increased encounter difficulty.\n"
        elif difficulty > 1.0:
            report += f"   • Moderate risk area - balanced challenge and rewards.\n"
        else:
            report += f"   • Safe cultivation environment for steady progress.\n"
        
        report += f"{'='*50}"
        
        return report
    
    def check_unlock_progress(self, player) -> Dict[LocationType, str]:
        """
        Check progress toward unlocking new locations
        Returns dict of location -> progress description
        """
        all_locations = [LocationType.PEACEFUL, LocationType.FOREST, 
                        LocationType.MOUNTAIN, LocationType.RUINS]
        available = self.location_manager.get_available_locations(player.realm, player.level)
        
        progress = {}
        
        for location_type in all_locations:
            if location_type in available:
                progress[location_type] = "✅ Unlocked"
            else:
                info = self.location_manager.get_location_info(location_type)
                # Simple progress check
                if player.realm == info.unlock_realm:
                    levels_needed = info.unlock_level - player.level
                    if levels_needed <= 0:
                        progress[location_type] = "🔓 Ready to unlock!"
                    else:
                        progress[location_type] = f"🔒 Need {levels_needed} more levels"
                else:
                    progress[location_type] = f"🔒 Need {info.unlock_realm} realm"
        
        return progress


def create_location_save_data(location_manager: LocationManager) -> Dict[str, Any]:
    """
    Create location-specific save data to extend your existing save system
    """
    return {
        'current_location': location_manager.get_current_location().value,
        'unlocked_locations_session': []  # Could track session unlocks if needed
    }


def load_location_save_data(location_manager: LocationManager, save_data: Dict[str, Any]):
    """
    Load location data from save file
    """
    if 'current_location' in save_data:
        try:
            location_type = LocationType(save_data['current_location'])
            location_manager.set_current_location(location_type)
        except ValueError:
            # Invalid location data, default to peaceful valley
            location_manager.set_current_location(LocationType.PEACEFUL)


# Example integration patterns for your existing systems
class AdvancedPlayerLocationBridge:
    """
    Example of how to bridge your Player class with location bonuses
    """
    
    @staticmethod
    def enhanced_cultivate(player, location_manager: LocationManager):
        """
        Example of enhanced cultivation that applies location bonuses
        """
        current_location = location_manager.get_current_location()
        
        # Apply location bonuses before cultivation
        integration_helper = LocationIntegrationHelper(location_manager)
        bonuses_applied = integration_helper.apply_location_cultivation_bonuses(
            player, current_location
        )
        
        # Call your existing cultivate method
        cultivation_messages = player.cultivate()
        
        # Apply location spirit stone bonus
        bonus_stones = integration_helper.apply_location_spirit_stone_bonus(
            player, current_location
        )
        
        # Enhance the last encounter with location flavor
        if hasattr(player.encounter_manager, '_last_encounter'):
            enhanced_encounter = integration_helper.enhance_encounter_with_location(
                player.encounter_manager._last_encounter, current_location
            )
        
        # Return enhanced messages
        enhanced_messages = cultivation_messages.copy()
        
        if bonuses_applied:
            bonus_text = ", ".join(f"{name}+{value:.1%}" for name, value in bonuses_applied.items())
            enhanced_messages.append(f"🌍 Location bonuses: {bonus_text}")
        
        if bonus_stones:
            bonus_display = format_spirit_stone_reward(bonus_stones)
            enhanced_messages.append(f"🌟 Location spirit stone bonus: {bonus_display}")
        
        return enhanced_messages


# Example usage
if __name__ == "__main__":
    # This shows how the integration would work with your systems
    print("=== Location Integration Helper Demo ===")
    print("This helper bridges your advanced player system with locations.")
    print("Use it in your main game loop for seamless integration!")