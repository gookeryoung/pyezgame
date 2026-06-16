// 15_ui_controls.cpp - Tabbed UI Controls Demo
//
// Demonstrates ALL immediate-mode UI helpers organized in tab pages:
//   Tab 1 BASIC    : Button, Checkbox, RadioBox, ToggleButton, Separator, Label
//   Tab 2 VALUES   : Slider, Spinner, ProgressBar, Knob, VSeparator
//   Tab 3 INPUT    : TextInput, Dropdown, TabBar, Tooltip
//   Tab 4 ADVANCED : ListBox, ColorPicker, Collapsible, ImageButton, Menu
//   Tab 5 STATUS   : status dashboard
//
// Controls:
//   Mouse left button : interact with all UI controls
//   Mouse wheel       : scroll in ListBox
//   Keyboard          : type in text input field
//   ESC               : quit
//
// Compile (Win32): g++ -o 15_ui_controls.exe 15_ui_controls.cpp -mwindows
// Compile (SDL):   g++ -std=c++11 -O2 -o 15_ui_controls 15_ui_controls.cpp -lSDL2

#if defined(_WIN32) && !defined(USE_SDL)
#include "../GameLib.h"
#else
#include "../GameLib.SDL.h"
#endif

#include <cstring>
#include <cstdio>

#define WIN_W 860
#define WIN_H 620

static void DrawPanel(GameLib &g, int x, int y, int w, int h, const char *title)
{
    g.FillRect(x, y, w, h, COLOR_RGB(28, 34, 50));
    g.DrawRect(x, y, w, h, COLOR_RGB(84, 94, 120));
    g.FillRect(x + 1, y + 1, w - 2, 20, COLOR_RGB(38, 48, 72));
    g.DrawText(x + 6, y + 6, title, COLOR_WHITE);
}

static void DrawBackdrop(GameLib &g)
{
    g.Clear(COLOR_RGB(18, 22, 34));
    for (int y = 0; y < g.GetHeight(); y += 40) {
        uint32_t stripe = ((y / 40) & 1) ? COLOR_RGB(20, 26, 40) : COLOR_RGB(16, 20, 32);
        g.FillRect(0, y, g.GetWidth(), 40, stripe);
    }
}

// ----- shared state struct -----
struct UIState {
    bool musicOn = true, sfxOn = true, showGrid = false, hardMode = false;
    int difficulty = 0;
    bool paused = false, turbo = false;
    int startCount = 0, resetCount = 0;
    const char *lastEvent = "NONE";
    bool quit = false;

    int volume = 75, brightness = 50, speed = 30;
    int hp = 100, level = 1, scoreMult = 1, knobVal = 50;

    char playerName[64] = "Player1";
    bool nameFocused = false;
    char searchText[64] = "";
    bool searchFocused = false;
    int resolutionIdx = 0; bool resolutionOpen = false;
    int qualityIdx = 1; bool qualityOpen = false;
    int innerTab = 0;

    const char *resolutions[5] = {"640x480","800x600","1024x768","1280x720","1920x1080"};
    const char *qualities[4] = {"LOW","MEDIUM","HIGH","ULTRA"};
    const char *tabNames[4] = {"GENERAL","GRAPHICS","AUDIO","CONTROLS"};

    const char *listItems[12] = {"APPLE","BANANA","CHERRY","DATE","ELDERBERRY",
                                 "FIG","GRAPE","HONEYDEW","KIWI","LEMON","MANGO","NECTARINE"};
    int listIdx = 0, listScroll = 0;
    bool sectionOpen = true, section2Open = false;

    uint32_t colorPalette[16] = {
        0xFF0000FF, 0xFF00FF00, 0xFFFF0000, 0xFFFFFF00,
        0xFF00FFFF, 0xFFFF00FF, 0xFFFFFFFF, 0xFF000000,
        0xFF800000, 0xFF008000, 0xFF000080, 0xFF808000,
        0xFF800080, 0xFF008080, 0xFFC0C0C0, 0xFF808080,
    };
    int colorIdx = 0;
    bool menuOpen = false;
    int menuResult = -1;
    const char *menuItems[5] = {"NEW GAME","LOAD GAME","OPTIONS","CREDITS","QUIT"};
    int iconId = -1;
};

