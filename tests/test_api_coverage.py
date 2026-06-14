"""检查 .pyi 中声明的公开接口是否在测试中均有覆盖。

运行方式:
    pytest tests/test_api_coverage.py -v
    pytest tests/test_api_coverage.py -v -s          # 打印详细未覆盖列表
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

# ── 路径常量 ──────────────────────────────────────────────

_PYI_PATH = Path(__file__).resolve().parent.parent / "pyezgame" / "__init__.pyi"
_TESTS_DIR = Path(__file__).resolve().parent


# ── 辅助函数 ──────────────────────────────────────────────


def _parse_pyi() -> tuple[list[str], list[str], list[str]]:
    """解析 .pyi 文件，返回 (模块级名称, GameLib 方法名, 模块级函数名)。"""
    source = _PYI_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    module_attrs: list[str] = []  # 模块级常量 (如 COLOR_BLACK)
    module_funcs: list[str] = []  # 模块级函数 (如 COLOR_RGB, clamp)
    gamelib_methods: list[str] = []  # GameLib 类方法

    for node in ast.iter_child_nodes(tree):
        # 模块级变量注解: COLOR_BLACK: int
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
            if not name.startswith("_"):
                module_attrs.append(name)

        # 模块级函数: def COLOR_RGB(...) / def clamp(...)
        elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            module_funcs.append(node.name)

        # GameLib 类
        elif isinstance(node, ast.ClassDef) and node.name == "GameLib":
            seen: set[str] = set()
            for item in ast.iter_child_nodes(node):
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    if item.name not in seen:
                        gamelib_methods.append(item.name)
                        seen.add(item.name)

    return module_attrs, module_funcs, gamelib_methods


def _collect_test_source() -> str:
    """读取 tests/ 下所有 test_*.py 文件的源码。"""
    parts: list[str] = []
    for p in sorted(_TESTS_DIR.glob("test_*.py")):
        if p.name == "test_api_coverage.py":
            continue
        parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _names_referenced_in_tests(source: str, names: list[str]) -> list[str]:
    """返回在测试源码中被引用的名称列表。"""
    return [n for n in names if n in source]


def _names_missing(source: str, names: list[str]) -> list[str]:
    """返回在测试源码中 **未** 被引用的名称列表。"""
    return [n for n in names if n not in source]


# ── 测试用例 ──────────────────────────────────────────────


class TestApiCoverage:
    """检查 .pyi 声明的公开接口是否都被测试覆盖。"""

    module_attrs: list[str] = []
    module_funcs: list[str] = []
    gamelib_methods: list[str] = []
    test_source: str = ""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        self.module_attrs, self.module_funcs, self.gamelib_methods = _parse_pyi()
        self.test_source = _collect_test_source()

    # ---- 模块级常量 ----

    def test_module_attr_coverage(self) -> None:
        missing = _names_missing(self.test_source, self.module_attrs)
        assert not missing, f"以下模块级常量未在测试中出现 ({len(missing)}/{len(self.module_attrs)}):\n" + "\n".join(
            f"  - {n}" for n in missing
        )

    # ---- 模块级函数 ----

    def test_module_func_coverage(self) -> None:
        missing = _names_missing(self.test_source, self.module_funcs)
        assert not missing, f"以下模块级函数未在测试中出现 ({len(missing)}/{len(self.module_funcs)}):\n" + "\n".join(
            f"  - {n}" for n in missing
        )

    # ---- GameLib 方法 ----

    def test_gamelib_method_coverage(self) -> None:
        missing = _names_missing(self.test_source, self.gamelib_methods)
        assert not missing, (
            f"以下 GameLib 方法未在测试中出现 ({len(missing)}/{len(self.gamelib_methods)}):\n"
            + "\n".join(f"  - {n}" for n in missing)
        )

    # ---- 汇总报告 (始终打印) ----

    def test_summary_report(self, capsys: pytest.CaptureFixture[str]) -> None:
        """打印覆盖率汇总，无论是否全部覆盖。"""
        attr_missing = _names_missing(self.test_source, self.module_attrs)
        func_missing = _names_missing(self.test_source, self.module_funcs)
        method_missing = _names_missing(self.test_source, self.gamelib_methods)

        total = len(self.module_attrs) + len(self.module_funcs) + len(self.gamelib_methods)
        covered = total - len(attr_missing) - len(func_missing) - len(method_missing)

        lines = [
            "",
            "=" * 60,
            "  pyi 接口覆盖报告",
            "=" * 60,
            f"  模块级常量:  {len(self.module_attrs) - len(attr_missing):>3}/{len(self.module_attrs):>3} 已覆盖",
            f"  模块级函数:  {len(self.module_funcs) - len(func_missing):>3}/{len(self.module_funcs):>3} 已覆盖",
            f"  GameLib方法: {len(self.gamelib_methods) - len(method_missing):>3}/{len(self.gamelib_methods):>3} 已覆盖",
            "-" * 60,
            f"  总计:        {covered:>3}/{total:>3}  ({covered * 100 // total}%)",
            "=" * 60,
        ]

        if attr_missing:
            lines.append("\n  未覆盖的模块级常量:")
            lines.extend(f"    - {n}" for n in attr_missing)
        if func_missing:
            lines.append("\n  未覆盖的模块级函数:")
            lines.extend(f"    - {n}" for n in func_missing)
        if method_missing:
            lines.append("\n  未覆盖的 GameLib 方法:")
            lines.extend(f"    - {n}" for n in method_missing)

        "\n".join(lines) + "\n"

        # 用 capsys 确保在 -s 模式下可见
        with capsys.disabled():
            pass

        # 如果有未覆盖的接口，标记为 xfail 而非 fail，方便渐进修复
        if covered < total:
            pytest.xfail(f"接口覆盖率 {covered}/{total}，有 {total - covered} 个接口未覆盖")
