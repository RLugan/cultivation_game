"""
Character Background System for Cultivation Game
Provides different starting backgrounds with unique bonuses and story context
Compatible with your advanced SpiritStoneManager
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

# Import your spirit stone system
from spirit_stones import SpiritStoneGrade

class BackgroundType(Enum):
    ORPHAN = "orphan"
    NOBLE = "noble"  
    MERCHANT = "merchant"
    WANDERER = "wanderer"
    SCHOLAR = "scholar"

@dataclass
class BackgroundBonus:
    """Represents a bonus or penalty from a background"""
    type: str  # 'spirit_stones', 'experience_multiplier', 'encounter_luck', etc.
    value: float
    description: str

@dataclass
class Background:
    """Character background with story and mechanical effects"""
    name: str
    title: str
    description: str
    story: str
    starting_bonuses: List[BackgroundBonus]
    ongoing_effects: List[BackgroundBonus]

class BackgroundSystem:
    """Manages character backgrounds and their effects"""
    
    def __init__(self):
        self.backgrounds = self._initialize_backgrounds()
    
    def _initialize_backgrounds(self) -> Dict[BackgroundType, Background]:
        """Initialize all available backgrounds"""
        return {
            BackgroundType.ORPHAN: Background(
                name="Street Orphan",
                title="The Survivor",
                description="Abandoned as a child, you learned to survive through wit and determination.",
                story="""
Life on the streets taught you that nothing comes easy. Every meal was earned, 
every shelter was temporary, and trust was a luxury you couldn't afford. 

When a mysterious old cultivator found you nearly dead from hunger, he saw 
something in your desperate eyes - a burning will to live that even the 
harshest circumstances couldn't extinguish.

"Child," he said, "your suffering has forged a spirit stronger than steel. 
In cultivation, this will be your greatest asset."

Before disappearing into the mist, he left you with basic cultivation knowledge 
and a few spirit stones. Now you must forge your own path to immortality.
                """.strip(),
                starting_bonuses=[
                    BackgroundBonus("spirit_stones_low", 50, "Street survival skills: +50 starting Low Spirit Stones"),
                    BackgroundBonus("foundation_quality", 5, "Hardened spirit: +5 foundation quality")
                ],
                ongoing_effects=[
                    BackgroundBonus("negative_resistance", 0.1, "10% chance to resist negative effects")
                ]
            ),
            
            BackgroundType.NOBLE: Background(
                name="Fallen Noble",
                title="The Disgraced",
                description="Born to privilege, your family's downfall drives you to reclaim honor through cultivation.",
                story="""
The silk robes and golden ornaments are gone now. Your family's estate lies 
in ruins, seized by political enemies who orchestrated your clan's downfall.

You remember the last words of your dying father: "Our bloodline carries the 
potential for greatness. What politics took from us, cultivation can restore."

Armed with your family's secret cultivation manual and the last of the clan's 
spirit stones, you begin the long journey to rebuild your legacy. The other 
nobles may scorn you now, but one day they will bow before your power.

Your refined upbringing gives you advantages, but the weight of expectation 
presses heavily on your shoulders.
                """.strip(),
                starting_bonuses=[
                    BackgroundBonus("spirit_stones_low", 100, "Family inheritance: +100 Low Spirit Stones"),
                    BackgroundBonus("spirit_stones_mid", 10, "Noble inheritance: +10 Mid Spirit Stones"),
                    BackgroundBonus("max_experience", 20, "Noble education: +20% XP capacity per level")
                ],
                ongoing_effects=[
                    BackgroundBonus("spirit_stone_bonus", 0.15, "15% more spirit stones from cultivation")
                ]
            ),
            
            BackgroundType.MERCHANT: Background(
                name="Traveling Merchant",
                title="The Opportunist", 
                description="Your business acumen and wide travels give you unique advantages in resource management.",
                story="""
For years, you traveled the trade routes between cities, dealing in everything 
from rare herbs to cultivation materials. You learned to spot value where 
others saw trash, and to turn a profit even in the most challenging circumstances.

During one particularly lucrative deal involving spirit stones, you accidentally 
absorbed some of their energy. The sensation was unlike anything you'd ever 
experienced - raw power flowing through your meridians.

That night, an elderly customer explained what had happened: "Young merchant, 
you have the potential for cultivation. Your years of handling spiritual materials 
have awakened your inner energy."