static void ResetAll(UIState &s) {
    s.musicOn = true; s.sfxOn = true; s.showGrid = false; s.hardMode = false;
    s.difficulty = 0; s.paused = false; s.turbo = false;
    s.volume = 75; s.brightness = 50; s.speed = 30;
    s.hp = 100; s.level = 1; s.scoreMult = 1; s.knobVal = 50;
    strcpy(s.playerName, "Player1"); s.searchText[0] = '\0';
    s.resolutionIdx = 0; s.qualityIdx = 1; s.innerTab = 0;
    s.listIdx = 0; s.listScroll = 0;
    s.sectionOpen = true; s.section2Open = false;
    s.colorIdx = 0; s.menuOpen = false; s.menuResult = -1;
    s.resetCount++;
    s.lastEvent = "RESET";
}

// ----- Tab drawing functions -----

static void DrawBasicTab(GameLib &game, int cx, int cy, UIState &s)
{
    int pw = 170, gap = 8, px = cx + 4;
    DrawPanel(game, px, cy, pw, 280, "Buttons");
    DrawPanel(game, px+pw+gap, cy, pw, 280, "Checkboxes");
    DrawPanel(game, px+2*(pw+gap), cy, pw, 280, "RadioBox");
    DrawPanel(game, px+3*(pw+gap), cy, pw, 280, "Toggle & Label");

    // Buttons
    int bx = px+10, by = cy+28;
    if (game.Button(bx, by, 148, 26, "START", COLOR_RGB(52,150,92)))
        { s.startCount++; s.lastEvent = "START"; }
    if (game.Button(bx, by+36, 148, 26, "RESET", COLOR_RGB(196,142,46)))
        ResetAll(s);
    if (game.Button(bx, by+72, 148, 26, "QUIT", COLOR_RGB(180,76,76)))
        s.quit = true;
    game.Separator(bx, by+110, 148);
    game.DrawText(bx, by+120, "States: NORMAL", COLOR_LIGHT_GRAY);
    game.DrawText(bx, by+134, " HOVER / PRESSED", COLOR_LIGHT_GRAY);

    // Checkboxes
    int bx2 = px+pw+gap+10;
    game.Checkbox(bx2, by, "MUSIC", &s.musicOn);
    game.Checkbox(bx2, by+28, "SFX", &s.sfxOn);
    game.Checkbox(bx2, by+56, "SHOW GRID", &s.showGrid);
    game.Checkbox(bx2, by+84, "HARD MODE", &s.hardMode);
    game.Separator(bx2, by+120, 148);
    game.DrawText(bx2, by+130, "Click toggles", COLOR_LIGHT_GRAY);
    game.DrawText(bx2, by+144, "checkbox on/off.", COLOR_LIGHT_GRAY);

    // RadioBox
    int bx3 = px+2*(pw+gap)+10;
    game.RadioBox(bx3, by, "EASY", &s.difficulty, 0);
    game.RadioBox(bx3, by+28, "MEDIUM", &s.difficulty, 1);
    game.RadioBox(bx3, by+56, "HARD", &s.difficulty, 2);
    game.Separator(bx3, by+96, 148);
    const char *diffNames[] = {"EASY","MEDIUM","HARD"};
    game.DrawText(bx3, by+108, "Selected:", COLOR_WHITE);
    game.DrawText(bx3, by+122, diffNames[s.difficulty], COLOR_YELLOW);
    game.DrawText(bx3, by+146, "Group shares one", COLOR_LIGHT_GRAY);
    game.DrawText(bx3, by+160, "int value.", COLOR_LIGHT_GRAY);

    // Toggle & Label
    int bx4 = px+3*(pw+gap)+10;
    game.ToggleButton(bx4, by, 148, 26, "PAUSE", &s.paused, COLOR_RGB(180,76,76));
    game.ToggleButton(bx4, by+36, 148, 26, "TURBO", &s.turbo, COLOR_RGB(52,150,92));
    game.Separator(bx4, by+76, 148);
    game.DrawText(bx4, by+86, "PAUSED:", COLOR_WHITE);
    game.DrawText(bx4, by+100, s.paused ? "YES" : "NO", s.paused ? COLOR_YELLOW : COLOR_LIGHT_GRAY);
    game.Label(bx4, by+130, 148, 20, "LABEL WIDGET", COLOR_RGB(70,50,120), COLOR_WHITE);
    game.Label(bx4, by+158, 148, 20, "WITH BG COLOR", COLOR_RGB(50,100,70), COLOR_WHITE);
}

