"""
Spirit Stone System for Cultivation Game
Manages spirit stones as currency for effect resolution and future economy
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
import random

class SpiritStoneGrade(Enum):
    LOW = "Low-Grade"
    MID = "Mid-Grade" 
    HIGH = "High-Grade"
    PEAK = "Peak-Grade"
    DIVINE = "Divine-Grade"

class SpiritStoneManager:
    """Manages spirit stone inventory and transactions"""
    
    # Spirit stone visual representations
    STONE_SYMBOLS = {
        SpiritStoneGrade.LOW: "🔸",
        SpiritStoneGrade.MID: "🔹", 
        SpiritStoneGrade.HIGH: "🔶",
        SpiritStoneGrade.PEAK: "🔷",
        SpiritStoneGrade.DIVINE: "🔴"
    }
    
    # Exchange rates (how many lower grade = 1 higher grade)
    EXCHANGE_RATES = {
        SpiritStoneGrade.LOW: 1,
        SpiritStoneGrade.MID: 10,
        SpiritStoneGrade.HIGH: 100,
        SpiritStoneGrade.PEAK: 1000,
        SpiritStoneGrade.DIVINE: 10000
    }
    
    def __init__(self):
        self.inventory: Dict[SpiritStoneGrade, int] = {
            grade: 0 for grade in SpiritStoneGrade
        }
        # Give starting stones for testing
        self.inventory[SpiritStoneGrade.LOW] = 50
        self.inventory[SpiritStoneGrade.MID] = 15
        self.inventory[SpiritStoneGrade.HIGH] = 3
    
    def add_stones(self, grade: SpiritStoneGrade, amount: int) -> None:
        """Add spirit stones to inventory"""
        self.inventory[grade] += amount
    
    def remove_stones(self, grade: SpiritStoneGrade, amount: int) -> bool:
        """Remove spirit stones if available. Returns True if successful."""
        if self.inventory[grade] >= amount:
            self.inventory[grade] -= amount
            return True
        return False
    
    def get_total_value_in_low_grade(self) -> int:
        """Calculate total wealth in low-grade stone equivalents"""
        total = 0
        for grade, amount in self.inventory.items():
            total += amount * self.EXCHANGE_RATES[grade]
        return total
    
    def can_afford_cost(self, cost: Dict[SpiritStoneGrade, int]) -> bool:
        """Check if player can afford a given cost"""
        # Try exact payment first
        for grade, amount in cost.items():
            if self.inventory[grade] < amount:
                # If can't pay exactly, check if we can convert higher grades
                return self._can_afford_with_conversion(cost)
        return True
    
    def _can_afford_with_conversion(self, cost: Dict[SpiritStoneGrade, int]) -> bool:
        """Check if cost can be paid with grade conversion"""
        total_cost = 0
        for grade, amount in cost.items():
            total_cost += amount * self.EXCHANGE_RATES[grade]
        
        return self.get_total_value_in_low_grade() >= total_cost
    
    def pay_cost(self, cost: Dict[SpiritStoneGrade, int]) -> bool:
        """Pay a cost, using grade conversion if needed"""
        if not self.can_afford_cost(cost):
            return False
        
        # Try to pay exactly first
        temp_inventory = self.inventory.copy()
        exact_payment = True
        
        for grade, amount in cost.items():
            if temp_inventory[grade] >= amount:
                temp_inventory[grade] -= amount
            else:
                exact_payment = False
                break
        
        if exact_payment:
            self.inventory = temp_inventory
            return True
        
        # Need to use conversion
        return self._pay_with_conversion(cost)
    
    def _pay_with_conversion(self, cost: Dict[SpiritStoneGrade, int]) -> bool:
        """Pay cost using grade conversion"""
        total_cost = 0
        for grade, amount in cost.items():
            total_cost += amount * self.EXCHANGE_RATES[grade]
        
        # Convert from highest to lowest grade
        remaining_cost = total_cost
        grades = list(reversed(list(SpiritStoneGrade)))
        
        for grade in grades:
            if remaining_cost <= 0:
                break
                
            stones_available = self.inventory[grade]
            stone_value = self.EXCHANGE_RATES[grade]
            
            if stones_available > 0 and remaining_cost > 0:
                stones_to_use = min(stones_available, (remaining_cost + stone_value - 1) // stone_value)
                self.inventory[grade] -= stones_to_use
                remaining_cost -= stones_to_use * stone_value
        
        return remaining_cost <= 0
    
    def get_display_string(self) -> str:
        """Get formatted display of spirit stone inventory"""
        display_parts = []
        for grade in SpiritStoneGrade:
            if self.inventory[grade] > 0:
                symbol = self.STONE_SYMBOLS[grade]
                display_parts.append(f"{symbol} {self.inventory[grade]}")
        
        if not display_parts:
            return "No spirit stones"
        
        return " | ".join(display_parts)
    
    def get_wealth_summary(self) -> str:
        """Get wealth summary with total value"""
        total_value = self.get_total_value_in_low_grade()
        return f"{self.get_display_string()} (Total: {total_value:,} 🔸 equivalent)"


class EffectResolutionSystem:
    """Handles curing negative effects using spirit stones"""
    
    def __init__(self, spirit_stone_manager: SpiritStoneManager):
        self.spirit_stones = spirit_stone_manager
        
        # Define cure costs for different effect types and severities
        self.cure_costs = {
            # Bottleneck effects
            "Qi Stagnation": {SpiritStoneGrade.LOW: 15, SpiritStoneGrade.MID: 2},
            "Meridian Blockage": {SpiritStoneGrade.LOW: 25, SpiritStoneGrade.MID: 3},
            "Foundation Cracks": {SpiritStoneGrade.MID: 5, SpiritStoneGrade.HIGH: 1},
            "Cultivation Deviation": {SpiritStoneGrade.MID: 8, SpiritStoneGrade.HIGH: 2},
            "Heart Demon": {SpiritStoneGrade.HIGH: 3, SpiritStoneGrade.PEAK: 1},
            
            # Anomaly effects
            "Chaotic Qi": {SpiritStoneGrade.LOW: 20, SpiritStoneGrade.MID: 2},
            "Elemental Imbalance": {SpiritStoneGrade.MID: 4, SpiritStoneGrade.HIGH: 1},
            "Spiritual Corruption": {SpiritStoneGrade.HIGH: 2, SpiritStoneGrade.PEAK: 1},
            "Dao Confusion": {SpiritStoneGrade.HIGH: 4, SpiritStoneGrade.PEAK: 2},
            "Void Taint": {SpiritStoneGrade.PEAK: 2, SpiritStoneGrade.DIVINE: 1},
            
            # Technique effects
            "Technique Backlash": {SpiritStoneGrade.LOW: 10, SpiritStoneGrade.MID: 1},
            "Elemental Rejection": {SpiritStoneGrade.MID: 3, SpiritStoneGrade.HIGH: 1},
            "Cultivation Instability": {SpiritStoneGrade.MID: 6, SpiritStoneGrade.HIGH: 2},
        }
    
    def get_cure_cost(self, effect_name: str) -> Optional[Dict[SpiritStoneGrade, int]]:
        """Get the spirit stone cost to cure an effect"""
        return self.cure_costs.get(effect_name)
    
    def format_cost(self, cost: Dict[SpiritStoneGrade, int]) -> str:
        """Format cost display"""
        cost_parts = []
        for grade, amount in cost.items():
            if amount > 0:
                symbol = self.spirit_stones.STONE_SYMBOLS[grade]
                cost_parts.append(f"{symbol} {amount}")
        return " + ".join(cost_parts)
    
    def can_cure_effect(self, effect_name: str) -> bool:
        """Check if player can afford to cure an effect"""
        cost = self.get_cure_cost(effect_name)
        if not cost:
            return False
        return self.spirit_stones.can_afford_cost(cost)
    
    def cure_effect(self, effect_name: str) -> bool:
        """Attempt to cure an effect, returns True if successful"""
        cost = self.get_cure_cost(effect_name)
        if not cost:
            return False
        
        if self.spirit_stones.pay_cost(cost):
            return True
        return False
    
    def get_curable_effects(self, effects: List[Dict]) -> List[Dict]:
        """Get list of effects that can be cured with current stones"""
        curable = []
        for effect in effects:
            if effect.get('type') == 'negative' and self.can_cure_effect(effect['name']):
                curable.append(effect)
        return curable
    
    def get_cure_options_display(self, effects: List[Dict]) -> str:
        """Get formatted display of cure options"""
        negative_effects = [e for e in effects if e.get('type') == 'negative']
        
        if not negative_effects:
            return "No negative effects to cure."
        
        lines = ["Available cures:"]
        for i, effect in enumerate(negative_effects, 1):
            cost = self.get_cure_cost(effect['name'])
            if cost:
                cost_str = self.format_cost(cost)
                affordable = "✓" if self.can_cure_effect(effect['name']) else "✗"
                lines.append(f"{i}. {effect['name']}: {cost_str} {affordable}")
            else:
                lines.append(f"{i}. {effect['name']}: Cannot be cured with spirit stones")
        
        return "\n".join(lines)


def generate_spirit_stone_reward(player_realm: str) -> Dict[SpiritStoneGrade, int]:
    """Generate spirit stone rewards based on player realm"""
    rewards = {}
    
    # Base rewards scale with realm
    realm_multipliers = {
        "Qi Gathering": 1.0,
        "Foundation Building": 1.5,
        "Core Formation": 2.0,
        "Nascent Soul": 3.0,
        "Soul Transformation": 4.0,
    }
    
    multiplier = realm_multipliers.get(player_realm, 1.0)
    
    # Random rewards with realm scaling
    if random.random() < 0.7:  # 70% chance for low grade
        rewards[SpiritStoneGrade.LOW] = random.randint(1, int(10 * multiplier))
    
    if random.random() < 0.4:  # 40% chance for mid grade
        rewards[SpiritStoneGrade.MID] = random.randint(1, int(3 * multiplier))
    
    if random.random() < 0.2:  # 20% chance for high grade
        rewards[SpiritStoneGrade.HIGH] = random.randint(1, max(1, int(1 * multiplier)))
    
    if random.random() < 0.05:  # 5% chance for peak grade
        rewards[SpiritStoneGrade.PEAK] = 1
    
    if random.random() < 0.01 and multiplier >= 2.0:  # 1% chance for divine (higher realms only)
        rewards[SpiritStoneGrade.DIVINE] = 1
    
    return rewards


def format_spirit_stone_reward(reward: Dict[SpiritStoneGrade, int]) -> str:
    """Format spirit stone reward for display"""
    if not reward:
        return "No spirit stones"
    
    parts = []
    for grade, amount in reward.items():
        if amount > 0:
            symbol = SpiritStoneManager.STONE_SYMBOLS[grade]
            parts.append(f"{symbol} {amount}")
    
    return " + ".join(parts)


# Example usage and testing
if __name__ == "__main__":
    # Initialize system
    stone_manager = SpiritStoneManager()
    cure_system = EffectResolutionSystem(stone_manager)
    
    print("=== Spirit Stone System Demo ===")
    print(f"Starting inventory: {stone_manager.get_wealth_summary()}")
    
    # Test curing effects
    test_effects = [
        {"name": "Qi Stagnation", "type": "negative", "description": "Cultivation speed reduced by 15%"},
        {"name": "Meridian Blockage", "type": "negative", "description": "Cultivation efficiency reduced by 20%"},
        {"name": "Enlightenment", "type": "positive", "description": "Cultivation speed increased by 25%"}
    ]
    
    print("\n=== Effect Resolution Demo ===")
    print(cure_system.get_cure_options_display(test_effects))
    
    # Test curing Qi Stagnation
    effect_to_cure = "Qi Stagnation"
    cost = cure_system.get_cure_cost(effect_to_cure)
    print(f"\nAttempting to cure {effect_to_cure}...")
    print(f"Cost: {cure_system.format_cost(cost)}")
    
    if cure_system.cure_effect(effect_to_cure):
        print("✓ Effect cured successfully!")
        print(f"Remaining inventory: {stone_manager.get_wealth_summary()}")
    else:
        print("✗ Cannot afford to cure this effect")
    
    # Test reward generation
    print("\n=== Reward Generation Demo ===")
    for realm in ["Qi Gathering", "Foundation Building", "Core Formation"]:
        reward = generate_spirit_stone_reward(realm)
        print(f"{realm}: {format_spirit_stone_reward(reward)}")