"""
Enhanced Cultivation Game - Complete Integration
Combines all systems: Realm/Stage, Foundation, Choice Encounters, and Locations
"""

import os
import sys
import time
import random
from typing import Optional, Dict, List

# Import all the enhanced systems
try:
    from player import EnhancedPlayer, migrate_old_player_to_enhanced
    from realm_stage_system import RealmStageManager, CultivationRealm
    from choice_encounters import CultivationChoiceManager
    from character_backgrounds import BackgroundSystem, BackgroundType
    from intro_story import IntroStory, StoryDisplay
    from save_system import SaveSystem
    from locations import LocationManager, LocationType
    from spirit_stones import generate_spirit_stone_reward, format_spirit_stone_reward
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Please make sure all required modules are in the same directory")
    input("Press Enter to exit...")
    sys.exit(1)

class EnhancedCultivationGame:
    def __init__(self):
        self.player: Optional[EnhancedPlayer] = None
        self.realm_manager = RealmStageManager()
        self.choice_manager = CultivationChoiceManager()
        self.background_system = BackgroundSystem()
        self.intro_story = IntroStory()
        self.story_display = StoryDisplay()
        self.save_system = SaveSystem()
        self.location_manager = LocationManager()
        self.unlocked_locations_this_session = []
        self.game_running = True
        self.current_session = 0
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def wait_for_enter(self, message: str = "Press Enter to continue..."):
        """Wait for user input before continuing"""
        input(f"\n{message}")
    
    def start_game(self):
        """Main game entry point"""
        self.clear_screen()
        
        # Check for existing save (try to migrate old players)
        if self.save_system.save_exists():
            print("🔄 **EXISTING CULTIVATION PROGRESS DETECTED** 🔄")
            save_info = self.save_system.get_save_info()
            if save_info:
                print(f"📅 Save Date: {save_info.get('timestamp', 'Unknown')}")
                print(f"🎮 Version: {save_info.get('game_phase', 'Unknown')}")
            
            choice = input("\nContinue existing cultivation journey? (y/n): ").lower().strip()
            if choice == 'y':
                self.load_existing_game()
            else:
                self.start_new_game()
        else:
            self.start_new_game()
        
        if self.player:
            self.main_game_loop()
    
    def start_new_game(self):
        """Start completely new game with enhanced character creation"""
        self.clear_screen()
        
        # Display opening story
        opening_story = self.intro_story.get_opening_story()
        self.story_display.display_story_with_pacing(opening_story)
        
        self.clear_screen()
        print("🌟 **CHARACTER CREATION** 🌟")
        print("="*50)
        
        # Get player name
        name = input("\nEnter your cultivator name: ").strip()
        if not name:
            name = "Nameless Cultivator"
        
        # Background selection
        print("\n" + "="*60)
        print("🎭 **CHOOSE YOUR ORIGIN** 🎭")
        print("="*60)
        
        background_selection = self.background_system.display_background_selection()
        print(background_selection)
        
        while True:
            try:
                choice = int(input(f"Choose your background (1-{len(BackgroundType)}): "))
                if 1 <= choice <= len(BackgroundType):
                    background_type = list(BackgroundType)[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(BackgroundType)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Show background story
        background_story = self.background_system.get_background_story(background_type)
        self.clear_screen()
        print(background_story)
        
        confirm = self.story_display.display_confirmation("Is this the path you wish to walk?")
        if not confirm:
            print("🔄 Returning to background selection...")
            return self.start_new_game()
        
        # Motivation selection
        self.clear_screen()
        motivation_prompt = self.intro_story.get_character_motivation_prompt()
        print(motivation_prompt)
        
        while True:
            try:
                choice = int(input("\nChoose your motivation (1-6): "))
                if 1 <= choice <= 6:
                    motivations = ["power", "knowledge", "justice", "transcendence", "wealth", "family"]
                    motivation = motivations[choice - 1]
                    break
                else:
                    print("Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Create enhanced player
        self.player = EnhancedPlayer(name)
        
        # Apply background bonuses
        self.background_system.apply_background_to_player(self.player, background_type)
        
        # Store motivation
        self.player.motivation = motivation
        
        # Show character creation summary
        self.display_character_creation_summary(background_type, motivation)
        
        # Display world primer and guidance
        self.clear_screen()
        world_primer = self.intro_story.get_world_primer()
        self.story_display.display_story_with_pacing(world_primer)
        
        self.clear_screen()
        first_guidance = self.intro_story.get_first_cultivation_guidance()
        print(first_guidance)
        self.wait_for_enter()
        
        # Save initial state
        if self.save_system.save_player(self.player):
            print("\n💾 Your cultivation journey has been recorded.")
        
        print(f"\n✨ Welcome to the path of immortality, {self.player.name}!")
        print("🌸 Your journey begins in the Peaceful Valley...")
        self.wait_for_enter()
    
    def load_existing_game(self):
        """Load existing game with migration support"""
        save_data = self.save_system.load_player()
        if save_data:
            try:
                # Try to load as enhanced player
                self.player = EnhancedPlayer.from_save_data(save_data)
            except:
                try:
                    # Try to load as old player and migrate
                    from player import Player as OldPlayer
                    old_player = self.save_system.dict_to_player(save_data)
                    self.player = migrate_old_player_to_enhanced(old_player)
                    print("🔄 Migrated old save to new enhanced system!")
                except:
                    print("❌ Could not load save data. Starting new game...")
                    return self.start_new_game()
            
            print(f"✨ Welcome back, {self.player.name}!")
            current_location = self.location_manager.get_current_location()
            location_info = self.location_manager.get_location_info(current_location)
            print(f"📍 You continue your cultivation in {location_info.name}")
            print(f"🧘 Current Cultivation: {self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)}")
            self.wait_for_enter()
        else:
            print("❌ Failed to load save data. Starting new game...")
            self.start_new_game()
    
    def display_character_creation_summary(self, background_type: BackgroundType, motivation: str):
        """Enhanced character creation summary"""
        self.clear_screen()
        background = self.background_system.get_background(background_type)
        motivation_effects = self.intro_story.get_motivation_effects()
        motivation_info = motivation_effects.get(motivation, {})
        
        print("="*60)
        print("🎭 **YOUR CULTIVATION IDENTITY** 🎭")
        print("="*60)
        
        print(f"\n📛 **Name:** {self.player.name}")
        print(f"🧘 **Cultivation:** {self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)}")
        print(f"🏮 **Background:** {background.name}")
        print(f"   {background.description}")
        
        print(f"\n🎯 **Motivation:** {motivation_info.get('name', motivation.title())}")
        print(f"   {motivation_info.get('description', 'Your driving force in cultivation.')}")
        
        print(f"\n💎 **Starting Resources:**")
        print(f"   {self.player.get_spirit_stone_display()}")
        print(f"   Foundation Quality: {self.player.foundation_quality}")
        
        print(f"\n💫 **Background Benefits:**")
        for bonus in background.starting_bonuses:
            print(f"   • {bonus.description}")
        
        print(f"\n🌟 **Ongoing Effects:**")
        for effect in background.ongoing_effects:
            print(f"   • {effect.description}")
        
        print("\n" + "="*60)
        self.wait_for_enter("Press Enter to begin your cultivation journey...")
    
    def main_game_loop(self):
        """Enhanced main game loop with all new systems"""
        while self.game_running:
            self.current_session += 1
            self.clear_screen()
            self.display_enhanced_status()
            
            # Check for newly unlocked locations
            self.check_location_unlocks()
            
            choice = self.get_menu_choice()
            self.handle_menu_choice(choice)
    
    def check_location_unlocks(self):
        """Check if new locations have been unlocked"""
        available_locations = self.location_manager.get_available_locations(
            self.player.realm.value, self.player.stage
        )
        
        for location_type in available_locations:
            if (location_type not in self.unlocked_locations_this_session and 
                location_type != LocationType.PEACEFUL):
                
                self.unlocked_locations_this_session.append(location_type)
                print(self.location_manager.display_location_unlock_message(location_type))
                self.wait_for_enter()
    
    def display_enhanced_status(self):
        """Enhanced status display with all new information"""
        current_location = self.location_manager.get_current_location()
        location_info = self.location_manager.get_location_info(current_location)
        
        print("="*70)
        print(f"🧘 **{self.player.name}** - Cultivation Status")
        print("="*70)
        
        # Cultivation progress
        cultivation_title = self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)
        next_stage_exp = self.player.get_next_stage_exp_requirement()
        
        print(f"⚡ Cultivation: {cultivation_title}")
        print(f"📊 Progress: {self.player.experience}/{self.player.get_current_stage_exp_requirement()} experience")
        if next_stage_exp > 0:
            print(f"🎯 Next Stage: {next_stage_exp} experience required")
        
        print(f"🏗️ Foundation: {self.player.foundation_quality} quality")
        
        # Combat power
        combat_power = self.realm_manager.calculate_combat_power(
            self.player.realm, self.player.stage, self.player.foundation_quality
        )
        print(f"⚔️ Combat Power: {combat_power:,}")
        
        # Location info
        print(f"\n📍 Location: {location_info.name}")
        bonuses = self.location_manager.get_cultivation_bonuses(current_location, self.player)
        if bonuses:
            bonus_text = ", ".join([f"{name.replace('_', ' ').title()}+{value:.1%}" 
                                  for name, value in bonuses.items() if value > 0])
            if bonus_text:
                print(f"   🌟 Active bonuses: {bonus_text}")
        
        # Elements and Dao
        if self.player.primary_element:
            primary_value = self.player.elemental_affinities.get(self.player.primary_element, 0)
            print(f"🌟 Primary Element: {self.player.primary_element.title()} ({primary_value})")
        
        # Show top dao comprehensions
        top_dao = sorted([(k, v) for k, v in self.player.dao_comprehension.items() if v > 0], 
                        key=lambda x: x[1], reverse=True)[:3]
        if top_dao:
            dao_text = ", ".join([f"{dao.title()}({value})" for dao, value in top_dao])
            print(f"🧠 Top Dao: {dao_text}")
        
        # Spirit stones and effects
        print(f"\n🔸 {self.player.get_spirit_stone_display()}")
        
        if self.player.ongoing_effects:
            positive = len([e for e in self.player.ongoing_effects if e.get('type') == 'positive'])
            negative = len([e for e in self.player.ongoing_effects if e.get('type') == 'negative'])
            print(f"🔮 Effects: {positive} positive, {negative} negative")
        
        # Breakthrough status
        if self.player.stage == 9:
            can_breakthrough, msg = self.realm_manager.can_breakthrough_realm(
                self.player.realm, self.player.stage, self.player.foundation_quality
            )
            if can_breakthrough:
                success_rate = self.realm_manager.calculate_breakthrough_success_rate(
                    self.player.realm, self.player.foundation_quality
                )
                print(f"🌟 Ready for breakthrough! Success rate: {success_rate:.1%}")
            else:
                print(f"⚠️ {msg}")
        elif self.player.recovery_time > 0:
            print(f"🩹 Recovering from failed breakthrough ({self.player.recovery_time} sessions)")
        
        print("="*70)
    
    def get_menu_choice(self) -> int:
        """Enhanced menu with all new options"""
        print("\n🎮 **CULTIVATION MENU** 🎮")
        print("1. 🧘 Cultivate (with focus choice)")
        print("2. 🔄 Cultivate Multiple Times")
        print("3. 🧘 Meditate for Recovery (free effect cure)")
        print("4. 🌟 Attempt Realm Breakthrough")
        print("5. 📊 View Detailed Status")
        print("6. 🔸 Manage Spirit Stones")
        print("7. 🩹 Cure Effects (spirit stones)")
        print("8. 🔮 View Active Effects")
        print("9. 📜 Last Session Details")
        print("10. 📈 Cultivation History")
        print("11. 🌍 Select Location")
        print("12. 🎭 Character Information")
        print("13. 🎯 Philosophy & Elements")
        print("14. ⚔️ Combat Power Analysis")
        print("15. 💾 Save Game")
        print("16. 🚪 Exit Game")
        
        try:
            choice = int(input("\nEnter your choice (1-16): "))
            return choice
        except ValueError:
            return -1
    
    def handle_menu_choice(self, choice: int):
        """Handle enhanced menu choices"""
        if choice == 1:
            self.cultivate_with_choice()
        elif choice == 2:
            self.cultivate_multiple()
        elif choice == 3:
            self.meditate_for_recovery()
        elif choice == 4:
            self.attempt_breakthrough()
        elif choice == 5:
            self.view_detailed_status()
        elif choice == 6:
            self.manage_spirit_stones()
        elif choice == 7:
            self.cure_effects()
        elif choice == 8:
            self.view_active_effects()
        elif choice == 9:
            self.view_last_session()
        elif choice == 10:
            self.view_cultivation_history()
        elif choice == 11:
            self.select_location()
        elif choice == 12:
            self.view_character_info()
        elif choice == 13:
            self.view_philosophy_elements()
        elif choice == 14:
            self.combat_power_analysis()
        elif choice == 15:
            self.save_game()
        elif choice == 16:
            self.exit_game()
        else:
            print("❌ Invalid choice. Please try again.")
            self.wait_for_enter()
    
    def cultivate_with_choice(self):
        """Enhanced cultivation with focus choices and choice encounters"""
        self.clear_screen()
        current_location = self.location_manager.get_current_location()
        location_info = self.location_manager.get_location_info(current_location)
        
        print(f"🧘 **CULTIVATION SESSION** in {location_info.name}")
        print(f"🌿 {location_info.description}")
        
        # Show cultivation choices
        print("\n🎯 Choose your cultivation focus:")
        choices = self.player.get_cultivation_choices()
        for i, (choice_key, choice_desc) in enumerate(choices, 1):
            print(f"{i}. {choice_desc}")
        
        while True:
            try:
                choice = int(input(f"\nSelect focus (1-{len(choices)}): "))
                if 1 <= choice <= len(choices):
                    focus = choices[choice - 1][0]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(choices)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Check for choice encounter
        if self.choice_manager.should_trigger_choice_encounter(self.current_session):
            choice_encounter = self.choice_manager.get_choice_encounter(self.player.realm.value)
            if choice_encounter:
                print(self.choice_manager.choice_manager.display_encounter_choice(choice_encounter))
                
                while True:
                    try:
                        encounter_choice = int(input(f"Choose your action (1-{len(choice_encounter.choices)}): "))
                        if 1 <= encounter_choice <= len(choice_encounter.choices):
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(choice_encounter.choices)}.")
                    except ValueError:
                        print("Please enter a valid number.")
                
                # Process choice encounter
                result = self.choice_manager.process_player_choice(
                    choice_encounter, encounter_choice - 1, self.player, self.current_session
                )
                
                print(f"\n💫 {result['message']}")
                if result.get('outcomes'):
                    for outcome in result['outcomes']:
                        print(f"   • {outcome}")
                
                print(f"\n🧘 Continuing with {focus} cultivation...")
                time.sleep(2)
        
        # Apply location bonuses
        bonuses = self.location_manager.get_cultivation_bonuses(current_location, self.player)
        if bonuses:
            for bonus_name, bonus_value in bonuses.items():
                if bonus_value > 0:
                    if 'dao' in bonus_name or 'philosophy' in bonus_name:
                        dao_type = bonus_name.split('_')[0]
                        if dao_type in self.player.dao_comprehension:
                            self.player.dao_comprehension[dao_type] += bonus_value
                    elif 'element' in bonus_name:
                        elem_type = bonus_name.split('_')[0]
                        if elem_type in self.player.elemental_affinities:
                            self.player.elemental_affinities[elem_type] += bonus_value * 0.5
        
        # Perform cultivation
        messages = self.player.cultivate_with_choice(focus)
        
        print(f"\n💫 Cultivation Results:")
        for message in messages:
            print(f"   {message}")
        
        # Location spirit stone bonus
        stone_multiplier = self.location_manager.get_spirit_stone_multiplier(current_location)
        if stone_multiplier > 1.0:
            bonus_stones = generate_spirit_stone_reward(self.player.realm.value)
            if bonus_stones:
                for grade, amount in bonus_stones.items():
                    bonus_amount = max(1, int(amount * (stone_multiplier - 1.0)))
                    self.player.spirit_stones.add_stones(grade, bonus_amount)
                
                bonus_display = format_spirit_stone_reward(bonus_stones)
                print(f"   🌟 Location bonus: {bonus_display}")
        
        self.wait_for_enter()
    
    def cultivate_multiple(self):
        """Enhanced batch cultivation with interruptions"""
        self.clear_screen()
        current_location = self.location_manager.get_current_location()
        location_info = self.location_manager.get_location_info(current_location)
        
        print(f"🔄 **BATCH CULTIVATION** in {location_info.name}")
        print(f"🌿 {location_info.description}")
        
        try:
            sessions = int(input("\nHow many cultivation sessions? (1-50): "))
            if sessions < 1 or sessions > 50:
                print("❌ Please enter a number between 1 and 50.")
                self.wait_for_enter()
                return
        except ValueError:
            print("❌ Please enter a valid number.")
            self.wait_for_enter()
            return
        
        # Get cultivation focus for all sessions
        print("\n🎯 Choose cultivation focus for all sessions:")
        choices = self.player.get_cultivation_choices()
        for i, (choice_key, choice_desc) in enumerate(choices, 1):
            print(f"{i}. {choice_desc}")
        
        while True:
            try:
                choice = int(input(f"\nSelect focus (1-{len(choices)}): "))
                if 1 <= choice <= len(choices):
                    focus = choices[choice - 1][0]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(choices)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\n🧘 Beginning {sessions} {focus} cultivation sessions...")
        
        # Track results
        initial_stage = self.player.stage
        initial_realm = self.player.realm
        total_foundation_gained = 0
        total_encounters = 0
        choice_encounters = 0
        breakthrough_attempts = 0
        
        for i in range(sessions):
            self.current_session += 1
            print(f"\n--- Session {i+1} ---")
            
            # Check for choice encounter interruption
            if self.choice_manager.should_trigger_choice_encounter(self.current_session):
                choice_encounter = self.choice_manager.get_choice_encounter(self.player.realm.value)
                if choice_encounter:
                    choice_encounters += 1
                    print(f"⚠️ Significant encounter interrupts batch cultivation!")
                    print(self.choice_manager.choice_manager.display_encounter_choice(choice_encounter))
                    
                    while True:
                        try:
                            encounter_choice = int(input(f"Choose (1-{len(choice_encounter.choices)}, 0 to skip): "))
                            if 0 <= encounter_choice <= len(choice_encounter.choices):
                                break
                            else:
                                print(f"Please enter 0 or 1-{len(choice_encounter.choices)}.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    if encounter_choice > 0:
                        result = self.choice_manager.process_player_choice(
                            choice_encounter, encounter_choice - 1, self.player, self.current_session
                        )
                        print(f"💫 {result['message']}")
                        if result.get('outcomes'):
                            for outcome in result['outcomes']:
                                print(f"   • {outcome}")
            
            # Apply location bonuses (reduced for batch)
            bonuses = self.location_manager.get_cultivation_bonuses(current_location, self.player)
            for bonus_name, bonus_value in bonuses.items():
                if bonus_value > 0:
                    if 'dao' in bonus_name:
                        dao_type = bonus_name.split('_')[0]
                        if dao_type in self.player.dao_comprehension:
                            self.player.dao_comprehension[dao_type] += bonus_value * 0.3
                    elif 'element' in bonus_name:
                        elem_type = bonus_name.split('_')[0]
                        if elem_type in self.player.elemental_affinities:
                            self.player.elemental_affinities[elem_type] += bonus_value * 0.15
            
            # Cultivate
            session_details = self.player.last_session_details
            messages = self.player.cultivate_with_choice(focus)
            
            # Track progress
            if session_details and 'foundation_gained' in session_details:
                total_foundation_gained += session_details['foundation_gained']
            
            if session_details and session_details.get('encounter'):
                total_encounters += 1
            
            # Show key results
            for message in messages:
                if any(keyword in message.lower() for keyword in 
                      ['advanced', 'breakthrough', 'foundation', 'spirit stones']):
                    print(f"   {message}")
            
            # Check for realm breakthrough opportunity
            if self.player.stage == 9 and self.player.recovery_time == 0:
                can_breakthrough, _ = self.realm_manager.can_breakthrough_realm(
                    self.player.realm, self.player.stage, self.player.foundation_quality
                )
                if can_breakthrough:
                    print(f"   🌟 Ready for realm breakthrough!")
                    attempt = input("   Attempt breakthrough now? (y/n): ").lower().strip()
                    if attempt == 'y':
                        breakthrough_attempts += 1
                        success, message, result_data = self.player.attempt_realm_breakthrough()
                        print(f"   {message}")
                        if not success:
                            break  # Stop batch if breakthrough fails
            
            time.sleep(0.1)  # Brief pause
        
        # Apply batch location bonus
        stone_multiplier = self.location_manager.get_spirit_stone_multiplier(current_location)
        if stone_multiplier > 1.0:
            bonus_stones = generate_spirit_stone_reward(self.player.realm.value)
            if bonus_stones:
                for grade, amount in bonus_stones.items():
                    bonus_amount = max(1, int(amount * sessions * (stone_multiplier - 1.0) * 0.3))
                    self.player.spirit_stones.add_stones(grade, bonus_amount)
        
        # Display summary
        final_stage = self.player.stage
        final_realm = self.player.realm
        
        print(f"\n{'='*60}")
        print(f"📊 **BATCH CULTIVATION SUMMARY**")
        print(f"{'='*60}")
        print(f"📍 Location: {location_info.name}")
        print(f"🎯 Focus: {focus.title()}")
        print(f"🧘 Sessions: {sessions}")
        print(f"📈 Progress: {initial_realm.value} Stage {initial_stage} → {final_realm.value} Stage {final_stage}")
        if total_foundation_gained > 0:
            print(f"🏗️ Foundation Gained: +{total_foundation_gained}")
        print(f"💫 Regular Encounters: {total_encounters}")
        print(f"🎯 Choice Encounters: {choice_encounters}")
        if breakthrough_attempts > 0:
            print(f"🌟 Breakthrough Attempts: {breakthrough_attempts}")
        print(f"{'='*60}")
        
        self.wait_for_enter()
    
    def meditate_for_recovery(self):
        """Free meditation to cure effects"""
        self.clear_screen()
        print("🧘 **MEDITATION FOR RECOVERY** 🧘")
        
        negative_effects = self.player.get_negative_effects()
        if not negative_effects:
            print("✨ You have no negative effects to cleanse through meditation.")
            print("💡 Meditation can still provide other benefits!")
            
            # Offer meditation for foundation/dao benefits
            meditate = input("\nMeditate for spiritual growth? (y/n): ").lower().strip()
            if meditate == 'y':
                foundation_gain = random.randint(1, 3)
                dao_gain = random.randint(1, 2)
                
                self.player.foundation_quality += foundation_gain
                # Random dao insight
                available_dao = [dao for dao, value in self.player.dao_comprehension.items() if value < 50]
                if available_dao:
                    chosen_dao = random.choice(available_dao)
                    self.player.dao_comprehension[chosen_dao] += dao_gain
                    print(f"🧘 Peaceful meditation grants +{foundation_gain} foundation and +{dao_gain} {chosen_dao} dao")
                else:
                    print(f"🧘 Peaceful meditation grants +{foundation_gain} foundation")
            
            self.wait_for_enter()
            return
        
        print("🔮 Current negative effects:")
        for i, effect in enumerate(negative_effects, 1):
            duration = f" ({effect['remaining_duration']} sessions)" if effect.get('remaining_duration') else ""
            print(f"   {i}. {effect['name']}{duration}")
            if effect.get('description'):
                print(f"      {effect['description']}")
        
        success, message = self.player.meditate_for_recovery()
        print(f"\n{message}")
        
        if success:
            # Additional benefits from successful meditation
            foundation_bonus = random.randint(1, 2)
            self.player.foundation_quality += foundation_bonus
            print(f"🏗️ Meditation also strengthened your foundation: +{foundation_bonus}")
        
        self.wait_for_enter()
    
    def attempt_breakthrough(self):
        """Attempt realm breakthrough with enhanced interface"""
        self.clear_screen()
        print("🌟 **REALM BREAKTHROUGH ATTEMPT** 🌟")
        
        if self.player.recovery_time > 0:
            print(f"🩹 You are still recovering from a previous breakthrough attempt.")
            print(f"⏰ Recovery time remaining: {self.player.recovery_time} sessions")
            self.wait_for_enter()
            return
        
        can_attempt, reason = self.realm_manager.can_breakthrough_realm(
            self.player.realm, self.player.stage, self.player.foundation_quality
        )
        
        if not can_attempt:
            print(f"❌ Cannot attempt breakthrough: {reason}")
            
            if self.player.stage < 9:
                next_exp = self.player.get_next_stage_exp_requirement()
                print(f"💡 Reach Stage 9 first. Need {next_exp - self.player.experience} more experience.")
            
            self.wait_for_enter()
            return
        
        # Show breakthrough information
        success_rate = self.realm_manager.calculate_breakthrough_success_rate(
            self.player.realm, self.player.foundation_quality
        )
        next_realm = self.realm_manager.get_next_realm(self.player.realm)
        
        print(f"📊 **Breakthrough Analysis:**")
        print(f"   Current: {self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)}")
        print(f"   Target: {next_realm.value if next_realm else 'Peak of Cultivation'}")
        print(f"   Success Rate: {success_rate:.1%}")
        print(f"   Foundation Quality: {self.player.foundation_quality}")
        
        # Show risks
        print(f"\n⚠️ **Risks of Failure:**")
        print(f"   • Loss of foundation quality (2-8 points)")
        print(f"   • Loss of experience (10-30%)")
        print(f"   • Recovery time (3-7 sessions)")
        print(f"   • Qi deviation effects")
        
        # Show benefits of success
        print(f"\n🌟 **Benefits of Success:**")
        print(f"   • Advance to {next_realm.value if next_realm else 'Unknown Realm'}")
        print(f"   • Foundation strengthening bonus")
        print(f"   • Clear negative effects")
        print(f"   • Possible elemental awakening")
        
        # Confirmation
        print(f"\n" + "="*50)
        confirm = input("Attempt breakthrough? (yes/no): ").lower().strip()
        
        if confirm not in ['yes', 'y']:
            print("🧘 You decide to continue cultivating for now.")
            self.wait_for_enter()
            return
        
        # Attempt breakthrough
        print(f"\n🌟 Attempting breakthrough...")
        print(f"💫 Gathering spiritual energy...")
        time.sleep(2)
        print(f"⚡ Challenging the heavenly dao...")
        time.sleep(2)
        
        success, message, result_data = self.player.attempt_realm_breakthrough()
        
        print(f"\n{message}")
        
        if success:
            print(f"🎉 Congratulations! You have transcended to a new realm!")
            if 'foundation_bonus' in result_data:
                print(f"🏗️ Breakthrough strengthened your foundation: +{result_data['foundation_bonus']}")
        else:
            if 'foundation_damage' in result_data:
                print(f"💔 Foundation damaged: -{result_data['foundation_damage']}")
            if 'exp_loss_percent' in result_data:
                print(f"📉 Experience lost: {result_data['exp_loss_percent']}%")
            if 'recovery_time' in result_data:
                print(f"🩹 Recovery needed: {result_data['recovery_time']} sessions")
        
        self.wait_for_enter()
    
    def view_detailed_status(self):
        """View comprehensive player status"""
        self.clear_screen()
        print(self.player.get_status())
        self.wait_for_enter()
    
    def manage_spirit_stones(self):
        """Enhanced spirit stone management"""
        self.clear_screen()
        current_location = self.location_manager.get_current_location()
        location_info = self.location_manager.get_location_info(current_location)
        
        print("🔸 **SPIRIT STONE MANAGEMENT** 🔸")
        print(f"📍 Current Location: {location_info.name}")
        print(f"💎 Spirit Stone Bonus: {location_info.spirit_stone_multiplier:.1f}x")
        print()
        print(self.player.get_spirit_stone_display())
        
        print("\nOptions:")
        print("1. View stone economics")
        print("2. View total wealth")
        print("3. Return to main menu")
        
        try:
            choice = int(input("\nChoice: "))
            if choice == 1:
                print("\nSpirit Stone Exchange Rates:")
                print("   🔸 Low-Grade: Base currency")
                print("   🔹 Mid-Grade: 10 Low-Grade stones")
                print("   🔶 High-Grade: 100 Low-Grade stones")
                print("   🔷 Peak-Grade: 1,000 Low-Grade stones")
                print("   🔴 Divine-Grade: 10,000 Low-Grade stones")
                print("\n💡 Higher grade stones are exponentially more valuable!")
            elif choice == 2:
                total_value = self.player.spirit_stones.get_total_value_in_low_grade()
                print(f"\nTotal wealth: {total_value:,} 🔸 equivalent")
                print("Your spiritual wealth determines your cultivation potential!")
        except ValueError:
            pass
        
        self.wait_for_enter()
    
    def cure_effects(self):
        """Enhanced effect curing with spirit stones"""
        self.clear_screen()
        negative_effects = self.player.get_negative_effects()
        
        if not negative_effects:
            print("✨ You have no negative effects to cure with spirit stones!")
            print("💡 Try meditation for free effect curing.")
            self.wait_for_enter()
            return
        
        print("🩹 **EFFECT CURING WITH SPIRIT STONES** 🩹")
        print("💡 Alternative: Use meditation (menu option 3) for free curing!")
        print()
        print(self.player.get_cure_options())
        
        print("\nNegative effects:")
        for i, effect in enumerate(negative_effects, 1):
            duration = f" ({effect['remaining_duration']} sessions)" if effect.get('remaining_duration') else ""
            print(f"{i}. {effect['name']}{duration}")
            if effect.get('description'):
                print(f"   {effect['description']}")
        
        try:
            choice = int(input(f"\nWhich effect to cure? (1-{len(negative_effects)}, 0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(negative_effects):
                effect_name = negative_effects[choice - 1]['name']
                success, message = self.player.cure_effect(effect_name)
                print(f"\n{message}")
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a valid number.")
        
        self.wait_for_enter()
    
    def view_active_effects(self):
        """View all active effects with enhanced details"""
        self.clear_screen()
        print("🔮 **ACTIVE EFFECTS** 🔮")
        
        if not self.player.ongoing_effects:
            print("✨ No active effects.")
        else:
            positive_effects = [e for e in self.player.ongoing_effects if e.get('type') == 'positive']
            negative_effects = [e for e in self.player.ongoing_effects if e.get('type') == 'negative']
            
            if positive_effects:
                print("\n🌟 **Positive Effects:**")
                for effect in positive_effects:
                    duration = f" ({effect['remaining_duration']} sessions)" if effect.get('remaining_duration') else ""
                    print(f"   • {effect['name']}{duration}")
                    if effect.get('description'):
                        print(f"     {effect['description']}")
                    if effect.get('exp_multiplier') and effect['exp_multiplier'] != 1.0:
                        print(f"     💫 Experience modifier: {effect['exp_multiplier']:.1%}")
            
            if negative_effects:
                print("\n🔴 **Negative Effects:**")
                for effect in negative_effects:
                    duration = f" ({effect['remaining_duration']} sessions)" if effect.get('remaining_duration') else ""
                    print(f"   • {effect['name']}{duration}")
                    if effect.get('description'):
                        print(f"     {effect['description']}")
                    if effect.get('exp_multiplier') and effect['exp_multiplier'] != 1.0:
                        print(f"     💫 Experience penalty: {effect['exp_multiplier']:.1%}")
        
        print(f"\n💡 Tip: Use meditation (menu option 3) for free effect curing!")
        self.wait_for_enter()
    
    def view_last_session(self):
        """View enhanced last session details"""
        self.clear_screen()
        print(self.player.get_last_session_summary())
        self.wait_for_enter()
    
    def view_cultivation_history(self):
        """View enhanced cultivation history"""
        self.clear_screen()
        print(self.player.get_cultivation_history())
        self.wait_for_enter()
    
    def select_location(self):
        """Enhanced location selection with compatibility info"""
        self.clear_screen()
        
        available_locations = self.location_manager.get_available_locations(
            self.player.realm.value, self.player.stage
        )
        
        if len(available_locations) == 1:
            print("🌸 You currently only have access to the Peaceful Valley.")
            print("🔓 Advance your cultivation to unlock new locations!")
            
            print(f"\n📋 **Unlock Requirements:**")
            all_locations = [LocationType.PEACEFUL, LocationType.FOREST, 
                           LocationType.MOUNTAIN, LocationType.RUINS]
            for location_type in all_locations:
                if location_type not in available_locations:
                    info = self.location_manager.get_location_info(location_type)
                    print(f"   🔒 {info.name}: {info.unlock_realm}, Level {info.unlock_level}+")
            
            self.wait_for_enter()
            return
        
        while True:
            self.clear_screen()
            menu_text = self.location_manager.display_location_menu(available_locations)
            print(menu_text)
            
            # Show compatibility analysis
            current_location = self.location_manager.get_current_location()
            print("🌟 **Your Compatibility Analysis:**")
            for location_type in available_locations:
                info = self.location_manager.get_location_info(location_type)
                bonuses = self.location_manager.get_cultivation_bonuses(location_type, self.player)
                
                marker = "👈 CURRENT" if location_type == current_location else "  "
                compatibility_score = sum(bonuses.values()) if bonuses else 0
                
                if compatibility_score > 0.15:
                    compatibility = "🟢 Excellent"
                elif compatibility_score > 0.08:
                    compatibility = "🟡 Good"
                elif compatibility_score > 0.03:
                    compatibility = "🟠 Fair"
                else:
                    compatibility = "🔴 Poor"
                
                print(f"{marker} {info.name}: {compatibility}")
                if bonuses:
                    bonus_parts = []
                    for bonus_name, bonus_value in bonuses.items():
                        if bonus_value > 0:
                            bonus_parts.append(f"{bonus_name.replace('_', ' ').title()}+{bonus_value:.1%}")
                    if bonus_parts:
                        print(f"      Active bonuses: {', '.join(bonus_parts)}")
            
            try:
                choice = int(input(f"\nSelect location (1-{len(available_locations) + 1}): "))
                
                if choice == len(available_locations) + 1:
                    return
                elif 1 <= choice <= len(available_locations):
                    selected_location = available_locations[choice - 1]
                    
                    if selected_location != current_location:
                        self.location_manager.set_current_location(selected_location)
                        location_info = self.location_manager.get_location_info(selected_location)
                        print(f"\n✨ You travel to {location_info.name}")
                        print(f"🌿 {location_info.description}")
                        
                        # Show what bonuses will be active
                        bonuses = self.location_manager.get_cultivation_bonuses(selected_location, self.player)
                        if bonuses:
                            print(f"\n🌟 Active cultivation bonuses:")
                            for bonus_name, bonus_value in bonuses.items():
                                if bonus_value > 0:
                                    print(f"   • {bonus_name.replace('_', ' ').title()}: +{bonus_value:.1%}")
                        
                        self.wait_for_enter()
                    else:
                        print("\n📍 You are already at this location.")
                        self.wait_for_enter()
                    return
                else:
                    print("❌ Invalid choice.")
                    self.wait_for_enter()
                    
            except ValueError:
                print("❌ Please enter a valid number.")
                self.wait_for_enter()
    
    def view_character_info(self):
        """Enhanced character information with background integration"""
        self.clear_screen()
        
        print("🎭 **CHARACTER INFORMATION** 🎭")
        print("="*60)
        
        # Basic identity
        cultivation_title = self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)
        print(f"\n📛 **Identity:**")
        print(f"   Name: {self.player.name}")
        print(f"   Cultivation: {cultivation_title}")
        print(f"   Foundation: {self.player.foundation_quality} quality")
        
        # Combat analysis
        combat_power = self.realm_manager.calculate_combat_power(
            self.player.realm, self.player.stage, self.player.foundation_quality
        )
        print(f"   Combat Power: {combat_power:,}")
        
        # Background information
        if hasattr(self.player, 'background'):
            background = self.player.background
            print(f"\n🏮 **Background: {background.name}**")
            print(f"   {background.description}")
            
            print(f"\n💫 **Background Benefits:**")
            for bonus in background.starting_bonuses:
                print(f"   • {bonus.description}")
            
            print(f"\n🌟 **Ongoing Effects:**")
            for effect in background.ongoing_effects:
                print(f"   • {effect.description}")
        
        # Motivation
        if hasattr(self.player, 'motivation'):
            motivation_effects = self.intro_story.get_motivation_effects()
            motivation_info = motivation_effects.get(self.player.motivation, {})
            print(f"\n🎯 **Motivation: {motivation_info.get('name', self.player.motivation.title())}**")
            print(f"   {motivation_info.get('description', 'Your driving force in cultivation.')}")
        
        # Elemental affinities
        if self.player.primary_element:
            print(f"\n🌟 **Elemental Mastery:**")
            primary_value = self.player.elemental_affinities.get(self.player.primary_element, 0)
            print(f"   Primary: {self.player.primary_element.title()} ({primary_value})")
            
            if self.player.secondary_elements:
                secondary_info = []
                for elem in self.player.secondary_elements:
                    value = self.player.elemental_affinities.get(elem, 0)
                    secondary_info.append(f"{elem.title()} ({value})")
                print(f"   Secondary: {', '.join(secondary_info)}")
        else:
            print(f"\n🌟 **Elemental Mastery:** Not yet awakened")
        
        # Location compatibility
        current_location = self.location_manager.get_current_location()
        print(f"\n🌍 **Location Compatibility:**")
        available_locations = self.location_manager.get_available_locations(
            self.player.realm.value, self.player.stage
        )
        
        for location_type in available_locations:
            info = self.location_manager.get_location_info(location_type)
            bonuses = self.location_manager.get_cultivation_bonuses(location_type, self.player)
            marker = "👈 CURRENT" if location_type == current_location else "  "
            
            total_bonus = sum(bonuses.values()) if bonuses else 0
            compatibility = "🟢 Excellent" if total_bonus > 0.15 else "🟡 Good" if total_bonus > 0.08 else "🔴 Limited"
            
            print(f"{marker} {info.name}: {compatibility}")
        
        # Breakthrough status
        if self.player.stage == 9:
            print(f"\n🌟 **Breakthrough Status:**")
            can_breakthrough, msg = self.realm_manager.can_breakthrough_realm(
                self.player.realm, self.player.stage, self.player.foundation_quality
            )
            if can_breakthrough:
                success_rate = self.realm_manager.calculate_breakthrough_success_rate(
                    self.player.realm, self.player.foundation_quality
                )
                print(f"   Ready for breakthrough! Success rate: {success_rate:.1%}")
            else:
                print(f"   {msg}")
        
        print("="*60)
        self.wait_for_enter()
    
    def view_philosophy_elements(self):
        """Enhanced philosophy and elemental view with dao system"""
        self.clear_screen()
        print("🎯 **DAO COMPREHENSION & ELEMENTAL MASTERY** 🎯")
        print("="*70)
        
        # Dao comprehension
        print("\n🧠 **Dao Comprehension:**")
        total_dao = sum(self.player.dao_comprehension.values())
        if total_dao == 0:
            print("   No dao insights yet. Gain comprehension through encounters and cultivation.")
        else:
            sorted_dao = sorted([(k, v) for k, v in self.player.dao_comprehension.items() if v > 0], 
                              key=lambda x: x[1], reverse=True)
            for dao, value in sorted_dao:
                percentage = (value / total_dao) * 100
                mastery_level = "Novice" if value < 10 else "Adept" if value < 25 else "Expert" if value < 50 else "Master"
                print(f"   • {dao.title()}: {value} ({percentage:.1f}%) - {mastery_level}")
        
        # Elemental mastery
        print("\n🌟 **Elemental Mastery:**")
        if not self.player.primary_element:
            print("   Elements not yet awakened. Achieve Foundation Building breakthrough to awaken.")
        else:
            print(f"   Primary Element: {self.player.primary_element.title()}")
            primary_value = self.player.elemental_affinities.get(self.player.primary_element, 0)
            mastery = "Basic" if primary_value < 20 else "Intermediate" if primary_value < 50 else "Advanced" if primary_value < 100 else "Master"
            print(f"      Affinity: {primary_value} ({mastery})")
            
            if self.player.secondary_elements:
                print(f"   Secondary Elements:")
                for elem in self.player.secondary_elements:
                    value = self.player.elemental_affinities.get(elem, 0)
                    mastery = "Basic" if value < 15 else "Intermediate" if value < 35 else "Advanced" if value < 75 else "Master"
                    print(f"      {elem.title()}: {value} ({mastery})")
        
        # Location analysis
        current_location = self.location_manager.get_current_location()
        location_info = self.location_manager.get_location_info(current_location)
        
        print(f"\n🌍 **Location Enhancement Analysis:**")
        print(f"📍 Currently in: {location_info.name}")
        
        # Dao bonuses
        print(f"\n🧠 Dao comprehension bonuses here:")
        for dao_type, bonus in location_info.philosophy_bonuses.items():
            current_value = self.player.dao_comprehension.get(dao_type, 0)
            actual_bonus = bonus * (1 + current_value * 0.1)
            print(f"   • {dao_type.title()}: +{actual_bonus:.1%} cultivation bonus")
        
        # Elemental bonuses
        print(f"\n🌟 Elemental enhancement here:")
        for element in location_info.elemental_affinities:
            current_affinity = self.player.elemental_affinities.get(element, 0)
            if current_affinity > 0:
                bonus = 0.02 * current_affinity
                print(f"   • {element.title()}: +{bonus:.1%} cultivation bonus (ACTIVE)")
            else:
                print(f"   • {element.title()}: Enhanced growth potential")
        
        # All locations overview
        print(f"\n🗺️ **All Locations Analysis:**")
        all_locations = [LocationType.PEACEFUL, LocationType.FOREST, 
                        LocationType.MOUNTAIN, LocationType.RUINS]
        available_locations = self.location_manager.get_available_locations(
            self.player.realm.value, self.player.stage
        )
        
        for location_type in all_locations:
            info = self.location_manager.get_location_info(location_type)
            status = "✅" if location_type in available_locations else "🔒"
            current = "👈" if location_type == current_location else "  "
            
            print(f"{current}{status} {info.name}")
            dao_focus = ", ".join([f"{d.title()}+{b:.0%}" for d, b in info.philosophy_bonuses.items()])
            elem_focus = ", ".join([e.title() for e in info.elemental_affinities])
            print(f"      🧠 Dao: {dao_focus}")
            print(f"      🌟 Elements: {elem_focus}")
        
        # Development recommendations
        print(f"\n💡 **Development Recommendations:**")
        
        # Find weakest dao areas
        weak_dao = [dao for dao, value in self.player.dao_comprehension.items() if value < 5]
        if weak_dao:
            print(f"   • Consider developing: {', '.join([d.title() for d in weak_dao[:3]])}")
        
        # Elemental recommendations
        if not self.player.primary_element:
            print(f"   • Reach Foundation Building to awaken elemental affinity")
        elif len(self.player.secondary_elements) < 2:
            print(f"   • Advance to Core Formation or higher for secondary elements")
        
        # Location recommendations
        bonuses = self.location_manager.get_cultivation_bonuses(current_location, self.player)
        total_bonus = sum(bonuses.values()) if bonuses else 0
        if total_bonus < 0.1:
            print(f"   • Consider changing location for better compatibility")
        
        print("="*70)
        self.wait_for_enter()
    
    def combat_power_analysis(self):
        """Combat power analysis and comparison tool"""
        self.clear_screen()
        print("⚔️ **COMBAT POWER ANALYSIS** ⚔️")
        print("="*60)
        
        # Current combat power
        combat_power = self.realm_manager.calculate_combat_power(
            self.player.realm, self.player.stage, self.player.foundation_quality
        )
        
        print(f"\n🔥 **Your Combat Power: {combat_power:,}**")
        
        # Power breakdown
        realm_info = self.realm_manager.get_realm_info(self.player.realm)
        base_power = realm_info.power_multiplier * 100
        stage_bonus = base_power * (self.player.stage - 1) * 0.2
        foundation_bonus = self.player.foundation_quality * 2
        
        print(f"\n📊 **Power Breakdown:**")
        print(f"   Realm Base: {base_power:,.0f}")
        print(f"   Stage Bonus: {stage_bonus:,.0f}")
        print(f"   Foundation: {foundation_bonus:,.0f}")
        print(f"   Total: {combat_power:,}")
        
        # Comparison with other realms/stages
        print(f"\n⚔️ **Combat Comparisons:**")
        
        # Same realm comparisons
        print(f"\nVs Same Realm ({self.player.realm.value}):")
        for stage in [1, 3, 6, 9]:
            if stage != self.player.stage:
                for foundation in [50, 100, 200]:
                    opponent_power = self.realm_manager.calculate_combat_power(
                        self.player.realm, stage, foundation
                    )
                    comparison = self.realm_manager.compare_combat_power(
                        self.player.realm, self.player.stage, self.player.foundation_quality,
                        self.player.realm, stage, foundation
                    )
                    print(f"   Stage {stage}, Foundation {foundation}: {comparison}")
        
        # Cross-realm comparisons
        print(f"\nVs Other Realms:")
        realm_list = list(CultivationRealm)
        current_index = realm_list.index(self.player.realm)
        
        # Lower realm
        if current_index > 0:
            lower_realm = realm_list[current_index - 1]
            opponent_power = self.realm_manager.calculate_combat_power(lower_realm, 9, 150)
            comparison = self.realm_manager.compare_combat_power(
                self.player.realm, self.player.stage, self.player.foundation_quality,
                lower_realm, 9, 150
            )
            print(f"   Peak {lower_realm.value} (Foundation 150): {comparison}")
        
        # Higher realm
        if current_index < len(realm_list) - 1:
            higher_realm = realm_list[current_index + 1]
            opponent_power = self.realm_manager.calculate_combat_power(higher_realm, 3, 100)
            comparison = self.realm_manager.compare_combat_power(
                self.player.realm, self.player.stage, self.player.foundation_quality,
                higher_realm, 3, 100
            )
            print(f"   Early {higher_realm.value} (Foundation 100): {comparison}")
        
        # Foundation importance demonstration
        print(f"\n🏗️ **Foundation Impact Analysis:**")
        print(f"If you had different foundation qualities:")
        for foundation in [50, 100, 200, 400]:
            if foundation != self.player.foundation_quality:
                alt_power = self.realm_manager.calculate_combat_power(
                    self.player.realm, self.player.stage, foundation
                )
                difference = alt_power - combat_power
                print(f"   Foundation {foundation}: {alt_power:,} ({difference:+,})")
        
        print(f"\n💡 **Analysis:**")
        print(f"   • Foundation contributes {foundation_bonus:,} power ({foundation_bonus/combat_power:.1%} of total)")
        print(f"   • Each foundation point = +2 combat power")
        print(f"   • Stage advancement = +{base_power * 0.2:,.0f} power per stage")
        print(f"   • Realm breakthrough = massive power multiplication")
        
        print("="*60)
        self.wait_for_enter()
    
    def save_game(self):
        """Enhanced save game with new data"""
        print("💾 Saving cultivation progress...")
        
        if self.save_system.save_player(self.player):
            print("✅ Game saved successfully!")
            print(f"📊 Saved: {self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)}")
            print(f"🏗️ Foundation: {self.player.foundation_quality}")
            print(f"🌍 Location: {self.location_manager.get_location_info(self.location_manager.get_current_location()).name}")
        else:
            print("❌ Failed to save game.")
        
        self.wait_for_enter()
    
    def exit_game(self):
        """Enhanced exit with comprehensive statistics"""
        self.clear_screen()
        print("🌸 **CULTIVATION SESSION COMPLETE** 🌸")
        print("="*70)
        
        # Core progression
        cultivation_title = self.realm_manager.get_cultivation_title(self.player.realm, self.player.stage)
        print(f"👤 Cultivator: {self.player.name}")
        print(f"🧘 Final Cultivation: {cultivation_title}")
        print(f"🏗️ Foundation Quality: {self.player.foundation_quality}")
        
        # Combat and spiritual development
        combat_power = self.realm_manager.calculate_combat_power(
            self.player.realm, self.player.stage, self.player.foundation_quality
        )
        print(f"⚔️ Combat Power: {combat_power:,}")
        
        # Spirit stone wealth
        total_value = self.player.spirit_stones.get_total_value_in_low_grade()
        print(f"🔸 Spirit Stone Wealth: {total_value:,} total value")
        
        # Dao and elemental development
        total_dao = sum(self.player.dao_comprehension.values())
        total_elements = sum(self.player.elemental_affinities.values())
        if total_dao > 0:
            print(f"🧠 Dao Comprehension: {total_dao:.1f} total insights")
        if self.player.primary_element:
            print(f"🌟 Primary Element: {self.player.primary_element.title()}")
        
        # Statistics
        print(f"\n📊 **Session Statistics:**")
        print(f"   Encounters: {self.player.total_encounters}")
        print(f"   Effects Cured: {self.player.effects_cured}")
        print(f"   Spirit Stones Earned: {self.player.spirit_stones_earned:,}")
        print(f"   Successful Breakthroughs: {self.player.total_breakthroughs}")
        print(f"   Foundation Sessions: {self.player.foundation_sessions}")
        
        # Location progress
        available_locations = self.location_manager.get_available_locations(
            self.player.realm.value, self.player.stage
        )
        print(f"   Locations Unlocked: {len(available_locations)}/4")
        
        # Background and motivation
        if hasattr(self.player, 'background'):
            print(f"   Background: {self.player.background.name}")
        if hasattr(self.player, 'motivation'):
            print(f"   Motivation: {self.player.motivation.title()}")
        
        print("\n" + "="*70)
        print("🌟 The dao is infinite, your journey eternal.")
        print("🧘 Each session brings you closer to true immortality.")
        print("💫 Return when you are ready to walk the path once more.")
        print("="*70)
        
        # Auto-save before exit
        print("\n💾 Auto-saving progress...")
        if self.save_system.save_player(self.player):
            print("✅ Progress saved successfully.")
        else:
            print("⚠️ Could not save progress.")
        
        self.game_running = False


def main():
    """Entry point for the enhanced cultivation game"""
    try:
        print("🌟 **INITIALIZING ENHANCED CULTIVATION REALM** 🌟")
        print("Loading advanced systems...")
        print("   ⚡ Realm & Stage System")
        print("   🏗️ Foundation Building")
        print("   🎯 Choice Encounters")
        print("   🌍 Location System")
        print("   🧠 Dao Comprehension")
        print("   🌟 Elemental Mastery")
        
        game = EnhancedCultivationGame()
        game.start_game()
        
    except KeyboardInterrupt:
        print("\n\n🌸 Cultivation interrupted by the heavens.")
        print("🧘 Your progress has been preserved. Return when ready!")
    except Exception as e:
        print(f"\n❌ A disturbance in the dao occurred: {e}")
        print("🔧 Please report this to the sect elders if it persists.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()