static void DrawValuesTab(GameLib &game, int cx, int cy, UIState &s)
{
    int pw = 240, gap = 8, px = cx + 4;
    DrawPanel(game, px, cy, pw, 280, "Sliders");
    DrawPanel(game, px+pw+gap, cy, pw, 280, "Spinners & Knob");
    DrawPanel(game, px+2*(pw+gap), cy, pw+50, 280, "Progress Bars");

    // Sliders
    int sx = px+10, sy = cy+30;
    game.DrawText(sx, sy, "VOLUME:", COLOR_WHITE);
    game.DrawPrintf(sx+100, sy, COLOR_YELLOW, "%d", s.volume);
    game.Slider(sx, sy+14, 218, &s.volume, 0, 100);

    game.DrawText(sx, sy+50, "BRIGHTNESS:", COLOR_WHITE);
    game.DrawPrintf(sx+100, sy+50, COLOR_YELLOW, "%d", s.brightness);
    game.Slider(sx, sy+64, 218, &s.brightness, 0, 100);

    game.DrawText(sx, sy+100, "SPEED:", COLOR_WHITE);
    game.DrawPrintf(sx+100, sy+100, COLOR_YELLOW, "%d", s.speed);
    game.Slider(sx, sy+114, 218, &s.speed, 0, 100);

    game.Separator(sx, sy+150, 218);
    game.DrawText(sx, sy+162, "Drag the handle", COLOR_LIGHT_GRAY);
    game.DrawText(sx, sy+176, "to adjust value.", COLOR_LIGHT_GRAY);

    // Spinners & Knob
    int sx2 = px+pw+gap+10;
    game.DrawText(sx2, sy+4, "HP:", COLOR_WHITE);
    game.Spinner(sx2+60, sy, 60, &s.hp, 0, 999, 10);
    game.DrawText(sx2, sy+48, "LEVEL:", COLOR_WHITE);
    game.Spinner(sx2+60, sy+44, 60, &s.level, 1, 99, 1);
    game.DrawText(sx2, sy+92, "MULT:", COLOR_WHITE);
    game.Spinner(sx2+60, sy+88, 60, &s.scoreMult, 1, 10, 1);
    game.VSeparator(sx2+140, sy, 130);

    game.DrawText(sx2+155, sy+4, "KNOB:", COLOR_WHITE);
    game.DrawPrintf(sx2+210, sy+4, COLOR_YELLOW, "%d", s.knobVal);
    game.Knob(sx2+162, sy+24, 56, &s.knobVal, 0, 100);
    game.ProgressBar(sx2+155, sy+88, 72, 12, s.knobVal, 100, COLOR_RGB(70,130,200));

    game.Separator(sx2, sy+150, 228);
    game.DrawText(sx2, sy+162, "Spinner: click -/+", COLOR_LIGHT_GRAY);
    game.DrawText(sx2, sy+176, "Knob: drag up/down", COLOR_LIGHT_GRAY);

    // Progress Bars
    int sx3 = px+2*(pw+gap)+10;
    game.DrawText(sx3, sy, "VOLUME:", COLOR_WHITE);
    game.ProgressBar(sx3, sy+14, 260, 16, s.volume, 100, COLOR_RGB(52,150,92));
    game.DrawText(sx3, sy+46, "BRIGHTNESS:", COLOR_WHITE);
    game.ProgressBar(sx3, sy+60, 260, 16, s.brightness, 100, COLOR_RGB(70,130,200));
    game.DrawText(sx3, sy+92, "SPEED:", COLOR_WHITE);
    game.ProgressBar(sx3, sy+106, 260, 16, s.speed, 100, COLOR_RGB(196,142,46));
    uint32_t hpColor = (s.hp > 500) ? COLOR_RGB(52,180,92) : COLOR_RGB(200,76,76);
    game.DrawText(sx3, sy+140, "HP:", COLOR_WHITE);
    game.ProgressBar(sx3, sy+154, 260, 16, s.hp, 999, hpColor);
    game.DrawText(sx3, sy+186, "KNOB:", COLOR_WHITE);
    game.ProgressBar(sx3, sy+200, 260, 16, s.knobVal, 100, COLOR_RGB(70,130,200));
    game.Separator(sx3, sy+230, 260);
    game.DrawText(sx3, sy+242, "Bars driven by", COLOR_LIGHT_GRAY);
    game.DrawText(sx3, sy+256, "slider/knob values.", COLOR_LIGHT_GRAY);
}