Now you see the ultimate business opportunity - not just trading in power, 
but cultivating it yourself.
                """.strip(),
                starting_bonuses=[
                    BackgroundBonus("spirit_stones_low", 80, "Trading capital: +80 Low Spirit Stones"),
                    BackgroundBonus("spirit_stones_mid", 15, "Trade connections: +15 Mid Spirit Stones"),
                    BackgroundBonus("spirit_stones_high", 2, "Rare finds: +2 High Spirit Stones"),
                    BackgroundBonus("cure_discount", 0.2, "Business connections: 20% cheaper effect cures")
                ],
                ongoing_effects=[
                    BackgroundBonus("spirit_stone_bonus", 0.25, "25% more spirit stones from cultivation"),
                    BackgroundBonus("cure_discount", 0.2, "20% discount on all cures")
                ]
            ),
            
            BackgroundType.WANDERER: Background(
                name="Mountain Wanderer", 
                title="The Seeker",
                description="Years of solitary travel have attuned you to the natural energies of the world.",
                story="""
The mountains called to you from a young age. While others sought comfort in 
cities and villages, you found peace in the wilderness. Years of walking ancient 
paths and sleeping under star-filled skies have made you sensitive to the 
natural flow of energy in the world.

One dawn, while meditating beside a mountain stream, you felt something shift 
within you. The sunrise seemed brighter, the water's song clearer, and for a 
moment, you touched something infinite.

An old hermit, emerging from a cave you'd never noticed before, nodded approvingly. 
"The dao has chosen you, young wanderer. Your connection to nature will serve 
you well in cultivation."

The path you've walked alone has prepared you for the greater journey ahead.
                """.strip(),
                starting_bonuses=[
                    BackgroundBonus("spirit_stones_low", 60, "Simple needs: +60 Low Spirit Stones"),
                    BackgroundBonus("spirit_stones_mid", 5, "Natural treasures: +5 Mid Spirit Stones"),
                    BackgroundBonus("encounter_bonus", 0.15, "Natural intuition: 15% better encounters")
                ],
                ongoing_effects=[
                    BackgroundBonus("encounter_bonus", 0.15, "15% chance for enhanced encounters"),
                    BackgroundBonus("experience_bonus", 0.1, "10% more experience from cultivation")
                ]
            ),
            
            BackgroundType.SCHOLAR: Background(
                name="Academy Scholar",
                title="The Learned", 
                description="Your extensive studies of cultivation theory give you deep understanding of the process.",
                story="""
While others played or worked, you buried yourself in books. The great library 
became your second home, and ancient texts your closest companions. You devoured 
every scroll about cultivation theory, memorizing techniques and principles 
that most practitioners never fully understand.

But theory and practice are different beasts. When you finally attempted your 
first meditation, expecting immediate results from your vast knowledge, nothing 
happened. Weeks of failure followed, despite knowing exactly what should occur.

An old librarian, watching your frustration, finally spoke: "Knowledge is the 
foundation, young scholar, but cultivation requires both mind and spirit. Your 
understanding runs deep - now you must learn to feel what you know."

