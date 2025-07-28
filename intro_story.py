"""
Intro Story System for Cultivation Game
Provides immersive introduction to the cultivation world
"""

class IntroStory:
    """Handles the opening narrative and world introduction"""
    
    @staticmethod
    def get_opening_story() -> str:
        """Get the main opening story that introduces the world"""
        return """
🌌 The Realm of Eternal Cultivation 🌌
═══════════════════════════════════════════════════════════════

In a world where mortals dream of immortality, the path of cultivation 
stretches before those brave enough to walk it. Here, spiritual energy 
flows through all things, waiting to be harnessed by those with the 
will and wisdom to do so.

The cultivation realms span from humble beginnings to godlike power:

🏛️  MORTAL REALM - Where all journeys begin
    Foundation Establishment → Qi Condensation → Core Formation

⛰️  SPIRITUAL REALM - Transcending mortal limits  
    Nascent Soul → Soul Transformation → Void Refinement

🌟 IMMORTAL REALM - Approaching the heavens
    Divine Ascension → Celestial Unity → Eternal Dao

But the path is treacherous. Many who seek power find only madness. 
Negative energies corrupt the unwary, and only through balance of 
spirit stones and inner strength can one hope to cleanse such afflictions.

The world is vast, filled with:
• 🏔️  Sacred mountains where ancient energies gather
• 🌲 Mystical forests hiding forgotten techniques  
• 🏛️  Powerful sects that guard their secrets jealously
• 👹 Dangerous encounters that test one's resolve

Spirit stones, crystallized spiritual energy, serve as both currency 
and purification tool. The wise cultivator learns to balance accumulation 
with expenditure, knowing that sometimes one must spend power to preserve it.

═══════════════════════════════════════════════════════════════

Your journey begins now, young cultivator. Will you rise to immortality, 
or become another cautionary tale whispered in the wind?

The dao awaits your choice...
        """.strip()
    
    @staticmethod
    def get_character_motivation_prompt() -> str:
        """Get text for character motivation selection"""
        return """
🎯 What drives your cultivation journey?

Your motivation will influence certain encounters and story elements:

1. 💪 Power - Seek strength to dominate and rule
   "I will become so powerful that none dare oppose me."

2. 🔍 Knowledge - Pursue the secrets of the universe  
   "I must understand the true nature of cultivation and reality."

3. ⚖️  Justice - Gain power to protect the innocent
   "With great power comes the responsibility to defend the weak."

4. 🌟 Transcendence - Escape the cycle of mortal suffering
   "I seek to rise above worldly concerns and achieve enlightenment."

5. 💰 Wealth - Accumulate resources and live in luxury
   "Power means nothing without the riches to enjoy it."

6. 🏠 Family - Restore honor or protect loved ones
   "Everything I do is for those who matter to me."
        """.strip()
    
    @staticmethod  
    def get_motivation_effects() -> dict:
        """Get the mechanical effects of different motivations"""
        return {
            "power": {
                "name": "Path of Domination",
                "description": "Slightly higher chance for combat encounters",
                "effect": "combat_encounter_bonus"
            },
            "knowledge": {
                "name": "Path of Wisdom", 
                "description": "Better understanding of effects and encounters",
                "effect": "knowledge_bonus"
            },
            "justice": {
                "name": "Path of Righteousness",
                "description": "Resistance to negative effects from helping others",
                "effect": "justice_resistance"
            },
            "transcendence": {
                "name": "Path of Enlightenment",
                "description": "Bonus experience from meditation encounters", 
                "effect": "meditation_bonus"
            },
            "wealth": {
                "name": "Path of Prosperity",
                "description": "Increased spirit stone rewards",
                "effect": "wealth_bonus"
            },
            "family": {
                "name": "Path of Devotion", 
                "description": "Stronger motivation provides stability bonuses",
                "effect": "stability_bonus"
            }
        }
    
    @staticmethod
    def get_world_primer() -> str:
        """Get basic world information for new players"""
        return """
🌍 Understanding Your World
═══════════════════════════════════════════════════════════════

KEY CONCEPTS:

🧘 Cultivation - The practice of absorbing spiritual energy to transcend 
   mortal limitations. Each session may bring progress, setbacks, or 
   unexpected encounters.

💎 Spirit Stones - Crystallized spiritual energy that serves as currency.
   Essential for purchasing cures for negative effects and other services.
   
   • 🔸 Low-Grade: Common, basic spiritual energy
   • 🔶 Mid-Grade: Refined energy, worth 100 low-grade  
   • 🔷 High-Grade: Pure energy, worth 10,000 low-grade
   • 💠 Supreme-Grade: Legendary energy, worth 1,000,000 low-grade

🔮 Effects - Cultivation can result in beneficial or harmful spiritual 
   effects. Positive effects aid your progress, while negative effects 
   hinder it and should be cured when possible.

🏛️  Realms - Your cultivation level, from Foundation Establishment to 
   the legendary Eternal Dao. Each realm requires more experience but 
   grants greater power and resistance.

⚠️  Balance - The path of cultivation requires balance. Reckless pursuit 
   of power often leads to spiritual corruption, while excessive caution 
   leads to stagnation.

═══════════════════════════════════════════════════════════════

Remember: Every master was once a beginner. Every expert was once 
an amateur. Your journey of a thousand li begins with a single step.
        """.strip()
    
    @staticmethod
    def get_first_cultivation_guidance() -> str:
        """Get guidance for the player's first cultivation session"""
        return """
🧘 Your First Steps on the Dao
═══════════════════════════════════════════════════════════════

You sit in the lotus position, following the breathing techniques 
from your background knowledge. The world grows quiet around you 
as you turn your attention inward...

CULTIVATION BASICS:
• Each session grants experience toward your next level
• Random encounters may occur, bringing effects or rewards
• Negative effects can be cured with spirit stones
• Your foundation quality affects your cultivation speed

Your background has given you certain advantages. Use them wisely.

The journey of immortality begins with this single breath...
        """.strip()

class StoryDisplay:
    """Handles story display with proper formatting and pacing"""
    
    @staticmethod
    def display_story_with_pacing(story_text: str, auto_continue: bool = False) -> None:
        """Display story text with appropriate pacing"""
        import time
        
        # Split into paragraphs for better pacing
        paragraphs = story_text.split('\n\n')
        
        for i, paragraph in enumerate(paragraphs):
            print(paragraph)
            if i < len(paragraphs) - 1:  # Not the last paragraph
                time.sleep(1.5)  # Brief pause between paragraphs
                print()  # Extra line break
        
        if not auto_continue:
            input("\nPress Enter to continue...")
    
    @staticmethod
    def clear_screen():
        """Clear the screen for better story presentation"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_choice_prompt(prompt: str, choices: list) -> int:
        """Display a choice prompt and get user selection"""
        print(prompt)
        print()
        
        while True:
            try:
                choice = input(f"Enter your choice (1-{len(choices)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(choices):
                    return choice_num - 1  # Return 0-based index
                else:
                    print(f"Please enter a number between 1 and {len(choices)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    @staticmethod
    def display_confirmation(message: str) -> bool:
        """Display a confirmation prompt"""
        print(f"\n{message}")
        while True:
            choice = input("Confirm? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'.")