static void DrawInputTab(GameLib &game, int cx, int cy, UIState &s)
{
    int pw = 240, gap = 8, px = cx + 4;
    DrawPanel(game, px, cy, pw, 280, "Text Input");
    DrawPanel(game, px+pw+gap, cy, pw, 280, "Dropdown");
    DrawPanel(game, px+2*(pw+gap), cy, pw+50, 280, "TabBar & Tooltip");

    // Text Input
    int tx = px+10, ty = cy+30;
    game.DrawText(tx, ty, "NAME:", COLOR_WHITE);
    game.TextInput(tx+50, ty-4, 160, s.playerName, sizeof(s.playerName), &s.nameFocused);
    game.DrawPrintf(tx, ty+18, COLOR_YELLOW, "Hello, %s!", s.playerName);

    game.DrawText(tx, ty+50, "SEARCH:", COLOR_WHITE);
    game.TextInput(tx+56, ty+46, 154, s.searchText, sizeof(s.searchText), &s.searchFocused);
    if (s.searchText[0])
        game.DrawPrintf(tx, ty+68, COLOR_LIGHT_GRAY, "Query: %s", s.searchText);
    else
        game.DrawText(tx, ty+68, "Type to search...", COLOR_GRAY);
    game.Separator(tx, ty+96, 218);
    game.DrawText(tx, ty+108, "Click field to focus,", COLOR_LIGHT_GRAY);
    game.DrawText(tx, ty+122, "BACKSPACE to delete.", COLOR_LIGHT_GRAY);

    // Dropdown
    int dx = px+pw+gap+10, dy = cy+30;
    game.DrawText(dx, dy, "RESOLUTION:", COLOR_WHITE);
    game.Dropdown(dx, dy+14, 218, s.resolutions, 5, &s.resolutionIdx, &s.resolutionOpen);
    game.DrawText(dx, dy+54, "QUALITY:", COLOR_WHITE);
    game.Dropdown(dx, dy+68, 218, s.qualities, 4, &s.qualityIdx, &s.qualityOpen);
    game.Separator(dx, dy+108, 218);
    game.DrawPrintf(dx, dy+120, COLOR_LIGHT_GRAY, "Res: %s", s.resolutions[s.resolutionIdx]);
    game.DrawPrintf(dx, dy+136, COLOR_LIGHT_GRAY, "Quality: %s", s.qualities[s.qualityIdx]);

    // TabBar & Tooltip
    int tabx = px+2*(pw+gap)+10, taby = cy+30;
    game.TabBar(tabx, taby, 280, s.tabNames, 4, &s.innerTab);
    game.FillRect(tabx, taby+26, 280, 60, COLOR_RGB(58,68,92));
    const char *tabContents[] = {"General settings","Graphics options","Audio settings","Key bindings"};
    game.DrawText(tabx+10, taby+34, s.tabNames[s.innerTab], COLOR_YELLOW);
    game.DrawText(tabx+10, taby+50, tabContents[s.innerTab], COLOR_LIGHT_GRAY);
    game.DrawPrintf(tabx+10, taby+66, COLOR_WHITE, "Tab %d/4", s.innerTab+1);

    game.Separator(tabx, taby+106, 280);
    game.DrawText(tabx, taby+118, "Hover button for tip:", COLOR_LIGHT_GRAY);
    if (game.Button(tabx, taby+136, 120, 24, "HOVER ME", COLOR_RGB(100,80,160)))
        s.lastEvent = "HOVER BTN";
    int mx = game.GetMouseX(), my = game.GetMouseY();
    if (GameLib::PointInRect(mx, my, tabx, taby+136, 120, 24))
        game.Tooltip(mx+12, my+12, "Click to trigger!");
    if (game.Button(tabx+140, taby+136, 120, 24, "TIP BUTTON", COLOR_RGB(80,120,160)))
        s.lastEvent = "TIP BTN";
    if (GameLib::PointInRect(mx, my, tabx+140, taby+136, 120, 24))
        game.Tooltip(mx+12, my+12, "Another tooltip!");
}

