"""18_magic_tower.py - Magic Tower 50 Floors

A classic Magic Tower (魔塔) game with 50 floors.
Features: turn-based combat, attribute growth, keys and doors, items collection.
Learn: grid-based RPG, state machine, procedural level generation, combat system
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import pyezgame as g

# ============================================================================
# Game Configuration
# ============================================================================

# Map configuration
CELL_SIZE = 32  # Pixel size per cell
MAP_COLS = 13  # Number of columns
MAP_ROWS = 13  # Number of rows
MAP_WIDTH = CELL_SIZE * MAP_COLS  # 416px
MAP_HEIGHT = CELL_SIZE * MAP_ROWS  # 416px

# Window dimensions
SIDEBAR_WIDTH = 200  # Right sidebar width
WIN_WIDTH = MAP_WIDTH + SIDEBAR_WIDTH + 20  # ~636px
WIN_HEIGHT = MAP_HEIGHT + 40  # ~456px

# Position offsets
MAP_X = 10
MAP_Y = 20

# Colors (ARGB format)
BG_COLOR = g.COLOR_RGB(20, 20, 35)
MAP_BG = g.COLOR_RGB(10, 10, 25)
SIDEBAR_BG = g.COLOR_RGB(25, 25, 45)
TEXT_COLOR = g.COLOR_RGB(220, 220, 240)
BORDER_COLOR = g.COLOR_RGB(60, 60, 100)
ACCENT_COLOR = g.COLOR_RGB(100, 140, 255)
DIM_TEXT = g.COLOR_RGB(140, 140, 180)

# Tile types
TILE_EMPTY = 0  # Empty ground
TILE_WALL = 1  # Wall
TILE_PLAYER = 2  # Player position
TILE_MONSTER = 3  # Monster
TILE_YELLOW_DOOR = 4  # Yellow door
TILE_BLUE_DOOR = 5  # Blue door
TILE_RED_DOOR = 6  # Red door
TILE_YELLOW_KEY = 7  # Yellow key
TILE_BLUE_KEY = 8  # Blue key
TILE_RED_KEY = 9  # Red key
TILE_POTION_SMALL = 10  # Small potion (+100 HP)
TILE_POTION_LARGE = 11  # Large potion (+500 HP)
TILE_GEM_RED = 12  # Red gem (+3 ATK)
TILE_GEM_BLUE = 13  # Blue gem (+3 DEF)
TILE_GOLD = 14  # Gold bag (+100 gold)
TILE_STAIRS_UP = 15  # Stairs up
TILE_STAIRS_DOWN = 16  # Stairs down
TILE_CHEST = 17  # Treasure chest

# Frame rate
FPS = 60

# Sprite sheet configuration (magic_tower.png)
# The sprite sheet contains various magic tower elements
# We'll use DrawSpriteEx to extract individual sprites
SPRITE_SHEET = "assets/magic_tower.png"

# Sprite definitions (x, y, width, height) in the sprite sheet
# These are approximate positions based on typical magic tower sprite sheets
SPRITES = {
    # Player
    "player": (0, 0, 32, 32),
    # Monsters (organized by type)
    "slime_green": (32, 0, 32, 32),
    "slime_red": (64, 0, 32, 32),
    "bat_small": (96, 0, 32, 32),
    "skeleton": (128, 0, 32, 32),
    "orc": (160, 0, 32, 32),
    "mage": (192, 0, 32, 32),
    "bat_large": (224, 0, 32, 32),
    "skeleton_captain": (256, 0, 32, 32),
    "demon_minion": (288, 0, 32, 32),
    "final_boss": (320, 0, 64, 64),  # Boss is larger
    # Doors
    "door_yellow": (0, 32, 32, 32),
    "door_blue": (32, 32, 32, 32),
    "door_red": (64, 32, 32, 32),
    # Keys
    "key_yellow": (96, 32, 32, 32),
    "key_blue": (128, 32, 32, 32),
    "key_red": (160, 32, 32, 32),
    # Potions
    "potion_small": (192, 32, 32, 32),
    "potion_large": (224, 32, 32, 32),
    # Gems
    "gem_red": (256, 32, 32, 32),
    "gem_blue": (288, 32, 32, 32),
    # Gold
    "gold": (320, 32, 32, 32),
    # Stairs
    "stairs_up": (0, 64, 32, 32),
    "stairs_down": (32, 64, 32, 32),
    # Chest
    "chest": (64, 64, 32, 32),
    # Wall and floor tiles
    "wall": (96, 64, 32, 32),
    "floor": (128, 64, 32, 32),
}


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class Player:
    """Player attributes"""

    hp: int = 1000  # Current HP
    max_hp: int = 1000  # Max HP
    attack: int = 15  # Attack power (increased for better early game)
    defense: int = 10  # Defense power
    gold: int = 0  # Gold amount
    exp: int = 0  # Experience points
    level: int = 1  # Level
    yellow_keys: int = 2  # Yellow keys (start with more)
    blue_keys: int = 0  # Blue keys
    red_keys: int = 0  # Red keys
    floor: int = 1  # Current floor (1-50)
    x: int = 6  # Map X coordinate
    y: int = 12  # Map Y coordinate


@dataclass
class Monster:
    """Monster definition"""

    name: str  # Monster name
    hp: int  # HP
    attack: int  # Attack
    defense: int  # Defense
    exp: int  # EXP reward
    gold: int  # Gold reward
    color: int  # Display color
    sprite_frame: int = 0  # Sprite frame index


# Predefined monster types (from easy to hard)
# Balanced for 50-floor progression
MONSTER_TYPES = {
    "slime_green": Monster("Green Slime", 30, 15, 2, 8, 3, g.COLOR_RGB(50, 200, 50)),
    "slime_red": Monster("Red Slime", 60, 30, 4, 15, 8, g.COLOR_RGB(200, 50, 50)),
    "bat_small": Monster("Small Bat", 100, 50, 8, 25, 15, g.COLOR_RGB(100, 100, 150)),
    "skeleton": Monster("Skeleton", 180, 90, 15, 45, 30, g.COLOR_RGB(200, 200, 200)),
    "orc": Monster("Orc Warrior", 350, 160, 25, 90, 60, g.COLOR_RGB(100, 150, 50)),
    "mage": Monster("Mage", 280, 220, 20, 110, 70, g.COLOR_RGB(150, 50, 200)),
    "bat_large": Monster("Large Bat", 450, 280, 35, 140, 100, g.COLOR_RGB(80, 80, 120)),
    "skeleton_captain": Monster("Skeleton Captain", 700, 400, 45, 250, 150, g.COLOR_RGB(180, 180, 180)),
    "demon_minion": Monster("Demon Minion", 1200, 600, 70, 500, 300, g.COLOR_RGB(200, 50, 50)),
    "final_boss": Monster("Final Boss", 8000, 1200, 150, 3000, 1500, g.COLOR_RGB(255, 0, 0)),
}


# ============================================================================
# Game State
# ============================================================================


@dataclass
class GameState:
    """Game state management"""

    player: Player = field(default_factory=Player)
    current_map: list[list[int]] = field(default_factory=list)
    monsters_on_map: dict[tuple[int, int], str] = field(default_factory=dict)  # (x, y) -> monster_type
    game_over: bool = False
    paused: bool = False
    victory: bool = False
    notification: str = ""
    notification_timer: float = 0.0
    combat_log: list[str] = field(default_factory=list)


# ============================================================================
# Helper Functions
# ============================================================================


def create_empty_map() -> list[list[int]]:
    """Create an empty map filled with walls"""
    return [[TILE_WALL for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]


def show_notification(game_state: GameState, text: str, duration: float = 2.0) -> None:
    """Show a notification message"""
    game_state.notification = text
    game_state.notification_timer = duration


def add_combat_log(game_state: GameState, message: str) -> None:
    """Add message to combat log"""
    game_state.combat_log.append(message)
    if len(game_state.combat_log) > 5:
        game_state.combat_log.pop(0)


# ============================================================================
# Level Generation
# ============================================================================


def generate_floor(floor_num: int) -> tuple[list[list[int]], dict[tuple[int, int], str]]:
    """
    Generate a floor layout based on floor number.
    Returns: (map_data, monsters_dict)
    """
    game_map = create_empty_map()
    monsters = {}

    # Create basic room structure (remove inner walls)
    for y in range(1, MAP_ROWS - 1):
        for x in range(1, MAP_COLS - 1):
            game_map[y][x] = TILE_EMPTY

    # Add some internal walls for variety
    wall_patterns = [
        # Horizontal walls
        [(3, 3), (3, 4), (3, 5)],
        [(5, 7), (5, 8), (5, 9)],
        [(9, 2), (9, 3), (9, 4)],
        # Vertical walls
        [(4, 6), (5, 6), (6, 6)],
        [(7, 10), (8, 10), (9, 10)],
    ]

    # Select patterns based on floor number
    pattern_idx = floor_num % len(wall_patterns)
    for wx, wy in wall_patterns[pattern_idx]:
        if 0 < wx < MAP_COLS - 1 and 0 < wy < MAP_ROWS - 1:
            game_map[wy][wx] = TILE_WALL

    # Place stairs (always accessible)
    game_map[12][6] = TILE_STAIRS_DOWN if floor_num == 1 else TILE_STAIRS_DOWN
    game_map[0][6] = TILE_STAIRS_UP if floor_num < 50 else TILE_EMPTY

    # Add doors on higher floors for strategic gameplay
    if floor_num > 10:
        # Add some doors to create interesting paths
        door_positions = [
            (3, 6),
            (9, 6),  # Vertical barriers
            (6, 3),
            (6, 9),  # Horizontal barriers
        ]
        num_doors = min(floor_num // 10, len(door_positions))
        for i in range(num_doors):
            if i < len(door_positions):
                dx, dy = door_positions[i]
                # Choose door type based on floor
                if floor_num <= 20:
                    game_map[dy][dx] = TILE_YELLOW_DOOR
                elif floor_num <= 35:
                    game_map[dy][dx] = TILE_BLUE_DOOR if random.random() < 0.5 else TILE_YELLOW_DOOR
                else:
                    door_type = random.choice([TILE_YELLOW_DOOR, TILE_BLUE_DOOR, TILE_RED_DOOR])
                    game_map[dy][dx] = door_type

    # Special handling for final boss floor
    if floor_num == 50:
        # Clear center area for boss fight
        for y in range(4, 9):
            for x in range(4, 9):
                game_map[y][x] = TILE_EMPTY
        monsters[(6, 6)] = "final_boss"
        return game_map, monsters

    # Get available empty positions
    empty_positions = []
    for y in range(1, MAP_ROWS - 1):
        for x in range(1, MAP_COLS - 1):
            if game_map[y][x] == TILE_EMPTY and not ((x == 6 and y == 12) or (x == 6 and y == 0)):
                empty_positions.append((x, y))
    # Shuffle positions
    for i in range(len(empty_positions) - 1, 0, -1):
        j = g.GameLib.random(0, i)
        empty_positions[i], empty_positions[j] = empty_positions[j], empty_positions[i]

    # Determine difficulty tier
    if floor_num <= 10:
        tier = 1  # Beginner: slimes only
    elif floor_num <= 20:
        tier = 2  # Easy: slimes + bats
    elif floor_num <= 30:
        tier = 3  # Medium: + skeletons, orcs
    elif floor_num <= 40:
        tier = 4  # Hard: + mages, large bats
    else:
        tier = 5  # Elite: skeleton captains, demon minions

    # Place monsters based on tier
    monster_pool = get_monster_pool(tier)
    # Adjust monster count based on floor (fewer on early floors, more on later)
    num_monsters = min(2 + floor_num // 4, 8, len(empty_positions))

    for _ in range(num_monsters):
        if empty_positions:
            x, y = empty_positions.pop()
            monster_type = random.choice(monster_pool)
            monsters[(x, y)] = monster_type
            game_map[y][x] = TILE_MONSTER

    # Place items
    place_items(game_map, floor_num, empty_positions)

    return game_map, monsters


def get_monster_pool(tier: int) -> list[str]:
    """Get available monster types for a difficulty tier"""
    pools = {
        1: ["slime_green", "slime_green", "slime_green", "slime_red"],  # More green slimes
        2: ["slime_red", "slime_red", "bat_small"],
        3: ["bat_small", "skeleton", "orc"],
        4: ["skeleton", "orc", "mage", "bat_large"],
        5: ["bat_large", "skeleton_captain", "demon_minion", "demon_minion"],
    }
    return pools.get(tier, ["slime_green"])


def place_items(game_map: list[list[int]], floor_num: int, positions: list[tuple[int, int]]) -> None:
    """Place items on the map"""
    # Determine item distribution based on floor
    if floor_num <= 5:
        # Very early floors: lots of keys and potions for learning
        item_weights = {
            TILE_YELLOW_KEY: 50,
            TILE_POTION_SMALL: 30,
            TILE_GOLD: 15,
            TILE_GEM_RED: 3,
            TILE_GEM_BLUE: 2,
        }
    elif floor_num <= 15:
        # Early floors: more keys and potions
        item_weights = {
            TILE_YELLOW_KEY: 35,
            TILE_POTION_SMALL: 25,
            TILE_GOLD: 20,
            TILE_GEM_RED: 10,
            TILE_GEM_BLUE: 8,
            TILE_CHEST: 2,
        }
    elif floor_num <= 30:
        # Mid floors: balanced with blue keys appearing
        item_weights = {
            TILE_YELLOW_KEY: 20,
            TILE_BLUE_KEY: 15,
            TILE_POTION_SMALL: 15,
            TILE_POTION_LARGE: 10,
            TILE_GOLD: 20,
            TILE_GEM_RED: 12,
            TILE_GEM_BLUE: 8,
        }
    else:
        # Late floors: more gems, gold, and red keys
        item_weights = {
            TILE_YELLOW_KEY: 8,
            TILE_BLUE_KEY: 12,
            TILE_RED_KEY: 5,
            TILE_POTION_LARGE: 25,
            TILE_GOLD: 20,
            TILE_GEM_RED: 15,
            TILE_GEM_BLUE: 12,
            TILE_CHEST: 3,
        }

    # Calculate total weight
    total_weight = sum(item_weights.values())

    # Place items (use ~35% of empty positions for better item density)
    num_items = max(4, len(positions) * 35 // 100)

    for _ in range(num_items):
        if not positions:
            break

        # Randomly select item type based on weights
        rand_val = g.GameLib.random(0, total_weight - 1)
        cumulative = 0
        selected_item = TILE_GOLD

        for item_type, weight in item_weights.items():
            cumulative += weight
            if rand_val < cumulative:
                selected_item = item_type
                break

        # Place item
        idx = random.randint(0, len(positions) - 1)
        x, y = positions.pop(idx)
        game_map[y][x] = selected_item


# ============================================================================
# Combat System
# ============================================================================


def combat(game: g.GameLib, game_state: GameState, monster_type: str) -> bool:
    """
    Turn-based combat system.
    Returns True if player wins, False if player loses.
    """
    monster_template = MONSTER_TYPES[monster_type]

    # Create a copy of the monster for this battle
    monster_hp = monster_template.hp
    monster_name = monster_template.name

    # Show combat start notification
    show_notification(game_state, f"Battle: {monster_name}!", 1.5)

    # Combat loop
    while True:
        # Player attacks
        player_damage = max(1, game_state.player.attack - monster_template.defense)
        monster_hp -= player_damage

        add_combat_log(game_state, f"You deal {player_damage} dmg")

        if monster_hp <= 0:
            # Victory!
            game_state.player.exp += monster_template.exp
            game_state.player.gold += monster_template.gold
            show_notification(game_state, f"Victory! +{monster_template.exp}EXP +{monster_template.gold}G", 2.0)

            # Play victory sound
            game.play_wav("assets/sound/victory.wav", False)

            # Check level up
            check_level_up(game_state)
            return True

        # Monster counterattacks
        monster_damage = max(1, monster_template.attack - game_state.player.defense)
        game_state.player.hp -= monster_damage

        add_combat_log(game_state, f"{monster_name} deals {monster_damage} dmg")

        if game_state.player.hp <= 0:
            # Defeat
            game_state.player.hp = 0
            show_notification(game_state, "You were defeated...", 3.0)
            game_state.game_over = True

            # Play game over sound
            game.play_wav("assets/sound/game_over.wav", False)
            return False


def check_level_up(game_state: GameState) -> None:
    """Check if player should level up"""
    exp_needed = game_state.player.level * 120  # Slightly harder to level up

    if game_state.player.exp >= exp_needed:
        game_state.player.level += 1
        game_state.player.max_hp += 80  # More HP per level
        game_state.player.hp = game_state.player.max_hp
        game_state.player.attack += 6  # More attack growth
        game_state.player.defense += 4  # More defense growth

        show_notification(game_state, f"Level Up! Lv.{game_state.player.level}", 2.5)

        # Play level up sound
        # game.play_sound("assets/sound/coin.wav", False)


# ============================================================================
# Movement & Interaction
# ============================================================================


def try_move(game: g.GameLib, game_state: GameState, dx: int, dy: int) -> bool:
    """
    Try to move the player by (dx, dy).
    Returns True if movement was successful.
    """
    if game_state.game_over or game_state.victory:
        return False

    new_x = game_state.player.x + dx
    new_y = game_state.player.y + dy

    # Check bounds
    if new_x < 0 or new_x >= MAP_COLS or new_y < 0 or new_y >= MAP_ROWS:
        return False

    tile = game_state.current_map[new_y][new_x]

    # Handle different tile types
    if tile == TILE_WALL:
        # Hit wall
        return False

    elif tile == TILE_MONSTER:
        # Fight monster
        monster_type = game_state.monsters_on_map.get((new_x, new_y))
        if monster_type:
            if combat(game, game_state, monster_type):
                # Remove monster from map
                del game_state.monsters_on_map[(new_x, new_y)]
                game_state.current_map[new_y][new_x] = TILE_EMPTY
                # Move to that position
                game_state.player.x = new_x
                game_state.player.y = new_y
                return True
            else:
                return False  # Player died
        return False

    elif tile == TILE_YELLOW_DOOR:
        if game_state.player.yellow_keys > 0:
            game_state.player.yellow_keys -= 1
            game_state.current_map[new_y][new_x] = TILE_EMPTY
            show_notification(game_state, "Used Yellow Key", 1.0)
            game.play_wav("assets/sound/click.wav", False)
        else:
            show_notification(game_state, "Need Yellow Key!", 1.0)
            return False

    elif tile == TILE_BLUE_DOOR:
        if game_state.player.blue_keys > 0:
            game_state.player.blue_keys -= 1
            game_state.current_map[new_y][new_x] = TILE_EMPTY
            show_notification(game_state, "Used Blue Key", 1.0)
            game.play_wav("assets/sound/click.wav", False)
        else:
            show_notification(game_state, "Need Blue Key!", 1.0)
            return False

    elif tile == TILE_RED_DOOR:
        if game_state.player.red_keys > 0:
            game_state.player.red_keys -= 1
            game_state.current_map[new_y][new_x] = TILE_EMPTY
            show_notification(game_state, "Used Red Key", 1.0)
            game.play_wav("assets/sound/click.wav", False)
        else:
            show_notification(game_state, "Need Red Key!", 1.0)
            return False

    elif tile == TILE_YELLOW_KEY:
        game_state.player.yellow_keys += 1
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, "+1 Yellow Key", 1.0)
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_BLUE_KEY:
        game_state.player.blue_keys += 1
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, "+1 Blue Key", 1.0)
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_RED_KEY:
        game_state.player.red_keys += 1
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, "+1 Red Key", 1.0)
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_POTION_SMALL:
        heal = 100
        game_state.player.hp = min(game_state.player.max_hp, game_state.player.hp + heal)
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, f"+{heal} HP", 1.0)
        game.play_wav("assets/sound/jump.wav", False)

    elif tile == TILE_POTION_LARGE:
        heal = 500
        game_state.player.hp = min(game_state.player.max_hp, game_state.player.hp + heal)
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, f"+{heal} HP", 1.0)
        game.play_wav("assets/sound/jump.wav", False)

    elif tile == TILE_GEM_RED:
        game_state.player.attack += 4  # Increased from 3
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, "+4 ATK", 1.0)
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_GEM_BLUE:
        game_state.player.defense += 4  # Increased from 3
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, "+4 DEF", 1.0)
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_GOLD:
        game_state.player.gold += 100
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        show_notification(game_state, "+100 Gold", 1.0)
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_CHEST:
        # Random reward from chest
        reward_type = random.randint(0, 2)
        if reward_type == 0:
            game_state.player.gold += 200
            show_notification(game_state, "Chest: +200 Gold", 1.5)
        elif reward_type == 1:
            game_state.player.attack += 5
            show_notification(game_state, "Chest: +5 ATK", 1.5)
        else:
            game_state.player.defense += 5
            show_notification(game_state, "Chest: +5 DEF", 1.5)
        game_state.current_map[new_y][new_x] = TILE_EMPTY
        game.play_wav("assets/sound/coin.wav", False)

    elif tile == TILE_STAIRS_UP:
        if game_state.player.floor < 50:
            go_to_floor(game, game_state, game_state.player.floor + 1)
            return False  # Don't move, just change floor

    elif tile == TILE_STAIRS_DOWN and game_state.player.floor > 1:
        go_to_floor(game, game_state, game_state.player.floor - 1)
        return False  # Don't move, just change floor

    # Move player to new position
    game_state.player.x = new_x
    game_state.player.y = new_y

    return True


def go_to_floor(game: g.GameLib, game_state: GameState, floor_num: int) -> None:
    """Change to a different floor"""
    if floor_num < 1 or floor_num > 50:
        return

    game_state.player.floor = floor_num

    # Generate new floor
    game_state.current_map, game_state.monsters_on_map = generate_floor(floor_num)

    # Reset player position to bottom center
    game_state.player.x = 6
    game_state.player.y = 12

    # Check if this is the final boss floor
    if floor_num == 50:
        show_notification(game_state, "FINAL BOSS FLOOR!", 3.0)
    else:
        show_notification(game_state, f"Floor {floor_num}", 1.5)

    # Play stair sound
    game.play_wav("assets/sound/click.wav", False)


# ============================================================================
# Rendering
# ============================================================================


def draw_tile(
    game: g.GameLib,
    sprite_sheet_id: int,
    x: int,
    y: int,
    tile_type: int,
    monster_type: str | None = None,
) -> None:
    """Draw a single tile using sprite sheet"""
    px = MAP_X + x * CELL_SIZE
    py = MAP_Y + y * CELL_SIZE

    if tile_type == TILE_WALL:
        # Draw wall from sprite sheet or fallback to rectangle
        if "wall" in SPRITES:
            sx, sy, sw, sh = SPRITES["wall"]
            game.draw_sprite_region(sprite_sheet_id, px, py, sx, sy, sw, sh)
        else:
            game.fill_rect(px, py, CELL_SIZE, CELL_SIZE, BORDER_COLOR)
            game.draw_rect(px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4, g.COLOR_RGB(40, 40, 70))

    elif tile_type == TILE_EMPTY:
        # Draw empty ground (can use floor tile or just background)
        if "floor" in SPRITES:
            sx, sy, sw, sh = SPRITES["floor"]
            game.draw_sprite_region(sprite_sheet_id, px, py, sx, sy, sw, sh)
        else:
            game.fill_rect(px, py, CELL_SIZE, CELL_SIZE, MAP_BG)

    elif tile_type == TILE_MONSTER and monster_type:
        # Draw monster from sprite sheet
        sprite_name = monster_type
        if sprite_name in SPRITES:
            sx, sy, sw, sh = SPRITES[sprite_name]
            game.draw_sprite_region(sprite_sheet_id, px, py, sx, sy, sw, sh)
        else:
            # Fallback to colored rectangle
            monster = MONSTER_TYPES[monster_type]
            game.fill_rect(px + 4, py + 4, CELL_SIZE - 8, CELL_SIZE - 8, monster.color)

    elif tile_type == TILE_YELLOW_DOOR:
        game.fill_rect(px + 6, py + 4, CELL_SIZE - 12, CELL_SIZE - 8, g.COLOR_RGB(200, 200, 50))
        game.draw_rect(px + 6, py + 4, CELL_SIZE - 12, CELL_SIZE - 8, g.COLOR_RGB(150, 150, 30))

    elif tile_type == TILE_BLUE_DOOR:
        game.fill_rect(px + 6, py + 4, CELL_SIZE - 12, CELL_SIZE - 8, g.COLOR_RGB(50, 100, 200))
        game.draw_rect(px + 6, py + 4, CELL_SIZE - 12, CELL_SIZE - 8, g.COLOR_RGB(30, 70, 150))

    elif tile_type == TILE_RED_DOOR:
        game.fill_rect(px + 6, py + 4, CELL_SIZE - 12, CELL_SIZE - 8, g.COLOR_RGB(200, 50, 50))
        game.draw_rect(px + 6, py + 4, CELL_SIZE - 12, CELL_SIZE - 8, g.COLOR_RGB(150, 30, 30))

    elif tile_type == TILE_YELLOW_KEY:
        game.fill_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 8, g.COLOR_RGB(200, 200, 50))

    elif tile_type == TILE_BLUE_KEY:
        game.fill_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 8, g.COLOR_RGB(50, 100, 200))

    elif tile_type == TILE_RED_KEY:
        game.fill_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 8, g.COLOR_RGB(200, 50, 50))

    elif tile_type == TILE_POTION_SMALL:
        game.fill_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 8, g.COLOR_RGB(255, 100, 100))

    elif tile_type == TILE_POTION_LARGE:
        game.fill_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 10, g.COLOR_RGB(255, 50, 50))

    elif tile_type == TILE_GEM_RED:
        # Draw diamond shape
        cx, cy = px + CELL_SIZE // 2, py + CELL_SIZE // 2
        game.fill_triangle(cx, cy - 10, cx - 8, cy, cx, cy + 10, g.COLOR_RGB(200, 50, 50))
        game.fill_triangle(cx, cy - 10, cx + 8, cy, cx, cy + 10, g.COLOR_RGB(200, 50, 50))

    elif tile_type == TILE_GEM_BLUE:
        cx, cy = px + CELL_SIZE // 2, py + CELL_SIZE // 2
        game.fill_triangle(cx, cy - 10, cx - 8, cy, cx, cy + 10, g.COLOR_RGB(50, 100, 200))
        game.fill_triangle(cx, cy - 10, cx + 8, cy, cx, cy + 10, g.COLOR_RGB(50, 100, 200))

    elif tile_type == TILE_GOLD:
        game.fill_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 8, g.COLOR_RGB(255, 215, 0))

    elif tile_type == TILE_STAIRS_UP:
        game.fill_rect(px + 8, py + 8, 16, 16, g.COLOR_RGB(150, 150, 150))
        game.draw_text(px + 10, py + 10, "↑", g.COLOR_WHITE)

    elif tile_type == TILE_STAIRS_DOWN:
        game.fill_rect(px + 8, py + 8, 16, 16, g.COLOR_RGB(150, 150, 150))
        game.draw_text(px + 10, py + 10, "↓", g.COLOR_WHITE)

    elif tile_type == TILE_CHEST:
        game.fill_rect(px + 6, py + 8, CELL_SIZE - 12, CELL_SIZE - 16, g.COLOR_RGB(150, 100, 50))
        game.draw_rect(px + 6, py + 8, CELL_SIZE - 12, CELL_SIZE - 16, g.COLOR_RGB(100, 70, 30))


def draw_map(game: g.GameLib, sprite_sheet_id: int, game_state: GameState) -> None:
    """Draw the current floor map"""
    for y in range(MAP_ROWS):
        for x in range(MAP_COLS):
            tile = game_state.current_map[y][x]
            monster_type = game_state.monsters_on_map.get((x, y))
            draw_tile(game, sprite_sheet_id, x, y, tile, monster_type)

    # Draw player using sprite sheet
    px = MAP_X + game_state.player.x * CELL_SIZE
    py = MAP_Y + game_state.player.y * CELL_SIZE
    if "player" in SPRITES:
        sx, sy, sw, sh = SPRITES["player"]
        game.draw_sprite_region(sprite_sheet_id, px, py, sx, sy, sw, sh)
    else:
        game.fill_rect(px + 6, py + 6, CELL_SIZE - 12, CELL_SIZE - 12, g.COLOR_RGB(100, 150, 255))
        # Player face
        game.fill_circle(px + 12, py + 14, 3, g.COLOR_WHITE)
        game.fill_circle(px + 20, py + 14, 3, g.COLOR_WHITE)


def draw_sidebar(game: g.GameLib, game_state: GameState) -> None:
    """Draw the right sidebar with player stats"""
    sx = MAP_X + MAP_WIDTH + 10
    sy = MAP_Y

    # Background
    game.fill_rect(sx - 5, sy - 5, SIDEBAR_WIDTH, MAP_HEIGHT + 10, SIDEBAR_BG)
    game.draw_rect(sx - 5, sy - 5, SIDEBAR_WIDTH, MAP_HEIGHT + 10, BORDER_COLOR)

    # Title
    game.draw_text_scale(sx, sy, "MAGIC TOWER", ACCENT_COLOR, 14, 14)

    yp = sy + 35

    # Player stats
    game.draw_text(sx, yp, "=== STATS ===", DIM_TEXT)
    yp += 20

    # HP
    game.draw_printf(sx, yp, TEXT_COLOR, f"HP: {game_state.player.hp}/{game_state.player.max_hp}")
    yp += 18

    # Attack
    game.draw_printf(sx, yp, TEXT_COLOR, f"ATK: {game_state.player.attack}")
    yp += 18

    # Defense
    game.draw_printf(sx, yp, TEXT_COLOR, f"DEF: {game_state.player.defense}")
    yp += 18

    # Level & EXP
    game.draw_printf(sx, yp, TEXT_COLOR, f"LV: {game_state.player.level}")
    yp += 18
    game.draw_printf(sx, yp, DIM_TEXT, f"EXP: {game_state.player.exp}")
    yp += 25

    # Gold
    game.draw_printf(sx, yp, g.COLOR_RGB(255, 215, 0), f"Gold: {game_state.player.gold}")
    yp += 25

    # Keys
    game.draw_text(sx, yp, "=== KEYS ===", DIM_TEXT)
    yp += 18
    game.draw_printf(sx, yp, g.COLOR_RGB(200, 200, 50), f"Yellow: {game_state.player.yellow_keys}")
    yp += 18
    game.draw_printf(sx, yp, g.COLOR_RGB(50, 100, 200), f"Blue: {game_state.player.blue_keys}")
    yp += 18
    game.draw_printf(sx, yp, g.COLOR_RGB(200, 50, 50), f"Red: {game_state.player.red_keys}")
    yp += 25

    # Floor
    game.draw_text(sx, yp, "=== FLOOR ===", DIM_TEXT)
    yp += 18
    game.draw_printf(sx, yp, ACCENT_COLOR, f"{game_state.player.floor}/50")
    yp += 30

    # Controls
    game.draw_text(sx, yp, "=== CONTROLS ===", DIM_TEXT)
    yp += 18
    controls = [
        "WASD/Arrows: Move",
        "P: Pause",
        "R: Restart",
        "ESC: Quit",
    ]
    for ctrl in controls:
        game.draw_text(sx, yp, ctrl, DIM_TEXT)
        yp += 16

    # FPS
    game.draw_printf(sx, sy + MAP_HEIGHT - 20, g.COLOR_DARK_GRAY, f"FPS: {game.get_fps():.0f}")


def draw_notifications(game: g.GameLib, game_state: GameState) -> None:
    """Draw notification messages"""
    if game_state.notification_timer > 0 and game_state.notification:
        # Draw notification box
        text_width = len(game_state.notification) * 8 + 20
        cx = MAP_X + MAP_WIDTH // 2
        cy = MAP_Y + MAP_HEIGHT // 3

        game.fill_rect(cx - text_width // 2, cy - 15, text_width, 30, g.COLOR_ARGB(200, 0, 0, 0))
        game.draw_rect(cx - text_width // 2, cy - 15, text_width, 30, g.COLOR_YELLOW)
        game.draw_text(cx - text_width // 2 + 10, cy - 8, game_state.notification, g.COLOR_YELLOW)


def draw_combat_log(game: g.GameLib, game_state: GameState) -> None:
    """Draw combat log at bottom of map"""
    if not game_state.combat_log:
        return

    log_y = MAP_Y + MAP_HEIGHT - len(game_state.combat_log) * 14 - 5

    for i, msg in enumerate(game_state.combat_log):
        game.draw_printf(MAP_X + 5, log_y + i * 14, g.COLOR_ARGB(180, 255, 255, 255), msg)


# ============================================================================
# Input Handling
# ============================================================================


def handle_input(game: g.GameLib, game_state: GameState) -> bool:
    """Handle keyboard input. Returns False to exit game."""

    # ESC to quit
    if game.is_key_pressed(g.KEY_ESCAPE):
        return False

    # R to restart
    if game.is_key_pressed(g.KEY_R):
        reset_game(game, game_state)
        return True

    # P to pause
    if game.is_key_pressed(g.KEY_P):
        game_state.paused = not game_state.paused
        return True

    # No input when game over or paused
    if game_state.game_over or game_state.victory or game_state.paused:
        return True

    # Movement keys

    if game.is_key_pressed(g.KEY_UP) or game.is_key_pressed(g.KEY_W):
        try_move(game, game_state, 0, -1)
    elif game.is_key_pressed(g.KEY_DOWN) or game.is_key_pressed(g.KEY_S):
        try_move(game, game_state, 0, 1)
    elif game.is_key_pressed(g.KEY_LEFT) or game.is_key_pressed(g.KEY_A):
        try_move(game, game_state, -1, 0)
    elif game.is_key_pressed(g.KEY_RIGHT) or game.is_key_pressed(g.KEY_D):
        try_move(game, game_state, 1, 0)

    return True


def reset_game(game: g.GameLib, game_state: GameState) -> None:
    """Reset the game to initial state"""
    game_state.player = Player()
    game_state.game_over = False
    game_state.paused = False
    game_state.victory = False
    game_state.notification = ""
    game_state.notification_timer = 0.0
    game_state.combat_log.clear()

    # Generate first floor
    game_state.current_map, game_state.monsters_on_map = generate_floor(1)

    show_notification(game_state, "Game Started!", 2.0)


# ============================================================================
# Main Game Loop
# ============================================================================


def main() -> None:
    """Main entry point"""
    game = g.GameLib()
    _ = game.open(WIN_WIDTH, WIN_HEIGHT, "18 - Magic Tower 50F", True)

    # Load sprite sheet
    sprite_sheet_id = game.load_sprite(SPRITE_SHEET)

    # Initialize game state
    game_state = GameState()
    reset_game(game, game_state)

    # Main loop
    while not game.is_closed():
        dt = game.get_delta_time()

        # Update notification timer
        if game_state.notification_timer > 0:
            game_state.notification_timer -= dt

        # Handle input
        if not handle_input(game, game_state):
            break

        # Check win condition
        if game_state.player.floor == 50 and (6, 6) not in game_state.monsters_on_map:
            game_state.victory = True
            show_notification(game_state, "VICTORY! You cleared the tower!", 5.0)

        # Rendering
        game.clear(BG_COLOR)

        # Draw map
        draw_map(game, sprite_sheet_id, game_state)

        # Draw sidebar
        draw_sidebar(game, game_state)

        # Draw notifications
        draw_notifications(game, game_state)

        # Draw combat log
        draw_combat_log(game, game_state)

        # Draw overlays
        if game_state.game_over:
            cx = MAP_X + MAP_WIDTH // 2
            cy = MAP_Y + MAP_HEIGHT // 2
            game.fill_rect(cx - 80, cy - 35, 160, 70, g.COLOR_ARGB(200, 0, 0, 0))
            game.draw_rect(cx - 80, cy - 35, 160, 70, g.COLOR_RED)
            game.draw_text_scale(cx - 48, cy - 28, "GAME OVER", g.COLOR_RGB(255, 80, 80), 10, 10)
            game.draw_text(cx - 45, cy + 0, TEXT_COLOR, f"Reached Floor {game_state.player.floor}")
            game.draw_text(cx - 45, cy + 18, g.COLOR_YELLOW, "R to restart")

        if game_state.victory:
            cx = MAP_X + MAP_WIDTH // 2
            cy = MAP_Y + MAP_HEIGHT // 2
            game.fill_rect(cx - 80, cy - 35, 160, 70, g.COLOR_ARGB(200, 0, 0, 0))
            game.draw_rect(cx - 80, cy - 35, 160, 70, g.COLOR_YELLOW)
            game.draw_text_scale(cx - 50, cy - 28, "VICTORY!", g.COLOR_RGB(255, 255, 100), 10, 10)
            game.draw_text(cx - 55, cy + 0, "Tower Cleared!", TEXT_COLOR)
            game.draw_text(cx - 45, cy + 18, "R to restart", g.COLOR_YELLOW)

        if game_state.paused and not game_state.game_over and not game_state.victory:
            cx = MAP_X + MAP_WIDTH // 2
            cy = MAP_Y + MAP_HEIGHT // 2
            game.fill_rect(cx - 55, cy - 18, 110, 36, g.COLOR_ARGB(200, 0, 0, 0))
            game.draw_text_scale(cx - 30, cy - 12, "PAUSED", g.COLOR_YELLOW, 10, 10)

        # Update display
        game.update()
        game.wait_frame(FPS)


if __name__ == "__main__":
    main()
