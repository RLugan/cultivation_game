"""
Choice-Based Encounter System for Cultivation Game
Gives players meaningful decisions during encounters
"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class EncounterChoice:
    def __init__(self, description: str, consequences: Dict, risk_level: str = "medium"):
        self.description = description
        self.consequences = consequences  # Dict of possible outcomes
        self.risk_level = risk_level  # low, medium, high

@dataclass
class ChoiceEncounter:
    name: str
    description: str
    choices: List[EncounterChoice]
    rarity: str
    context: str  # Additional context for immersion

class ChoiceEncounterManager:
    """Manages choice-based encounters with meaningful decisions"""
    
    def __init__(self):
        self.choice_encounters = self._initialize_choice_encounters()
        self.last_choice_made = None
    
    def _initialize_choice_encounters(self) -> List[ChoiceEncounter]:
        """Initialize all choice-based encounters"""
        encounters = []
        
        # Foundation Building Encounters
        encounters.append(ChoiceEncounter(
            name="Ancient Foundation Pill",
            description="You discover an ancient pill glowing with spiritual energy. Its power could strengthen your foundation, but ancient pills are unpredictable.",
            context="The pill emanates a faint aura of bygone eras. Will you risk consumption?",
            rarity="uncommon",
            choices=[
                EncounterChoice(
                    "🌟 Consume the pill immediately",
                    {
                        "success": {
                            "probability": 0.7,
                            "foundation": 15,
                            "message": "The ancient pill strengthens your foundation significantly!"
                        },
                        "failure": {
                            "probability": 0.3,
                            "negative_effect": {
                                'name': 'Pill Poisoning',
                                'type': 'negative',
                                'description': 'Ancient pill caused spiritual poisoning',
                                'exp_multiplier': 0.8,
                                'remaining_duration': 5
                            },
                            "message": "The ancient pill was corrupted! You suffer from spiritual poisoning."
                        }
                    },
                    "high"
                ),
                EncounterChoice(
                    "🧪 Study the pill carefully first",
                    {
                        "success": {
                            "probability": 0.9,
                            "foundation": 8,
                            "dao_comprehension": {"balance": 2},
                            "message": "Careful study reveals the pill's secrets and safely grants benefits."
                        },
                        "partial": {
                            "probability": 0.1,
                            "foundation": 3,
                            "message": "Your study reveals the pill is too degraded to be safely useful."
                        }
                    },
                    "low"
                ),
                EncounterChoice(
                    "💰 Preserve it as a valuable treasure",
                    {
                        "success": {
                            "probability": 1.0,
                            "spirit_stones": {"mid": 3, "high": 1},
                            "message": "You preserve the pill as a treasure, sensing its future value."
                        }
                    },
                    "low"
                )
            ]
        ))
        
        # Elemental Awakening Encounter
        encounters.append(ChoiceEncounter(
            name="Elemental Spirit Convergence",
            description="Multiple elemental spirits gather around you, each offering to share their essence. You can only accept one offering.",
            context="Fire crackles, water flows, earth rumbles, and wind whispers. Each spirit awaits your choice.",
            rarity="rare",
            choices=[
                EncounterChoice(
                    "🔥 Accept the Fire Spirit's offering",
                    {
                        "success": {
                            "probability": 1.0,
                            "elemental_affinity": {"fire": 12},
                            "dao_comprehension": {"fire": 3},
                            "message": "Fire spirit essence awakens your inner flame!"
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "💧 Accept the Water Spirit's offering",
                    {
                        "success": {
                            "probability": 1.0,
                            "elemental_affinity": {"water": 12},
                            "dao_comprehension": {"water": 3},
                            "message": "Water spirit essence flows through your meridians!"
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "🌍 Accept the Earth Spirit's offering", 
                    {
                        "success": {
                            "probability": 1.0,
                            "elemental_affinity": {"earth": 12},
                            "foundation": 8,
                            "message": "Earth spirit essence solidifies your foundation!"
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "💨 Accept the Wind Spirit's offering",
                    {
                        "success": {
                            "probability": 1.0,
                            "elemental_affinity": {"air": 12},
                            "experience": 20,
                            "message": "Wind spirit essence accelerates your cultivation!"
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "⚖️ Try to balance all four elements",
                    {
                        "success": {
                            "probability": 0.4,
                            "elemental_affinity": {"fire": 5, "water": 5, "earth": 5, "air": 5},
                            "dao_comprehension": {"balance": 8},
                            "message": "You achieve perfect elemental balance! A rare feat!"
                        },
                        "failure": {
                            "probability": 0.6,
                            "negative_effect": {
                                'name': 'Elemental Chaos',
                                'type': 'negative',
                                'description': 'Conflicting elements disrupt your cultivation',
                                'exp_multiplier': 0.7,
                                'remaining_duration': 8
                            },
                            "message": "The conflicting elements create chaos in your spiritual body!"
                        }
                    },
                    "high"
                )
            ]
        ))
        
        # Dao Insight Encounter
        encounters.append(ChoiceEncounter(
            name="Mysterious Dao Monument",
            description="An ancient stone monument covered in mysterious symbols appears before you. Each symbol resonates with different aspects of the Dao.",
            context="The monument hums with ancient wisdom. Different sections glow faintly, each representing a path of understanding.",
            rarity="uncommon",
            choices=[
                EncounterChoice(
                    "⚔️ Study the Sword Dao inscriptions",
                    {
                        "success": {
                            "probability": 0.8,
                            "dao_comprehension": {"sword": 5},
                            "message": "The sword dao inscriptions reveal the path of sharpness and precision!"
                        },
                        "failure": {
                            "probability": 0.2,
                            "message": "The sword dao mysteries remain beyond your current understanding."
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "🌿 Study the Nature Dao inscriptions",
                    {
                        "success": {
                            "probability": 0.8,
                            "dao_comprehension": {"nature": 5},
                            "foundation": 5,
                            "message": "The nature dao inscriptions teach you harmony with the natural world!"
                        },
                        "failure": {
                            "probability": 0.2,
                            "message": "The nature dao concepts slip away like morning mist."
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "💀 Study the Destruction Dao inscriptions",
                    {
                        "success": {
                            "probability": 0.6,
                            "dao_comprehension": {"destruction": 8},
                            "experience": 25,
                            "message": "The destruction dao reveals the power to unmake and reshape!"
                        },
                        "failure": {
                            "probability": 0.4,
                            "negative_effect": {
                                'name': 'Dao Backlash',
                                'type': 'negative', 
                                'description': 'Destruction dao damaged your spiritual stability',
                                'exp_multiplier': 0.85,
                                'remaining_duration': 6
                            },
                            "message": "The destruction dao proves too volatile for your current level!"
                        }
                    },
                    "high"
                ),
                EncounterChoice(
                    "📚 Try to comprehend all inscriptions",
                    {
                        "success": {
                            "probability": 0.3,
                            "dao_comprehension": {"sword": 2, "nature": 2, "destruction": 2, "balance": 4},
                            "message": "Your broad understanding grants insight into the interconnection of all Dao!"
                        },
                        "partial": {
                            "probability": 0.5,
                            "dao_comprehension": {"balance": 2},
                            "message": "You gain some understanding of dao balance, but the deeper mysteries elude you."
                        },
                        "failure": {
                            "probability": 0.2,
                            "negative_effect": {
                                'name': 'Mental Exhaustion',
                                'type': 'negative',
                                'description': 'Overextending your comprehension causes mental fatigue',
                                'exp_multiplier': 0.9,
                                'remaining_duration': 4
                            },
                            "message": "Attempting to grasp too much leaves your mind exhausted."
                        }
                    },
                    "high"
                )
            ]
        ))
        
        # Resource Gathering Encounter
        encounters.append(ChoiceEncounter(
            name="Spirit Stone Mine Discovery",
            description="You discover a small spirit stone mine with visible veins of spiritual energy. However, the mine seems unstable and dangerous to extract from.",
            context="Glowing crystals peek through rock crevices. You sense both opportunity and danger in the unstable formations.",
            rarity="common",
            choices=[
                EncounterChoice(
                    "⛏️ Mine aggressively for maximum yield",
                    {
                        "success": {
                            "probability": 0.6,
                            "spirit_stones": {"low": 8, "mid": 3, "high": 1},
                            "message": "Aggressive mining yields a rich haul of spirit stones!"
                        },
                        "failure": {
                            "probability": 0.4,
                            "spirit_stones": {"low": 2},
                            "negative_effect": {
                                'name': 'Mining Injuries',
                                'type': 'negative',
                                'description': 'Cave-in caused physical injuries affecting cultivation',
                                'exp_multiplier': 0.8,
                                'remaining_duration': 6
                            },
                            "message": "The mine collapses! You escape with injuries and few stones."
                        }
                    },
                    "high"
                ),
                EncounterChoice(
                    "🎯 Mine carefully and safely",
                    {
                        "success": {
                            "probability": 0.9,
                            "spirit_stones": {"low": 5, "mid": 1},
                            "message": "Careful mining yields a modest but safe harvest."
                        },
                        "failure": {
                            "probability": 0.1,
                            "spirit_stones": {"low": 1},
                            "message": "Even careful mining yields little from the depleted veins."
                        }
                    },
                    "low"
                ),
                EncounterChoice(
                    "🔍 Study the formation first",
                    {
                        "success": {
                            "probability": 0.8,
                            "spirit_stones": {"low": 3, "mid": 2},
                            "dao_comprehension": {"earth": 2},
                            "message": "Understanding the formation improves your extraction and earth dao insight!"
                        },
                        "failure": {
                            "probability": 0.2,
                            "dao_comprehension": {"earth": 1},
                            "message": "Your study reveals the formation's nature but yields little material reward."
                        }
                    },
                    "medium"
                )
            ]
        ))
        
        # Breakthrough Assistance Encounter
        encounters.append(ChoiceEncounter(
            name="Senior Cultivator's Guidance",
            description="A mysterious senior cultivator observes your cultivation and offers guidance. Their aura suggests immense power, but their intentions are unclear.",
            context="The senior's eyes seem to see through your very soul. They speak little but their presence radiates ancient wisdom.",
            rarity="rare",
            choices=[
                EncounterChoice(
                    "🙏 Humbly request breakthrough guidance",
                    {
                        "success": {
                            "probability": 0.8,
                            "foundation": 10,
                            "breakthrough_bonus": 0.15,  # 15% better breakthrough success rate
                            "dao_comprehension": {"balance": 3},
                            "message": "The senior imparts valuable insights about breakthrough principles!"
                        },
                        "failure": {
                            "probability": 0.2,
                            "message": "The senior finds you unprepared and offers no guidance."
                        }
                    },
                    "low"
                ),
                EncounterChoice(
                    "⚔️ Challenge them to test your strength",
                    {
                        "success": {
                            "probability": 0.3,
                            "experience": 50,
                            "dao_comprehension": {"sword": 5, "destruction": 3},
                            "foundation": 8,
                            "message": "Your boldness impresses the senior! They spar with you and you learn much!"
                        },
                        "failure": {
                            "probability": 0.7,
                            "negative_effect": {
                                'name': 'Cultivation Setback',
                                'type': 'negative',
                                'description': 'Overwhelming defeat shakes your confidence',
                                'exp_multiplier': 0.7,
                                'remaining_duration': 10
                            },
                            "message": "The senior easily defeats you, leaving you humbled and shaken."
                        }
                    },
                    "high"
                ),
                EncounterChoice(
                    "🤝 Offer to exchange insights",
                    {
                        "success": {
                            "probability": 0.6,
                            "dao_comprehension": {"balance": 2, "wisdom": 3},
                            "spirit_stones": {"mid": 2},
                            "message": "A mutual exchange of insights benefits both of you!"
                        },
                        "partial": {
                            "probability": 0.3,
                            "dao_comprehension": {"balance": 1},
                            "message": "You share insights, though you gain less than you give."
                        },
                        "failure": {
                            "probability": 0.1,
                            "message": "The senior finds your insights lacking and departs without exchange."
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "👁️ Observe them secretly to learn",
                    {
                        "success": {
                            "probability": 0.5,
                            "dao_comprehension": {"shadow": 4, "balance": 2},
                            "experience": 15,
                            "message": "Silent observation teaches you about stealth and the senior's techniques!"
                        },
                        "failure": {
                            "probability": 0.5,
                            "negative_effect": {
                                'name': 'Senior\'s Displeasure',
                                'type': 'negative',
                                'description': 'The senior noticed your spying and is displeased',
                                'exp_multiplier': 0.85,
                                'remaining_duration': 7
                            },
                            "message": "The senior detects your observation and expresses their displeasure!"
                        }
                    },
                    "medium"
                )
            ]
        ))
        
        # Tribulation Training Encounter
        encounters.append(ChoiceEncounter(
            name="Natural Lightning Formation",
            description="You encounter a natural formation where lightning constantly strikes. This could be dangerous tribulation training or a deadly trap.",
            context="Lightning arcs between ancient conductors, creating a natural tribulation chamber. The air crackles with power.",
            rarity="uncommon",
            choices=[
                EncounterChoice(
                    "⚡ Train directly in the lightning",
                    {
                        "success": {
                            "probability": 0.4,
                            "foundation": 15,
                            "elemental_affinity": {"lightning": 10},
                            "tribulation_resistance": 0.1,  # 10% better tribulation resistance
                            "message": "Lightning tempering strengthens your body and spirit dramatically!"
                        },
                        "failure": {
                            "probability": 0.6,
                            "negative_effect": {
                                'name': 'Lightning Scars',
                                'type': 'negative',
                                'description': 'Lightning damage impairs cultivation efficiency',
                                'exp_multiplier': 0.6,
                                'remaining_duration': 12
                            },
                            "foundation": -5,
                            "message": "The lightning proves too powerful! You escape scarred and weakened."
                        }
                    },
                    "high"
                ),
                EncounterChoice(
                    "🛡️ Train at the formation's edge",
                    {
                        "success": {
                            "probability": 0.8,
                            "foundation": 6,
                            "elemental_affinity": {"lightning": 5},
                            "dao_comprehension": {"lightning": 2},
                            "message": "Cautious training at the edge provides steady improvement!"
                        },
                        "failure": {
                            "probability": 0.2,
                            "negative_effect": {
                                'name': 'Minor Lightning Burns',
                                'type': 'negative',
                                'description': 'Minor electrical damage reduces cultivation speed',
                                'exp_multiplier': 0.9,
                                'remaining_duration': 4
                            },
                            "message": "Even at the edge, stray lightning causes minor injuries."
                        }
                    },
                    "medium"
                ),
                EncounterChoice(
                    "📚 Study the formation's principles",
                    {
                        "success": {
                            "probability": 0.9,
                            "dao_comprehension": {"lightning": 4, "balance": 2},
                            "experience": 20,
                            "message": "Understanding the formation's principles advances your theoretical knowledge!"
                        },
                        "failure": {
                            "probability": 0.1,
                            "message": "The formation's complexity exceeds your current understanding."
                        }
                    },
                    "low"
                )
            ]
        ))
        
        return encounters
    
    def get_random_choice_encounter(self, rarity_weights: Dict[str, float] = None) -> Optional[ChoiceEncounter]:
        """Get a random choice encounter based on rarity weights"""
        if rarity_weights is None:
            rarity_weights = {"common": 0.5, "uncommon": 0.3, "rare": 0.15, "very_rare": 0.05}
        
        # Filter encounters by rarity
        available_encounters = []
        for encounter in self.choice_encounters:
            weight = rarity_weights.get(encounter.rarity, 0)
            if weight > 0 and random.random() < weight:
                available_encounters.append(encounter)
        
        return random.choice(available_encounters) if available_encounters else None
    
    def process_choice_encounter(self, encounter: ChoiceEncounter, choice_index: int, player) -> Dict:
        """Process the player's choice and return results"""
        if choice_index < 0 or choice_index >= len(encounter.choices):
            return {"error": "Invalid choice index"}
        
        chosen_option = encounter.choices[choice_index]
        self.last_choice_made = chosen_option.description
        
        # Determine outcome based on probabilities
        outcome_roll = random.random()
        cumulative_prob = 0.0
        
        result = {
            "encounter_name": encounter.name,
            "choice_made": chosen_option.description,
            "risk_level": chosen_option.risk_level,
            "outcomes": []
        }
        
        for outcome_name, outcome_data in chosen_option.consequences.items():
            probability = outcome_data.get("probability", 0)
            cumulative_prob += probability
            
            if outcome_roll <= cumulative_prob:
                # This outcome occurs
                result["primary_outcome"] = outcome_name
                result["message"] = outcome_data.get("message", "")
                
                # Apply all effects from this outcome
                for effect_type, effect_value in outcome_data.items():
                    if effect_type in ["probability", "message"]:
                        continue
                    
                    self._apply_encounter_effect(player, effect_type, effect_value, result)
                
                break
        
        return result
    
    def _apply_encounter_effect(self, player, effect_type: str, effect_value, result: Dict):
        """Apply a specific encounter effect to the player"""
        if effect_type == "experience":
            player.experience += effect_value
            result["outcomes"].append(f"Gained {effect_value} experience")
            
        elif effect_type == "foundation":
            player.foundation_quality += effect_value
            if effect_value > 0:
                result["outcomes"].append(f"Foundation increased by {effect_value}")
            else:
                result["outcomes"].append(f"Foundation decreased by {abs(effect_value)}")
            
        elif effect_type == "dao_comprehension":
            for dao_type, dao_value in effect_value.items():
                if dao_type in player.dao_comprehension:
                    player.dao_comprehension[dao_type] += dao_value
                    result["outcomes"].append(f"Gained {dao_value} {dao_type} dao comprehension")
        
        elif effect_type == "elemental_affinity":
            for element, element_value in effect_value.items():
                if element in player.elemental_affinities:
                    player.elemental_affinities[element] += element_value
                    result["outcomes"].append(f"Gained {element_value} {element} affinity")
        
        elif effect_type == "spirit_stones":
            for grade_name, amount in effect_value.items():
                from spirit_stones import SpiritStoneGrade
                try:
                    grade = SpiritStoneGrade(grade_name.upper().replace("_", "-") + "-GRADE" if "_" in grade_name else grade_name.upper())
                    player.spirit_stones.add_stones(grade, amount)
                    result["outcomes"].append(f"Gained {amount} {grade_name} spirit stones")
                except:
                    # Fallback for grade name issues
                    result["outcomes"].append(f"Gained spirit stones: {grade_name}x{amount}")
        
        elif effect_type == "negative_effect":
            player.ongoing_effects.append(effect_value)
            result["outcomes"].append(f"Afflicted with: {effect_value['name']}")
        
        elif effect_type == "breakthrough_bonus":
            # Store breakthrough bonus for later use
            if not hasattr(player, 'breakthrough_bonuses'):
                player.breakthrough_bonuses = []
            player.breakthrough_bonuses.append(("encounter_guidance", effect_value))
            result["outcomes"].append(f"Gained {effect_value:.1%} breakthrough success bonus")
        
        elif effect_type == "tribulation_resistance":
            # Store tribulation resistance for later use
            if not hasattr(player, 'tribulation_bonuses'):
                player.tribulation_bonuses = []
            player.tribulation_bonuses.append(("lightning_training", effect_value))
            result["outcomes"].append(f"Gained {effect_value:.1%} tribulation resistance")
    
    def display_encounter_choice(self, encounter: ChoiceEncounter) -> str:
        """Format encounter for display to player"""
        display = f"\n{'='*60}\n"
        display += f"💫 **{encounter.name}** 💫\n"
        display += f"{'='*60}\n\n"
        display += f"{encounter.description}\n\n"
        display += f"🌟 {encounter.context}\n\n"
        display += f"Choose your action:\n"
        
        for i, choice in enumerate(encounter.choices, 1):
            risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}
            risk_indicator = risk_emoji.get(choice.risk_level, "⚪")
            display += f"{i}. {choice.description} {risk_indicator}\n"
        
        display += f"\n🟢 = Low Risk | 🟡 = Medium Risk | 🔴 = High Risk\n"
        display += f"{'='*60}\n"
        
        return display
    
    def get_encounter_by_name(self, name: str) -> Optional[ChoiceEncounter]:
        """Get specific encounter by name (for testing)"""
        for encounter in self.choice_encounters:
            if encounter.name == name:
                return encounter
        return None