static void DrawAdvancedTab(GameLib &game, int cx, int cy, UIState &s)
{
    int pw = 175, gap = 8, px = cx + 4;
    DrawPanel(game, px, cy, pw, 280, "ListBox");
    DrawPanel(game, px+pw+gap, cy, pw, 280, "ColorPicker");
    DrawPanel(game, px+2*(pw+gap), cy, pw, 280, "Collapsible");
    DrawPanel(game, px+3*(pw+gap), cy, pw+30, 280, "ImageButton & Menu");

    // ListBox
    int lx = px+6, ly = cy+26;
    game.ListBox(lx, ly, pw-12, 200, s.listItems, 12, &s.listIdx, &s.listScroll);
    game.DrawPrintf(lx, ly+210, COLOR_YELLOW, "Selected: %s", s.listItems[s.listIdx]);
    game.DrawText(lx, ly+228, "Scroll with wheel", COLOR_LIGHT_GRAY);

    // ColorPicker
    int cpx = px+pw+gap+6, cpy = cy+26;
    game.ColorPicker(cpx, cpy, s.colorPalette, 16, &s.colorIdx);
    uint32_t selColor = s.colorPalette[s.colorIdx];
    game.FillRect(cpx, cpy+70, pw-12, 18, selColor);
    game.DrawRect(cpx, cpy+70, pw-12, 18, COLOR_RGB(84,94,120));
    game.DrawPrintf(cpx, cpy+96, COLOR_LIGHT_GRAY, "R:%d G:%d B:%d",
                    COLOR_GET_R(selColor), COLOR_GET_G(selColor), COLOR_GET_B(selColor));
    game.DrawPrintf(cpx, cpy+112, COLOR_LIGHT_GRAY, "#%08X", selColor);

    // Collapsible
    int clx = px+2*(pw+gap)+6, cly = cy+26;
    game.Collapsible(clx, cly, pw-12, "DETAILS", &s.sectionOpen);
    if (s.sectionOpen) {
        game.FillRect(clx, cly+22, pw-12, 50, COLOR_RGB(40,46,62));
        game.DrawText(clx+8, cly+30, "Expanded content", COLOR_LIGHT_GRAY);
        game.DrawText(clx+8, cly+44, "inside section", COLOR_LIGHT_GRAY);
    }
    game.Collapsible(clx, cly+80, pw-12, "EXTRA", &s.section2Open);
    if (s.section2Open) {
        game.FillRect(clx, cly+102, pw-12, 36, COLOR_RGB(40,46,62));
        game.DrawText(clx+8, cly+110, "More content", COLOR_LIGHT_GRAY);
    }
    game.Separator(clx, cly+150, pw-12);
    game.DrawText(clx, cly+162, "Click header to", COLOR_LIGHT_GRAY);
    game.DrawText(clx, cly+176, "toggle open/close.", COLOR_LIGHT_GRAY);

    // ImageButton & Menu
    int ibx = px+3*(pw+gap)+6, iby = cy+26;
    if (game.ImageButton(ibx, iby, 50, 50, s.iconId, COLOR_RGB(60,70,100)))
        s.lastEvent = "IMAGE BTN";
    game.DrawText(ibx+60, iby+10, "ImageButton", COLOR_WHITE);
    game.DrawText(ibx+60, iby+26, "with sprite", COLOR_LIGHT_GRAY);

    game.Separator(ibx, iby+66, pw+18);
    if (game.Button(ibx, iby+78, 120, 24, "OPEN MENU", COLOR_RGB(80,120,160)))
        s.menuOpen = true;
    int menuResultIdx = game.Menu(ibx, iby+108, s.menuItems, 5, &s.menuOpen);
    if (menuResultIdx >= 0) {
        s.menuResult = menuResultIdx;
        s.lastEvent = "MENU";
    }
    game.DrawText(ibx, iby+118, "Last pick:", COLOR_WHITE);
    if (s.menuResult >= 0)
        game.DrawText(ibx, iby+134, s.menuItems[s.menuResult], COLOR_YELLOW);
    game.DrawText(ibx, iby+164, "Click outside to", COLOR_LIGHT_GRAY);
    game.DrawText(ibx, iby+178, "dismiss menu.", COLOR_LIGHT_GRAY);
}