Your scholarly approach may be slower, but it builds a foundation that will 
never crumble.
                """.strip(),
                starting_bonuses=[
                    BackgroundBonus("spirit_stones_low", 70, "Research stipend: +70 Low Spirit Stones"),
                    BackgroundBonus("spirit_stones_mid", 8, "Academic resources: +8 Mid Spirit Stones"),
                    BackgroundBonus("max_experience", 30, "Deep understanding: +30% XP capacity per level")
                ],
                ongoing_effects=[
                    BackgroundBonus("experience_bonus", 0.2, "20% more experience from cultivation"),
                    BackgroundBonus("effect_insight", 1.0, "Always understand effect details")
                ]
            )
        }
    
    def get_background(self, background_type: BackgroundType) -> Background:
        """Get a specific background"""
        return self.backgrounds[background_type]
    
    def get_all_backgrounds(self) -> List[Background]:
        """Get all available backgrounds"""
        return list(self.backgrounds.values())
    
    def display_background_selection(self) -> str:
        """Generate background selection display text"""
        text = "🎭 Choose Your Background:\n"
        text += "=" * 50 + "\n\n"
        
        for i, bg_type in enumerate(BackgroundType, 1):
            bg = self.backgrounds[bg_type]
            text += f"{i}. {bg.name} - {bg.title}\n"
            text += f"   {bg.description}\n"
            text += f"   Starting Bonuses:\n"
            for bonus in bg.starting_bonuses:
                text += f"     • {bonus.description}\n"
            text += "\n"
        
        return text
    
    def apply_background_to_player(self, player, background_type: BackgroundType):
        """Apply background bonuses to a player using your advanced spirit stone system"""
        background = self.backgrounds[background_type]
        
        # Store background info on player
        player.background = background
        
        # Apply starting bonuses
        for bonus in background.starting_bonuses:
            if bonus.type == "spirit_stones_low":
                # Use your SpiritStoneManager's add_stones method
                player.spirit_stones.add_stones(SpiritStoneGrade.LOW, int(bonus.value))
            elif bonus.type == "spirit_stones_mid":
                player.spirit_stones.add_stones(SpiritStoneGrade.MID, int(bonus.value))
            elif bonus.type == "spirit_stones_high":
                player.spirit_stones.add_stones(SpiritStoneGrade.HIGH, int(bonus.value))
            elif bonus.type == "spirit_stones_peak":
                player.spirit_stones.add_stones(SpiritStoneGrade.PEAK, int(bonus.value))
            elif bonus.type == "foundation_quality":
                player.foundation_quality += bonus.value
            elif bonus.type == "max_experience":
                # Increase max experience for current level
                player.max_experience = int(player.max_experience * (1 + bonus.value/100))
        
        # Store ongoing effects for later use
        if not hasattr(player, 'background_effects'):
            player.background_effects = []
        player.background_effects.extend(background.ongoing_effects)
        
        print(f"✨ Applied {background.name} bonuses to your cultivation journey!")
    
    def get_background_story(self, background_type: BackgroundType) -> str:
        """Get the full story for a background"""
        background = self.backgrounds[background_type]
        story_text = f"🌟 {background.name} - {background.title} 🌟\n"
        story_text += "=" * 60 + "\n\n"
        story_text += background.story + "\n\n"
        story_text += "Starting Benefits:\n"
        for bonus in background.starting_bonuses:
            story_text += f"• {bonus.description}\n"
        story_text += "\nOngoing Effects:\n"
        for effect in background.ongoing_effects:
            story_text += f"• {effect.description}\n"
        
        return story_text
    
    def get_background_bonus_for_location(self, player, location_name: str) -> float:
        """Get background-specific bonus for a location (for future location integration)"""
        if not hasattr(player, 'background'):
            return 0.0
        
        background_name = player.background.name.lower()
        location_lower = location_name.lower()
        
        # Define background-location synergies
        synergies = {
            "street orphan": {
                "peaceful valley": 0.05,  # Feels like a safe home
                "ancient ruins": 0.03     # Street wisdom helps navigate dangers
            },
            "fallen noble": {
                "dragon's peak": 0.08,    # Accustomed to elevated places
                "ancient ruins": 0.05     # Noble heritage connects to ancient nobility
            },
            "traveling merchant": {
                "whispering forest": 0.05, # Good at finding hidden treasures
                "dragon's peak": 0.03      # Trade route experience
            },
            "mountain wanderer": {
                "whispering forest": 0.10, # Natural environment mastery
                "dragon's peak": 0.12,     # Mountain expertise
                "peaceful valley": 0.03    # Connection to nature
            },
            "academy scholar": {
                "peaceful valley": 0.06,   # Quiet study environment
                "ancient ruins": 0.15      # Ancient knowledge resonance
            }
        }
        
        return synergies.get(background_name, {}).get(location_lower, 0.0)


# Compatibility functions for integration with other systems
def get_background_spirit_stone_bonus(player) -> float:
    """Get spirit stone bonus from background for integration with other systems"""
    if not hasattr(player, 'background_effects'):
        return 0.0
    
    for effect in player.background_effects:
        if effect.type == "spirit_stone_bonus":
            return effect.value
    
    return 0.0


def get_background_experience_bonus(player) -> float:
    """Get experience bonus from background for integration with other systems"""
    if not hasattr(player, 'background_effects'):
        return 0.0
    
    for effect in player.background_effects:
        if effect.type == "experience_bonus":
            return effect.value
    
    return 0.0


def get_background_encounter_bonus(player) -> float:
    """Get encounter bonus from background for integration with other systems"""
    if not hasattr(player, 'background_effects'):
        return 0.0
    
    for effect in player.background_effects:
        if effect.type == "encounter_bonus":
            return effect.value
    
    return 0.0


# Example usage
if __name__ == "__main__":
    # Test the background system
    background_system = BackgroundSystem()
    
    print("=== Background System Test ===")
    print(background_system.display_background_selection())
    
    # Test getting a specific background
    orphan_bg = background_system.get_background(BackgroundType.ORPHAN)
    print(f"\nOrphan Background: {orphan_bg.name}")
    print(f"Description: {orphan_bg.description}")
    print(f"Starting bonuses: {len(orphan_bg.starting_bonuses)}")
    print(f"Ongoing effects: {len(orphan_bg.ongoing_effects)}")