import random
import time
import os

class Entity:
    """Base class for all living creatures."""
    def __init__(self, name, health, attack, defense, mp=0, magic=0, crit=0, dodge=0):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack
        self.defense_power = defense
        
        self.max_mp = mp
        self.mp = mp
        self.magic = magic
        self.crit_chance = crit       
        self.dodge_chance = dodge     
        
        self.poison_duration = 0
        self.shield = 0

    def is_alive(self):
        return self.health > 0

    def check_dodge(self):
        return random.random() < self.dodge_chance

    def take_damage(self, incoming_damage):
        if self.check_dodge():
            print(f"💨 {self.name} dodged the attack!")
            return 0
            
        actual_damage = max(1, incoming_damage - self.defense_power)
        
        if self.shield > 0:
            if actual_damage <= self.shield:
                self.shield -= actual_damage
                print(f"🛡️ {self.name}'s Barrier absorbed ALL damage! (Barrier left: {self.shield})")
                return 0
            else:
                actual_damage -= self.shield
                print(f"🛡️ {self.name}'s Barrier broke! Absorbed {self.shield} damage.")
                self.shield = 0
        
        self.health = max(0, self.health - actual_damage)
        print(f"💥 {self.name} took {actual_damage} damage! (HP: {self.health}/{self.max_health})")
        return actual_damage

    def process_poison(self):
        if self.poison_duration > 0 and self.is_alive():
            poison_damage = max(2, int(self.max_health * 0.10))
            self.health = max(0, self.health - poison_damage)
            self.poison_duration -= 1
            print(f"🤢 {self.name} suffers from poison! -{poison_damage} HP. (Turns left: {self.poison_duration})")


