import random
import time

class Entity:
    """Base class for all living creatures in the game."""
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack
        self.defense_power = defense

    def is_alive(self):
        return self.health > 0

    def take_damage(self, incoming_damage):
        # Prevent damage from going negative
        actual_damage = max(1, incoming_damage - self.defense_power)
        self.health = max(0, self.health - actual_damage)
        print(f"💥 {self.name} took {actual_damage} damage! (HP: {self.health}/{self.max_health})")
        return actual_damage


class Player(Entity):
    """The user-controlled hero with an inventory system."""
    def __init__(self, name, job_class):
        self.job_class = job_class
        self.level = 1
        self.xp = 0
        self.gold = 50
        self.inventory = ["Health Potion"]
        
        # Set base stats based on chosen class
        if job_class.lower() == "warrior":
            super().__init__(name, health=120, attack=15, defense=8)
        elif job_class.lower() == "mage":
            super().__init__(name, health=80, attack=22, defense=3)
        else:  # Default Rogue
            super().__init__(name, health=100, attack=18, defense=5)

    def use_potion(self):
        if "Health Potion" in self.inventory:
            self.inventory.remove("Health Potion")
            heal_amount = 40
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"🧪 {self.name} drank a potion and restored {heal_amount} HP!")
        else:
            print("❌ You don't have any potions left!")


class Enemy(Entity):
    """An AI foe generated dynamically."""
    def __init__(self, name, tier=1):
        super().__init__(
            name=name, 
            health=40 * tier, 
            attack=10 + (2 * tier), 
            defense=2 * tier
        )


def battle_loop(player, enemy):
    """Manages sequential turn combat until someone falls."""
    print(f"\n⚔️ A wild {enemy.name} blocks your path!")
    
    while player.is_alive() and enemy.is_alive():
        time.sleep(0.5)
        print(f"\n--- {player.name}'s Turn ---")
        print(f"HP: {player.health}/{player.max_health} | Enemy HP: {enemy.health}/{enemy.max_health}")
        action = input("Choose action: (1) Attack  (2) Use Potion\n> ")

        if action == "1":
            # Player attacks enemy
            damage = player.attack_power + random.randint(-3, 3)
            enemy.take_damage(damage)
        elif action == "2":
            player.use_potion()
        else:
            print("🤔 You stumbled around and missed your chance!")

        # Enemy's turn
        if enemy.is_alive():
            time.sleep(0.5)
            print(f"\n--- {enemy.name}'s Turn ---")
            enemy_damage = enemy.attack_power + random.randint(-2, 2)
            player.take_damage(enemy_damage)

    # Resolution
    if player.is_alive():
        print(f"\n🎉 Victory! You defeated the {enemy.name}!")
        player.gold += 20
        return True
    else:
        print("\n💀 You have been defeated... Game Over.")
        return False


# --- Main Game Flow Loop ---
def main():
    print("🔮 Welcome to the Python Text RPG Realm! 🔮")
    name = input("Enter your hero's name: ")
    job = input("Choose a class (Warrior, Mage, Rogue): ")
    
    hero = Player(name, job)
    print(f"\nCharacter created! Welcome {hero.name} the {hero.job_class.capitalize()}.")

    # Cycle through a tiny sequence of enemies
    monsters = ["Slime", "Goblin Scout", "Orc Marauder"]
    for index, monster_name in enumerate(monsters, start=1):
        foe = Enemy(monster_name, tier=index)
        victory = battle_loop(hero, foe)
        
        if not victory:
            break
        else:
            print(f"💰 Found 20 gold pieces! Total Gold: {hero.gold}")
            # Offer shop intervention before next fight
            choice = input("\nDo you want to buy a potion for 20 gold? (y/n): ")
            if choice.lower() == 'y' and hero.gold >= 20:
                hero.gold -= 20
                hero.inventory.append("Health Potion")
                print("🛒 Purchased 1 Health Potion.")

    if hero.is_alive():
        print("\n🏆 Congratulations! You have purged the realm of evil!")

if __name__ == "__main__":
    main()