# Integration helper for main game
class CultivationChoiceManager:
    """Manages when to trigger choice encounters vs normal encounters"""
    
    def __init__(self):
        self.choice_manager = ChoiceEncounterManager()
        self.choice_encounter_chance = 0.25  # 25% chance for choice encounter
        self.last_choice_session = 0
        self.sessions_since_choice = 0
    
    def should_trigger_choice_encounter(self, current_session: int) -> bool:
        """Determine if this session should have a choice encounter"""
        self.sessions_since_choice = current_session - self.last_choice_session
        
        # Increase chance if it's been a while since last choice encounter
        adjusted_chance = self.choice_encounter_chance
        if self.sessions_since_choice > 10:
            adjusted_chance += 0.1  # +10% after 10 sessions
        if self.sessions_since_choice > 20:
            adjusted_chance += 0.15  # +25% total after 20 sessions
        
        return random.random() < adjusted_chance
    
    def get_choice_encounter(self, player_realm: str) -> Optional[ChoiceEncounter]:
        """Get appropriate choice encounter for player realm"""
        # Adjust rarity weights based on realm
        realm_rarity_weights = {
            "Body Tempering": {"common": 0.7, "uncommon": 0.2, "rare": 0.1},
            "Qi Gathering": {"common": 0.6, "uncommon": 0.3, "rare": 0.1},
            "Foundation Building": {"common": 0.4, "uncommon": 0.4, "rare": 0.2},
            "Core Formation": {"common": 0.3, "uncommon": 0.4, "rare": 0.25, "very_rare": 0.05},
            "Nascent Soul": {"common": 0.2, "uncommon": 0.3, "rare": 0.4, "very_rare": 0.1}
        }
        
        weights = realm_rarity_weights.get(player_realm, {"common": 0.5, "uncommon": 0.3, "rare": 0.2})
        return self.choice_manager.get_random_choice_encounter(weights)
    
    def process_player_choice(self, encounter: ChoiceEncounter, choice_index: int, player, current_session: int) -> Dict:
        """Process player choice and update tracking"""
        self.last_choice_session = current_session
        self.sessions_since_choice = 0
        
        return self.choice_manager.process_choice_encounter(encounter, choice_index, player)


# Example usage
if __name__ == "__main__":
    # Test the choice encounter system
    choice_manager = ChoiceEncounterManager()
    
    print("=== Choice Encounter System Test ===")
    
    # Get a test encounter
    test_encounter = choice_manager.get_encounter_by_name("Ancient Foundation Pill")
    if test_encounter:
        print(choice_manager.display_encounter_choice(test_encounter))
        
        # Simulate player choice (choice 0 = consume immediately)
        from enhanced_player import EnhancedPlayer
        test_player = EnhancedPlayer("Test Player")
        
        result = choice_manager.process_choice_encounter(test_encounter, 0, test_player)
        print(f"\nResult: {result}")