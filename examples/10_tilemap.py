"""10_tilemap.py - Tilemap Two-Layer Scrolling

Two-layer scrolling demo:
  - Background layer: far view (sky, clouds, hills), half speed for parallax effect
  - Foreground layer: ground, platforms, bricks, stairs, full speed
  - Character sprite loaded from assets/, camera follows
  - Decorative trees loaded from assets/

Controls: <- -> / A D move character, ESC to quit
Learn: create_tilemap, fill_tile_rect, clear_tilemap, world_to_tile_col/row,
       get_tile_at_pixel, draw_tilemap, load_sprite, draw_sprite_ex,
       SPRITE_COLORKEY, SPRITE_FLIP_H, parallax scrolling
"""

import os

import pyezgame as g

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TS = 16  # Tile size
CHAR_W = 32
CHAR_FOOT = 44

# Foreground tile IDs
FG_GRASS = 0
FG_DIRT = 1
FG_BRICK = 2
FG_STONE = 3

# Background tile IDs
BG_SKY = 0
BG_CLOUD_L = 1
BG_CLOUD_R = 2
BG_HILL_TOP = 3
BG_HILL = 4


def sprite_fill(game, sid, x0, y0, w, h, c) -> None:
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            game.set_sprite_pixel(sid, x, y, c)


def make_bg_tileset(game):
    sid = game.create_sprite(5 * TS, TS)
    sky = g.COLOR_RGB(135, 206, 235)

    sprite_fill(game, sid, BG_SKY * TS, 0, TS, TS, sky)

    ox = BG_CLOUD_L * TS
    sprite_fill(game, sid, ox, 0, TS, TS, sky)
    sprite_fill(game, sid, ox + 4, 6, 12, 6, g.COLOR_WHITE)
    sprite_fill(game, sid, ox + 6, 3, 8, 5, g.COLOR_WHITE)

    ox = BG_CLOUD_R * TS
    sprite_fill(game, sid, ox, 0, TS, TS, sky)
    sprite_fill(game, sid, ox, 6, 12, 6, g.COLOR_WHITE)
    sprite_fill(game, sid, ox + 2, 3, 8, 5, g.COLOR_WHITE)

    ox = BG_HILL_TOP * TS
    sprite_fill(game, sid, ox, 0, TS, TS, sky)
    for y in range(TS):
        hw = 1 + y * 7 // 15
        for x in range(8 - hw, 8 + hw):
            if 0 <= x < TS:
                game.set_sprite_pixel(sid, ox + x, y, g.COLOR_RGB(70, 130, 70))

    sprite_fill(game, sid, BG_HILL * TS, 0, TS, TS, g.COLOR_RGB(70, 130, 70))
    return sid


