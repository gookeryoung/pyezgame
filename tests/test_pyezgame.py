"""pyezgame 功能测试 - 使用 unittest 测试不需要窗口的纯逻辑功能"""

from __future__ import annotations

import os
import tempfile
import unittest

import pyezgame
from pyezgame import GameLib


class TestModuleImport(unittest.TestCase):
    """模块导入与版本"""

    def test_version_exists(self) -> None:
        self.assertTrue(hasattr(pyezgame, "__version__"))

    def test_version_is_string(self) -> None:
        self.assertIsInstance(pyezgame.__version__, str)

    def test_version_format(self) -> None:
        parts = pyezgame.__version__.split(".")
        self.assertGreaterEqual(len(parts), 2, f"版本号格式异常: {pyezgame.__version__}")


class TestColorConstants(unittest.TestCase):
    """颜色常量"""

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

    def test_all_color_constants_exist(self) -> None:
        for name in self.COLOR_NAMES:
            with self.subTest(color=name):
                self.assertTrue(hasattr(pyezgame, name), f"{name} 不存在")

    def test_all_color_constants_are_int(self) -> None:
        for name in self.COLOR_NAMES:
            with self.subTest(color=name):
                self.assertIsInstance(getattr(pyezgame, name), int, f"{name} 不是整数")


class TestColorHelpers(unittest.TestCase):
    """颜色辅助函数"""

    def test_color_rgb_red(self) -> None:
        c = pyezgame.COLOR_RGB(255, 0, 0)
        self.assertEqual(pyezgame.COLOR_GET_R(c), 255)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_A(c), 255)

    def test_color_rgb_green(self) -> None:
        c = pyezgame.COLOR_RGB(0, 255, 0)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 255)

    def test_color_rgb_blue(self) -> None:
        c = pyezgame.COLOR_RGB(0, 0, 255)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 255)

    def test_color_rgb_black(self) -> None:
        c = pyezgame.COLOR_RGB(0, 0, 0)
        self.assertEqual(pyezgame.COLOR_GET_R(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 0)

    def test_color_rgb_white(self) -> None:
        c = pyezgame.COLOR_RGB(255, 255, 255)
        self.assertEqual(pyezgame.COLOR_GET_R(c), 255)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 255)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 255)

    def test_color_argb(self) -> None:
        c = pyezgame.COLOR_ARGB(128, 200, 100, 50)
        self.assertEqual(pyezgame.COLOR_GET_A(c), 128)
        self.assertEqual(pyezgame.COLOR_GET_R(c), 200)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 100)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 50)

    def test_color_argb_fully_transparent(self) -> None:
        c = pyezgame.COLOR_ARGB(0, 255, 255, 255)
        self.assertEqual(pyezgame.COLOR_GET_A(c), 0)

    def test_get_components_all_zero(self) -> None:
        c = pyezgame.COLOR_ARGB(0, 0, 0, 0)
        self.assertEqual(pyezgame.COLOR_GET_A(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_R(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 0)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 0)

    def test_get_components_all_max(self) -> None:
        c = pyezgame.COLOR_ARGB(255, 255, 255, 255)
        self.assertEqual(pyezgame.COLOR_GET_A(c), 255)
        self.assertEqual(pyezgame.COLOR_GET_R(c), 255)
        self.assertEqual(pyezgame.COLOR_GET_G(c), 255)
        self.assertEqual(pyezgame.COLOR_GET_B(c), 255)


class TestKeyConstants(unittest.TestCase):
    """键盘常量"""

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
        "KEY_Z",
        "KEY_0",
        "KEY_9",
        "KEY_F1",
        "KEY_F12",
        "KEY_ADD",
        "KEY_SUBTRACT",
    ]

    def test_all_key_constants_exist(self) -> None:
        for name in self.KEY_NAMES:
            with self.subTest(key=name):
                self.assertTrue(hasattr(pyezgame, name), f"{name} 不存在")

    def test_all_key_constants_are_int(self) -> None:
        for name in self.KEY_NAMES:
            with self.subTest(key=name):
                self.assertIsInstance(getattr(pyezgame, name), int, f"{name} 不是整数")