static void DrawStatusTab(GameLib &game, int cx, int cy, UIState &s)
{
    int pw = 240, gap = 8, px = cx + 4;
    DrawPanel(game, px, cy, pw, 280, "Events");
    DrawPanel(game, px+pw+gap, cy, pw, 280, "Counts & Flags");
    DrawPanel(game, px+2*(pw+gap), cy, pw+50, 280, "All States");

    // Events
    int ex = px+10, ey = cy+28;
    game.Label(ex, ey, 218, 20, "LAST EVENT", COLOR_RGB(38,48,72), COLOR_WHITE);
    game.Label(ex, ey+28, 218, 20, s.lastEvent, COLOR_RGB(52,60,82), COLOR_YELLOW);
    game.Separator(ex, ey+60, 218);
    game.DrawText(ex, ey+72, "Interact with any", COLOR_LIGHT_GRAY);
    game.DrawText(ex, ey+86, "control to see its", COLOR_LIGHT_GRAY);
    game.DrawText(ex, ey+100, "event name here.", COLOR_LIGHT_GRAY);

    // Counts & Flags
    int fx = px+pw+gap+10, fy = cy+28;
    game.DrawText(fx, fy, "COUNTS", COLOR_WHITE);
    game.DrawPrintf(fx, fy+16, COLOR_LIGHT_GRAY, "START: %d", s.startCount);
    game.DrawPrintf(fx, fy+32, COLOR_LIGHT_GRAY, "RESET: %d", s.resetCount);
    game.Separator(fx, fy+56, 218);
    game.DrawText(fx, fy+68, "FLAGS", COLOR_WHITE);
    game.DrawPrintf(fx, fy+84, COLOR_LIGHT_GRAY, "MUSIC: %s", s.musicOn ? "ON" : "OFF");
    game.DrawPrintf(fx, fy+100, COLOR_LIGHT_GRAY, "SFX:   %s", s.sfxOn ? "ON" : "OFF");
    game.DrawPrintf(fx, fy+116, COLOR_LIGHT_GRAY, "GRID:  %s", s.showGrid ? "ON" : "OFF");
    game.DrawPrintf(fx, fy+132, COLOR_LIGHT_GRAY, "HARD:  %s", s.hardMode ? "ON" : "OFF");

    // All States
    int sx = px+2*(pw+gap)+10, sy = cy+28;
    const char *diffNames[] = {"EASY","MEDIUM","HARD"};
    game.DrawText(sx, sy, "CURRENT VALUES", COLOR_WHITE);
    game.DrawPrintf(sx, sy+16, COLOR_LIGHT_GRAY, "Volume:     %d", s.volume);
    game.DrawPrintf(sx, sy+32, COLOR_LIGHT_GRAY, "Brightness: %d", s.brightness);
    game.DrawPrintf(sx, sy+48, COLOR_LIGHT_GRAY, "Speed:      %d", s.speed);
    game.DrawPrintf(sx, sy+64, COLOR_LIGHT_GRAY, "HP:         %d", s.hp);
    game.DrawPrintf(sx, sy+80, COLOR_LIGHT_GRAY, "Level:      %d", s.level);
    game.DrawPrintf(sx, sy+96, COLOR_LIGHT_GRAY, "ScoreMult:  %d", s.scoreMult);
    game.DrawPrintf(sx, sy+112, COLOR_LIGHT_GRAY, "Knob:       %d", s.knobVal);
    game.Separator(sx, sy+136, 260);
    game.DrawPrintf(sx, sy+148, COLOR_LIGHT_GRAY, "Diff:  %s", diffNames[s.difficulty]);
    game.DrawPrintf(sx, sy+164, COLOR_LIGHT_GRAY, "Pause: %s Turbo: %s",
                    s.paused ? "Y" : "N", s.turbo ? "Y" : "N");
    game.DrawPrintf(sx, sy+180, COLOR_LIGHT_GRAY, "Res:   %s", s.resolutions[s.resolutionIdx]);
    game.DrawPrintf(sx, sy+196, COLOR_LIGHT_GRAY, "Name:  %s", s.playerName);
}

