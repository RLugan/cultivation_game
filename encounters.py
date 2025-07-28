"""
Cultivation Game - Enhanced Encounter System
Handles location-specific encounters with dynamic difficulty scaling
"""

import random
from typing import Dict, List, Optional

class EncounterManager:
    def __init__(self):
        # Base encounter chances (modified by location difficulty)
        self.base_encounter_chance = 0.30
        
        # Encounter type weights (will be modified by location)
        self.encounter_weights = {
            "positive": 40,
            "negative": 35, 
            "neutral": 25
        }
    
    def process_encounter(self, player, location_encounters: Dict, difficulty_multiplier: float = 1.0) -> Optional[Dict]:
        """
        Process a potential encounter during cultivation
        
        Args:
            player: Player object
            location_encounters: Location-specific encounters from LocationManager
            difficulty_multiplier: Location difficulty modifier
        
        Returns:
            Dictionary with encounter details or None if no encounter
        """
        # Adjust encounter chance based on location difficulty
        encounter_chance = self.base_encounter_chance * difficulty_multiplier
        
        if random.random() > encounter_chance:
            return None
        
        # Determine encounter type with location-influenced weights
        weights = self._adjust_weights_for_difficulty(difficulty_multiplier)
        encounter_type = random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
        
        # Get location-specific encounter
        encounters_pool = location_encounters.get(encounter_type, [])
        if not encounters_pool:
            return None
        
        encounter_description = random.choice(encounters_pool)
        
        # Process encounter effects
        encounter_result = {
            'type': encounter_type,
            'description': encounter_description,
            'interrupts': False
        }
        
        # Apply encounter effects based on type and difficulty
        self._apply_encounter_effects(player, encounter_type, difficulty_multiplier, encounter_result)
        
        # Display encounter
        self._display_encounter(encounter_result)
        
        return encounter_result
    
    def _adjust_weights_for_difficulty(self, difficulty_multiplier: float) -> Dict[str, int]:
        """Adjust encounter type weights based on location difficulty"""
        if difficulty_multiplier <= 1.0:
            # Safer locations favor positive encounters
            return {
                "positive": 45,
                "negative": 25,
                "neutral": 30
            }
        elif difficulty_multiplier <= 1.5:
            # Moderate danger locations
            return {
                "positive": 35,
                "negative": 40,
                "neutral": 25
            }
        else:
            # High danger locations favor negative encounters
            return {
                "positive": 25,
                "negative": 50,
                "neutral": 25
            }
    
    def _apply_encounter_effects(self, player, encounter_type: str, difficulty_multiplier: float, encounter_result: Dict):
        """Apply mechanical effects of encounters"""
        
        if encounter_type == "positive":
            self._apply_positive_effects(player, difficulty_multiplier, encounter_result)
        elif encounter_type == "negative":
            self._apply_negative_effects(player, difficulty_multiplier, encounter_result)
        else:  # neutral
            self._apply_neutral_effects(player, difficulty_multiplier, encounter_result)
    
    def _apply_positive_effects(self, player, difficulty_multiplier: float, encounter_result: Dict):
        """Apply positive encounter effects"""
        effect_roll = random.random()
        
        # Scale positive effects with location difficulty (better rewards in dangerous places)
        power_multiplier = max(1.0, difficulty_multiplier * 0.8)
        
        if effect_roll < 0.3:
            # Experience boost
            exp_bonus = int(random.randint(3, 8) * power_multiplier)
            player.cultivation_experience += exp_bonus
            encounter_result['effect'] = f"+{exp_bonus} cultivation experience"
            
        elif effect_roll < 0.5:
            # Spirit stone bonus
            stone_bonus = int(random.randint(1, 3) * power_multiplier)
            player.spirit_stones['low'] += stone_bonus
            encounter_result['effect'] = f"+{stone_bonus} Low Spirit Stones"
            
        elif effect_roll < 0.7:
            # Temporary cultivation boost
            boost_effects = [
                "Enhanced Qi Flow (+10% next breakthrough chance)",
                "Spiritual Clarity (+5% cultivation efficiency)", 
                "Harmonious State (+8% next breakthrough chance)",
                "Enlightened Mind (+12% cultivation insight)"
            ]
            effect = random.choice(boost_effects)
            player.active_effects.append(effect)
            encounter_result['effect'] = f"Gained: {effect}"
            
        elif effect_roll < 0.9:
            # Remove negative effect if any
            if player.active_effects:
                negative_effects = [e for e in player.active_effects if any(word in e.lower() for word in ['disrupted', 'blocked', 'impaired', 'unstable'])]
                if negative_effects:
                    removed_effect = random.choice(negative_effects)
                    player.active_effects.remove(removed_effect)
                    encounter_result['effect'] = f"Cleansed: {removed_effect}"
                else:
                    # No negative effects to remove, give experience instead
                    exp_bonus = int(random.randint(2, 5) * power_multiplier)
                    player.cultivation_experience += exp_bonus
                    encounter_result['effect'] = f"+{exp_bonus} cultivation experience"
            else:
                # No effects to remove, give experience
                exp_bonus = int(random.randint(2, 5) * power_multiplier)
                player.cultivation_experience += exp_bonus
                encounter_result['effect'] = f"+{exp_bonus} cultivation experience"
        else:
            # Rare powerful bonus (higher chance in dangerous locations)
            if difficulty_multiplier >= 1.5 and random.random() < 0.3:
                # Chance for higher grade spirit stones in dangerous locations
                if random.random() < 0.7:
                    player.spirit_stones['mid'] += 1
                    encounter_result['effect'] = "+1 Mid Spirit Stone (rare find!)"
                else:
                    player.spirit_stones['high'] += 1
                    encounter_result['effect'] = "+1 High Spirit Stone (legendary find!)"
            else:
                # Regular powerful effect
                powerful_effects = [
                    "Deep Enlightenment (+20% next breakthrough chance)",
                    "Qi Purification (removes all negative effects)",
                    "Spiritual Resonance (+15% cultivation efficiency)"
                ]
                effect = random.choice(powerful_effects)
                
                if "removes all negative effects" in effect:
                    # Actually remove all negative effects
                    negative_effects = [e for e in player.active_effects if any(word in e.lower() for word in ['disrupted', 'blocked', 'impaired', 'unstable', 'confused'])]
                    for neg_effect in negative_effects:
                        player.active_effects.remove(neg_effect)
                
                player.active_effects.append(effect)
                encounter_result['effect'] = f"Gained: {effect}"
    
    def _apply_negative_effects(self, player, difficulty_multiplier: float, encounter_result: Dict):
        """Apply negative encounter effects"""
        effect_roll = random.random()
        
        # Scale negative effects with location difficulty
        severity_multiplier = difficulty_multiplier
        
        if effect_roll < 0.4:
            # Temporary cultivation impairment
            impairments = [
                "Disrupted Qi Flow (-5% breakthrough chance)",
                "Mental Distraction (-3% cultivation focus)",
                "Unstable Foundation (-7% breakthrough chance)", 
                "Confused State (-4% cultivation efficiency)"
            ]
            
            # More severe effects in dangerous locations
            if severity_multiplier >= 1.5:
                severe_impairments = [
                    "Severely Disrupted Qi (-12% breakthrough chance)",
                    "Major Mental Block (-10% cultivation focus)",
                    "Dangerous Instability (-15% breakthrough chance)"
                ]
                impairments.extend(severe_impairments)
            
            effect = random.choice(impairments)
            player.active_effects.append(effect)
            encounter_result['effect'] = f"Afflicted: {effect}"
            
        elif effect_roll < 0.6:
            # Experience loss
            if player.cultivation_experience > 0:
                exp_loss = min(random.randint(2, 6), player.cultivation_experience)
                if severity_multiplier >= 1.5:
                    exp_loss = min(random.randint(4, 10), player.cultivation_experience)
                
                player.cultivation_experience -= exp_loss
                encounter_result['effect'] = f"-{exp_loss} cultivation experience"
            else:
                # No experience to lose, apply minor effect instead
                effect = "Momentary Setback (-2% next cultivation session)"
                player.active_effects.append(effect)
                encounter_result['effect'] = f"Afflicted: {effect}"
                
        elif effect_roll < 0.8:
            # Resource loss (spirit stones)
            if sum(player.spirit_stones.values()) > 0:
                # Lose low spirit stones first
                if player.spirit_stones['low'] > 0:
                    loss = min(random.randint(1, 2), player.spirit_stones['low'])
                    if severity_multiplier >= 1.5:
                        loss = min(random.randint(1, 4), player.spirit_stones['low'])
                    
                    player.spirit_stones['low'] -= loss
                    encounter_result['effect'] = f"-{loss} Low Spirit Stones"
                else:
                    # Apply effect instead if no stones to lose
                    effect = "Resource Shortage (-3% cultivation efficiency)"
                    player.active_effects.append(effect)
                    encounter_result['effect'] = f"Afflicted: {effect}"
            else:
                # No resources to lose
                effect = "Spiritual Exhaustion (-5% next breakthrough chance)"
                player.active_effects.append(effect)
                encounter_result['effect'] = f"Afflicted: {effect}"
        
        else:
            # Severe encounter (more likely in dangerous locations)
            if severity_multiplier >= 1.8 and random.random() < 0.3:
                # Chance for cultivation session interruption in very dangerous places
                severe_effects = [
                    "Qi Deviation (cultivation session interrupted!)",
                    "Spiritual Backlash (cultivation session interrupted!)",
                    "Environmental Hazard (cultivation session interrupted!)"
                ]
                effect = random.choice(severe_effects)
                player.active_effects.append(effect.split(" (")[0])  # Add the effect without the interruption note
                encounter_result['effect'] = f"Critical: {effect}"
                encounter_result['interrupts'] = True
            else:
                # Regular severe effect
                severe_effects = [
                    "Major Qi Blockage (-10% breakthrough chance)",
                    "Spiritual Contamination (-8% cultivation purity)",
                    "Foundation Damage (-12% next breakthrough chance)"
                ]
                effect = random.choice(severe_effects)
                player.active_effects.append(effect)
                encounter_result['effect'] = f"Severe: {effect}"
    
    def _apply_neutral_effects(self, player, difficulty_multiplier: float, encounter_result: Dict):
        """Apply neutral encounter effects (usually informational or minor temporary)"""
        effect_roll = random.random()
        
        if effect_roll < 0.5:
            # Informational encounters - no mechanical effect
            insights = [
                "You gain insight into the nature of qi flow",
                "The cultivation environment reveals its secrets",
                "You observe other cultivators' techniques",
                "Ancient wisdom becomes clearer to you",
                "The connection between mind and spirit deepens"
            ]
            encounter_result['effect'] = random.choice(insights)
            
        elif effect_roll < 0.8:
            # Minor temporary effects (neutral)
            temp_effects = [
                "Heightened Awareness (temporary +2% perception)",
                "Calm Focus (temporary mental clarity)",
                "Energy Circulation (temporary qi balance)",
                "Mindful State (temporary emotional stability)"
            ]
            effect = random.choice(temp_effects)
            encounter_result['effect'] = f"Temporary: {effect}"
            # Note: These don't go into active_effects as they're very temporary
            
        else:
            # Discovery encounters
            discoveries = [
                "You discover traces of ancient cultivation techniques",
                "Hidden patterns in the environment become visible",
                "You sense the presence of spiritual treasures nearby", 
                "The local qi formations reveal optimization opportunities",
                "You notice signs of legendary cultivators' passage"
            ]
            encounter_result['effect'] = random.choice(discoveries)
    
    def _display_encounter(self, encounter_result: Dict):
        """Display encounter to player with improved formatting"""
        type_icon = {
            'positive': '🌟',
            'negative': '⚠️ ',
            'neutral': 'ℹ️ '
        }
        
        print(f"\n{type_icon.get(encounter_result['type'], '❓')} **ENCOUNTER**")
        print(f"{encounter_result['description']}")
        
        if encounter_result.get('effect'):
            print(f"💫 {encounter_result['effect']}")
        
        if encounter_result.get('interrupts'):
            print(f"🚨 This encounter interrupts your cultivation session!")
    
    def get_effect_severity(self, effect_description: str) -> str:
        """Determine the severity of an effect for curing costs"""
        effect_lower = effect_description.lower()
        
        if any(word in effect_lower for word in ['severe', 'major', 'critical', 'dangerous']):
            return 'severe'
        elif any(word in effect_lower for word in ['disrupted', 'blocked', 'impaired', 'unstable']):
            return 'moderate'
        else:
            return 'minor'