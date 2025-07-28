"""
Enhanced Player class with authentic cultivation realm system
Integrates with existing spirit stone and encounter systems
"""

from typing import Dict, List, Optional, Tuple
import random
from cultivation_encounters import SmartEncounterManager, generate_encounter_reward
from spirit_stones import SpiritStoneManager, EffectResolutionSystem, generate_spirit_stone_reward, format_spirit_stone_reward
from realm_stage_system import RealmStageManager, CultivationRealm, convert_old_level_to_realm_stage

class EnhancedPlayer:
    def __init__(self, name: str = "Cultivator"):
        self.name = name
        
        # New realm/stage system
        self.realm = CultivationRealm.BODY_TEMPERING
        self.stage = 1
        self.experience = 0
        self.realm_manager = RealmStageManager()
        
        # Enhanced foundation system
        self.foundation_quality = 10  # Start with basic foundation
        self.foundation_stability = 100  # Affects breakthrough success
        
        # Philosophy and Elements (converted to Dao system)
        self.dao_comprehension = {
            "sword": 0,
            "fire": 0,
            "water": 0,
            "earth": 0,
            "wind": 0,
            "lightning": 0,
            "ice": 0,
            "nature": 0,
            "light": 0,
            "shadow": 0,
            "balance": 0,
            "destruction": 0
        }
        
        # Elemental affinities (awakened during breakthrough)
        self.elemental_affinities = {
            "fire": 0,
            "water": 0,
            "earth": 0,
            "air": 0,
            "lightning": 0,
            "ice": 0,
            "nature": 0,
            "light": 0,
            "shadow": 0
        }
        self.primary_element = None  # Awakened at Foundation Building
        self.secondary_elements = []  # Additional elements gained later
        
        # Encounter and Effect Systems (existing)
        self.encounter_manager = SmartEncounterManager()
        self.ongoing_effects = []
        
        # Spirit Stone System (existing)
        self.spirit_stones = SpiritStoneManager()
        self.effect_resolution = EffectResolutionSystem(self.spirit_stones)
        
        # Cultivation choices and progression
        self.cultivation_method = "balanced"  # balanced, aggressive, stable
        self.breakthrough_failures = 0
        self.recovery_time = 0  # Sessions before next breakthrough attempt
        
        # Tracking (existing)
        self.total_encounters = 0
        self.effects_cured = 0
        self.spirit_stones_earned = 0
        self.total_breakthroughs = 0
        self.foundation_sessions = 0
        
        # Cultivation History (existing)
        self.cultivation_history = []
        self.last_session_details = None
    
    def get_current_stage_exp_requirement(self) -> int:
        """Get experience requirement for current stage"""
        return self.realm_manager.get_stage_exp_requirement(self.realm, self.stage)
    
    def get_next_stage_exp_requirement(self) -> int:
        """Get experience requirement for next stage"""
        if self.stage < 9:
            return self.realm_manager.get_stage_exp_requirement(self.realm, self.stage + 1)
        return 0
    
    def add_experience(self, amount: int) -> Tuple[bool, List[str]]:
        """Add experience and handle stage ups. Returns (advanced, messages)"""
        self.experience += amount
        messages = []
        advanced = False
        
        # Check for stage advancement
        while self.stage < 9:
            required_exp = self.get_current_stage_exp_requirement()
            if self.experience >= required_exp:
                self.experience -= required_exp
                self.stage += 1
                advanced = True
                
                # Foundation bonus for key stages
                foundation_bonus = self.realm_manager.get_foundation_stage_bonus(self.stage)
                if foundation_bonus > 0:
                    self.foundation_quality += foundation_bonus
                    messages.append(f"🏗️ Foundation strengthened! +{foundation_bonus} foundation quality")
                
                messages.append(f"📈 Advanced to {self.realm_manager.get_cultivation_title(self.realm, self.stage)}")
                
                # Check if ready for realm breakthrough
                if self.stage == 9:
                    can_breakthrough, breakthrough_msg = self.realm_manager.can_breakthrough_realm(
                        self.realm, self.stage, self.foundation_quality
                    )
                    if can_breakthrough:
                        messages.append(f"🌟 Ready for breakthrough to next realm!")
                    else:
                        messages.append(f"⚠️ {breakthrough_msg}")
            else:
                break
        
        return advanced, messages
    
    def attempt_realm_breakthrough(self) -> Tuple[bool, str, Dict]:
        """Attempt to breakthrough to next realm"""
        if self.recovery_time > 0:
            return False, f"Still recovering from last attempt. Wait {self.recovery_time} more sessions.", {}
        
        can_attempt, reason = self.realm_manager.can_breakthrough_realm(
            self.realm, self.stage, self.foundation_quality
        )
        
        if not can_attempt:
            return False, reason, {}
        
        # Calculate bonus factors
        bonus_factors = {}
        
        # Dao comprehension bonuses
        total_dao = sum(self.dao_comprehension.values())
        if total_dao > 20:
            bonus_factors['dao_mastery'] = min(0.15, total_dao * 0.002)
        
        # Foundation stability bonus
        if self.foundation_stability > 80:
            bonus_factors['foundation_stability'] = (self.foundation_stability - 80) * 0.001
        
        # Attempt breakthrough
        success, message, result_data = self.realm_manager.attempt_breakthrough(
            self.realm, self.foundation_quality, bonus_factors
        )
        
        if success:
            # Successful breakthrough
            old_realm = self.realm
            self.realm = result_data['new_realm']
            self.stage = 1
            self.experience = 0
            self.total_breakthroughs += 1
            
            # Foundation bonus from breakthrough
            foundation_bonus = result_data.get('foundation_bonus', 0)
            self.foundation_quality += foundation_bonus
            
            # Elemental awakening
            elemental_message = self.realm_manager.get_elemental_awakening_message(self.realm)
            if elemental_message:
                self._trigger_elemental_awakening()
                message += f"\n{elemental_message}"
            
            # Clear some negative effects on breakthrough
            self._clear_breakthrough_effects()
            
        else:
            # Failed breakthrough
            self.breakthrough_failures += 1
            
            # Apply penalties
            foundation_damage = result_data.get('foundation_damage', 0)
            exp_loss_percent = result_data.get('exp_loss_percent', 0)
            recovery_time = result_data.get('recovery_time', 0)
            
            self.foundation_quality = max(10, self.foundation_quality - foundation_damage)
            exp_loss = int(self.experience * exp_loss_percent / 100)
            self.experience = max(0, self.experience - exp_loss)
            self.recovery_time = recovery_time
            
            # Add qi deviation effect
            qi_deviation = {
                'name': 'Qi Deviation',
                'type': 'negative',
                'description': 'Failed breakthrough caused qi instability',
                'exp_multiplier': 0.7,
                'remaining_duration': recovery_time
            }
            self.ongoing_effects.append(qi_deviation)
        
        return success, message, result_data
    
    def _trigger_elemental_awakening(self):
        """Trigger elemental awakening on appropriate breakthroughs"""
        if self.realm == CultivationRealm.FOUNDATION_BUILDING and not self.primary_element:
            # First elemental awakening - random primary element
            elements = list(self.elemental_affinities.keys())
            self.primary_element = random.choice(elements)
            self.elemental_affinities[self.primary_element] = random.randint(15, 30)
            
        elif self.realm in [CultivationRealm.CORE_FORMATION, CultivationRealm.NASCENT_SOUL]:
            # Chance for secondary element or strengthen existing
            if random.random() < 0.6:  # 60% chance
                if len(self.secondary_elements) < 2:
                    # Gain new secondary element
                    available = [e for e in self.elemental_affinities.keys() 
                               if e != self.primary_element and e not in self.secondary_elements]
                    if available:
                        new_element = random.choice(available)
                        self.secondary_elements.append(new_element)
                        self.elemental_affinities[new_element] = random.randint(8, 20)
                else:
                    # Strengthen existing elements
                    if self.primary_element:
                        self.elemental_affinities[self.primary_element] += random.randint(5, 15)
                    for elem in self.secondary_elements:
                        if random.random() < 0.5:
                            self.elemental_affinities[elem] += random.randint(3, 10)
    
    def _clear_breakthrough_effects(self):
        """Clear some negative effects on successful breakthrough"""
        negative_effects = [e for e in self.ongoing_effects if e.get('type') == 'negative']
        effects_to_remove = min(2, len(negative_effects))  # Remove up to 2 negative effects
        
        for _ in range(effects_to_remove):
            if negative_effects:
                effect_to_remove = random.choice(negative_effects)
                self.ongoing_effects.remove(effect_to_remove)
                negative_effects.remove(effect_to_remove)
    
    def cultivate_with_choice(self, cultivation_focus: str = "balanced") -> List[str]:
        """Enhanced cultivation with player choice"""
        messages = []
        session_details = {
            "base_exp": 0,
            "final_exp": 0,
            "encounter": None,
            "spirit_stones": {},
            "level_ups": [],
            "effects_before": len(self.ongoing_effects),
            "effects_after": 0,
            "cultivation_focus": cultivation_focus,
            "foundation_gained": 0,
            "elemental_gains": {},
            "dao_gains": {}
        }
        
        # Reduce recovery time
        if self.recovery_time > 0:
            self.recovery_time -= 1
        
        # Apply cultivation focus
        if cultivation_focus == "foundation":
            base_exp = random.randint(3, 8)  # Lower exp
            foundation_gain = random.randint(3, 8)  # Higher foundation
            self.foundation_quality += foundation_gain
            self.foundation_sessions += 1
            session_details["foundation_gained"] = foundation_gain
            messages.append(f"🏗️ Foundation-focused cultivation: +{foundation_gain} foundation quality")
            
        elif cultivation_focus == "aggressive":
            base_exp = random.randint(12, 20)  # Higher exp
            foundation_risk = random.random()
            if foundation_risk < 0.3:  # 30% chance of foundation damage
                foundation_loss = random.randint(1, 3)
                self.foundation_quality = max(10, self.foundation_quality - foundation_loss)
                messages.append(f"⚠️ Aggressive cultivation damaged foundation: -{foundation_loss}")
            
        else:  # balanced
            base_exp = random.randint(8, 15)
            if random.random() < 0.2:  # 20% chance for foundation gain
                foundation_gain = random.randint(1, 3)
                self.foundation_quality += foundation_gain
                session_details["foundation_gained"] = foundation_gain
        
        session_details["base_exp"] = base_exp
        
        # Apply ongoing effects
        modified_exp = self._apply_ongoing_effects(base_exp)
        session_details["final_exp"] = modified_exp
        
        # Process encounter
        encounter_result = self.encounter_manager.process_encounter(
            self.realm.value, self.stage, self.ongoing_effects
        )
        
        if encounter_result:
            self.total_encounters += 1
            encounter_type, encounter_data = encounter_result
            
            session_details["encounter"] = {
                "type": encounter_type,
                "name": encounter_data["name"],
                "description": encounter_data.get("description", ""),
                "rarity": encounter_data.get("rarity", "common")
            }
            
            # Process encounter rewards
            rewards = generate_encounter_reward(encounter_type, encounter_data, self.realm.value)
            
            # Apply rewards with enhanced messaging
            for reward_type, reward_value in rewards.items():
                if reward_type == "experience":
                    modified_exp += reward_value
                    session_details["final_exp"] = modified_exp
                elif reward_type == "philosophy":
                    # Convert philosophy to dao comprehension
                    for phil_type, phil_value in reward_value.items():
                        if phil_type in self.dao_comprehension:
                            self.dao_comprehension[phil_type] += phil_value
                            session_details["dao_gains"][phil_type] = phil_value
                            messages.append(f"🧠 Dao insight: +{phil_value} {phil_type} comprehension")
                elif reward_type == "foundation":
                    self.foundation_quality += reward_value
                    session_details["foundation_gained"] += reward_value
                    messages.append(f"🏗️ Foundation strengthened: +{reward_value}")
                elif reward_type == "elemental":
                    for elem_type, elem_value in reward_value.items():
                        if elem_type in self.elemental_affinities:
                            self.elemental_affinities[elem_type] += elem_value
                            session_details["elemental_gains"][elem_type] = elem_value
                            messages.append(f"🌟 Elemental affinity: +{elem_value} {elem_type}")
                elif reward_type == "ongoing_effect":
                    self.ongoing_effects.append(reward_value)
            
            # Generate spirit stone rewards for encounters
            spirit_reward = generate_spirit_stone_reward(self.realm.value)
            if spirit_reward:
                session_details["spirit_stones"] = spirit_reward
                for grade, amount in spirit_reward.items():
                    self.spirit_stones.add_stones(grade, amount)
                    self.spirit_stones_earned += amount
                
                messages.append(f"🔸 Spirit stones earned: {format_spirit_stone_reward(spirit_reward)}")
            
            # Add encounter message
            messages.append(f"💫 {encounter_type.title()}: {encounter_data['name']}")
            if encounter_data.get('description'):
                messages.append(f"   {encounter_data['description']}")
        
        # Add experience and handle stage advancement
        advanced, advancement_messages = self.add_experience(modified_exp)
        session_details["level_ups"] = advancement_messages
        messages.extend(advancement_messages)
        
        # Base cultivation message
        messages.insert(0, f"Cultivated for {modified_exp} experience ({cultivation_focus} focus)")
        
        # Natural effect recovery
        self._process_natural_recovery()
        
        # Clean up expired effects
        self._cleanup_expired_effects()
        session_details["effects_after"] = len(self.ongoing_effects)
        
        # Store session details
        self.last_session_details = session_details
        self.cultivation_history.append(session_details)
        if len(self.cultivation_history) > 10:
            self.cultivation_history.pop(0)
        
        return messages
    
    def _process_natural_recovery(self):
        """Process natural recovery from negative effects"""
        negative_effects = [e for e in self.ongoing_effects if e.get('type') == 'negative']
        
        for effect in negative_effects[:]:  # Copy list to avoid modification during iteration
            # Foundation quality affects recovery rate
            recovery_chance = 0.10 + (self.foundation_quality / 1000)  # Base 10% + foundation bonus
            
            # Higher realm cultivators recover faster
            realm_bonus = list(CultivationRealm).index(self.realm) * 0.02
            recovery_chance += realm_bonus
            
            if random.random() < recovery_chance:
                self.ongoing_effects.remove(effect)
                # Note: We don't add a message here to avoid spam, but it happens silently
    
    def meditate_for_recovery(self) -> Tuple[bool, str]:
        """Dedicated meditation to cure negative effects (no spirit stone cost)"""
        negative_effects = [e for e in self.ongoing_effects if e.get('type') == 'negative']
        
        if not negative_effects:
            return False, "✨ You have no negative effects to cleanse through meditation."
        
        # Meditation success rate based on foundation and dao comprehension
        base_rate = 0.6 + (self.foundation_quality / 500)  # 60% base + foundation bonus
        dao_bonus = min(0.2, sum(self.dao_comprehension.values()) / 500)  # Up to 20% from dao
        
        success_rate = min(0.9, base_rate + dao_bonus)
        
        if random.random() < success_rate:
            # Successfully cure 1-2 effects
            effects_to_cure = min(2, len(negative_effects))
            cured_effects = []
            
            for _ in range(effects_to_cure):
                if negative_effects:
                    effect = random.choice(negative_effects)
                    self.ongoing_effects.remove(effect)
                    negative_effects.remove(effect)
                    cured_effects.append(effect['name'])
            
            return True, f"🧘 Meditation successful! Cleansed: {', '.join(cured_effects)}"
        else:
            return False, f"🧘 Meditation helped but couldn't fully cleanse the effects. Try again later."
    
    def _apply_ongoing_effects(self, base_exp: int) -> int:
        """Apply ongoing effects to cultivation (existing functionality)"""
        modified_exp = base_exp
        
        for effect in self.ongoing_effects:
            if effect['type'] == 'positive':
                if 'exp_multiplier' in effect:
                    modified_exp = int(modified_exp * effect['exp_multiplier'])
                elif 'exp_bonus' in effect:
                    modified_exp += effect['exp_bonus']
            elif effect['type'] == 'negative':
                if 'exp_multiplier' in effect:
                    modified_exp = int(modified_exp * effect['exp_multiplier'])
                elif 'exp_penalty' in effect:
                    modified_exp = max(1, modified_exp - effect['exp_penalty'])
        
        return modified_exp
    
    def _cleanup_expired_effects(self) -> None:
        """Remove expired effects (existing functionality)"""
        active_effects = []
        for effect in self.ongoing_effects:
            remaining = effect.get('remaining_duration')
            if remaining is None:
                active_effects.append(effect)
            elif remaining > 0:
                effect['remaining_duration'] = remaining - 1
                active_effects.append(effect)
        
        self.ongoing_effects = active_effects
    
    def get_negative_effects(self) -> List[Dict]:
        """Get list of negative effects that can be cured (existing functionality)"""
        return [e for e in self.ongoing_effects if e.get('type') == 'negative']
    
    def cure_effect(self, effect_name: str) -> Tuple[bool, str]:
        """Attempt to cure a negative effect using spirit stones (existing functionality)"""
        effect_to_cure = None
        effect_index = -1
        
        for i, effect in enumerate(self.ongoing_effects):
            if effect['name'] == effect_name and effect.get('type') == 'negative':
                effect_to_cure = effect
                effect_index = i
                break
        
        if not effect_to_cure:
            return False, "Effect not found or not negative"
        
        if not self.effect_resolution.can_cure_effect(effect_name):
            cost = self.effect_resolution.get_cure_cost(effect_name)
            if cost:
                cost_str = self.effect_resolution.format_cost(cost)
                return False, f"Cannot afford cure. Cost: {cost_str}"
            else:
                return False, "This effect cannot be cured with spirit stones"
        
        if self.effect_resolution.cure_effect(effect_name):
            self.ongoing_effects.pop(effect_index)
            self.effects_cured += 1
            return True, f"✓ {effect_name} cured successfully!"
        else:
            return False, "Failed to cure effect"
    
    def get_cultivation_choices(self) -> List[Tuple[str, str]]:
        """Get available cultivation focus choices"""
        choices = [
            ("balanced", "⚖️ Balanced Cultivation - Normal progress with occasional foundation gain"),
            ("aggressive", "🔥 Aggressive Cultivation - Higher experience but risk foundation damage"),
            ("foundation", "🏗️ Foundation Building - Lower experience but guaranteed foundation gain")
        ]
        
        return choices
    
    def get_status(self) -> str:
        """Get comprehensive player status with new realm system"""
        status_lines = [
            f"=== {self.name} ===",
            f"Cultivation: {self.realm_manager.get_cultivation_title(self.realm, self.stage)}",
            f"Experience: {self.experience}/{self.get_current_stage_exp_requirement()}",
            f"Foundation Quality: {self.foundation_quality}",
            ""
        ]
        
        # Combat power
        combat_power = self.realm_manager.calculate_combat_power(self.realm, self.stage, self.foundation_quality)
        status_lines.append(f"Combat Power: {combat_power:,}")
        
        # Spirit stones
        status_lines.append(f"Spirit Stones: {self.spirit_stones.get_display_string()}")
        status_lines.append(f"Total Value: {self.spirit_stones.get_total_value_in_low_grade():,} 🔸 equivalent")
        status_lines.append("")
        
        # Elemental affinities
        if self.primary_element:
            primary_value = self.elemental_affinities.get(self.primary_element, 0)
            status_lines.append(f"Primary Element: {self.primary_element.title()} ({primary_value})")
            
            if self.secondary_elements:
                secondary_str = ", ".join([f"{e.title()} ({self.elemental_affinities.get(e, 0)})" 
                                         for e in self.secondary_elements])
                status_lines.append(f"Secondary Elements: {secondary_str}")
        else:
            status_lines.append("Elements: Not yet awakened")
        status_lines.append("")
        
        # Dao comprehension
        if any(v > 0 for v in self.dao_comprehension.values()):
            dao_parts = [f"{k}: {v}" for k, v in self.dao_comprehension.items() if v > 0]
            status_lines.append(f"Dao Comprehension: {' | '.join(dao_parts)}")
        
        # Ongoing Effects
        if self.ongoing_effects:
            status_lines.append("\nOngoing Effects:")
            for effect in self.ongoing_effects:
                effect_type = "+" if effect.get('type') == 'positive' else "-"
                duration = f" ({effect['remaining_duration']} turns)" if effect.get('remaining_duration') else ""
                status_lines.append(f"  {effect_type} {effect['name']}{duration}")
                if effect.get('description'):
                    status_lines.append(f"    {effect['description']}")
        
        # Breakthrough status
        if self.stage == 9:
            can_breakthrough, msg = self.realm_manager.can_breakthrough_realm(
                self.realm, self.stage, self.foundation_quality
            )
            if can_breakthrough:
                success_rate = self.realm_manager.calculate_breakthrough_success_rate(
                    self.realm, self.foundation_quality
                )
                status_lines.append(f"\n🌟 Ready for breakthrough! Success rate: {success_rate:.1%}")
            else:
                status_lines.append(f"\n⚠️ {msg}")
        elif self.recovery_time > 0:
            status_lines.append(f"\n🩹 Recovering from failed breakthrough ({self.recovery_time} sessions remaining)")
        
        # Statistics
        status_lines.extend([
            "",
            f"Total Encounters: {self.total_encounters}",
            f"Effects Cured: {self.effects_cured}",
            f"Spirit Stones Earned: {self.spirit_stones_earned:,}",
            f"Successful Breakthroughs: {self.total_breakthroughs}",
            f"Foundation Sessions: {self.foundation_sessions}"
        ])
        
        return "\n".join(status_lines)
    
    def get_cure_options(self) -> str:
        """Get formatted display of cure options (existing functionality)"""
        return self.effect_resolution.get_cure_options_display(self.ongoing_effects)
    
    def get_spirit_stone_display(self) -> str:
        """Get formatted display of spirit stone wealth (existing functionality)"""
        return self.spirit_stones.get_wealth_summary()
    
    def get_last_session_summary(self) -> str:
        """Get detailed summary of the last cultivation session"""
        if not self.last_session_details:
            return "No cultivation session recorded yet."
        
        details = self.last_session_details
        lines = []
        
        lines.append("=== Last Cultivation Session ===")
        lines.append(f"Cultivation Focus: {details['cultivation_focus'].title()}")
        lines.append(f"Base Experience: {details['base_exp']}")
        lines.append(f"Final Experience: {details['final_exp']}")
        
        if details["foundation_gained"] > 0:
            lines.append(f"Foundation Gained: +{details['foundation_gained']}")
        
        if details["dao_gains"]:
            dao_text = ", ".join([f"{k}+{v}" for k, v in details["dao_gains"].items()])
            lines.append(f"Dao Insights: {dao_text}")
        
        if details["elemental_gains"]:
            elem_text = ", ".join([f"{k}+{v}" for k, v in details["elemental_gains"].items()])
            lines.append(f"Elemental Growth: {elem_text}")
        
        if details["encounter"]:
            enc = details["encounter"]
            lines.append(f"\n💫 Encounter: {enc['type'].title()}")
            lines.append(f"   Name: {enc['name']}")
            lines.append(f"   Rarity: {enc['rarity'].title()}")
            if enc["description"]:
                lines.append(f"   Description: {enc['description']}")
        
        if details["spirit_stones"]:
            stones_earned = format_spirit_stone_reward(details["spirit_stones"])
            lines.append(f"\n🔸 Spirit Stones Earned: {stones_earned}")
        
        if details["level_ups"]:
            lines.append(f"\n🆙 Advancement:")
            for level_msg in details["level_ups"]:
                lines.append(f"   • {level_msg}")
        
        effect_change = details["effects_after"] - details["effects_before"]
        if effect_change != 0:
            if effect_change > 0:
                lines.append(f"\n🔮 +{effect_change} new effect(s) gained")
            else:
                lines.append(f"\n✨ {abs(effect_change)} effect(s) expired/cured")
        
        return "\n".join(lines)
    
    def get_cultivation_history(self) -> str:
        """Get history of recent cultivation sessions"""
        if not self.cultivation_history:
            return "No cultivation history available."
        
        lines = []
        lines.append("=== Recent Cultivation History ===")
        
        for i, session in enumerate(reversed(self.cultivation_history[-5:]), 1):
            lines.append(f"\nSession {i} ago:")
            lines.append(f"  Focus: {session['cultivation_focus'].title()}")
            lines.append(f"  Experience: {session['final_exp']} XP")
            
            if session["foundation_gained"] > 0:
                lines.append(f"  Foundation: +{session['foundation_gained']}")
            
            if session["encounter"]:
                enc = session["encounter"]
                lines.append(f"  Encounter: {enc['name']} ({enc['type']})")
            
            if session["spirit_stones"]:
                stones = format_spirit_stone_reward(session["spirit_stones"])
                lines.append(f"  Stones: {stones}")
            
            if session["level_ups"]:
                lines.append(f"  Advancement: {len(session['level_ups'])} changes")
        
        return "\n".join(lines)
    
    # Compatibility methods for existing save system
    def to_save_data(self) -> Dict:
        """Convert to save format compatible with existing save system"""
        return {
            'name': self.name,
            'realm': self.realm.value,
            'stage': self.stage,
            'experience': self.experience,
            'foundation_quality': self.foundation_quality,
            'foundation_stability': self.foundation_stability,
            'dao_comprehension': self.dao_comprehension,
            'elemental_affinities': self.elemental_affinities,
            'primary_element': self.primary_element,
            'secondary_elements': self.secondary_elements,
            'ongoing_effects': self.ongoing_effects,
            'spirit_stones': {grade.value: amount for grade, amount in self.spirit_stones.inventory.items()},
            'cultivation_method': self.cultivation_method,
            'breakthrough_failures': self.breakthrough_failures,
            'recovery_time': self.recovery_time,
            'total_encounters': self.total_encounters,
            'effects_cured': self.effects_cured,
            'spirit_stones_earned': self.spirit_stones_earned,
            'total_breakthroughs': self.total_breakthroughs,
            'foundation_sessions': self.foundation_sessions,
            'cultivation_history': self.cultivation_history,
            'last_session_details': self.last_session_details
        }
    
    @classmethod
    def from_save_data(cls, save_data: Dict):
        """Create player from save data"""
        player = cls(save_data['name'])
        
        # Load realm/stage data
        try:
            player.realm = CultivationRealm(save_data.get('realm', 'Body Tempering'))
        except ValueError:
            player.realm = CultivationRealm.BODY_TEMPERING
        
        player.stage = save_data.get('stage', 1)
        player.experience = save_data.get('experience', 0)
        player.foundation_quality = save_data.get('foundation_quality', 10)
        player.foundation_stability = save_data.get('foundation_stability', 100)
        
        # Load dao and elemental data
        player.dao_comprehension = save_data.get('dao_comprehension', player.dao_comprehension)
        player.elemental_affinities = save_data.get('elemental_affinities', player.elemental_affinities)
        player.primary_element = save_data.get('primary_element', None)
        player.secondary_elements = save_data.get('secondary_elements', [])
        
        # Load effects and other data
        player.ongoing_effects = save_data.get('ongoing_effects', [])
        player.cultivation_method = save_data.get('cultivation_method', 'balanced')
        player.breakthrough_failures = save_data.get('breakthrough_failures', 0)
        player.recovery_time = save_data.get('recovery_time', 0)
        
        # Load statistics
        player.total_encounters = save_data.get('total_encounters', 0)
        player.effects_cured = save_data.get('effects_cured', 0)
        player.spirit_stones_earned = save_data.get('spirit_stones_earned', 0)
        player.total_breakthroughs = save_data.get('total_breakthroughs', 0)
        player.foundation_sessions = save_data.get('foundation_sessions', 0)
        
        # Load history
        player.cultivation_history = save_data.get('cultivation_history', [])
        player.last_session_details = save_data.get('last_session_details', None)
        
        # Load spirit stones
        if 'spirit_stones' in save_data:
            from spirit_stones import SpiritStoneGrade
            for grade_name, amount in save_data['spirit_stones'].items():
                try:
                    grade = SpiritStoneGrade(grade_name)
                    player.spirit_stones.inventory[grade] = amount
                except ValueError:
                    continue
        
        return player


