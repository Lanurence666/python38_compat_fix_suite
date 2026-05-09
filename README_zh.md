# Python 3.8 兼容性修复套件

**中文** | [Русский](README_ru.md) | [English](README.md)

一套自动化脚本，用于将 Python 项目从 3.9+ 回移至 Python 3.8，涵盖 Python 源码和 C/C++ 扩展模块。

## 这个套件做什么？

当你有一个需要 Python 3.9+ 的项目，但需要在 Python 3.8 上运行时，你会面临两类不兼容问题：

1. **Python 语法和标准库变更**（PEP 585、604、584、616 等）
2. **Python C API 变更**（新函数、变更的签名、移除的宏等）

本套件提供两个脚本，自动检测并修复这些问题：

- **`fix_py38_python.py`** — 修复 Python 源码（`.py` 文件）
- **`fix_py38_c.py`** — 修复 C/C++ 扩展源码（`.c`、`.h`、`.cpp` 文件）

两个脚本均支持**国际化**：输出信息以系统语言显示（英文、中文或俄文）。你可以通过在 `lang/` 目录中创建 JSON 文件来添加更多语言。

## 我们的成果

我们已成功使用本套件将两个主要科学计算库回移至 Python 3.8：

| 项目 | 版本 | 状态 | 仓库 |
|------|------|------|------|
| **NumPy** | 2.x（最新 main） | 在 Python 3.8 上编译并测试通过 | [numpy_backport_py38](https://github.com/Lanurence666/numpy_backport_py38) |
| **SciPy** | 1.x（最新 main） | 在 Python 3.8 上编译并测试通过 | [scipy_backport_py38](https://github.com/Lanurence666/scipy_backport_py38) |

两个项目均以最大优化标志编译，并发布为可安装的 wheel 包。

## fix_py38_python.py — Python 源码修复

### 修复内容

| # | 功能 | PEP/版本 | 修复策略 |
|---|------|----------|----------|
| 1 | 内置泛型（`list[X]`、`dict[K,V]` 等） | PEP 585 / 3.9+ | 替换为 `typing.List[X]`、`typing.Dict[K,V]` 等 |
| 2 | 联合类型（注解中的 `X \| Y`） | PEP 604 / 3.10+ | 替换为 `Union[X, Y]` |
| 3 | 字典合并运算符（`d1 \| d2`、`d1 \|= d2`） | PEP 584 / 3.9+ | 替换为 `{**d1, **d2}` 和 `d1.update(d2)` |
| 4 | `str.removeprefix()` / `str.removesuffix()` | PEP 616 / 3.9+ | 使用 `str.startswith()`/`str.endswith()` 的回退实现 |
| 5 | `typing.Annotated` | PEP 593 / 3.9+ | `try/except` 回退到 `typing_extensions` |
| 6 | `functools.cache` | 3.9+ | 替换为 `functools.lru_cache(maxsize=None)` |
| 7 | `importlib.metadata` | 3.9+ | `try/except` 回退到 `importlib_metadata` |
| 8 | `typing.TypeAlias` / `TypeGuard` / `ParamSpec` / `Concatenate` | 3.9+ | `try/except` 回退到 `typing_extensions` |
| 9 | `isinstance(x, A \| B)` / `issubclass(x, A \| B)` | 3.10+ | 替换为 `isinstance(x, (A, B))` |
| 10 | `zoneinfo` | 3.9+ | `try/except` 回退到 `backports.zoneinfo` |
| 11 | `graphlib` | 3.9+ | `try/except` 回退 |
| 12 | `math.lcm()` | 3.9+ | `try/except` 回退实现 |
| 13 | `math.nextafter()` / `math.ulp()` | 3.9+ | `try/except` 回退实现 |
| 14 | `collections.XXX` → `collections.abc.XXX` | 3.9+ 弃用 | 替换弃用的导入 |
| 15 | `random.randbytes()` | 3.9+ | `try/except` 回退实现 |
| 16 | `ast.unparse()` | 3.9+ | `try/except` 回退到 `astunparse` |
| 17 | `bytes/bytearray.removeprefix/removesuffix` | 3.9+ | 运行时 monkey-patch 回退 |
| 18 | 括号化上下文管理器 | 3.10+ | 去括号 |
| 19 | `setup.py` / `pyproject.toml` 中的 Python 版本约束 | — | 更新版本要求 |
| 20 | `zip(..., strict=True)` | 3.10+ | `_zip_strict()` 回退实现 |
| 21 | `int.bit_count()` | 3.10+ | `_int_bit_count()` 回退实现 |
| 22 | `aiter()` / `anext()` | 3.10+ | `_aiter_compat()` / `_anext_compat()` 回退 |
| 23 | `bisect` 模块 `key=` 参数 | 3.10+ | 回退实现 |
| 24 | `dataclass(slots=True)` | 3.10+ | 移除 `slots` 参数 |
| 25 | `collections.abc.Callable[...]` 下标语法 | 3.9+ | 替换为 `typing.Callable[...]` |
| 26 | `functools.lru_cached_property` | 3.9+ | `try/except` 带完整回退类 |
| 27 | `functools.cached_property` | 3.8+ | 自动添加缺失的导入 |
| 28 | `types.GenericAlias` / `EllipsisType` / `NotImplementedType` | 3.9+ | 在 `__init__.py` 中 monkey-patch |
| 29 | 重复导入 | — | 合并 `from X import` 语句 |
| 30 | `array_api_compat` 中的 PEP 585 类型标注 | 3.9+ | 替换类型注解中的内置泛型 |

### Python 3.10–3.15 函数（仅检测，不自动修复）

脚本检测以下功能但**不**自动修复，因为它们需要手动干预：

| 功能 | 版本 | 原因 |
|------|------|------|
| `typing.NotRequired` | 3.11+ | 需要带版本检查的 `typing_extensions` |
| `collections.abc.Buffer` | 3.12+ | 无简单回退 |
| `BaseException.add_note()` | 3.11+ | 无法回退 |
| `tomllib` | 3.11+ | 使用 `tomli` 作为回退（手动） |
| `asyncio.TaskGroup` | 3.11+ | 结构性变更，无简单回退 |
| `math.exp2()` / `math.cbrt()` | 3.11+ | 需手动回退 |
| `datetime.UTC` | 3.11+ | 需手动回退 |
| `itertools.batched()` | 3.12+ | 需手动回退 |
| `pathlib.Path.walk()` | 3.12+ | 需手动回退 |
| `distutils`（3.12 中移除） | 3.12 | 使用 `setuptools` 替代 |
| `warnings.deprecated()` | 3.13+ | 无简单回退 |
| `copy.replace()` | 3.13+ | 无简单回退 |
| PEP 594 移除的模块 | 3.13 | 需手动迁移 |
| `annotationlib` | 3.14+ | 无回退 |
| `frozendict` | 3.15+ | 无回退 |
| `dbm.sqlite3` | 3.15+ | 无回退 |

## fix_py38_c.py — C/C++ 源码修复

### 修复内容

**策略：**
1. 部署 `pythoncapi_compat.h` 兼容头文件到项目中
2. 在使用 Python 3.9+ C API 的 C/C++ 文件中添加 `#include`
3. 修复直接使用 Python 3.9+ C API 而未通过兼容层的代码
4. 修复 `CMakeLists.txt` / `setup.py` 中的 Python 版本约束
5. 修复 `pythoncapi_compat.h` 中 Python 3.8 已有函数的静态/非静态声明冲突
6. 自动检测并更新不完整的 `pythoncapi_compat.h` 文件

### Python 3.9+ C API 变更覆盖

| API | 版本 | 兼容策略 |
|-----|------|----------|
| `PyObject_CallNoArgs()` | 3.9+ | 通过 `pythoncapi_compat.h` 的内联包装 |
| `PyObject_CallOneArg()` | 3.9+ | 内联包装 |
| `Py_IS_TYPE()` | 3.9+ | 宏包装 |
| `Py_SET_TYPE()` / `Py_SET_SIZE()` / `Py_SET_REFCNT()` | 3.9+ | 宏包装 |
| `PyModule_AddType()` | 3.9+ | 内联包装 |
| `PyModule_AddObjectRef()` | 3.10+ | 内联包装 |
| `PyObject_Vectorcall()` | 3.9+ | 内联包装 |
| `PyType_GetModule()` | 3.9+ | 通过 `__module__` 查找的兼容实现 |
| `PyType_GetModuleByDef()` | 3.9+ | 存根实现（需人工审查） |
| `PyType_GetSlot()` | 3.9+ | 通过 `tp_base` 链遍历的完整兼容 |
| `Py_NewRef()` / `Py_XNewRef()` | 3.10+ | 内联包装 |
| `Py_Is()` / `Py_IsNone()` / `Py_IsTrue()` / `Py_IsFalse()` | 3.10+ | 宏包装 |
| `PyFrame_GetCode()` / `PyFrame_GetBack()` | 3.9+ | 内联包装 |
| `PyErr_GetRaisedException()` / `PyErr_SetRaisedException()` | 3.12+ | 内联包装 |
| `PyObject_VectorcallDict()` / `PyObject_VectorcallMethod()` | 3.12+ | `PyObject_Call` 回退 |
| `PyDict_GetItemRef()` / `PyDict_GetItemStringRef()` | 3.13+ | `PyDict_GetItemWithError` 回退 |
| `PyList_GetItemRef()` | 3.13+ | `PyList_GetItem` + `Py_XINCREF` 回退 |
| `PyLong_AsInt()` | 3.13+ | `PyLong_AsLong` + 范围检查回退 |
| `Py_MOD_GIL_NOT_USED` / `PyUnstable_Module_SetGIL()` | 3.13+ | `#ifdef Py_GIL_DISABLED` 或版本检查保护 |

### Python 3.8 系统头文件冲突

以下函数已存在于 Python 3.8 系统头文件中。脚本自动调整 `pythoncapi_compat.h` 中的版本检查，避免静态/非静态声明冲突：

- `PyType_GetSlot` — 自 Python 3.8 起存在于 `object.h`
- `PyModule_AddFunctions` — 自 Python 3.8 起存在于 `modsupport.h`
- `PyInterpreterState_GetDict` — 自 Python 3.8 起存在于 `pystate.h`
- `PyErr_GetExcInfo` / `PyErr_SetExcInfo` — 自 Python 3.8 起存在于 `pyerrors.h`

### GCC 编译器兼容性修复

- `#pragma warning(disable:...)` → 用 `#ifdef _MSC_VER` 包裹
- `__declspec(deprecated)` → 添加 GCC `__attribute__((deprecated))` 替代
- `_aligned_malloc` → 用 `#ifdef _MSC_VER` 保护
- `PY_SSIZE_T_CLEAN` → 确保在 `#include <Python.h>` 之前定义

## pythoncapi_compat.h

本套件包含的 `pythoncapi_compat.h` 文件来自 [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat) 项目，采用 **Zero Clause BSD (0BSD)** 许可证。

我们在上游头文件基础上添加了额外的兼容实现（`EXTRA_COMPAT` 部分），涵盖上游未覆盖的 Python 3.12–3.15 API。

## 国际化 (i18n)

脚本支持多语言控制台输出。语言文件以 JSON 格式存储在 `lang/` 目录中：

```
lang/
├── en.json    # 英文（默认）
├── zh.json    # 中文
└── ru.json    # 俄文 (Русский)
```

**工作原理：**
- 脚本通过 `locale.getdefaultlocale()` 自动检测系统语言
- 如果有对应语言的翻译文件，将自动使用
- 如果未找到翻译文件，默认使用英文
- 你可以通过创建 `lang/<语言代码>.json` 文件来添加新语言

**添加新语言：**
1. 复制 `lang/en.json` 为 `lang/<你的语言代码>.json`
2. 翻译值（不是键）为你的语言
3. 将文件放入 `lang/` 目录 — 将自动检测

## 使用方法

### 前提条件

- Python 3.8+
- `i18n.py` 模块和 `lang/` 目录必须与脚本在同一目录

### 修复 Python 源码

```bash
# 修复当前目录
python fix_py38_python.py

# 修复指定项目目录
python fix_py38_python.py /path/to/project
```

### 修复 C/C++ 源码

```bash
# 修复当前目录
python fix_py38_c.py

# 修复指定项目目录
python fix_py38_c.py /path/to/project
```

### 推荐工作流程

1. **备份代码**（git commit 或复制）
2. 先运行 `fix_py38_python.py` 修复 Python 语法
3. 运行 `fix_py38_c.py` 修复 C/C++ 扩展
4. **人工检查**所有修改
5. 编译并测试
6. 手动修复剩余问题

## ⚠️ 重要警告

1. **这些脚本会就地修改源文件。** 运行前务必备份或使用版本控制。
2. **需要人工审查。** 自动修复无法正确处理所有情况，特别是：
   - 带有嵌套泛型的复杂类型注解
   - `PyCMethod` / `METH_METHOD`（Python 3.9+）— 替换为注释标记
   - `PyType_GetModuleByDef` — 存根实现，运行时可能失败
   - 非字典上下文中的字典合并运算符（numpy 数组、集合等）
3. **并非所有 Python 3.9+ 功能都能自动修复。** 参见上方的仅检测列表。
4. **运行后请充分测试。** 编译所有 C 扩展并运行项目的测试套件。
5. **`pythoncapi_compat.h` 来自 [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat)**，采用 Zero Clause BSD 许可。我们在其基础上添加了额外的兼容实现。

## 文件结构

```
python38_compat_fix_suite/
├── fix_py38_python.py       # Python 源码修复脚本
├── fix_py38_c.py            # C/C++ 源码修复脚本
├── pythoncapi_compat.h      # C API 兼容头文件（上游 + 扩展）
├── i18n.py                  # 国际化模块
├── lang/
│   ├── en.json              # 英文翻译
│   ├── zh.json              # 中文翻译
│   └── ru.json              # 俄文翻译
├── README.md                # 英文文档
├── README_ru.md             # 俄文文档
└── README_zh.md             # 本文件（中文文档）
```

## 许可证

- **脚本**（`fix_py38_python.py`、`fix_py38_c.py`、`i18n.py`）：MIT 许可证
- **`pythoncapi_compat.h`**：Zero Clause BSD (0BSD) — 来自 [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat)
