/**
 * GameLib Python Bindings
 * pybind11 wrapper for GameLib
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

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

PYBIND11_MODULE(_pyezgame, m) {
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
    }, "Create RGB color", py::arg("r"), py::arg("g"), py::arg("b"));

    m.def("COLOR_ARGB", [](int a, int r, int g, int b) {
        return (uint32_t)(((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF));
    }, "Create ARGB color", py::arg("a"), py::arg("r"), py::arg("g"), py::arg("b"));

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
    py::class_<GameLib>(m, "GameLib")
        .def(py::init<>())

        // ---- Window and Main Loop ----
        .def("open", &GameLib::Open,
             py::arg("width"), py::arg("height"), py::arg("title"),
             py::arg("center") = false, py::arg("resizable") = false)
        .def("is_closed", &GameLib::IsClosed)
        .def("update", &GameLib::Update)
        .def("wait_frame", &GameLib::WaitFrame, py::arg("fps"))
        .def("get_delta_time", &GameLib::GetDeltaTime)
        .def("get_fps", &GameLib::GetFPS)
        .def("get_time", &GameLib::GetTime)
        .def("get_width", &GameLib::GetWidth)
        .def("get_height", &GameLib::GetHeight)
        .def("win_resize", &GameLib::WinResize, py::arg("width"), py::arg("height"))
        .def("set_maximized", &GameLib::SetMaximized, py::arg("maximized"))
        .def("set_title", &GameLib::SetTitle, py::arg("title"))
        .def("show_fps", &GameLib::ShowFps, py::arg("show"))
        .def("show_mouse", &GameLib::ShowMouse, py::arg("show"))
        .def("aspect_lock", &GameLib::AspectLock,
             py::arg("lock"), py::arg("color") = COLOR_BLACK)
        .def("show_message", &GameLib::ShowMessage,
             py::arg("text"), py::arg("title") = nullptr,
             py::arg("buttons") = MESSAGEBOX_OK)

        // ---- Framebuffer ----
        .def("clear", &GameLib::Clear, py::arg("color") = COLOR_BLACK)
        .def("set_pixel", &GameLib::SetPixel, py::arg("x"), py::arg("y"), py::arg("color"))
        .def("get_pixel", &GameLib::GetPixel, py::arg("x"), py::arg("y"))
        .def("set_clip", &GameLib::SetClip,
             py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"))
        .def("clear_clip", &GameLib::ClearClip)
        .def("get_clip", [](const GameLib& self) {
            int x, y, w, h;
            self.GetClip(&x, &y, &w, &h);
            return py::make_tuple(x, y, w, h);
        })
        .def("get_clip_x", &GameLib::GetClipX)
        .def("get_clip_y", &GameLib::GetClipY)
        .def("get_clip_w", &GameLib::GetClipW)
        .def("get_clip_h", &GameLib::GetClipH)
        .def("screenshot", &GameLib::Screenshot, py::arg("filename"))

        // ---- Drawing ----
        .def("draw_line", &GameLib::DrawLine,
             py::arg("x1"), py::arg("y1"), py::arg("x2"), py::arg("y2"), py::arg("color"))
        .def("draw_rect", &GameLib::DrawRect,
             py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"), py::arg("color"))
        .def("fill_rect", &GameLib::FillRect,
             py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"), py::arg("color"))
        .def("draw_circle", &GameLib::DrawCircle,
             py::arg("cx"), py::arg("cy"), py::arg("r"), py::arg("color"))
        .def("fill_circle", &GameLib::FillCircle,
             py::arg("cx"), py::arg("cy"), py::arg("r"), py::arg("color"))
        .def("draw_ellipse", &GameLib::DrawEllipse,
             py::arg("cx"), py::arg("cy"), py::arg("rx"), py::arg("ry"), py::arg("color"))
        .def("fill_ellipse", &GameLib::FillEllipse,
             py::arg("cx"), py::arg("cy"), py::arg("rx"), py::arg("ry"), py::arg("color"))
        .def("draw_triangle", &GameLib::DrawTriangle,
             py::arg("x1"), py::arg("y1"), py::arg("x2"), py::arg("y2"),
             py::arg("x3"), py::arg("y3"), py::arg("color"))
        .def("fill_triangle", &GameLib::FillTriangle,
             py::arg("x1"), py::arg("y1"), py::arg("x2"), py::arg("y2"),
             py::arg("x3"), py::arg("y3"), py::arg("color"))

        // ---- Text Rendering (built-in 8x8 font) ----
        .def("draw_text", &GameLib::DrawText,
             py::arg("x"), py::arg("y"), py::arg("text"), py::arg("color"))
        .def("draw_number", &GameLib::DrawNumber,
             py::arg("x"), py::arg("y"), py::arg("number"), py::arg("color"))
        .def("draw_text_scale", &GameLib::DrawTextScale,
             py::arg("x"), py::arg("y"), py::arg("text"), py::arg("color"),
             py::arg("w"), py::arg("h"))
        .def("draw_printf", [](GameLib& self, int x, int y, uint32_t color, const char* text) {
            self.DrawText(x, y, text, color);
        }, py::arg("x"), py::arg("y"), py::arg("color"), py::arg("text"))
        .def("draw_printf_scale", [](GameLib& self, int x, int y, uint32_t color, int w, int h, const char* text) {
            self.DrawTextScale(x, y, text, color, w, h);
        }, py::arg("x"), py::arg("y"), py::arg("color"), py::arg("w"), py::arg("h"), py::arg("text"))

        // ---- Font Text Rendering (scalable fonts) ----
        .def("draw_text_font",
             py::overload_cast<int, int, const char*, uint32_t, const char*, int>(
                 &GameLib::DrawTextFont),
             py::arg("x"), py::arg("y"), py::arg("text"), py::arg("color"),
             py::arg("font_name"), py::arg("font_size"))
        .def("draw_text_font",
             py::overload_cast<int, int, const char*, uint32_t, int>(
                 &GameLib::DrawTextFont),
             py::arg("x"), py::arg("y"), py::arg("text"), py::arg("color"),
             py::arg("font_size"))
        .def("get_text_width_font",
             py::overload_cast<const char*, const char*, int>(
                 &GameLib::GetTextWidthFont),
             py::arg("text"), py::arg("font_name"), py::arg("font_size"))
        .def("get_text_width_font",
             py::overload_cast<const char*, int>(
                 &GameLib::GetTextWidthFont),
             py::arg("text"), py::arg("font_size"))
        .def("get_text_height_font",
             py::overload_cast<const char*, const char*, int>(
                 &GameLib::GetTextHeightFont),
             py::arg("text"), py::arg("font_name"), py::arg("font_size"))
        .def("get_text_height_font",
             py::overload_cast<const char*, int>(
                 &GameLib::GetTextHeightFont),
             py::arg("text"), py::arg("font_size"))
        .def("draw_printf_font",
             [](GameLib& self, int x, int y, uint32_t color, const char* font_name, int font_size, const char* text) {
                 self.DrawTextFont(x, y, text, color, font_name, font_size);
             }, py::arg("x"), py::arg("y"), py::arg("color"), py::arg("font_name"), py::arg("font_size"), py::arg("text"))
        .def("draw_printf_font",
             [](GameLib& self, int x, int y, uint32_t color, int font_size, const char* text) {
                 self.DrawTextFont(x, y, text, color, font_size);
             }, py::arg("x"), py::arg("y"), py::arg("color"), py::arg("font_size"), py::arg("text"))

        // ---- Sprite System ----
        .def("create_sprite", &GameLib::CreateSprite,
             py::arg("width"), py::arg("height"))
        .def("load_sprite", &GameLib::LoadSprite, py::arg("filename"))
        .def("load_sprite_bmp", &GameLib::LoadSpriteBMP, py::arg("filename"))
        .def("free_sprite", &GameLib::FreeSprite, py::arg("id"))
        .def("draw_sprite", &GameLib::DrawSprite,
             py::arg("id"), py::arg("x"), py::arg("y"))
        .def("draw_sprite_ex", &GameLib::DrawSpriteEx,
             py::arg("id"), py::arg("x"), py::arg("y"), py::arg("flags"))
        .def("draw_sprite_region", &GameLib::DrawSpriteRegion,
             py::arg("id"), py::arg("x"), py::arg("y"),
             py::arg("sx"), py::arg("sy"), py::arg("sw"), py::arg("sh"))
        .def("draw_sprite_region_ex", &GameLib::DrawSpriteRegionEx,
             py::arg("id"), py::arg("x"), py::arg("y"),
             py::arg("sx"), py::arg("sy"), py::arg("sw"), py::arg("sh"),
             py::arg("flags") = 0)
        .def("draw_sprite_scaled", &GameLib::DrawSpriteScaled,
             py::arg("id"), py::arg("x"), py::arg("y"),
             py::arg("w"), py::arg("h"), py::arg("flags") = 0)
        .def("draw_sprite_rotated", &GameLib::DrawSpriteRotated,
             py::arg("id"), py::arg("cx"), py::arg("cy"),
             py::arg("angle_deg"), py::arg("flags") = 0)
        .def("draw_sprite_frame", &GameLib::DrawSpriteFrame,
             py::arg("id"), py::arg("x"), py::arg("y"),
             py::arg("frame_w"), py::arg("frame_h"), py::arg("frame_index"),
             py::arg("flags") = 0)
        .def("draw_sprite_frame_scaled", &GameLib::DrawSpriteFrameScaled,
             py::arg("id"), py::arg("x"), py::arg("y"),
             py::arg("frame_w"), py::arg("frame_h"), py::arg("frame_index"),
             py::arg("w"), py::arg("h"), py::arg("flags") = 0)
        .def("draw_sprite_frame_rotated", &GameLib::DrawSpriteFrameRotated,
             py::arg("id"), py::arg("cx"), py::arg("cy"),
             py::arg("frame_w"), py::arg("frame_h"), py::arg("frame_index"),
             py::arg("angle_deg"), py::arg("flags") = 0)
        .def("set_sprite_pixel", &GameLib::SetSpritePixel,
             py::arg("id"), py::arg("x"), py::arg("y"), py::arg("color"))
        .def("get_sprite_pixel", &GameLib::GetSpritePixel,
             py::arg("id"), py::arg("x"), py::arg("y"))
        .def("get_sprite_width", &GameLib::GetSpriteWidth, py::arg("id"))
        .def("get_sprite_height", &GameLib::GetSpriteHeight, py::arg("id"))
        .def("set_sprite_color_key", &GameLib::SetSpriteColorKey,
             py::arg("id"), py::arg("color"))
        .def("get_sprite_color_key", &GameLib::GetSpriteColorKey, py::arg("id"))

        // ---- Tilemap System ----
        .def("create_tilemap", &GameLib::CreateTilemap,
             py::arg("cols"), py::arg("rows"), py::arg("tile_size"), py::arg("tileset_id"))
        .def("save_tilemap", &GameLib::SaveTilemap,
             py::arg("filename"), py::arg("map_id"))
        .def("load_tilemap", &GameLib::LoadTilemap,
             py::arg("filename"), py::arg("tileset_id"))
        .def("free_tilemap", &GameLib::FreeTilemap, py::arg("map_id"))
        .def("set_tile", &GameLib::SetTile,
             py::arg("map_id"), py::arg("col"), py::arg("row"), py::arg("tile_id"))
        .def("get_tile", &GameLib::GetTile,
             py::arg("map_id"), py::arg("col"), py::arg("row"))
        .def("get_tilemap_cols", &GameLib::GetTilemapCols, py::arg("map_id"))
        .def("get_tilemap_rows", &GameLib::GetTilemapRows, py::arg("map_id"))
        .def("get_tile_size", &GameLib::GetTileSize, py::arg("map_id"))
        .def("world_to_tile_col", &GameLib::WorldToTileCol,
             py::arg("map_id"), py::arg("x"))
        .def("world_to_tile_row", &GameLib::WorldToTileRow,
             py::arg("map_id"), py::arg("y"))
        .def("get_tile_at_pixel", &GameLib::GetTileAtPixel,
             py::arg("map_id"), py::arg("x"), py::arg("y"))
        .def("fill_tile_rect", &GameLib::FillTileRect,
             py::arg("map_id"), py::arg("col"), py::arg("row"),
             py::arg("cols"), py::arg("rows"), py::arg("tile_id"))
        .def("clear_tilemap", &GameLib::ClearTilemap,
             py::arg("map_id"), py::arg("tile_id") = -1)
        .def("draw_tilemap", &GameLib::DrawTilemap,
             py::arg("map_id"), py::arg("x"), py::arg("y"), py::arg("flags") = 0)

        // ---- Grid Helpers ----
        .def("draw_grid", &GameLib::DrawGrid,
             py::arg("x"), py::arg("y"), py::arg("rows"), py::arg("cols"),
             py::arg("cell_size"), py::arg("color"))
        .def("fill_cell", &GameLib::FillCell,
             py::arg("grid_x"), py::arg("grid_y"), py::arg("row"), py::arg("col"),
             py::arg("cell_size"), py::arg("color"))

        // ---- Input ----
        .def("is_key_down", &GameLib::IsKeyDown, py::arg("key"))
        .def("is_key_pressed", &GameLib::IsKeyPressed, py::arg("key"))
        .def("is_key_released", &GameLib::IsKeyReleased, py::arg("key"))
        .def("get_mouse_x", &GameLib::GetMouseX)
        .def("get_mouse_y", &GameLib::GetMouseY)
        .def("is_mouse_down", &GameLib::IsMouseDown, py::arg("button"))
        .def("is_mouse_pressed", &GameLib::IsMousePressed, py::arg("button"))
        .def("is_mouse_released", &GameLib::IsMouseReleased, py::arg("button"))
        .def("get_mouse_wheel_delta", &GameLib::GetMouseWheelDelta)
        .def("is_active", &GameLib::IsActive)

        // ---- Sound ----
        .def("play_beep", &GameLib::PlayBeep,
             py::arg("frequency"), py::arg("duration"),
             py::arg("repeat") = 1, py::arg("volume") = 1000)
        .def("play_wav", &GameLib::PlayWAV,
             py::arg("filename"), py::arg("repeat") = 1, py::arg("volume") = 1000)
        .def("stop_wav", &GameLib::StopWAV, py::arg("channel"))
        .def("is_playing", &GameLib::IsPlaying, py::arg("channel"))
        .def("set_volume", &GameLib::SetVolume,
             py::arg("channel"), py::arg("volume"))
        .def("stop_all", &GameLib::StopAll)
        .def("set_master_volume", &GameLib::SetMasterVolume, py::arg("volume"))
        .def("get_master_volume", &GameLib::GetMasterVolume)
        .def("play_music", &GameLib::PlayMusic,
             py::arg("filename"), py::arg("loop") = true)
        .def("stop_music", &GameLib::StopMusic)
        .def("is_music_playing", &GameLib::IsMusicPlaying)

        // ---- Scene Management ----
        .def("set_scene", &GameLib::SetScene, py::arg("scene"))
        .def("get_scene", &GameLib::GetScene)
        .def("is_scene_changed", &GameLib::IsSceneChanged)
        .def("get_previous_scene", &GameLib::GetPreviousScene)

        // ---- UI Helpers ----
        .def("button", &GameLib::Button,
             py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"),
             py::arg("text"), py::arg("color"))
        .def("checkbox", [](GameLib& self, int x, int y, const char* text, bool checked) {
            bool result = self.Checkbox(x, y, text, &checked);
            return py::make_tuple(result, checked);
        }, py::arg("x"), py::arg("y"), py::arg("text"), py::arg("checked"))
        .def("radio_box", [](GameLib& self, int x, int y, const char* text, int value, int index) {
            bool result = self.RadioBox(x, y, text, &value, index);
            return py::make_tuple(result, value);
        }, py::arg("x"), py::arg("y"), py::arg("text"), py::arg("value"), py::arg("index"))
        .def("toggle_button", [](GameLib& self, int x, int y, int w, int h,
                                  const char* text, bool toggled, uint32_t color) {
            bool result = self.ToggleButton(x, y, w, h, text, &toggled, color);
            return py::make_tuple(result, toggled);
        }, py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"),
           py::arg("text"), py::arg("toggled"), py::arg("color"))
        .def("slider", [](GameLib& self, int x, int y, int w, int value, int min_val, int max_val) {
            bool result = self.Slider(x, y, w, &value, min_val, max_val);
            return py::make_tuple(result, value);
        }, py::arg("x"), py::arg("y"), py::arg("w"), py::arg("value"),
           py::arg("min_val"), py::arg("max_val"))
        .def("progress_bar", &GameLib::ProgressBar,
             py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"),
             py::arg("value"), py::arg("max_val"), py::arg("color"))
        .def("spinner", [](GameLib& self, int x, int y, int w, int value,
                            int min_val, int max_val, int step) {
            bool result = self.Spinner(x, y, w, &value, min_val, max_val, step);
            return py::make_tuple(result, value);
        }, py::arg("x"), py::arg("y"), py::arg("w"), py::arg("value"),
           py::arg("min_val"), py::arg("max_val"), py::arg("step"))
        .def("separator", &GameLib::Separator,
             py::arg("x"), py::arg("y"), py::arg("w"))
        .def("label", &GameLib::Label,
             py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"),
             py::arg("text"), py::arg("bg_color"), py::arg("text_color"))

        // ---- Static Methods: Save/Load ----
        .def_static("save_int", &GameLib::SaveInt,
             py::arg("filename"), py::arg("key"), py::arg("value"))
        .def_static("save_float", &GameLib::SaveFloat,
             py::arg("filename"), py::arg("key"), py::arg("value"))
        .def_static("save_string", &GameLib::SaveString,
             py::arg("filename"), py::arg("key"), py::arg("value"))
        .def_static("load_int", &GameLib::LoadInt,
             py::arg("filename"), py::arg("key"), py::arg("default_value") = 0)
        .def_static("load_float", &GameLib::LoadFloat,
             py::arg("filename"), py::arg("key"), py::arg("default_value") = 0.0f)
        .def_static("load_string", [](const char* filename, const char* key, const char* default_value) {
            const char* result = GameLib::LoadString(filename, key, default_value);
            return std::string(result ? result : "");
        }, py::arg("filename"), py::arg("key"), py::arg("default_value") = "")
        .def_static("has_save_key", &GameLib::HasSaveKey,
             py::arg("filename"), py::arg("key"))
        .def_static("delete_save_key", &GameLib::DeleteSaveKey,
             py::arg("filename"), py::arg("key"))
        .def_static("delete_save", &GameLib::DeleteSave, py::arg("filename"))

        // ---- Static Methods: Utilities ----
        .def_static("random", &GameLib::Random, py::arg("min_val"), py::arg("max_val"))
        .def_static("rect_overlap", &GameLib::RectOverlap,
             py::arg("x1"), py::arg("y1"), py::arg("w1"), py::arg("h1"),
             py::arg("x2"), py::arg("y2"), py::arg("w2"), py::arg("h2"))
        .def_static("circle_overlap", &GameLib::CircleOverlap,
             py::arg("cx1"), py::arg("cy1"), py::arg("r1"),
             py::arg("cx2"), py::arg("cy2"), py::arg("r2"))
        .def_static("point_in_rect", &GameLib::PointInRect,
             py::arg("px"), py::arg("py"), py::arg("x"), py::arg("y"),
             py::arg("w"), py::arg("h"))
        .def_static("distance", &GameLib::Distance,
             py::arg("x1"), py::arg("y1"), py::arg("x2"), py::arg("y2"))
        ;
}