class TestMouseConstants(unittest.TestCase):
    """鼠标常量"""

    def test_mouse_constants_exist(self) -> None:
        for name in ["MOUSE_LEFT", "MOUSE_RIGHT", "MOUSE_MIDDLE"]:
            with self.subTest(button=name):
                self.assertTrue(hasattr(pyezgame, name), f"{name} 不存在")
                self.assertIsInstance(getattr(pyezgame, name), int)


class TestSpriteFlagConstants(unittest.TestCase):
    """精灵标志常量"""

    def test_sprite_flags_exist(self) -> None:
        for name in [
            "SPRITE_FLIP_H",
            "SPRITE_FLIP_V",
            "SPRITE_COLORKEY",
            "SPRITE_ALPHA",
        ]:
            with self.subTest(flag=name):
                self.assertTrue(hasattr(pyezgame, name), f"{name} 不存在")
                self.assertIsInstance(getattr(pyezgame, name), int)


class TestMessageBoxConstants(unittest.TestCase):
    """消息框常量"""

    def test_messagebox_constants_exist(self) -> None:
        for name in [
            "MESSAGEBOX_OK",
            "MESSAGEBOX_YESNO",
            "MESSAGEBOX_RESULT_OK",
            "MESSAGEBOX_RESULT_YES",
            "MESSAGEBOX_RESULT_NO",
        ]:
            with self.subTest(msgbox=name):
                self.assertTrue(hasattr(pyezgame, name), f"{name} 不存在")
                self.assertIsInstance(getattr(pyezgame, name), int)


class TestGameLibInstantiate(unittest.TestCase):
    """GameLib 实例化"""

    def test_instantiate(self) -> None:
        g = GameLib()
        self.assertIsNotNone(g)


class TestRandom(unittest.TestCase):
    """随机数"""

    def test_random_in_range(self) -> None:
        for _ in range(100):
            r = GameLib.random(1, 10)
            self.assertGreaterEqual(r, 1)
            self.assertLessEqual(r, 10)

    def test_random_min_equals_max(self) -> None:
        for _ in range(10):
            self.assertEqual(GameLib.random(5, 5), 5)


class TestRectOverlap(unittest.TestCase):
    """矩形碰撞检测"""

    def test_full_overlap(self) -> None:
        self.assertTrue(GameLib.rect_overlap(0, 0, 10, 10, 0, 0, 10, 10))

    def test_partial_overlap(self) -> None:
        self.assertTrue(GameLib.rect_overlap(0, 0, 10, 10, 5, 5, 10, 10))

    def test_no_overlap(self) -> None:
        self.assertFalse(GameLib.rect_overlap(0, 0, 10, 10, 20, 20, 10, 10))

    def test_edge_touch(self) -> None:
        self.assertFalse(GameLib.rect_overlap(0, 0, 10, 10, 10, 0, 10, 10))

    def test_containment(self) -> None:
        self.assertTrue(GameLib.rect_overlap(0, 0, 20, 20, 5, 5, 5, 5))


class TestCircleOverlap(unittest.TestCase):
    """圆形碰撞检测"""

    def test_concentric(self) -> None:
        self.assertTrue(GameLib.circle_overlap(0, 0, 10, 0, 0, 5))

    def test_far_apart(self) -> None:
        self.assertFalse(GameLib.circle_overlap(0, 0, 5, 100, 100, 5))

    def test_tangent(self) -> None:
        self.assertTrue(GameLib.circle_overlap(0, 0, 5, 10, 0, 5))

    def test_no_overlap(self) -> None:
        self.assertFalse(GameLib.circle_overlap(0, 0, 5, 11, 0, 5))


class TestPointInRect(unittest.TestCase):
    """点在矩形内判断"""

    def test_inside(self) -> None:
        self.assertTrue(GameLib.point_in_rect(5, 5, 0, 0, 10, 10))

    def test_top_left_corner(self) -> None:
        self.assertTrue(GameLib.point_in_rect(0, 0, 0, 0, 10, 10))

    def test_near_bottom_right(self) -> None:
        self.assertTrue(GameLib.point_in_rect(9, 9, 0, 0, 10, 10))

    def test_outside_bottom_right(self) -> None:
        self.assertFalse(GameLib.point_in_rect(10, 10, 0, 0, 10, 10))

    def test_outside_left(self) -> None:
        self.assertFalse(GameLib.point_in_rect(-1, 5, 0, 0, 10, 10))