class Player(Entity):
    def __init__(self, name, job_class):
        self.level = 1
        self.xp = 0
        self.xp_needed = 50
        self.score = 0  
        self.floor_xp_earned = 0  
        
        self.inventory = {
            "Small Health Potion": 2,
            "Medium Health Potion": 0,
            "Big Health Potion": 0,
            "Small Mana Potion": 1,
            "Medium Mana Potion": 0,
            "Big Mana Potion": 0,
            "Poison Coating": 1
        }
        
        self.is_hidden = False

        job_lower = job_class.lower()
        if job_lower == "warrior":
            self.job_class = "Warrior"
            self.gold = 30
            super().__init__(name, health=120, attack=20, defense=10, mp=120, magic=0, crit=0.05, dodge=0.01)
            self.growth = {"hp": 150, "mp": 40, "atk": 35, "def": 25, "mag": 0, "crit": 0.01, "dodge": 0.002}
        elif job_lower == "mage":
            self.job_class = "Mage"
            self.gold = 80
            super().__init__(name, health=80, attack=5, defense=-5, mp=500, magic=50, crit=0.0, dodge=0.0001)
            self.growth = {"hp": 80, "mp": 150, "atk": 5, "def": 15, "mag": 70, "crit": 0.0, "dodge": 0.0000}
        else:
            self.job_class = "Rogue"
            self.gold = 50
            super().__init__(name, health=100, attack=30, defense=5, mp=100, magic=0, crit=0.20, dodge=0.10)
            self.growth = {"hp": 110, "mp": 30, "atk": 45, "def": 18, "mag": 0, "crit": 0.02, "dodge": 0.01}

    def display_stats(self, current_floor, multiplier):
        print("\n📊 ==================== HERO STATS ====================")
        print(f"   Name: {self.name} the {self.job_class} | Level: {self.level}")
        print(f"   HP: {self.health}/{self.max_health} | MP: {self.mp}/{self.max_mp}")
        print(f"   ATK: {self.attack_power} | DEF: {self.defense_power} | MAGIC: {self.magic}")
        print(f"   CRIT: {self.crit_chance * 100:.1f}% | DODGE: {self.dodge_chance * 100:.2f}%")
        print(f"   Gold: {self.gold} | XP: {self.xp}/{self.xp_needed} | TOTAL SCORE: {self.score}")
        print(f"   Current Floor: {current_floor} | Reward Multiplier: {multiplier:.2f}x")
        print("======================================================")
        input("Press Enter to close stats...")

    def use_item_menu(self):
        owned_items = {item: count for item, count in self.inventory.items() if count > 0}
        if not owned_items:
            print("\n🎒 Your inventory is completely empty!")
            time.sleep(0.5)
            return False

        print("\n🎒 --- INVENTORY ---")
        items_list = list(owned_items.keys())
        for idx, item in enumerate(items_list, start=1):
            print(f"({idx}) {item}: {owned_items[item]}x")
        print("(0) Back to Skills")
        
        choice = input("Select an item to use:\n> ")
        if choice == "0" or not choice.isdigit():
            return False
            
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(items_list):
            item_name = items_list[choice_idx]
                
            if "Health Potion" in item_name:
                if "Small" in item_name: heal = int(self.max_health * 0.25)
                elif "Medium" in item_name: heal = int(self.max_health * 0.60)
                elif "Big" in item_name: heal = int(self.max_health * 0.85)
                self.health = min(self.max_health, self.health + heal)
                self.inventory[item_name] -= 1
                print(f"🧪 Restored {heal} HP! (HP: {self.health}/{self.max_health})")
                return True
            elif "Mana Potion" in item_name:
                if "Small" in item_name: mana = int(self.max_mp * 0.20)
                elif "Medium" in item_name: mana = int(self.max_mp * 0.45)
                elif "Big" in item_name: mana = int(self.max_mp * 0.80)
                self.mp = min(self.max_mp, self.mp + mana)
                self.inventory[item_name] -= 1
                print(f"🔮 Restored {mana} MP! (MP: {self.mp}/{self.max_mp})")
                return True
            elif item_name == "Poison Coating":
                self.inventory[item_name] -= 1
                print("🧪 Weapon coated in poison!")
                return "apply_poison"
        return False

    def gain_xp(self, amount):
        self.xp += amount
        self.floor_xp_earned += amount  
        print(f"✨ Gained {amount} XP! ({self.xp}/{self.xp_needed})")
        while self.xp >= self.xp_needed:  
            self.level += 1
            self.xp -= self.xp_needed
            self.xp_needed = int(self.xp_needed * 1.5)
            
            self.max_health += self.growth["hp"]
            self.health = self.max_health  
            self.max_mp += self.growth["mp"]
            self.mp = self.max_mp
            
            self.attack_power += self.growth["atk"]
            self.defense_power += self.growth["def"]
            self.magic += self.growth["mag"]
            self.crit_chance += self.growth["crit"]
            self.dodge_chance += self.growth["dodge"]
            print(f"🎉 LEVEL UP! You reached Level {self.level} and fully recovered!")


class Enemy(Entity):
    def __init__(self, name, data, floor, reward_multiplier, is_boss=False):
        floor_multiplier = (3.50) ** (floor - 1)
        boss_multiplier = 1.5 if is_boss else 1.0
        final_mult = floor_multiplier * boss_multiplier

        super().__init__(
            name=f"[BOSS] {name}" if is_boss else name, 
            health=max(10, int(data["hp"] * final_mult)), 
            attack=max(2, int(data["atk"] * final_mult)), 
            defense=max(0, int(data["def"] * final_mult))
        )
        self.is_boss = is_boss
        self.boss_type = name if is_boss else None
        self.xp_reward = int(data["xp"] * floor_multiplier * reward_multiplier)
        self.gold_reward = int(data["gold"] * floor_multiplier * reward_multiplier)


# Databases
MONSTER_DATABASE = {
    "Green Slime": {"hp": 30, "atk": 8, "def": 2, "xp": 15, "gold": 10},
    "Goblin Scout": {"hp": 45, "atk": 11, "def": 4, "xp": 20, "gold": 15},
    "Orc Warrior": {"hp": 70, "atk": 15, "def": 6, "xp": 35, "gold": 25},
    "Cave Troll": {"hp": 120, "atk": 22, "def": 8, "xp": 60, "gold": 50},
    "Vampire Bat": {"hp": 50, "atk": 13, "def": 3, "xp": 22, "gold": 18},
    "Feral Wolf": {"hp": 55, "atk": 14, "def": 2, "xp": 24, "gold": 14},
    "Skeleton Knight": {"hp": 85, "atk": 17, "def": 9, "xp": 40, "gold": 30},
    "Basilisk Fledgling": {"hp": 110, "atk": 20, "def": 7, "xp": 55, "gold": 45},
    "Shadow Specter": {"hp": 65, "atk": 24, "def": 1, "xp": 45, "gold": 35},
    "Stone Golem": {"hp": 150, "atk": 18, "def": 15, "xp": 70, "gold": 40}
}

