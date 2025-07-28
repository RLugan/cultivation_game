"""
Realm and Stage System for Cultivation Game
Implements authentic cultivation progression with stages 1-9 per realm
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import random

class CultivationRealm(Enum):
    BODY_TEMPERING = "Body Tempering"
    QI_GATHERING = "Qi Gathering"
    FOUNDATION_BUILDING = "Foundation Building"
    CORE_FORMATION = "Core Formation"
    NASCENT_SOUL = "Nascent Soul"
    SOUL_TRANSFORMATION = "Soul Transformation"
    VOID_REFINEMENT = "Void Refinement"
    BODY_INTEGRATION = "Body Integration"
    MAHAYANA = "Mahayana"
    HEAVENLY_IMMORTAL = "Heavenly Immortal"

@dataclass
class RealmInfo:
    name: str
    description: str
    stage_exp_base: int  # Base experience for stage 1
    stage_exp_multiplier: float  # Multiplier for each subsequent stage
    breakthrough_difficulty: float  # Difficulty of realm breakthrough
    lifespan_years: int
    power_multiplier: float  # Combat power multiplier for this realm
    foundation_requirement: int  # Minimum foundation quality for breakthrough

class RealmStageManager:
    """Manages cultivation realm and stage progression"""
    
    def __init__(self):
        self.realms = self._initialize_realms()
        self.realm_order = list(CultivationRealm)
    
    def _initialize_realms(self) -> Dict[CultivationRealm, RealmInfo]:
        return {
            CultivationRealm.BODY_TEMPERING: RealmInfo(
                name="Body Tempering",
                description="Strengthening the mortal body to handle spiritual energy",
                stage_exp_base=50,
                stage_exp_multiplier=1.2,
                breakthrough_difficulty=0.8,
                lifespan_years=100,
                power_multiplier=1.0,
                foundation_requirement=20
            ),
            
            CultivationRealm.QI_GATHERING: RealmInfo(
                name="Qi Gathering",
                description="Learning to sense and gather spiritual energy",
                stage_exp_base=80,
                stage_exp_multiplier=1.25,
                breakthrough_difficulty=1.0,
                lifespan_years=150,
                power_multiplier=2.0,
                foundation_requirement=40
            ),
            
            CultivationRealm.FOUNDATION_BUILDING: RealmInfo(
                name="Foundation Building",
                description="Building a solid foundation for future cultivation",
                stage_exp_base=120,
                stage_exp_multiplier=1.3,
                breakthrough_difficulty=1.2,
                lifespan_years=300,
                power_multiplier=5.0,
                foundation_requirement=80
            ),
            
            CultivationRealm.CORE_FORMATION: RealmInfo(
                name="Core Formation",
                description="Forming a spiritual core to contain vast amounts of qi",
                stage_exp_base=200,
                stage_exp_multiplier=1.4,
                breakthrough_difficulty=1.5,
                lifespan_years=500,
                power_multiplier=12.0,
                foundation_requirement=150
            ),
            
            CultivationRealm.NASCENT_SOUL: RealmInfo(
                name="Nascent Soul",
                description="Birth of the spiritual infant, beginning of true immortality",
                stage_exp_base=350,
                stage_exp_multiplier=1.5,
                breakthrough_difficulty=2.0,
                lifespan_years=1000,
                power_multiplier=30.0,
                foundation_requirement=250
            ),
            
            CultivationRealm.SOUL_TRANSFORMATION: RealmInfo(
                name="Soul Transformation",
                description="Transforming the nascent soul into true spiritual form",
                stage_exp_base=600,
                stage_exp_multiplier=1.6,
                breakthrough_difficulty=2.5,
                lifespan_years=2000,
                power_multiplier=75.0,
                foundation_requirement=400
            ),
            
            CultivationRealm.VOID_REFINEMENT: RealmInfo(
                name="Void Refinement",
                description="Refining the soul through understanding of the void",
                stage_exp_base=1000,
                stage_exp_multiplier=1.7,
                breakthrough_difficulty=3.0,
                lifespan_years=5000,
                power_multiplier=180.0,
                foundation_requirement=600
            ),
            
            CultivationRealm.BODY_INTEGRATION: RealmInfo(
                name="Body Integration",
                description="Integrating body and soul into perfect unity",
                stage_exp_base=1800,
                stage_exp_multiplier=1.8,
                breakthrough_difficulty=4.0,
                lifespan_years=10000,
                power_multiplier=400.0,
                foundation_requirement=900
            ),
            
            CultivationRealm.MAHAYANA: RealmInfo(
                name="Mahayana",
                description="The great vehicle towards true enlightenment",
                stage_exp_base=3000,
                stage_exp_multiplier=2.0,
                breakthrough_difficulty=5.0,
                lifespan_years=25000,
                power_multiplier=1000.0,
                foundation_requirement=1400
            ),
            
            CultivationRealm.HEAVENLY_IMMORTAL: RealmInfo(
                name="Heavenly Immortal",
                description="Transcendence beyond mortal comprehension",
                stage_exp_base=5000,
                stage_exp_multiplier=2.2,
                breakthrough_difficulty=7.0,
                lifespan_years=100000,
                power_multiplier=2500.0,
                foundation_requirement=2000
            )
        }
    
    def get_realm_info(self, realm: CultivationRealm) -> RealmInfo:
        """Get information about a cultivation realm"""
        return self.realms[realm]
    
    def get_stage_exp_requirement(self, realm: CultivationRealm, stage: int) -> int:
        """Get experience requirement for a specific stage"""
        if stage < 1 or stage > 9:
            return 0
        
        realm_info = self.realms[realm]
        base_exp = realm_info.stage_exp_base
        multiplier = realm_info.stage_exp_multiplier
        
        # Each stage requires more exp than the last
        return int(base_exp * (multiplier ** (stage - 1)))
    
    def get_next_realm(self, current_realm: CultivationRealm) -> Optional[CultivationRealm]:
        """Get the next realm in progression"""
        try:
            current_index = self.realm_order.index(current_realm)
            if current_index + 1 < len(self.realm_order):
                return self.realm_order[current_index + 1]
            return None
        except ValueError:
            return None
    
    def can_breakthrough_realm(self, realm: CultivationRealm, stage: int, foundation_quality: int) -> Tuple[bool, str]:
        """Check if player can attempt realm breakthrough"""
        if stage != 9:
            return False, f"Must reach Stage 9 before attempting breakthrough (currently Stage {stage})"
        
        realm_info = self.realms[realm]
        if foundation_quality < realm_info.foundation_requirement:
            needed = realm_info.foundation_requirement - foundation_quality
            return False, f"Foundation too weak! Need {needed} more foundation quality"
        
        return True, "Ready for breakthrough attempt"
    
    def calculate_breakthrough_success_rate(self, realm: CultivationRealm, foundation_quality: int, 
                                         bonus_factors: Dict[str, float] = None) -> float:
        """Calculate success rate for realm breakthrough"""
        realm_info = self.realms[realm]
        
        # Base success rate depends on foundation quality vs requirement
        foundation_ratio = foundation_quality / realm_info.foundation_requirement
        base_rate = min(0.95, 0.3 + (foundation_ratio - 1.0) * 0.4)  # 30% minimum, up to 95%
        
        # Apply difficulty modifier
        difficulty_penalty = (realm_info.breakthrough_difficulty - 1.0) * 0.1
        final_rate = max(0.05, base_rate - difficulty_penalty)
        
        # Apply bonus factors (pills, techniques, etc.)
        if bonus_factors:
            for factor_name, factor_value in bonus_factors.items():
                final_rate += factor_value
        
        return min(0.95, max(0.05, final_rate))
    
    def attempt_breakthrough(self, realm: CultivationRealm, foundation_quality: int, 
                           bonus_factors: Dict[str, float] = None) -> Tuple[bool, str, Dict[str, any]]:
        """Attempt realm breakthrough"""
        success_rate = self.calculate_breakthrough_success_rate(realm, foundation_quality, bonus_factors)
        
        success = random.random() < success_rate
        result_data = {
            'success_rate': success_rate,
            'foundation_used': foundation_quality,
            'realm_attempted': realm.value
        }
        
        if success:
            next_realm = self.get_next_realm(realm)
            if next_realm:
                message = f"🌟 Breakthrough Success! Advanced from {realm.value} to {next_realm.value}!"
                result_data['new_realm'] = next_realm
                result_data['foundation_bonus'] = random.randint(5, 15)  # Breakthrough strengthens foundation
                return True, message, result_data
            else:
                return False, "Already at the pinnacle of cultivation!", result_data
        else:
            # Breakthrough failure
            foundation_damage = random.randint(2, 8)
            exp_loss_percent = random.randint(10, 30)
            
            message = f"💥 Breakthrough Failed! Lost {foundation_damage} foundation quality and {exp_loss_percent}% experience."
            result_data['foundation_damage'] = foundation_damage
            result_data['exp_loss_percent'] = exp_loss_percent
            result_data['recovery_time'] = random.randint(3, 7)  # Sessions before next attempt
            
            return False, message, result_data
    
    def get_cultivation_title(self, realm: CultivationRealm, stage: int) -> str:
        """Get full cultivation title"""
        stage_names = {
            1: "Initial", 2: "Early", 3: "Mid", 4: "Late", 5: "Peak Early",
            6: "Peak Mid", 7: "Peak Late", 8: "Half-Step", 9: "Peak"
        }
        
        stage_name = stage_names.get(stage, f"Stage {stage}")
        return f"{stage_name} {realm.value}"
    
    def calculate_combat_power(self, realm: CultivationRealm, stage: int, foundation_quality: int) -> int:
        """Calculate relative combat power"""
        realm_info = self.realms[realm]
        
        # Base power from realm
        base_power = realm_info.power_multiplier * 100
        
        # Stage bonus (each stage adds 20% to base power)
        stage_bonus = base_power * (stage - 1) * 0.2
        
        # Foundation bonus (significant impact)
        foundation_bonus = foundation_quality * 2
        
        total_power = int(base_power + stage_bonus + foundation_bonus)
        return total_power
    
    def compare_combat_power(self, player_realm: CultivationRealm, player_stage: int, player_foundation: int,
                           opponent_realm: CultivationRealm, opponent_stage: int, opponent_foundation: int) -> str:
        """Compare combat power between cultivators"""
        player_power = self.calculate_combat_power(player_realm, player_stage, player_foundation)
        opponent_power = self.calculate_combat_power(opponent_realm, opponent_stage, opponent_foundation)
        
        power_ratio = player_power / opponent_power
        
        if power_ratio >= 2.0:
            return "Overwhelming advantage - you could defeat them with ease"
        elif power_ratio >= 1.5:
            return "Significant advantage - you would likely win"
        elif power_ratio >= 1.2:
            return "Moderate advantage - you have the upper hand"
        elif power_ratio >= 0.9:
            return "Evenly matched - outcome uncertain"
        elif power_ratio >= 0.7:
            return "Slight disadvantage - they have the advantage"
        elif power_ratio >= 0.5:
            return "Significant disadvantage - you would likely lose"
        else:
            return "Overwhelming disadvantage - you would be defeated easily"
    
    def get_elemental_awakening_message(self, realm: CultivationRealm) -> Optional[str]:
        """Get elemental awakening message for breakthrough"""
        if realm == CultivationRealm.FOUNDATION_BUILDING:
            return "🌟 Foundation Building breakthrough awakens your elemental affinity!"
        elif realm == CultivationRealm.CORE_FORMATION:
            return "⚡ Core Formation allows deeper elemental understanding!"
        elif realm == CultivationRealm.NASCENT_SOUL:
            return "🔥 Nascent Soul birth resonates with elemental forces!"
        return None
    
    def get_foundation_stage_bonus(self, stage: int) -> float:
        """Get foundation building bonus for reaching certain stages"""
        # Stages 3, 6, 9 provide foundation bonuses
        if stage in [3, 6, 9]:
            return stage * 2.0  # +6, +12, +18 foundation at key stages
        return 0.0
    
    def display_realm_progress(self, realm: CultivationRealm, stage: int, current_exp: int) -> str:
        """Display current cultivation progress"""
        required_exp = self.get_stage_exp_requirement(realm, stage)
        next_stage_exp = self.get_stage_exp_requirement(realm, stage + 1) if stage < 9 else 0
        
        progress_text = f"🧘 {self.get_cultivation_title(realm, stage)}\n"
        progress_text += f"📊 Progress: {current_exp}/{required_exp} experience\n"
        
        if stage < 9:
            progress_text += f"🎯 Next Stage: {next_stage_exp} experience required\n"
        else:
            next_realm = self.get_next_realm(realm)
            if next_realm:
                progress_text += f"🌟 Ready for breakthrough to {next_realm.value}\n"
            else:
                progress_text += f"👑 Peak of cultivation achieved!\n"
        
        return progress_text


# Helper functions for integration with existing player system
def convert_old_level_to_realm_stage(old_level: int) -> Tuple[CultivationRealm, int]:
    """Convert old level system to new realm/stage system"""
    realm_mapping = [
        (10, CultivationRealm.BODY_TEMPERING),
        (20, CultivationRealm.QI_GATHERING),
        (35, CultivationRealm.FOUNDATION_BUILDING),
        (55, CultivationRealm.CORE_FORMATION),
        (80, CultivationRealm.NASCENT_SOUL),
        (110, CultivationRealm.SOUL_TRANSFORMATION),
        (150, CultivationRealm.VOID_REFINEMENT),
        (200, CultivationRealm.BODY_INTEGRATION),
        (300, CultivationRealm.MAHAYANA),
        (999, CultivationRealm.HEAVENLY_IMMORTAL)
    ]
    
    for level_cap, realm in realm_mapping:
        if old_level <= level_cap:
            # Calculate stage within realm
            prev_cap = 0 if realm == CultivationRealm.BODY_TEMPERING else realm_mapping[realm_mapping.index((level_cap, realm)) - 1][0]
            level_in_realm = old_level - prev_cap
            stage = min(9, max(1, (level_in_realm * 9) // (level_cap - prev_cap) + 1))
            return realm, stage
    
    return CultivationRealm.HEAVENLY_IMMORTAL, 9


# Example usage
if __name__ == "__main__":
    # Test the realm system
    realm_manager = RealmStageManager()
    
    print("=== Realm Stage System Test ===")
    
    # Test stage experience requirements
    qi_gathering = CultivationRealm.QI_GATHERING
    for stage in range(1, 10):
        exp_req = realm_manager.get_stage_exp_requirement(qi_gathering, stage)
        print(f"Qi Gathering Stage {stage}: {exp_req} experience required")
    
    # Test breakthrough
    print(f"\n=== Breakthrough Test ===")
    can_breakthrough, message = realm_manager.can_breakthrough_realm(qi_gathering, 9, 50)
    print(f"Can breakthrough: {can_breakthrough} - {message}")
    
    # Test combat power
    print(f"\n=== Combat Power Test ===")
    player_power = realm_manager.calculate_combat_power(CultivationRealm.FOUNDATION_BUILDING, 5, 100)
    opponent_power = realm_manager.calculate_combat_power(CultivationRealm.QI_GATHERING, 9, 80)
    print(f"Player power: {player_power}")
    print(f"Opponent power: {opponent_power}")
    
    comparison = realm_manager.compare_combat_power(
        CultivationRealm.FOUNDATION_BUILDING, 5, 100,
        CultivationRealm.QI_GATHERING, 9, 80
    )
    print(f"Combat comparison: {comparison}")