class TestDistance(unittest.TestCase):
    """两点距离计算"""

    def test_3_4_5_triangle(self) -> None:
        d = GameLib.distance(0, 0, 3, 4)
        self.assertAlmostEqual(d, 5.0, places=3)

    def test_same_point_origin(self) -> None:
        self.assertEqual(GameLib.distance(0, 0, 0, 0), 0.0)

    def test_same_point(self) -> None:
        self.assertEqual(GameLib.distance(1, 1, 1, 1), 0.0)


class TestSaveLoadInt(unittest.TestCase):
    """整数存档读写"""

    path: str = ""

    def setUp(self) -> None:
        fd, self.path = tempfile.mkstemp(suffix=".sav")
        os.close(fd)

    def tearDown(self) -> None:
        GameLib.delete_save(self.path)
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_save_and_load(self) -> None:
        self.assertTrue(GameLib.save_int(self.path, "score", 12345))
        self.assertEqual(GameLib.load_int(self.path, "score"), 12345)

    def test_missing_key_returns_default(self) -> None:
        self.assertEqual(GameLib.load_int(self.path, "no_key", 999), 999)

    def test_overwrite(self) -> None:
        GameLib.save_int(self.path, "score", 111)
        GameLib.save_int(self.path, "score", 67890)
        self.assertEqual(GameLib.load_int(self.path, "score"), 67890)


class TestSaveLoadFloat(unittest.TestCase):
    """浮点数存档读写"""

    path: str = ""

    def setUp(self) -> None:
        fd, self.path = tempfile.mkstemp(suffix=".sav")
        os.close(fd)

    def tearDown(self) -> None:
        GameLib.delete_save(self.path)
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_save_and_load(self) -> None:
        self.assertTrue(GameLib.save_float(self.path, "pi", 3.14159))
        self.assertAlmostEqual(GameLib.load_float(self.path, "pi"), 3.14159, places=4)

    def test_missing_key_returns_default(self) -> None:
        self.assertEqual(GameLib.load_float(self.path, "missing", 1.5), 1.5)


class TestSaveLoadString(unittest.TestCase):
    """字符串存档读写"""

    path: str = ""

    def setUp(self) -> None:
        fd, self.path = tempfile.mkstemp(suffix=".sav")
        os.close(fd)

    def tearDown(self) -> None:
        GameLib.delete_save(self.path)
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_save_and_load(self) -> None:
        self.assertTrue(GameLib.save_string(self.path, "name", "hello world"))
        self.assertEqual(GameLib.load_string(self.path, "name"), "hello world")

    def test_missing_key_returns_default(self) -> None:
        self.assertEqual(
            GameLib.load_string(self.path, "missing", "default"), "default",
        )


class TestSaveKeyOperations(unittest.TestCase):
    """存档 key 操作"""

    path: str = ""

    def setUp(self) -> None:
        fd, self.path = tempfile.mkstemp(suffix=".sav")
        os.close(fd)

    def tearDown(self) -> None:
        GameLib.delete_save(self.path)
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_has_save_key(self) -> None:
        GameLib.save_int(self.path, "a", 1)
        GameLib.save_int(self.path, "b", 2)
        self.assertTrue(GameLib.has_save_key(self.path, "a"))
        self.assertTrue(GameLib.has_save_key(self.path, "b"))
        self.assertFalse(GameLib.has_save_key(self.path, "c"))

    def test_delete_save_key(self) -> None:
        GameLib.save_int(self.path, "a", 1)
        GameLib.save_int(self.path, "b", 2)
        self.assertTrue(GameLib.delete_save_key(self.path, "a"))
        self.assertFalse(GameLib.has_save_key(self.path, "a"))
        self.assertTrue(GameLib.has_save_key(self.path, "b"))

    def test_delete_save(self) -> None:
        GameLib.save_int(self.path, "x", 1)
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(GameLib.delete_save(self.path))
        self.assertEqual(GameLib.load_int(self.path, "x", -1), -1)


if __name__ == "__main__":
    unittest.main()
