# Python Text RPG Game 🎮

A turn-based text RPG adventure game built in Python. Create your hero, choose a class, and battle through increasingly difficult enemies!

## Features

- **Character Classes**: Choose between Warrior, Mage, or Rogue with unique stats
- **Turn-Based Combat**: Strategic battles with attack and item actions
- **Inventory System**: Collect and use health potions in battle
- **Enemy Scaling**: Face progressively harder foes as you advance
- **Economy System**: Earn gold and purchase potions

## How to Run

```bash
python game.py
```

## Game Mechanics

### Character Classes

| Class   | Health | Attack | Defense | Best For |
|---------|--------|--------|---------|----------|
| Warrior | 120    | 15     | 8       | Survivability |
| Mage    | 80     | 22     | 3       | High Damage |
| Rogue   | 100    | 18     | 5       | Balanced |

### Combat

- **Attack**: Deal damage based on your class's attack power (±3 variance)
- **Use Potion**: Restore 40 HP from your inventory
- **Defense**: Reduce incoming damage based on your defense stat
- **Damage Formula**: `actual_damage = max(1, incoming_damage - defense)`

### Progression

- Defeat 3 enemies: Slime → Goblin Scout → Orc Marauder
- Earn 20 gold per victory
- Buy Health Potions for 20 gold each

## Game Architecture

### Classes

- **Entity**: Base class for all living creatures (health, attack, defense)
- **Player**: User-controlled hero with inventory and gold
- **Enemy**: AI-controlled foes with scaling difficulty

## Future Enhancements

- [ ] Leveling and XP system
- [ ] Skill trees and special abilities
- [ ] More enemy types and boss battles
- [ ] Save/load game state
- [ ] Experience points system
- [ ] Equipment and armor upgrades

## Author

simonyi1994
