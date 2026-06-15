// 15_ui_controls.cpp - Enhanced UI Controls Demo
//
// Demonstrates the immediate-mode UI helpers:
//   Button, Checkbox, RadioBox, ToggleButton,
//   Slider, Spinner, ProgressBar, Separator, Label.
// Labels use the built-in 8x8 bitmap font, so keep them ASCII.
//
// Controls:
//   Mouse left button : interact with all UI controls
//   ESC               : quit
//
// Learn: Button, Checkbox, RadioBox, ToggleButton,
//        Slider, Spinner, ProgressBar, Separator, Label,
//        release-trigger UI, built-in 8x8 UI labels
//
// Compile (Win32): g++ -o 15_ui_controls.exe 15_ui_controls.cpp -mwindows
// Compile (SDL):   g++ -std=c++11 -O2 -o 15_ui_controls 15_ui_controls.cpp -lSDL2

#if defined(_WIN32) && !defined(USE_SDL)
#include "../GameLib.h"
#else
#include "../GameLib.SDL.h"
#endif

static void DrawPanel(GameLib &game, int x, int y, int w, int h, const char *title)
{
    game.FillRect(x, y, w, h, COLOR_RGB(28, 34, 50));
    game.DrawRect(x, y, w, h, COLOR_RGB(84, 94, 120));
    game.FillRect(x + 1, y + 1, w - 2, 22, COLOR_RGB(38, 48, 72));
    game.DrawText(x + 8, y + 7, title, COLOR_WHITE);
}

static void DrawBackdrop(GameLib &game, bool showGrid)
{
    game.Clear(COLOR_RGB(18, 22, 34));

    for (int y = 0; y < game.GetHeight(); y += 40) {
        uint32_t stripe = ((y / 40) & 1) ? COLOR_RGB(20, 26, 40) : COLOR_RGB(16, 20, 32);
        game.FillRect(0, y, game.GetWidth(), 40, stripe);
    }

    if (!showGrid) return;

    uint32_t gridColor = COLOR_ARGB(70, 120, 138, 168);
    for (int x = 0; x < game.GetWidth(); x += 20)
        game.DrawLine(x, 0, x, game.GetHeight() - 1, gridColor);
    for (int y = 0; y < game.GetHeight(); y += 20)
        game.DrawLine(0, y, game.GetWidth() - 1, y, gridColor);
}