BOSS_DATABASE = ["Corrupted Dragon", "Arch-Lich", "Demon Lord", "Gargoyle King"]


def battle_loop(player, enemy, floor, mult):
    print(f"\n⚔️ A {enemy.name} blocks your path!")
    poison_weapon_active = False
    
    while player.is_alive() and enemy.is_alive():
        time.sleep(0.1)
        player.process_poison()
        enemy.process_poison()
        
        if not enemy.is_alive() or not player.is_alive():
            break

        print(f"\n--- {player.name}'s Turn ---")
        print(f"HP: {player.health}/{player.max_health} | MP: {player.mp}/{player.max_mp} | Barrier: {player.shield}")
        print(f"Enemy HP: {enemy.health}/{enemy.max_health}")
        
        if player.job_class == "Warrior":
            print("(1) Simple Attack | (2) Big Attack | (3) Holy Strike")
        elif player.job_class == "Mage":
            print("(1) Simple Attack | (2) Fireball | (3) Mana Blast | (4) Barrier")
        elif player.job_class == "Rogue":
            print("(1) Simple Attack | (2) Poison Strike | (3) Hide in Shadow")
            
        print("(0) Items/Potions | (S) Check Stats")
        action = input("> ").lower()

        if action == "s":
            player.display_stats(floor, mult)
            continue

        turn_taken = False
        base_dmg = player.attack_power if player.job_class != "Mage" else player.magic
        current_crit = player.crit_chance
        final_dmg = 0
        inflict_poison_rounds = 0

        if action == "0":
            item_result = player.use_item_menu()
            if item_result == "apply_poison":
                poison_weapon_active = True
                turn_taken = True
            elif item_result:
                turn_taken = True
            continue

        if player.job_class == "Warrior":
            if action == "1": final_dmg = base_dmg; turn_taken = True
            elif action == "2" and player.mp >= 40:
                player.mp -= 40; final_dmg = int(base_dmg * 1.5); current_crit += 0.15; turn_taken = True
            elif action == "3" and player.mp >= 100:
                player.mp -= 100; final_dmg = int(base_dmg * 2.5); current_crit += 0.20; turn_taken = True
            else: print("❌ Choice missing or not enough MP!")

        elif player.job_class == "Mage":
            if action == "1": final_dmg = player.attack_power; turn_taken = True
            elif action == "2" and player.mp >= 30:
                player.mp -= 30; final_dmg = int(player.magic * 1.5); turn_taken = True
            elif action == "3" and player.mp >= 80:
                player.mp -= 80; final_dmg = int(player.magic * 2.0); turn_taken = True
            elif action == "4" and player.mp >= 40:
                player.mp -= 40
                shield_gain = int(player.magic * 1.5)
                player.shield += shield_gain
                print(f"🛡️ Barrier cast! Gained {shield_gain} Shield.")
                turn_taken = True
            else: print("❌ Choice missing or not enough MP!")

        elif player.job_class == "Rogue":
            if action == "1": final_dmg = base_dmg; turn_taken = True
            elif action == "2" and player.mp >= 25:
                player.mp -= 25; final_dmg = int(base_dmg * 1.1); inflict_poison_rounds = 5; turn_taken = True
            elif action == "3" and player.mp >= 40:
                player.mp -= 40; player.dodge_chance += 0.50; player.is_hidden = True; turn_taken = True
            else: print("❌ Choice missing or not enough MP!")

        if turn_taken and final_dmg > 0:
            final_dmg += random.randint(-2, 2)
            if random.random() < current_crit:
                final_dmg = int(final_dmg * 1.5)
                print("🎯 CRITICAL HIT!")
            enemy.take_damage(final_dmg)
            
            if poison_weapon_active or inflict_poison_rounds > 0:
                enemy.poison_duration = max(enemy.poison_duration, 5)
                print(f"🧪 {enemy.name} has been poisoned for 5 rounds!")
                poison_weapon_active = False

        if turn_taken and enemy.is_alive():
            time.sleep(0.1)
            print(f"\n--- {enemy.name}'s Turn ---")
            
            if enemy.is_boss and random.random() < 0.50:
                if enemy.boss_type == "Corrupted Dragon":
                    print("🔥 [BOSS SKILL] Corrupted Dragon breathed catastrophic fire!")
                    dragon_fire = int(enemy.attack_power * 1.6)
                    player.take_damage(dragon_fire)
                elif enemy.boss_type == "Arch-Lich":
                    print("🔮 [BOSS SKILL] Arch-Lich casts Mana Drain!")
                    drain_amt = int(player.max_mp * 0.25)
                    player.mp = max(0, player.mp - drain_amt)
                    player.take_damage(int(enemy.attack_power * 1.2))
                elif enemy.boss_type == "Demon Lord":
                    print("🤢 [BOSS SKILL] Demon Lord slashes with a Toxic Blade!")
                    player.poison_duration = max(player.poison_duration, 3)
                    player.take_damage(enemy.attack_power)
                elif enemy.boss_type == "Gargoyle King":
                    print("🧱 [BOSS SKILL] Gargoyle King slams down hard, bypassing armor!")
                    garg_dmg = int(enemy.attack_power * 1.3)
                    orig_def = player.defense_power
                    player.defense_power = int(player.defense_power / 2)
                    player.take_damage(garg_dmg)
                    player.defense_power = orig_def
            else:
                enemy_damage = enemy.attack_power + random.randint(-2, 2)
                player.take_damage(enemy_damage)
            
            if player.job_class == "Rogue" and player.is_hidden:
                player.dodge_chance -= 0.50
                player.is_hidden = False

    if player.is_alive():
        print(f"\n🎉 Victory! Defeated {enemy.name}! Loot received: +{enemy.gold_reward} Gold!")
        player.gold += enemy.gold_reward
        player.gain_xp(enemy.xp_reward)
        player.shield = 0
        return True
    return False