def main() -> None:
    game = g.GameLib()
    SW, SH = 640, 480
    _ = game.open(SW, SH, "10 - Tilemap Two-Layer Scrolling", True)
    game.show_fps(True)

    tileset_path = g.get_respath("../clib/assets/tileset.png")
    char_path = g.get_respath("../clib/assets/character.png")
    tree_path = g.get_respath("../clib/assets/tree.png")

    fg_ts = game.load_sprite(tileset_path)
    bg_ts = make_bg_tileset(game)
    char_spr = game.load_sprite(char_path)
    tree_spr = game.load_sprite(tree_path)

    # Create maps
    FG_C, FG_R = 80, 30
    BG_C, BG_R = 60, 30
    fg_map = game.create_tilemap(FG_C, FG_R, TS, fg_ts)
    bg_map = game.create_tilemap(BG_C, BG_R, TS, bg_ts)
    fg_cols = game.get_tilemap_cols(fg_map)
    fg_rows = game.get_tilemap_rows(fg_map)
    fg_tile_size = game.get_tile_size(fg_map)
    bg_rows = game.get_tilemap_rows(bg_map)
    fg_world_width = fg_cols * fg_tile_size
    fg_world_height = fg_rows * fg_tile_size

    # Fill background
    game.clear_tilemap(bg_map, BG_SKY)
    cloud_pos = [(5, 4), (18, 3), (33, 5), (48, 2), (55, 6)]
    for cx, cy in cloud_pos:
        game.set_tile(bg_map, cx, cy, BG_CLOUD_L)
        game.set_tile(bg_map, cx + 1, cy, BG_CLOUD_R)
    hills = [(8, 13, 24), (22, 30, 22), (40, 47, 25)]
    for h_start, h_end, h_top in hills:
        hill_cols = h_end - h_start
        game.fill_tile_rect(bg_map, h_start, h_top, hill_cols, 1, BG_HILL_TOP)
        game.fill_tile_rect(bg_map, h_start, h_top + 1, hill_cols, bg_rows - (h_top + 1), BG_HILL)

    # Fill foreground
    game.clear_tilemap(fg_map)
    game.fill_tile_rect(fg_map, 0, fg_rows - 3, fg_cols, 1, FG_GRASS)
    game.fill_tile_rect(fg_map, 0, fg_rows - 2, fg_cols, 2, FG_DIRT)
    game.fill_tile_rect(fg_map, 20, fg_rows - 3, 3, 3, -1)
    game.fill_tile_rect(fg_map, 48, fg_rows - 3, 3, 3, -1)
    game.fill_tile_rect(fg_map, 12, 23, 6, 1, FG_BRICK)
    game.fill_tile_rect(fg_map, 30, 20, 6, 1, FG_BRICK)
    game.fill_tile_rect(fg_map, 42, 24, 5, 1, FG_BRICK)
    for step in range(5):
        game.fill_tile_rect(fg_map, 60, fg_rows - 4 - step, step + 1, 1, FG_STONE)
    game.fill_tile_rect(fg_map, 66, 17, 7, 1, FG_STONE)

    # Trees (decoration)
    tree_x_list = [5 * TS, 25 * TS, 38 * TS, 55 * TS, 70 * TS]
    tree_y = (FG_R - 3) * TS - 61

    # Player
    player_x = 48.0
    player_y = float((fg_rows - 3) * fg_tile_size - CHAR_FOOT)
    speed = 180.0
    facing = 1

    while not game.is_closed():
        dt = game.get_delta_time()
        if dt > 0.05:
            dt = 0.05

        if game.is_key_down(g.KEY_RIGHT) or game.is_key_down(g.KEY_D):
            player_x += speed * dt
            facing = 1
        if game.is_key_down(g.KEY_LEFT) or game.is_key_down(g.KEY_A):
            player_x -= speed * dt
            facing = -1
        player_x = max(0.0, min(player_x, fg_world_width - CHAR_W))

        camera_x = player_x - SW / 2 + CHAR_W / 2
        max_cam = float(fg_world_width - SW)
        camera_x = max(0.0, min(camera_x, max_cam))

        foot_x = int(player_x) + CHAR_W // 2
        foot_y = int(player_y) + CHAR_FOOT
        foot_col = game.world_to_tile_col(fg_map, foot_x)
        foot_row = game.world_to_tile_row(fg_map, foot_y)
        foot_tile = game.get_tile_at_pixel(fg_map, foot_x, foot_y)

        game.clear(g.COLOR_RGB(135, 206, 235))

        game.draw_tilemap(bg_map, -int(camera_x * 0.5), 0)

        cam_x = int(camera_x)
        game.draw_tilemap(fg_map, -cam_x, 0)

        for tx in tree_x_list:
            game.draw_sprite_ex(tree_spr, tx - cam_x, tree_y, g.SPRITE_COLORKEY)

        px = int(player_x) - cam_x
        py = int(player_y)
        pflags = g.SPRITE_COLORKEY | (g.SPRITE_FLIP_H if facing < 0 else 0)
        game.draw_sprite_ex(char_spr, px, py, pflags)

        game.fill_rect(0, 0, 300, 50, g.COLOR_RGB(15, 15, 25))
        game.draw_text(8, 6, "<- -> / A D Move    ESC Quit", g.COLOR_WHITE)
        game.draw_printf(8, 20, g.COLOR_LIGHT_GRAY, f"Camera: {cam_x}   World: {fg_world_width}x{fg_world_height}")
        game.draw_printf(8, 34, g.COLOR_LIGHT_GRAY, f"Foot tile: ({foot_col},{foot_row}) = {foot_tile}")

        if game.is_key_pressed(g.KEY_ESCAPE):
            break
        game.update()
        game.wait_frame(60)

    game.free_tilemap(fg_map)
    game.free_tilemap(bg_map)
    game.free_sprite(char_spr)
    game.free_sprite(tree_spr)


if __name__ == "__main__":
    main()