int main()
{
    GameLib game;
    game.Open(1100, 620, "15 - UI Controls", true);

    // --- State variables ---
    bool musicOn = true, sfxOn = true, showGrid = false, hardMode = false;
    int difficulty = 0;
    bool paused = false, turbo = false;
    int startCount = 0, resetCount = 0;
    const char *lastEvent = "NONE";

    // --- New widget states ---
    int volume = 75;
    int brightness = 50;
    int speed = 30;
    int hp = 100;
    int level = 1;
    int scoreMult = 1;

    const char *diffNames[] = {"EASY", "MEDIUM", "HARD"};

    while (!game.IsClosed()) {
        if (game.IsKeyPressed(KEY_ESCAPE)) break;

        DrawBackdrop(game, showGrid);

        // === Top bar ===
        game.FillRect(0, 0, 1100, 56, COLOR_RGB(10, 14, 24));
        game.DrawTextScale(20, 14, "UI CONTROLS", COLOR_WHITE, 16, 16);
        game.DrawText(20, 40, "Mouse: press/release inside to trigger. ESC quits.", COLOR_LIGHT_GRAY);

        // =================================================================
        // ROW 1 - Original controls (y=70 .. y=300)
        // =================================================================

        DrawPanel(game, 20, 70, 180, 230, "Buttons");
        DrawPanel(game, 216, 70, 180, 230, "Checkboxes");
        DrawPanel(game, 412, 70, 180, 230, "RadioBox");
        DrawPanel(game, 608, 70, 180, 230, "Toggle");

        // --- Buttons ---
        if (game.Button(40, 108, 140, 28, "START", COLOR_RGB(52, 150, 92))) {
            startCount++; lastEvent = "START";
        }
        if (game.Button(40, 148, 140, 28, "RESET", COLOR_RGB(196, 142, 46))) {
            musicOn = true; sfxOn = true; showGrid = false; hardMode = false;
            volume = 75; brightness = 50; speed = 30;
            hp = 100; level = 1; scoreMult = 1;
            resetCount++; lastEvent = "RESET";
        }
        if (game.Button(40, 188, 140, 28, "QUIT", COLOR_RGB(180, 76, 76))) break;

        game.Separator(40, 228, 140);
        game.DrawText(40, 240, "States: NORMAL", COLOR_LIGHT_GRAY);
        game.DrawText(40, 256, " HOVER / PRESSED", COLOR_LIGHT_GRAY);

        // --- Checkboxes ---
        if (game.Checkbox(236, 108, "MUSIC", &musicOn))
            lastEvent = musicOn ? "MUSIC ON" : "MUSIC OFF";
        if (game.Checkbox(236, 140, "SFX", &sfxOn))
            lastEvent = sfxOn ? "SFX ON" : "SFX OFF";
        if (game.Checkbox(236, 172, "SHOW GRID", &showGrid))
            lastEvent = showGrid ? "GRID ON" : "GRID OFF";
        if (game.Checkbox(236, 204, "HARD MODE", &hardMode))
            lastEvent = hardMode ? "HARD ON" : "HARD OFF";

        game.Separator(236, 236, 140);
        game.DrawText(236, 248, "Click toggles the", COLOR_LIGHT_GRAY);
        game.DrawText(236, 264, "checkbox on/off.", COLOR_LIGHT_GRAY);

        // --- RadioBox ---
        if (game.RadioBox(432, 108, "EASY", &difficulty, 0)) lastEvent = "EASY";
        if (game.RadioBox(432, 140, "MEDIUM", &difficulty, 1)) lastEvent = "MEDIUM";
        if (game.RadioBox(432, 172, "HARD", &difficulty, 2)) lastEvent = "HARD";

        game.Separator(432, 208, 140);
        game.DrawText(432, 220, "Selected:", COLOR_WHITE);
        game.DrawText(432, 236, diffNames[difficulty], COLOR_YELLOW);
        game.DrawText(432, 260, "Group shares one", COLOR_LIGHT_GRAY);
        game.DrawText(432, 276, "int value.", COLOR_LIGHT_GRAY);

        // --- Toggle ---
        if (game.ToggleButton(628, 108, 140, 28, "PAUSE", &paused, COLOR_RGB(180, 76, 76)))
            lastEvent = paused ? "PAUSED" : "RESUME";
        if (game.ToggleButton(628, 148, 140, 28, "TURBO", &turbo, COLOR_RGB(52, 150, 92)))
            lastEvent = turbo ? "TURBO ON" : "TURBO OFF";

        game.Separator(628, 188, 140);
        game.DrawText(628, 200, "Toggled=ON shows", COLOR_WHITE);
        game.DrawText(628, 216, "sunken bevel.", COLOR_LIGHT_GRAY);
        game.DrawText(628, 244, "PAUSED:", COLOR_WHITE);
        game.DrawText(628, 260, paused ? "YES" : "NO", paused ? COLOR_YELLOW : COLOR_LIGHT_GRAY);

        // =================================================================
        // ROW 2 - New controls (y=316 .. y=606)
        // =================================================================

        DrawPanel(game, 20, 316, 260, 290, "Sliders");
        DrawPanel(game, 296, 316, 260, 290, "Spinners");
        DrawPanel(game, 572, 316, 260, 290, "Progress Bars");
        DrawPanel(game, 848, 316, 232, 290, "Status");

        // --- Sliders ---
        game.DrawText(40, 354, "VOLUME:", COLOR_WHITE);
        game.DrawPrintf(160, 354, COLOR_YELLOW, "%d", volume);
        game.Slider(40, 370, 220, &volume, 0, 100);

        game.DrawText(40, 402, "BRIGHTNESS:", COLOR_WHITE);
        game.DrawPrintf(160, 402, COLOR_YELLOW, "%d", brightness);
        game.Slider(40, 418, 220, &brightness, 0, 100);

        game.DrawText(40, 450, "SPEED:", COLOR_WHITE);
        game.DrawPrintf(160, 450, COLOR_YELLOW, "%d", speed);
        game.Slider(40, 466, 220, &speed, 0, 100);

        game.Separator(40, 498, 220);
        game.DrawText(40, 510, "Drag the handle to", COLOR_LIGHT_GRAY);
        game.DrawText(40, 526, "adjust the value.", COLOR_LIGHT_GRAY);
        game.DrawText(40, 556, "Range: 0 ~ 100", COLOR_LIGHT_GRAY);

        // --- Spinners ---
        game.DrawText(316, 354, "HP:", COLOR_WHITE);
        game.Spinner(370, 350, 120, &hp, 0, 999, 10);

        game.DrawText(316, 402, "LEVEL:", COLOR_WHITE);
        game.Spinner(370, 398, 120, &level, 1, 99, 1);

        game.DrawText(316, 450, "SCORE MULT:", COLOR_WHITE);
        game.Spinner(420, 446, 70, &scoreMult, 1, 10, 1);

        game.Separator(316, 498, 220);
        game.DrawText(316, 510, "Click -/+ buttons", COLOR_LIGHT_GRAY);
        game.DrawText(316, 526, "to change value.", COLOR_LIGHT_GRAY);
        game.DrawText(316, 556, "Step is configurable.", COLOR_LIGHT_GRAY);

        // --- Progress Bars ---
        game.DrawText(592, 354, "VOLUME BAR:", COLOR_WHITE);
        game.ProgressBar(592, 370, 220, 18, volume, 100, COLOR_RGB(52, 150, 92));

        game.DrawText(592, 402, "BRIGHTNESS BAR:", COLOR_WHITE);
        game.ProgressBar(592, 418, 220, 18, brightness, 100, COLOR_RGB(70, 130, 200));

        game.DrawText(592, 450, "LOADING BAR:", COLOR_WHITE);
        game.ProgressBar(592, 466, 220, 18, speed, 100, COLOR_RGB(196, 142, 46));

        game.Separator(592, 498, 220);
        game.DrawText(592, 510, "Bars are driven by", COLOR_LIGHT_GRAY);
        game.DrawText(592, 526, "slider values above.", COLOR_LIGHT_GRAY);

        // HP progress bar
        game.DrawText(592, 554, "HP:", COLOR_WHITE);
        uint32_t hpColor = (hp > 50) ? COLOR_RGB(52, 180, 92) : COLOR_RGB(200, 76, 76);
        game.ProgressBar(620, 550, 192, 18, hp, 999, hpColor);

        // --- Status panel ---
        game.Label(858, 350, 212, 20, "LAST EVENT", COLOR_RGB(38, 48, 72), COLOR_WHITE);
        game.Label(858, 376, 212, 20, lastEvent, COLOR_RGB(52, 60, 82), COLOR_YELLOW);

        game.DrawText(858, 410, "COUNTS", COLOR_WHITE);
        game.DrawPrintf(858, 426, COLOR_LIGHT_GRAY, "START: %d", startCount);
        game.DrawPrintf(858, 442, COLOR_LIGHT_GRAY, "RESET: %d", resetCount);

        game.Separator(858, 462, 212);

        game.DrawText(858, 474, "FLAGS", COLOR_WHITE);
        game.DrawPrintf(858, 490, COLOR_LIGHT_GRAY, "MUSIC:%s", musicOn ? "ON" : "OFF");
        game.DrawPrintf(858, 506, COLOR_LIGHT_GRAY, "SFX:  %s", sfxOn ? "ON" : "OFF");
        game.DrawPrintf(858, 522, COLOR_LIGHT_GRAY, "GRID: %s", showGrid ? "ON" : "OFF");
        game.DrawPrintf(858, 538, COLOR_LIGHT_GRAY, "HARD: %s", hardMode ? "ON" : "OFF");

        game.DrawPrintf(858, 558, COLOR_LIGHT_GRAY, "DIFF:%s", diffNames[difficulty]);
        game.DrawPrintf(858, 574, COLOR_LIGHT_GRAY, "PAUSE:%s TURBO:%s",
                        paused ? "Y" : "N", turbo ? "Y" : "N");

        game.Update();
        game.WaitFrame(60);
    }

    return 0;
}
