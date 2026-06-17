"""pyezgame 功能测试 - 使用 pytest 测试不需要窗口的纯逻辑功能"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator

import pyezgame
import pytest
from pyezgame import GameLib, clamp, get_asset_path, get_respath

# ── Fixtures ──────────────────────────────────────────────


@pytest.fixture()
def save_file(tmp_path: pytest.TempPathFactory) -> Iterator[str]:
    """提供一个临时存档文件路径，测试结束后自动清理。"""
    fd, path = tempfile.mkstemp(suffix=".sav", dir=str(tmp_path))
    os.close(fd)
    yield path
    GameLib.delete_save(path)
    if os.path.exists(path):
        os.unlink(path)


# ── 模块导入与版本 ────────────────────────────────────────


class TestModuleImport:
    """模块导入与版本"""

    def test_version_exists(self) -> None:
        assert hasattr(pyezgame, "__version__")

    def test_version_is_string(self) -> None:
        assert isinstance(pyezgame.__version__, str)

    def test_version_format(self) -> None:
        parts = pyezgame.__version__.split(".")
        assert len(parts) >= 2, f"版本号格式异常: {pyezgame.__version__}"


# ── 颜色常量 ──────────────────────────────────────────────


COLOR_NAMES = [
    "COLOR_BLACK",
    "COLOR_WHITE",
    "COLOR_RED",
    "COLOR_GREEN",
    "COLOR_BLUE",
    "COLOR_YELLOW",
    "COLOR_CYAN",
    "COLOR_MAGENTA",
    "COLOR_ORANGE",
    "COLOR_PINK",
    "COLOR_PURPLE",
    "COLOR_GRAY",
    "COLOR_DARK_GRAY",
    "COLOR_LIGHT_GRAY",
    "COLOR_DARK_RED",
    "COLOR_DARK_GREEN",
    "COLOR_DARK_BLUE",
    "COLOR_SKY_BLUE",
    "COLOR_BROWN",
    "COLOR_GOLD",
    "COLOR_TRANSPARENT",
    "COLORKEY_DEFAULT",
]


class TestColorConstants:
    """颜色常量"""

    @pytest.mark.parametrize("name", COLOR_NAMES)
    def test_color_constant_exists(self, name: str) -> None:
        assert hasattr(pyezgame, name), f"{name} 不存在"

    @pytest.mark.parametrize("name", COLOR_NAMES)
    def test_color_constant_is_int(self, name: str) -> None:
        assert isinstance(getattr(pyezgame, name), int), f"{name} 不是整数"


# ── 颜色辅助函数 ──────────────────────────────────────────


class TestColorHelpers:
    """颜色辅助函数"""

    def test_color_rgb_red(self) -> None:
        c = pyezgame.COLOR_RGB(255, 0, 0)
        assert pyezgame.COLOR_GET_R(c) == 255
        assert pyezgame.COLOR_GET_G(c) == 0
        assert pyezgame.COLOR_GET_B(c) == 0
        assert pyezgame.COLOR_GET_A(c) == 255

    def test_color_rgb_green(self) -> None:
        c = pyezgame.COLOR_RGB(0, 255, 0)
        assert pyezgame.COLOR_GET_G(c) == 255

    def test_color_rgb_blue(self) -> None:
        c = pyezgame.COLOR_RGB(0, 0, 255)
        assert pyezgame.COLOR_GET_B(c) == 255

    def test_color_rgb_black(self) -> None:
        c = pyezgame.COLOR_RGB(0, 0, 0)
        assert pyezgame.COLOR_GET_R(c) == 0
        assert pyezgame.COLOR_GET_G(c) == 0
        assert pyezgame.COLOR_GET_B(c) == 0

    def test_color_rgb_white(self) -> None:
        c = pyezgame.COLOR_RGB(255, 255, 255)
        assert pyezgame.COLOR_GET_R(c) == 255
        assert pyezgame.COLOR_GET_G(c) == 255
        assert pyezgame.COLOR_GET_B(c) == 255

    def test_color_argb(self) -> None:
        c = pyezgame.COLOR_ARGB(128, 200, 100, 50)
        assert pyezgame.COLOR_GET_A(c) == 128
        assert pyezgame.COLOR_GET_R(c) == 200
        assert pyezgame.COLOR_GET_G(c) == 100
        assert pyezgame.COLOR_GET_B(c) == 50

    def test_color_argb_fully_transparent(self) -> None:
        c = pyezgame.COLOR_ARGB(0, 255, 255, 255)
        assert pyezgame.COLOR_GET_A(c) == 0

    def test_get_components_all_zero(self) -> None:
        c = pyezgame.COLOR_ARGB(0, 0, 0, 0)
        assert pyezgame.COLOR_GET_A(c) == 0
        assert pyezgame.COLOR_GET_R(c) == 0
        assert pyezgame.COLOR_GET_G(c) == 0
        assert pyezgame.COLOR_GET_B(c) == 0

    def test_get_components_all_max(self) -> None:
        c = pyezgame.COLOR_ARGB(255, 255, 255, 255)
        assert pyezgame.COLOR_GET_A(c) == 255
        assert pyezgame.COLOR_GET_R(c) == 255
        assert pyezgame.COLOR_GET_G(c) == 255
        assert pyezgame.COLOR_GET_B(c) == 255


# ── 键盘常量 ──────────────────────────────────────────────


KEY_NAMES = [
    "KEY_LEFT",
    "KEY_RIGHT",
    "KEY_UP",
    "KEY_DOWN",
    "KEY_SPACE",
    "KEY_ENTER",
    "KEY_ESCAPE",
    "KEY_TAB",
    "KEY_SHIFT",
    "KEY_CONTROL",
    "KEY_BACK",
    "KEY_A",
    "KEY_B",
    "KEY_C",
    "KEY_D",
    "KEY_E",
    "KEY_F",
    "KEY_G",
    "KEY_H",
    "KEY_I",
    "KEY_J",
    "KEY_K",
    "KEY_L",
    "KEY_M",
    "KEY_N",
    "KEY_O",
    "KEY_P",
    "KEY_Q",
    "KEY_R",
    "KEY_S",
    "KEY_T",
    "KEY_U",
    "KEY_V",
    "KEY_W",
    "KEY_X",
    "KEY_Y",
    "KEY_Z",
    "KEY_0",
    "KEY_1",
    "KEY_2",
    "KEY_3",
    "KEY_4",
    "KEY_5",
    "KEY_6",
    "KEY_7",
    "KEY_8",
    "KEY_9",
    "KEY_F1",
    "KEY_F2",
    "KEY_F3",
    "KEY_F4",
    "KEY_F5",
    "KEY_F6",
    "KEY_F7",
    "KEY_F8",
    "KEY_F9",
    "KEY_F10",
    "KEY_F11",
    "KEY_F12",
    "KEY_ADD",
    "KEY_SUBTRACT",
]


class TestKeyConstants:
    """键盘常量"""

    @pytest.mark.parametrize("name", KEY_NAMES)
    def test_key_constant_exists(self, name: str) -> None:
        assert hasattr(pyezgame, name), f"{name} 不存在"

    @pytest.mark.parametrize("name", KEY_NAMES)
    def test_key_constant_is_int(self, name: str) -> None:
        assert isinstance(getattr(pyezgame, name), int), f"{name} 不是整数"


# ── 鼠标常量 ──────────────────────────────────────────────


class TestMouseConstants:
    """鼠标常量"""

    @pytest.mark.parametrize("name", ["MOUSE_LEFT", "MOUSE_RIGHT", "MOUSE_MIDDLE"])
    def test_mouse_constants(self, name: str) -> None:
        assert hasattr(pyezgame, name), f"{name} 不存在"
        assert isinstance(getattr(pyezgame, name), int)


# ── 精灵标志常量 ──────────────────────────────────────────


class TestSpriteFlagConstants:
    """精灵标志常量"""

    @pytest.mark.parametrize(
        "name",
        ["SPRITE_FLIP_H", "SPRITE_FLIP_V", "SPRITE_COLORKEY", "SPRITE_ALPHA"],
    )
    def test_sprite_flags(self, name: str) -> None:
        assert hasattr(pyezgame, name), f"{name} 不存在"
        assert isinstance(getattr(pyezgame, name), int)


# ── 消息框常量 ────────────────────────────────────────────


class TestMessageBoxConstants:
    """消息框常量"""

    @pytest.mark.parametrize(
        "name",
        [
            "MESSAGEBOX_OK",
            "MESSAGEBOX_YESNO",
            "MESSAGEBOX_RESULT_OK",
            "MESSAGEBOX_RESULT_YES",
            "MESSAGEBOX_RESULT_NO",
        ],
    )
    def test_messagebox_constants(self, name: str) -> None:
        assert hasattr(pyezgame, name), f"{name} 不存在"
        assert isinstance(getattr(pyezgame, name), int)


# ── GameLib 实例化 ────────────────────────────────────────


class TestGameLibInstantiate:
    """GameLib 实例化"""

    def test_instantiate(self) -> None:
        g = GameLib()
        assert g is not None


# ── 随机数 ────────────────────────────────────────────────


class TestRandom:
    """随机数"""

    def test_random_in_range(self) -> None:
        for _ in range(100):
            r = GameLib.random(1, 10)
            assert 1 <= r <= 10

    def test_random_min_equals_max(self) -> None:
        for _ in range(10):
            assert GameLib.random(5, 5) == 5


# ── 矩形碰撞检测 ──────────────────────────────────────────


class TestRectOverlap:
    """矩形碰撞检测"""

    def test_full_overlap(self) -> None:
        assert GameLib.rect_overlap(0, 0, 10, 10, 0, 0, 10, 10)

    def test_partial_overlap(self) -> None:
        assert GameLib.rect_overlap(0, 0, 10, 10, 5, 5, 10, 10)

    def test_no_overlap(self) -> None:
        assert not GameLib.rect_overlap(0, 0, 10, 10, 20, 20, 10, 10)

    def test_edge_touch(self) -> None:
        assert not GameLib.rect_overlap(0, 0, 10, 10, 10, 0, 10, 10)

    def test_containment(self) -> None:
        assert GameLib.rect_overlap(0, 0, 20, 20, 5, 5, 5, 5)


# ── 圆形碰撞检测 ──────────────────────────────────────────


class TestCircleOverlap:
    """圆形碰撞检测"""

    def test_concentric(self) -> None:
        assert GameLib.circle_overlap(0, 0, 10, 0, 0, 5)

    def test_far_apart(self) -> None:
        assert not GameLib.circle_overlap(0, 0, 5, 100, 100, 5)

    def test_tangent(self) -> None:
        assert GameLib.circle_overlap(0, 0, 5, 10, 0, 5)

    def test_no_overlap(self) -> None:
        assert not GameLib.circle_overlap(0, 0, 5, 11, 0, 5)


# ── 点在矩形内判断 ────────────────────────────────────────


class TestPointInRect:
    """点在矩形内判断"""

    def test_inside(self) -> None:
        assert GameLib.point_in_rect(5, 5, 0, 0, 10, 10)

    def test_top_left_corner(self) -> None:
        assert GameLib.point_in_rect(0, 0, 0, 0, 10, 10)

    def test_near_bottom_right(self) -> None:
        assert GameLib.point_in_rect(9, 9, 0, 0, 10, 10)

    def test_outside_bottom_right(self) -> None:
        assert not GameLib.point_in_rect(10, 10, 0, 0, 10, 10)

    def test_outside_left(self) -> None:
        assert not GameLib.point_in_rect(-1, 5, 0, 0, 10, 10)


# ── 两点距离计算 ──────────────────────────────────────────


class TestDistance:
    """两点距离计算"""

    def test_3_4_5_triangle(self) -> None:
        assert GameLib.distance(0, 0, 3, 4) == pytest.approx(5.0, abs=1e-3)

    def test_same_point_origin(self) -> None:
        assert GameLib.distance(0, 0, 0, 0) == 0.0

    def test_same_point(self) -> None:
        assert GameLib.distance(1, 1, 1, 1) == 0.0


# ── 整数存档读写 ──────────────────────────────────────────


class TestSaveLoadInt:
    """整数存档读写"""

    def test_save_and_load(self, save_file: str) -> None:
        assert GameLib.save_int(save_file, "score", 12345)
        assert GameLib.load_int(save_file, "score") == 12345

    def test_missing_key_returns_default(self, save_file: str) -> None:
        assert GameLib.load_int(save_file, "no_key", 999) == 999

    def test_overwrite(self, save_file: str) -> None:
        GameLib.save_int(save_file, "score", 111)
        GameLib.save_int(save_file, "score", 67890)
        assert GameLib.load_int(save_file, "score") == 67890


# ── 浮点数存档读写 ────────────────────────────────────────


class TestSaveLoadFloat:
    """浮点数存档读写"""

    def test_save_and_load(self, save_file: str) -> None:
        assert GameLib.save_float(save_file, "pi", 3.14159)
        assert GameLib.load_float(save_file, "pi") == pytest.approx(3.14159, abs=1e-4)

    def test_missing_key_returns_default(self, save_file: str) -> None:
        assert GameLib.load_float(save_file, "missing", 1.5) == 1.5


# ── 字符串存档读写 ────────────────────────────────────────


class TestSaveLoadString:
    """字符串存档读写"""

    def test_save_and_load(self, save_file: str) -> None:
        assert GameLib.save_string(save_file, "name", "hello world")
        assert GameLib.load_string(save_file, "name") == "hello world"

    def test_missing_key_returns_default(self, save_file: str) -> None:
        assert GameLib.load_string(save_file, "missing", "default") == "default"


# ── 存档 key 操作 ─────────────────────────────────────────


class TestSaveKeyOperations:
    """存档 key 操作"""

    def test_has_save_key(self, save_file: str) -> None:
        GameLib.save_int(save_file, "a", 1)
        GameLib.save_int(save_file, "b", 2)
        assert GameLib.has_save_key(save_file, "a")
        assert GameLib.has_save_key(save_file, "b")
        assert not GameLib.has_save_key(save_file, "c")

    def test_delete_save_key(self, save_file: str) -> None:
        GameLib.save_int(save_file, "a", 1)
        GameLib.save_int(save_file, "b", 2)
        assert GameLib.delete_save_key(save_file, "a")
        assert not GameLib.has_save_key(save_file, "a")
        assert GameLib.has_save_key(save_file, "b")

    def test_delete_save(self, save_file: str) -> None:
        GameLib.save_int(save_file, "x", 1)
        assert os.path.exists(save_file)
        assert GameLib.delete_save(save_file)
        assert GameLib.load_int(save_file, "x", -1) == -1


# ── clamp 工具函数 ──────────────────────────────────────


class TestClamp:
    """clamp 工具函数"""

    def test_value_in_range(self) -> None:
        assert clamp(5, 0, 10) == 5

    def test_value_below_min(self) -> None:
        assert clamp(-5, 0, 10) == 0

    def test_value_above_max(self) -> None:
        assert clamp(15, 0, 10) == 10

    def test_value_at_min(self) -> None:
        assert clamp(0, 0, 10) == 0

    def test_value_at_max(self) -> None:
        assert clamp(10, 0, 10) == 10

    def test_min_equals_max(self) -> None:
        assert clamp(99, 5, 5) == 5

    def test_negative_range(self) -> None:
        assert clamp(-3, -10, -1) == -3
        assert clamp(0, -10, -1) == -1
        assert clamp(-20, -10, -1) == -10


# ── get_asset_path 工具函数 ─────────────────────────────


class TestGetAssetPath:
    """get_asset_path 工具函数"""

    def test_returns_string(self) -> None:
        result = get_asset_path("coin.png")
        assert isinstance(result, str)

    def test_ends_with_filename(self) -> None:
        result = get_asset_path("coin.png")
        assert result.endswith("coin.png")

    def test_contains_assets(self) -> None:
        result = get_asset_path("heart.png")
        assert "assets/heart.png" in result

    def test_uses_forward_slashes(self) -> None:
        result = get_asset_path("star.png")
        assert "\\" not in result  # POSIX path, no backslashes


# ── get_respath 工具函数 ─────────────────────────────


class TestGetRespath:
    """get_respath 工具函数"""

    def test_returns_string(self) -> None:
        result = get_respath("utils.py")
        assert isinstance(result, str)

    def test_contains_package_name(self) -> None:
        result = get_respath("utils.py")
        assert "pyezgame" in result
        assert result.endswith("utils.py")

    def test_uses_forward_slashes(self) -> None:
        result = get_respath("__init__.py")
        assert "\\" not in result  # POSIX path, no backslashes
