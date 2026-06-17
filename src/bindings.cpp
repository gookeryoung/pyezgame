/**
 * GameLib Python Bindings
 * nanobind wrapper for GameLib
 * - Windows: uses GameLib.h (Win32 GDI backend)
 * - Linux/macOS: uses GameLib.SDL.h (SDL2 backend)
 */

#ifdef _WIN32
    #define GAMELIB_IMPLEMENTATION
    #include "../clib/GameLib.h"
#else
    #define GAMELIB_SDL_IMPLEMENTATION
    #include "../clib/GameLib.SDL.h"
#endif

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

namespace nb = nanobind;

NB_MODULE(_pyezgame, m) {
    m.doc() = "Python bindings for GameLib - a beginner-friendly game development library";

    // =========================================================================
    // Constants: Colors
    // =========================================================================
    m.attr("COLOR_BLACK")       = COLOR_BLACK;
    m.attr("COLOR_WHITE")       = COLOR_WHITE;
    m.attr("COLOR_RED")         = COLOR_RED;
    m.attr("COLOR_GREEN")       = COLOR_GREEN;
    m.attr("COLOR_BLUE")        = COLOR_BLUE;
    m.attr("COLOR_YELLOW")      = COLOR_YELLOW;
    m.attr("COLOR_CYAN")        = COLOR_CYAN;
    m.attr("COLOR_MAGENTA")     = COLOR_MAGENTA;
    m.attr("COLOR_ORANGE")      = COLOR_ORANGE;
    m.attr("COLOR_PINK")        = COLOR_PINK;
    m.attr("COLOR_PURPLE")      = COLOR_PURPLE;
    m.attr("COLOR_GRAY")        = COLOR_GRAY;
    m.attr("COLOR_DARK_GRAY")   = COLOR_DARK_GRAY;
    m.attr("COLOR_LIGHT_GRAY")  = COLOR_LIGHT_GRAY;
    m.attr("COLOR_DARK_RED")    = COLOR_DARK_RED;
    m.attr("COLOR_DARK_GREEN")  = COLOR_DARK_GREEN;
    m.attr("COLOR_DARK_BLUE")   = COLOR_DARK_BLUE;
    m.attr("COLOR_SKY_BLUE")    = COLOR_SKY_BLUE;
    m.attr("COLOR_BROWN")       = COLOR_BROWN;
    m.attr("COLOR_GOLD")        = COLOR_GOLD;
    m.attr("COLOR_TRANSPARENT") = COLOR_TRANSPARENT;
    m.attr("COLORKEY_DEFAULT")  = COLORKEY_DEFAULT;

    // Color helper functions
    m.def("COLOR_RGB", [](int r, int g, int b) {
        return (uint32_t)(0xFF000000 | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF));
    }, "Create RGB color", nb::arg("r"), nb::arg("g"), nb::arg("b"));

    m.def("COLOR_ARGB", [](int a, int r, int g, int b) {
        return (uint32_t)(((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF));
    }, "Create ARGB color", nb::arg("a"), nb::arg("r"), nb::arg("g"), nb::arg("b"));

    m.def("COLOR_GET_A", [](uint32_t c) { return (c >> 24) & 0xFF; }, "Get alpha component");
    m.def("COLOR_GET_R", [](uint32_t c) { return (c >> 16) & 0xFF; }, "Get red component");
    m.def("COLOR_GET_G", [](uint32_t c) { return (c >> 8) & 0xFF; }, "Get green component");
    m.def("COLOR_GET_B", [](uint32_t c) { return c & 0xFF; }, "Get blue component");

    // =========================================================================
    // Constants: Keyboard
    // =========================================================================
    m.attr("KEY_LEFT")     = KEY_LEFT;
    m.attr("KEY_RIGHT")    = KEY_RIGHT;
    m.attr("KEY_UP")       = KEY_UP;
    m.attr("KEY_DOWN")     = KEY_DOWN;
    m.attr("KEY_SPACE")    = KEY_SPACE;
    m.attr("KEY_ENTER")    = KEY_ENTER;
    m.attr("KEY_ESCAPE")   = KEY_ESCAPE;
    m.attr("KEY_TAB")      = KEY_TAB;
    m.attr("KEY_SHIFT")    = KEY_SHIFT;
    m.attr("KEY_CONTROL")  = KEY_CONTROL;
    m.attr("KEY_BACK")     = KEY_BACK;

    // Letter keys
    m.attr("KEY_A") = KEY_A; m.attr("KEY_B") = KEY_B; m.attr("KEY_C") = KEY_C;
    m.attr("KEY_D") = KEY_D; m.attr("KEY_E") = KEY_E; m.attr("KEY_F") = KEY_F;
    m.attr("KEY_G") = KEY_G; m.attr("KEY_H") = KEY_H; m.attr("KEY_I") = KEY_I;
    m.attr("KEY_J") = KEY_J; m.attr("KEY_K") = KEY_K; m.attr("KEY_L") = KEY_L;
    m.attr("KEY_M") = KEY_M; m.attr("KEY_N") = KEY_N; m.attr("KEY_O") = KEY_O;
    m.attr("KEY_P") = KEY_P; m.attr("KEY_Q") = KEY_Q; m.attr("KEY_R") = KEY_R;
    m.attr("KEY_S") = KEY_S; m.attr("KEY_T") = KEY_T; m.attr("KEY_U") = KEY_U;
    m.attr("KEY_V") = KEY_V; m.attr("KEY_W") = KEY_W; m.attr("KEY_X") = KEY_X;
    m.attr("KEY_Y") = KEY_Y; m.attr("KEY_Z") = KEY_Z;

    // Number keys
    m.attr("KEY_0") = KEY_0; m.attr("KEY_1") = KEY_1; m.attr("KEY_2") = KEY_2;
    m.attr("KEY_3") = KEY_3; m.attr("KEY_4") = KEY_4; m.attr("KEY_5") = KEY_5;
    m.attr("KEY_6") = KEY_6; m.attr("KEY_7") = KEY_7; m.attr("KEY_8") = KEY_8;
    m.attr("KEY_9") = KEY_9;

    // Function keys
    m.attr("KEY_F1")  = KEY_F1;  m.attr("KEY_F2")  = KEY_F2;  m.attr("KEY_F3")  = KEY_F3;
    m.attr("KEY_F4")  = KEY_F4;  m.attr("KEY_F5")  = KEY_F5;  m.attr("KEY_F6")  = KEY_F6;
    m.attr("KEY_F7")  = KEY_F7;  m.attr("KEY_F8")  = KEY_F8;  m.attr("KEY_F9")  = KEY_F9;
    m.attr("KEY_F10") = KEY_F10; m.attr("KEY_F11") = KEY_F11; m.attr("KEY_F12") = KEY_F12;
    m.attr("KEY_ADD")      = KEY_ADD;
    m.attr("KEY_SUBTRACT") = KEY_SUBTRACT;

    // =========================================================================
    // Constants: Mouse
    // =========================================================================
    m.attr("MOUSE_LEFT")   = MOUSE_LEFT;
    m.attr("MOUSE_RIGHT")  = MOUSE_RIGHT;
    m.attr("MOUSE_MIDDLE") = MOUSE_MIDDLE;

    // =========================================================================
    // Constants: Message Box
    // =========================================================================
    m.attr("MESSAGEBOX_OK")          = MESSAGEBOX_OK;
    m.attr("MESSAGEBOX_YESNO")       = MESSAGEBOX_YESNO;
    m.attr("MESSAGEBOX_RESULT_OK")   = MESSAGEBOX_RESULT_OK;
    m.attr("MESSAGEBOX_RESULT_YES")  = MESSAGEBOX_RESULT_YES;
    m.attr("MESSAGEBOX_RESULT_NO")   = MESSAGEBOX_RESULT_NO;

    // =========================================================================
    // Constants: Sprite Flags
    // =========================================================================
    m.attr("SPRITE_FLIP_H")   = SPRITE_FLIP_H;
    m.attr("SPRITE_FLIP_V")   = SPRITE_FLIP_V;
    m.attr("SPRITE_COLORKEY") = SPRITE_COLORKEY;
    m.attr("SPRITE_ALPHA")    = SPRITE_ALPHA;

    // =========================================================================
    // GameLib Class
    // =========================================================================
    nb::class_<GameLib>(m, "GameLib")
        .def(nb::init<>())

        // ---- Window and Main Loop ----
        .def("open", &GameLib::Open,
             nb::arg("width"), nb::arg("height"), nb::arg("title"),
             nb::arg("center") = false, nb::arg("resizable") = false)
        .def("is_closed", &GameLib::IsClosed)
        .def("update", &GameLib::Update)
        .def("wait_frame", &GameLib::WaitFrame, nb::arg("fps"))
        .def("get_delta_time", &GameLib::GetDeltaTime)
        .def("get_fps", &GameLib::GetFPS)
        .def("get_time", &GameLib::GetTime)
        .def("get_width", &GameLib::GetWidth)
        .def("get_height", &GameLib::GetHeight)
        .def("win_resize", &GameLib::WinResize, nb::arg("width"), nb::arg("height"))
        .def("set_maximized", &GameLib::SetMaximized, nb::arg("maximized"))
        .def("set_title", &GameLib::SetTitle, nb::arg("title"))
        .def("show_fps", &GameLib::ShowFps, nb::arg("show"))
        .def("show_mouse", &GameLib::ShowMouse, nb::arg("show"))
        .def("aspect_lock", &GameLib::AspectLock,
             nb::arg("lock"), nb::arg("color") = COLOR_BLACK)
        .def("show_message", &GameLib::ShowMessage,
             nb::arg("text"), nb::arg("title") = nullptr,
             nb::arg("buttons") = MESSAGEBOX_OK)

        // ---- Framebuffer ----
        .def("clear", &GameLib::Clear, nb::arg("color") = COLOR_BLACK)
        .def("set_pixel", &GameLib::SetPixel, nb::arg("x"), nb::arg("y"), nb::arg("color"))
        .def("get_pixel", &GameLib::GetPixel, nb::arg("x"), nb::arg("y"))
        .def("set_clip", &GameLib::SetClip,
             nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"))
        .def("clear_clip", &GameLib::ClearClip)
        .def("get_clip", [](const GameLib& self) {
            int x, y, w, h;
            self.GetClip(&x, &y, &w, &h);
            return nb::make_tuple(x, y, w, h);
        })
        .def("get_clip_x", &GameLib::GetClipX)
        .def("get_clip_y", &GameLib::GetClipY)
        .def("get_clip_w", &GameLib::GetClipW)
        .def("get_clip_h", &GameLib::GetClipH)
        .def("screenshot", &GameLib::Screenshot, nb::arg("filename"))

        // ---- Drawing ----
        .def("draw_line", &GameLib::DrawLine,
             nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"), nb::arg("color"))
        .def("draw_rect", &GameLib::DrawRect,
             nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"), nb::arg("color"))
        .def("fill_rect", &GameLib::FillRect,
             nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"), nb::arg("color"))
        .def("draw_circle", &GameLib::DrawCircle,
             nb::arg("cx"), nb::arg("cy"), nb::arg("r"), nb::arg("color"))
        .def("fill_circle", &GameLib::FillCircle,
             nb::arg("cx"), nb::arg("cy"), nb::arg("r"), nb::arg("color"))
        .def("draw_ellipse", &GameLib::DrawEllipse,
             nb::arg("cx"), nb::arg("cy"), nb::arg("rx"), nb::arg("ry"), nb::arg("color"))
        .def("fill_ellipse", &GameLib::FillEllipse,
             nb::arg("cx"), nb::arg("cy"), nb::arg("rx"), nb::arg("ry"), nb::arg("color"))
        .def("draw_triangle", &GameLib::DrawTriangle,
             nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"),
             nb::arg("x3"), nb::arg("y3"), nb::arg("color"))
        .def("fill_triangle", &GameLib::FillTriangle,
             nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"),
             nb::arg("x3"), nb::arg("y3"), nb::arg("color"))

        // ---- Text Rendering (built-in 8x8 font) ----
        .def("draw_text", &GameLib::DrawText,
             nb::arg("x"), nb::arg("y"), nb::arg("text"), nb::arg("color"))
        .def("draw_number", &GameLib::DrawNumber,
             nb::arg("x"), nb::arg("y"), nb::arg("number"), nb::arg("color"))
        .def("draw_text_scale", &GameLib::DrawTextScale,
             nb::arg("x"), nb::arg("y"), nb::arg("text"), nb::arg("color"),
             nb::arg("w"), nb::arg("h"))
        .def("draw_printf", [](GameLib& self, int x, int y, uint32_t color, const char* text) {
            self.DrawText(x, y, text, color);
        }, nb::arg("x"), nb::arg("y"), nb::arg("color"), nb::arg("text"))
        .def("draw_printf_scale", [](GameLib& self, int x, int y, uint32_t color, int w, int h, const char* text) {
            self.DrawTextScale(x, y, text, color, w, h);
        }, nb::arg("x"), nb::arg("y"), nb::arg("color"), nb::arg("w"), nb::arg("h"), nb::arg("text"))

        // ---- Font Text Rendering (scalable fonts) ----
        .def("draw_text_font",
             nb::overload_cast<int, int, const char*, uint32_t, const char*, int>(
                 &GameLib::DrawTextFont),
             nb::arg("x"), nb::arg("y"), nb::arg("text"), nb::arg("color"),
             nb::arg("font_name"), nb::arg("font_size"))
        .def("draw_text_font",
             nb::overload_cast<int, int, const char*, uint32_t, int>(
                 &GameLib::DrawTextFont),
             nb::arg("x"), nb::arg("y"), nb::arg("text"), nb::arg("color"),
             nb::arg("font_size"))
        .def("get_text_width_font",
             nb::overload_cast<const char*, const char*, int>(
                 &GameLib::GetTextWidthFont),
             nb::arg("text"), nb::arg("font_name"), nb::arg("font_size"))
        .def("get_text_width_font",
             nb::overload_cast<const char*, int>(
                 &GameLib::GetTextWidthFont),
             nb::arg("text"), nb::arg("font_size"))
        .def("get_text_height_font",
             nb::overload_cast<const char*, const char*, int>(
                 &GameLib::GetTextHeightFont),
             nb::arg("text"), nb::arg("font_name"), nb::arg("font_size"))
        .def("get_text_height_font",
             nb::overload_cast<const char*, int>(
                 &GameLib::GetTextHeightFont),
             nb::arg("text"), nb::arg("font_size"))
        .def("draw_printf_font",
             [](GameLib& self, int x, int y, uint32_t color, const char* font_name, int font_size, const char* text) {
                 self.DrawTextFont(x, y, text, color, font_name, font_size);
             }, nb::arg("x"), nb::arg("y"), nb::arg("color"), nb::arg("font_name"), nb::arg("font_size"), nb::arg("text"))
        .def("draw_printf_font",
             [](GameLib& self, int x, int y, uint32_t color, int font_size, const char* text) {
                 self.DrawTextFont(x, y, text, color, font_size);
             }, nb::arg("x"), nb::arg("y"), nb::arg("color"), nb::arg("font_size"), nb::arg("text"))

        // ---- Sprite System ----
        .def("create_sprite", &GameLib::CreateSprite,
             nb::arg("width"), nb::arg("height"))
        .def("load_sprite", &GameLib::LoadSprite, nb::arg("filename"))
        .def("load_sprite_bmp", &GameLib::LoadSpriteBMP, nb::arg("filename"))
        .def("free_sprite", &GameLib::FreeSprite, nb::arg("id"))
        .def("draw_sprite", &GameLib::DrawSprite,
             nb::arg("id"), nb::arg("x"), nb::arg("y"))
        .def("draw_sprite_ex", &GameLib::DrawSpriteEx,
             nb::arg("id"), nb::arg("x"), nb::arg("y"), nb::arg("flags"))
        .def("draw_sprite_region", &GameLib::DrawSpriteRegion,
             nb::arg("id"), nb::arg("x"), nb::arg("y"),
             nb::arg("sx"), nb::arg("sy"), nb::arg("sw"), nb::arg("sh"))
        .def("draw_sprite_region_ex", &GameLib::DrawSpriteRegionEx,
             nb::arg("id"), nb::arg("x"), nb::arg("y"),
             nb::arg("sx"), nb::arg("sy"), nb::arg("sw"), nb::arg("sh"),
             nb::arg("flags") = 0)
        .def("draw_sprite_scaled", &GameLib::DrawSpriteScaled,
             nb::arg("id"), nb::arg("x"), nb::arg("y"),
             nb::arg("w"), nb::arg("h"), nb::arg("flags") = 0)
        .def("draw_sprite_rotated", &GameLib::DrawSpriteRotated,
             nb::arg("id"), nb::arg("cx"), nb::arg("cy"),
             nb::arg("angle_deg"), nb::arg("flags") = 0)
        .def("draw_sprite_frame", &GameLib::DrawSpriteFrame,
             nb::arg("id"), nb::arg("x"), nb::arg("y"),
             nb::arg("frame_w"), nb::arg("frame_h"), nb::arg("frame_index"),
             nb::arg("flags") = 0)
        .def("draw_sprite_frame_scaled", &GameLib::DrawSpriteFrameScaled,
             nb::arg("id"), nb::arg("x"), nb::arg("y"),
             nb::arg("frame_w"), nb::arg("frame_h"), nb::arg("frame_index"),
             nb::arg("w"), nb::arg("h"), nb::arg("flags") = 0)
        .def("draw_sprite_frame_rotated", &GameLib::DrawSpriteFrameRotated,
             nb::arg("id"), nb::arg("cx"), nb::arg("cy"),
             nb::arg("frame_w"), nb::arg("frame_h"), nb::arg("frame_index"),
             nb::arg("angle_deg"), nb::arg("flags") = 0)
        .def("set_sprite_pixel", &GameLib::SetSpritePixel,
             nb::arg("id"), nb::arg("x"), nb::arg("y"), nb::arg("color"))
        .def("get_sprite_pixel", &GameLib::GetSpritePixel,
             nb::arg("id"), nb::arg("x"), nb::arg("y"))
        .def("get_sprite_width", &GameLib::GetSpriteWidth, nb::arg("id"))
        .def("get_sprite_height", &GameLib::GetSpriteHeight, nb::arg("id"))
        .def("set_sprite_color_key", &GameLib::SetSpriteColorKey,
             nb::arg("id"), nb::arg("color"))
        .def("get_sprite_color_key", &GameLib::GetSpriteColorKey, nb::arg("id"))

        // ---- Tilemap System ----
        .def("create_tilemap", &GameLib::CreateTilemap,
             nb::arg("cols"), nb::arg("rows"), nb::arg("tile_size"), nb::arg("tileset_id"))
        .def("save_tilemap", &GameLib::SaveTilemap,
             nb::arg("filename"), nb::arg("map_id"))
        .def("load_tilemap", &GameLib::LoadTilemap,
             nb::arg("filename"), nb::arg("tileset_id"))
        .def("free_tilemap", &GameLib::FreeTilemap, nb::arg("map_id"))
        .def("set_tile", &GameLib::SetTile,
             nb::arg("map_id"), nb::arg("col"), nb::arg("row"), nb::arg("tile_id"))
        .def("get_tile", &GameLib::GetTile,
             nb::arg("map_id"), nb::arg("col"), nb::arg("row"))
        .def("get_tilemap_cols", &GameLib::GetTilemapCols, nb::arg("map_id"))
        .def("get_tilemap_rows", &GameLib::GetTilemapRows, nb::arg("map_id"))
        .def("get_tile_size", &GameLib::GetTileSize, nb::arg("map_id"))
        .def("world_to_tile_col", &GameLib::WorldToTileCol,
             nb::arg("map_id"), nb::arg("x"))
        .def("world_to_tile_row", &GameLib::WorldToTileRow,
             nb::arg("map_id"), nb::arg("y"))
        .def("get_tile_at_pixel", &GameLib::GetTileAtPixel,
             nb::arg("map_id"), nb::arg("x"), nb::arg("y"))
        .def("fill_tile_rect", &GameLib::FillTileRect,
             nb::arg("map_id"), nb::arg("col"), nb::arg("row"),
             nb::arg("cols"), nb::arg("rows"), nb::arg("tile_id"))
        .def("clear_tilemap", &GameLib::ClearTilemap,
             nb::arg("map_id"), nb::arg("tile_id") = -1)
        .def("draw_tilemap", &GameLib::DrawTilemap,
             nb::arg("map_id"), nb::arg("x"), nb::arg("y"), nb::arg("flags") = 0)

        // ---- Grid Helpers ----
        .def("draw_grid", &GameLib::DrawGrid,
             nb::arg("x"), nb::arg("y"), nb::arg("rows"), nb::arg("cols"),
             nb::arg("cell_size"), nb::arg("color"))
        .def("fill_cell", &GameLib::FillCell,
             nb::arg("grid_x"), nb::arg("grid_y"), nb::arg("row"), nb::arg("col"),
             nb::arg("cell_size"), nb::arg("color"))

        // ---- Input ----
        .def("is_key_down", &GameLib::IsKeyDown, nb::arg("key"))
        .def("is_key_pressed", &GameLib::IsKeyPressed, nb::arg("key"))
        .def("is_key_released", &GameLib::IsKeyReleased, nb::arg("key"))
        .def("get_mouse_x", &GameLib::GetMouseX)
        .def("get_mouse_y", &GameLib::GetMouseY)
        .def("is_mouse_down", &GameLib::IsMouseDown, nb::arg("button"))
        .def("is_mouse_pressed", &GameLib::IsMousePressed, nb::arg("button"))
        .def("is_mouse_released", &GameLib::IsMouseReleased, nb::arg("button"))
        .def("get_mouse_wheel_delta", &GameLib::GetMouseWheelDelta)
        .def("is_active", &GameLib::IsActive)

        // ---- Sound ----
        .def("play_beep", &GameLib::PlayBeep,
             nb::arg("frequency"), nb::arg("duration"),
             nb::arg("repeat") = 1, nb::arg("volume") = 1000)
        .def("play_wav", &GameLib::PlayWAV,
             nb::arg("filename"), nb::arg("repeat") = 1, nb::arg("volume") = 1000)
        .def("stop_wav", &GameLib::StopWAV, nb::arg("channel"))
        .def("is_playing", &GameLib::IsPlaying, nb::arg("channel"))
        .def("set_volume", &GameLib::SetVolume,
             nb::arg("channel"), nb::arg("volume"))
        .def("stop_all", &GameLib::StopAll)
        .def("set_master_volume", &GameLib::SetMasterVolume, nb::arg("volume"))
        .def("get_master_volume", &GameLib::GetMasterVolume)
        .def("play_music", &GameLib::PlayMusic,
             nb::arg("filename"), nb::arg("loop") = true)
        .def("stop_music", &GameLib::StopMusic)
        .def("is_music_playing", &GameLib::IsMusicPlaying)

        // ---- Scene Management ----
        .def("set_scene", &GameLib::SetScene, nb::arg("scene"))
        .def("get_scene", &GameLib::GetScene)
        .def("is_scene_changed", &GameLib::IsSceneChanged)
        .def("get_previous_scene", &GameLib::GetPreviousScene)

        // ---- UI Helpers ----
        .def("button", &GameLib::Button,
             nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
             nb::arg("text"), nb::arg("color"))
        .def("checkbox", [](GameLib& self, int x, int y, const char* text, bool checked) {
            bool result = self.Checkbox(x, y, text, &checked);
            return nb::make_tuple(result, checked);
        }, nb::arg("x"), nb::arg("y"), nb::arg("text"), nb::arg("checked"))
        .def("radio_box", [](GameLib& self, int x, int y, const char* text, int value, int index) {
            bool result = self.RadioBox(x, y, text, &value, index);
            return nb::make_tuple(result, value);
        }, nb::arg("x"), nb::arg("y"), nb::arg("text"), nb::arg("value"), nb::arg("index"))
        .def("toggle_button", [](GameLib& self, int x, int y, int w, int h,
                                  const char* text, bool toggled, uint32_t color) {
            bool result = self.ToggleButton(x, y, w, h, text, &toggled, color);
            return nb::make_tuple(result, toggled);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
           nb::arg("text"), nb::arg("toggled"), nb::arg("color"))
        .def("slider", [](GameLib& self, int x, int y, int w, int value, int min_val, int max_val) {
            bool result = self.Slider(x, y, w, &value, min_val, max_val);
            return nb::make_tuple(result, value);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("value"),
           nb::arg("min_val"), nb::arg("max_val"))
        .def("progress_bar", &GameLib::ProgressBar,
             nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
             nb::arg("value"), nb::arg("max_val"), nb::arg("color"))
        .def("spinner", [](GameLib& self, int x, int y, int w, int value,
                            int min_val, int max_val, int step) {
            bool result = self.Spinner(x, y, w, &value, min_val, max_val, step);
            return nb::make_tuple(result, value);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("value"),
           nb::arg("min_val"), nb::arg("max_val"), nb::arg("step"))
        .def("separator", &GameLib::Separator,
             nb::arg("x"), nb::arg("y"), nb::arg("w"))
        .def("label", &GameLib::Label,
             nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
             nb::arg("text"), nb::arg("bg_color"), nb::arg("text_color"))
        .def("v_separator", &GameLib::VSeparator,
             nb::arg("x"), nb::arg("y"), nb::arg("h"))
        .def("text_input", [](GameLib& self, int x, int y, int w, const char* buffer, bool focused) {
            char buf[256];
            strncpy(buf, buffer ? buffer : "", sizeof(buf) - 1);
            buf[sizeof(buf) - 1] = '\0';
            bool result = self.TextInput(x, y, w, buf, (int)sizeof(buf), &focused);
            return nb::make_tuple(result, std::string(buf), focused);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("buffer"), nb::arg("focused"))
        .def("dropdown", [](GameLib& self, int x, int y, int w,
                             const std::vector<std::string>& items,
                             int selected_index, bool open) {
            std::vector<const char*> ptrs;
            ptrs.reserve(items.size());
            for (auto& s : items) ptrs.push_back(s.c_str());
            bool result = self.Dropdown(x, y, w, ptrs.data(), (int)ptrs.size(), &selected_index, &open);
            return nb::make_tuple(result, selected_index, open);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("items"),
           nb::arg("selected_index"), nb::arg("open"))
        .def("tab_bar", [](GameLib& self, int x, int y, int w,
                            const std::vector<std::string>& tabs,
                            int selected_tab) {
            std::vector<const char*> ptrs;
            ptrs.reserve(tabs.size());
            for (auto& s : tabs) ptrs.push_back(s.c_str());
            bool result = self.TabBar(x, y, w, ptrs.data(), (int)ptrs.size(), &selected_tab);
            return nb::make_tuple(result, selected_tab);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("tabs"),
           nb::arg("selected_tab"))
        .def("tooltip", &GameLib::Tooltip,
             nb::arg("x"), nb::arg("y"), nb::arg("text"))
        .def("image_button", [](GameLib& self, int x, int y, int w, int h, int sprite_id, uint32_t color) {
            bool result = self.ImageButton(x, y, w, h, sprite_id, color);
            return result;
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
           nb::arg("sprite_id"), nb::arg("color"))
        .def("list_box", [](GameLib& self, int x, int y, int w, int h,
                             const std::vector<std::string>& items,
                             int selected_index, int scroll_offset) {
            std::vector<const char*> ptrs;
            ptrs.reserve(items.size());
            for (auto& s : items) ptrs.push_back(s.c_str());
            bool result = self.ListBox(x, y, w, h, ptrs.data(), (int)ptrs.size(),
                                       &selected_index, &scroll_offset);
            return nb::make_tuple(result, selected_index, scroll_offset);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
           nb::arg("items"), nb::arg("selected_index"), nb::arg("scroll_offset"))
        .def("collapsible", [](GameLib& self, int x, int y, int w, const char* title, bool open) {
            bool result = self.Collapsible(x, y, w, title, &open);
            return nb::make_tuple(result, open);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("title"), nb::arg("open"))
        .def("color_picker", [](GameLib& self, int x, int y,
                                 const std::vector<uint32_t>& colors,
                                 int selected_index) {
            bool result = self.ColorPicker(x, y, colors.data(), (int)colors.size(),
                                           &selected_index);
            return nb::make_tuple(result, selected_index);
        }, nb::arg("x"), nb::arg("y"), nb::arg("colors"), nb::arg("selected_index"))
        .def("knob", [](GameLib& self, int x, int y, int size, int value, int min_val, int max_val) {
            bool result = self.Knob(x, y, size, &value, min_val, max_val);
            return nb::make_tuple(result, value);
        }, nb::arg("x"), nb::arg("y"), nb::arg("size"), nb::arg("value"),
           nb::arg("min_val"), nb::arg("max_val"))
        .def("menu", [](GameLib& self, int x, int y,
                         const std::vector<std::string>& items, bool open) {
            std::vector<const char*> ptrs;
            ptrs.reserve(items.size());
            for (auto& s : items) ptrs.push_back(s.c_str());
            int result = self.Menu(x, y, ptrs.data(), (int)ptrs.size(), &open);
            return nb::make_tuple(result, open);
        }, nb::arg("x"), nb::arg("y"), nb::arg("items"), nb::arg("open"))
        .def("tab_panel", [](GameLib& self, int x, int y, int w, int h,
                              const std::vector<std::string>& tabs, int selected_tab) {
            std::vector<const char*> ptrs;
            ptrs.reserve(tabs.size());
            for (auto& s : tabs) ptrs.push_back(s.c_str());
            int result = self.TabPanel(x, y, w, h, ptrs.data(), (int)ptrs.size(), selected_tab);
            const int tabH = 26;
            return nb::make_tuple(result, x + 4, y + tabH + 4, w - 8, h - tabH - 8);
        }, nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"),
           nb::arg("tabs"), nb::arg("selected_tab"))

        // ---- Static Methods: Save/Load ----
        .def_static("save_int", &GameLib::SaveInt,
             nb::arg("filename"), nb::arg("key"), nb::arg("value"))
        .def_static("save_float", &GameLib::SaveFloat,
             nb::arg("filename"), nb::arg("key"), nb::arg("value"))
        .def_static("save_string", &GameLib::SaveString,
             nb::arg("filename"), nb::arg("key"), nb::arg("value"))
        .def_static("load_int", &GameLib::LoadInt,
             nb::arg("filename"), nb::arg("key"), nb::arg("default_value") = 0)
        .def_static("load_float", &GameLib::LoadFloat,
             nb::arg("filename"), nb::arg("key"), nb::arg("default_value") = 0.0f)
        .def_static("load_string", [](const char* filename, const char* key, const char* default_value) {
            const char* result = GameLib::LoadString(filename, key, default_value);
            return std::string(result ? result : "");
        }, nb::arg("filename"), nb::arg("key"), nb::arg("default_value") = "")
        .def_static("has_save_key", &GameLib::HasSaveKey,
             nb::arg("filename"), nb::arg("key"))
        .def_static("delete_save_key", &GameLib::DeleteSaveKey,
             nb::arg("filename"), nb::arg("key"))
        .def_static("delete_save", &GameLib::DeleteSave, nb::arg("filename"))

        // ---- Static Methods: Utilities ----
        .def_static("random", &GameLib::Random, nb::arg("min_val"), nb::arg("max_val"))
        .def_static("rect_overlap", &GameLib::RectOverlap,
             nb::arg("x1"), nb::arg("y1"), nb::arg("w1"), nb::arg("h1"),
             nb::arg("x2"), nb::arg("y2"), nb::arg("w2"), nb::arg("h2"))
        .def_static("circle_overlap", &GameLib::CircleOverlap,
             nb::arg("cx1"), nb::arg("cy1"), nb::arg("r1"),
             nb::arg("cx2"), nb::arg("cy2"), nb::arg("r2"))
        .def_static("point_in_rect", &GameLib::PointInRect,
             nb::arg("px"), nb::arg("py"), nb::arg("x"), nb::arg("y"),
             nb::arg("w"), nb::arg("h"))
        .def_static("distance", &GameLib::Distance,
             nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"))
        ;
}