int main()
{
    GameLib game;
    game.Open(WIN_W, WIN_H, "15 - Tabbed UI Controls", true);

    UIState state;

    // create sprite for ImageButton
    state.iconId = game.CreateSprite(20, 20);
    for (int py = 0; py < 20; py++)
        for (int px = 0; px < 20; px++) {
            uint32_t c = ((px+py)%2==0) ? COLOR_RGB(px*12, py*12, 200) : COLOR_RGB(40,40,60);
            game.SetSpritePixel(state.iconId, px, py, c);
        }

    const char *tabNames[] = {"BASIC","VALUES","INPUT","ADVANCED","STATUS"};
    int activeTab = 0;

    while (!game.IsClosed()) {
        if (game.IsKeyPressed(KEY_ESCAPE)) break;
        if (state.quit) break;

        DrawBackdrop(game);

        // Title bar
        game.FillRect(0, 0, WIN_W, 44, COLOR_RGB(10, 14, 24));
        game.DrawTextScale(16, 10, "UI CONTROLS", COLOR_WHITE, 14, 14);
        game.DrawPrintf(16, 30, COLOR_LIGHT_GRAY, "Tab: %s  |  ESC quits", tabNames[activeTab]);

        // Main TabPanel
        activeTab = game.TabPanel(20, 52, WIN_W - 40, WIN_H - 62, tabNames, 5, activeTab);

        int cx = 24, cy = 82;  // content area approx

        if (activeTab == 0) DrawBasicTab(game, cx, cy, state);
        else if (activeTab == 1) DrawValuesTab(game, cx, cy, state);
        else if (activeTab == 2) DrawInputTab(game, cx, cy, state);
        else if (activeTab == 3) DrawAdvancedTab(game, cx, cy, state);
        else if (activeTab == 4) DrawStatusTab(game, cx, cy, state);

        game.Update();
        game.WaitFrame(60);
    }

    return 0;
}