def handle_highscore(final_score):
    """--- HIGHSCORE FILE SYSTEM ---"""
    filename = "highscore.txt"
    current_best = 0
    
    # Ha létezik a fájl, beolvassuk a rekordot
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                content = file.read().strip()
                if content.isdigit():
                    current_best = int(content)
        except:
            pass

    print(f"\n🏆 Current High Score record: {current_best} points.")
    
    # Ha megdőlt a rekord, felülírjuk a fájlt
    if final_score > current_best:
        print(f"✨ NEW RECORD! You beat the old high score! ✨")
        try:
            with open(filename, "w") as file:
                file.write(str(final_score))
            print(f"💾 Saved new record to {filename}!")
        except Exception as e:
            print("❌ Failed to write to file.")
    else:
        print("Keep training to break the record!")


# --- Main Loop Engine ---
if __name__ == "__main__":
    print("🔮 Welcome to the Ultimate Hardcore Floor RPG! 🔮")
    name = input("Enter your hero's name: ")
    job = input("Choose a class (Warrior, Mage, Rogue): ")
    
    hero = Player(name, job)
    print(f"\nCharacter created! Welcome, {hero.name} the {hero.job_class}!")

    current_floor = 1
    fight_counter = 1
    current_reward_multiplier = 1.0  

    while hero.is_alive():
        is_boss_fight = (fight_counter % 5 == 0)
        
        print(f"\n================ FLOOR {current_floor} (Fight {fight_counter}/5) ================")
        if is_boss_fight:
            print("🚨 WARNING: A FLOOR BOSS approaches! 🚨")
        input("Press Enter to move forward...")

        if is_boss_fight:
            boss_name = random.choice(BOSS_DATABASE)
            boss_base = {"hp": 180, "atk": 25, "def": 10, "xp": 100, "gold": 80}
            enemy = Enemy(boss_name, boss_base, current_floor, current_reward_multiplier, is_boss=True)
        else:
            monster_name = random.choice(list(MONSTER_DATABASE.keys()))
            enemy = Enemy(monster_name, MONSTER_DATABASE[monster_name], current_floor, current_reward_multiplier, is_boss=False)

        if not battle_loop(hero, enemy, current_floor, current_reward_multiplier):
            print(f"\n💀 You died on Floor {current_floor}. Game Over.")
            print(f"🥇 FINAL SCORE: {hero.score}")
            # Ranglista mentése / ellenőrzése
            handle_highscore(hero.score)
            break
            
        if is_boss_fight:
            print(f"\n🏰 Congratulations! You cleared FLOOR {current_floor}!")
            floor_score = current_floor * hero.floor_xp_earned
            hero.score += floor_score
            print(f"📈 Score earned on this floor: {floor_score} (Total Score: {hero.score})")
            
            hero.floor_xp_earned = 0 
            current_floor += 1
            fight_counter = 1  
        else:
            fight_counter += 1

        # Merchant (No Gamble)
        if hero.is_alive():
            in_shop = True
            while in_shop:
                price_mult = 1.15 ** (current_floor - 1)
                prices = {
                    "1": ("Small Health Potion", int(20 * price_mult)),
                    "2": ("Medium Health Potion", int(40 * price_mult)),
                    "3": ("Big Health Potion", int(75 * price_mult)),
                    "4": ("Small Mana Potion", int(25 * price_mult)),
                    "5": ("Medium Mana Potion", int(50 * price_mult)),
                    "6": ("Big Mana Potion", int(90 * price_mult)),
                    "7": ("Poison Coating", int(35 * price_mult))
                }
                
                print(f"\n🛒 --- WANDERING MERCHANT --- (Gold: {hero.gold})")
                for key, val in prices.items():
                    print(f"({key}) {val[0]} [{val[1]} Gold]")
                print("(S) Check Stats | (0) Leave Shop")
                buy = input("What do you want to buy?\n> ").lower()
                
                if buy == "0":
                    in_shop = False
                elif buy == "s":
                    hero.display_stats(current_floor, current_reward_multiplier)
                elif buy in prices:
                    item_name, item_cost = prices[buy]
                    qty_input = input(f"How many [{item_name}] do you want to buy? (Enter number):\n> ")
                    
                    if qty_input.isdigit():
                        qty = int(qty_input)
                        total_cost = item_cost * qty
                        if qty > 0 and hero.gold >= total_cost:
                            hero.gold -= total_cost
                            hero.inventory[item_name] += qty
                            print(f"🧪 Purchased {qty}x [{item_name}] for {total_cost} Gold!")
                        elif qty <= 0:
                            print("❌ Invalid quantity.")
                        else:
                            print("❌ You do not have enough Gold for that amount!")
                    else:
                        print("❌ Please enter a valid number.")

            # REST OR GO ON SYSTEM
            print(f"\n💤 What will you do next, {hero.name}?")
            print(f"Current HP: {hero.health}/{hero.max_health} | MP: {hero.mp}/{hero.max_mp}")
            print(f"Current Reward Multiplier: {current_reward_multiplier:.2f}x")
            print("(1) Rest  -> Full HP/MP recovery, resets multiplier to 1x")
            print(f"(2) Go On -> No recovery, MULTIPLIES reward by 1.5x (Next: {current_reward_multiplier * 1.5:.2f}x!)")
            post_shop_choice = input("> ")
            
            if post_shop_choice == "1":
                hero.health = hero.max_health
                hero.mp = hero.max_mp
                current_reward_multiplier = 1.0
                print("🏕️ You rested. HP and MP fully restored! Multiplier reset to 1x.")
            else:
                current_reward_multiplier *= 1.5
                print(f"🏃 You push forward! Reward multiplier stacked to {current_reward_multiplier:.2f}x!")