# Example usage and migration helper
def migrate_old_player_to_enhanced(old_player) -> EnhancedPlayer:
    """Migrate existing player to enhanced system"""
    enhanced = EnhancedPlayer(old_player.name)
    
    # Convert old level/realm to new system
    if hasattr(old_player, 'level'):
        realm, stage = convert_old_level_to_realm_stage(old_player.level)
        enhanced.realm = realm
        enhanced.stage = stage
    
    # Transfer existing data
    if hasattr(old_player, 'foundation_quality'):
        enhanced.foundation_quality = old_player.foundation_quality
    
    if hasattr(old_player, 'philosophy'):
        for phil_type, value in old_player.philosophy.items():
            if phil_type in enhanced.dao_comprehension:
                enhanced.dao_comprehension[phil_type] = value
    
    if hasattr(old_player, 'elemental_affinities'):
        enhanced.elemental_affinities = old_player.elemental_affinities.copy()
        # Set primary element to highest affinity
        if enhanced.elemental_affinities:
            primary = max(enhanced.elemental_affinities.items(), key=lambda x: x[1])
            if primary[1] > 0:
                enhanced.primary_element = primary[0]
    
    if hasattr(old_player, 'ongoing_effects'):
        enhanced.ongoing_effects = old_player.ongoing_effects.copy()
    
    if hasattr(old_player, 'spirit_stones'):
        enhanced.spirit_stones = old_player.spirit_stones
    
    # Transfer statistics
    for attr in ['total_encounters', 'effects_cured', 'spirit_stones_earned']:
        if hasattr(old_player, attr):
            setattr(enhanced, attr, getattr(old_player, attr))
    
    return enhanced


if __name__ == "__main__":
    # Test the enhanced player system
    player = EnhancedPlayer("Test Cultivator")
    
    print("=== Enhanced Player System Test ===")
    print(player.get_status())
    
    # Test cultivation with different focuses
    print("\n=== Cultivation Test ===")
    for focus in ["balanced", "foundation", "aggressive"]:
        print(f"\n--- {focus.title()} Cultivation ---")
        messages = player.cultivate_with_choice(focus)
        for msg in messages:
            print(msg)
    
    print("\n=== Final Status ===")
    print(player.get_status())