"""06_sound.py - Sound Demo

Demo GameLib sound features: beep, multi-channel WAV, background music.
Learn: play_beep, play_wav, stop_wav, is_playing, set_volume, stop_all,
       set_master_volume, get_master_volume, play_music, stop_music
"""
import os
import pyezgame as g

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def choose_existing_path(path_a, path_b):
    if os.path.isfile(path_a):
        return path_a
    if os.path.isfile(path_b):
        return path_b
    abs_a = os.path.join(SCRIPT_DIR, path_a)
    abs_b = os.path.join(SCRIPT_DIR, path_b)
    if os.path.isfile(abs_a):
        return abs_a
    if os.path.isfile(abs_b):
        return abs_b
    return path_a


def main():
    game = g.GameLib()
    game.open(640, 480, "06 - Sound Demo", True)

    last_wav_channel = -1
    last_music_ok = True
    wav_effect = choose_existing_path("../clib/assets/sound/explosion.wav",
                                      "assets/sound/explosion.wav")
    music_file = choose_existing_path("../clib/assets/music/battle1.mid",
                                      "assets/music/battle1.mid")
    music_label = "Background Music (MCI MIDI):"
    music_hint = "(uses assets/music/battle1.mid via MCI sequencer)"

    # Key note frequencies (C4 to B4)
    notes = [262, 294, 330, 349, 392, 440, 494, 523]
    note_names = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        game.clear(g.COLOR_DARK_BLUE)

        # --- Title ---
        game.draw_text_scale(180, 20, "Sound Demo", g.COLOR_GOLD, 16, 16)

        # === Section 1: Beep Piano ===
        game.draw_text(40, 70, "Piano (Beep) - Press 1~8:", g.COLOR_WHITE)
        game.draw_text(40, 85, "Non-blocking, returns channel ID", g.COLOR_GREEN)

        active_note = -1
        key_map = [g.KEY_1, g.KEY_2, g.KEY_3, g.KEY_4,
                   g.KEY_5, g.KEY_6, g.KEY_7, g.KEY_8]
        for i in range(8):
            bx = 40 + i * 70
            by = 105
            pressed = game.is_key_pressed(key_map[i])
            if pressed:
                active_note = i

            key_color = g.COLOR_YELLOW if active_note == i else g.COLOR_WHITE
            game.fill_rect(bx, by, 55, 100, key_color)
            game.draw_rect(bx, by, 55, 100, g.COLOR_BLACK)
            game.draw_text(bx + 20, by + 75, note_names[i], g.COLOR_BLACK)

            if pressed:
                game.play_beep(notes[i], 150)

        # === Section 2: Multi-Channel WAV Sound ===
        game.draw_text(40, 230, "WAV Sound Effect (multi-channel):", g.COLOR_WHITE)

        game.fill_rect(40, 250, 200, 30, g.COLOR_GREEN)
        game.draw_text(55, 258, "W - Play WAV", g.COLOR_BLACK)
        if game.is_key_pressed(g.KEY_W):
            last_wav_channel = game.play_wav(wav_effect, 1, 800)

        game.fill_rect(260, 250, 200, 30, g.COLOR_RED)
        game.draw_text(290, 258, "S - Stop WAV", g.COLOR_BLACK)
        if game.is_key_pressed(g.KEY_S):
            if last_wav_channel > 0:
                game.stop_wav(last_wav_channel)
            last_wav_channel = -1

        game.fill_rect(460, 250, 140, 30, g.COLOR_ORANGE)
        game.draw_text(480, 258, "A - Stop All", g.COLOR_BLACK)
        if game.is_key_pressed(g.KEY_A):
            game.stop_all()

        game.draw_text(40, 290, "(uses assets/sound/explosion.wav)", g.COLOR_GRAY)
        game.draw_printf(40, 305, g.COLOR_LIGHT_GRAY, f"Last WAV channel: {last_wav_channel}")
        if last_wav_channel > 0:
            playing = "Yes" if game.is_playing(last_wav_channel) == 1 else "No"
            game.draw_printf(40, 320, g.COLOR_LIGHT_GRAY, f"Playing: {playing}")

        # === Section 3: Master Volume ===
        game.draw_text(40, 340, "Master Volume: +/- to adjust", g.COLOR_WHITE)
        master_vol = game.get_master_volume()
        if game.is_key_pressed(g.KEY_ADD):
            master_vol = game.set_master_volume(master_vol + 100)
        if game.is_key_pressed(g.KEY_SUBTRACT):
            master_vol = game.set_master_volume(master_vol - 100)
        game.draw_printf(40, 355, g.COLOR_LIGHT_GRAY, f"Volume: {master_vol}/1000")

        # === Section 4: Background Music ===
        game.draw_text(40, 380, music_label, g.COLOR_WHITE)

        music_playing = game.is_music_playing()

        game.fill_rect(40, 400, 200, 30,
                        g.COLOR_DARK_GREEN if music_playing else g.COLOR_GREEN)
        game.draw_text(55, 408, "M - Play Music", g.COLOR_BLACK)
        if game.is_key_pressed(g.KEY_M) and not music_playing:
            last_music_ok = game.play_music(music_file)
            music_playing = game.is_music_playing()

        game.fill_rect(260, 400, 200, 30, g.COLOR_RED)
        game.draw_text(275, 408, "N - Stop Music", g.COLOR_BLACK)
        if game.is_key_pressed(g.KEY_N) and music_playing:
            game.stop_music()

        music_status = "Playing" if game.is_music_playing() else "Stopped"
        game.draw_printf(40, 445, g.COLOR_LIGHT_GRAY, f"Music: {music_status}")
        last_status = "OK" if last_music_ok else "Failed"
        game.draw_printf(40, 460, g.COLOR_LIGHT_GRAY, f"Last music start: {last_status}")

        game.draw_text(40, 430, music_hint, g.COLOR_GRAY)
        game.draw_text(40, 470, "ESC to exit", g.COLOR_DARK_GRAY)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
