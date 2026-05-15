# Python 3.8 Compatibility Fix Suite

[Русский](README_ru.md) | [中文](README_zh.md) | **English**

A suite of automated scripts to backport Python projects from 3.9+ to Python 3.8, covering both Python source code and C/C++ extension modules.

## What Does This Suite Do?

When you have a Python project that requires Python 3.9+ but need to run it on Python 3.8, you face two categories of incompatibilities:

1. **Python syntax and standard library changes** (PEP 585, 604, 584, 616, etc.)
2. **Python C API changes** (new functions, changed signatures, removed macros, etc.)

This suite provides two scripts that automatically detect and fix these issues:

- **`fix_py38_python.py`** — Fixes Python source code (`.py` files)
- **`fix_py38_c.py`** — Fixes C/C++ extension source code (`.c`, `.h`, `.cpp` files)

Both scripts are **i18n-aware**: output messages are displayed in your system language (English, Chinese, or Russian). You can add more languages by creating JSON files in the `lang/` directory.

## Our Results

We have successfully used this suite to backport two major scientific computing libraries to Python 3.8:

| Project | Version | Status | Repository |
|---------|---------|--------|------------|
| **NumPy** | 2.x (latest main) | Compiled & tested on Python 3.8 | [numpy_backport_py38](https://github.com/Lanurence666/numpy_backport_py38) |
| **SciPy** | 1.x (latest main) | Compiled & tested on Python 3.8 | [scipy_backport_py38](https://github.com/Lanurence666/scipy_backport_py38) |
| **PyTorch** | 2.13.0a0 (latest main) | Compiled & tested on Python 3.8 | [pytorch_backport_py38](https://github.com/Lanurence666/pytorch_backport_py38) |

Both projects were compiled with maximum optimization flags and released as installable wheels. PyTorch was installed in editable (development) mode for testing.

## fix_py38_python.py — Python Source Fixes

### What It Fixes

| # | Feature | PEP/Version | Fix Strategy |
|---|---------|-------------|--------------|
| 1 | Built-in generics (`list[X]`, `dict[K,V]`, etc.) | PEP 585 / 3.9+ | Replace with `typing.List[X]`, `typing.Dict[K,V]`, etc. |
| 2 | Union types (`X \| Y` in annotations) | PEP 604 / 3.10+ | Replace with `Union[X, Y]` |
| 3 | Dictionary merge operators (`d1 \| d2`, `d1 \|= d2`) | PEP 584 / 3.9+ | Replace with `{**d1, **d2}` and `d1.update(d2)` |
| 4 | `str.removeprefix()` / `str.removesuffix()` | PEP 616 / 3.9+ | Fallback implementation with `str.startswith()`/`str.endswith()` |
| 5 | `typing.Annotated` | PEP 593 / 3.9+ | `try/except` fallback to `typing_extensions` |
| 6 | `functools.cache` | 3.9+ | Replace with `functools.lru_cache(maxsize=None)` |
| 7 | `importlib.metadata` | 3.9+ | `try/except` fallback to `importlib_metadata` |
| 8 | `typing.TypeAlias` / `TypeGuard` / `ParamSpec` / `Concatenate` | 3.9+ | `try/except` fallback to `typing_extensions` |
| 9 | `isinstance(x, A \| B)` / `issubclass(x, A \| B)` | 3.10+ | Replace with `isinstance(x, (A, B))` |
| 10 | `zoneinfo` | 3.9+ | `try/except` fallback to `backports.zoneinfo` |
| 11 | `graphlib` | 3.9+ | `try/except` fallback |
| 12 | `math.lcm()` | 3.9+ | `try/except` fallback implementation |
| 13 | `math.nextafter()` / `math.ulp()` | 3.9+ | `try/except` fallback implementation |
| 14 | `collections.XXX` → `collections.abc.XXX` | 3.9+ deprecation | Replace deprecated imports |
| 15 | `random.randbytes()` | 3.9+ | `try/except` fallback implementation |
| 16 | `ast.unparse()` | 3.9+ | `try/except` fallback to `astunparse` |
| 17 | `bytes/bytearray.removeprefix/removesuffix` | 3.9+ | Runtime monkey-patch fallback |
| 18 | Parenthesized context managers | 3.10+ | Unparenthesize |
| 19 | `setup.py` / `pyproject.toml` Python version constraints | — | Update version requirements |
| 20 | `zip(..., strict=True)` | 3.10+ | `_zip_strict()` fallback implementation |
| 21 | `int.bit_count()` | 3.10+ | `_int_bit_count()` fallback implementation |
| 22 | `aiter()` / `anext()` | 3.10+ | `_aiter_compat()` / `_anext_compat()` fallback |
| 23 | `bisect` module `key=` parameter | 3.10+ | Fallback implementation |
| 24 | `dataclass(slots=True)` | 3.10+ | Remove `slots` parameter |
| 25 | `collections.abc.Callable[...]` subscripting | 3.9+ | Replace with `typing.Callable[...]` |
| 26 | `functools.lru_cached_property` | 3.9+ | `try/except` with full fallback class |
| 27 | `functools.cached_property` | 3.8+ | Auto-add missing import |
| 28 | `types.GenericAlias` / `EllipsisType` / `NotImplementedType` | 3.9+ | Monkey-patch in `__init__.py` |
| 29 | Duplicate imports | — | Merge `from X import` statements |
| 30 | `array_api_compat` PEP 585 typing | 3.9+ | Replace built-in generics in type annotations |
| 31 | `AttributeError(msg, name=..., obj=...)` keyword-only args | 3.10+ | Remove `name=None`/`obj=None` or use `_AttributeError_compat()` helper |

### Python 3.10–3.15 Functions (Detected but NOT Auto-Fixed)

The script detects the following features but does **not** automatically fix them, as they require manual intervention:

| Feature | Version | Reason |
|---------|---------|--------|
| `typing.NotRequired` | 3.11+ | Requires `typing_extensions` with version check |
| `collections.abc.Buffer` | 3.12+ | No simple fallback |
| `BaseException.add_note()` | 3.11+ | No fallback possible |
| `tomllib` | 3.11+ | Use `tomli` as fallback (manual) |
| `asyncio.TaskGroup` | 3.11+ | Structural change, no simple fallback |
| `math.exp2()` / `math.cbrt()` | 3.11+ | Manual fallback needed |
| `datetime.UTC` | 3.11+ | Manual fallback needed |
| `itertools.batched()` | 3.12+ | Manual fallback needed |
| `pathlib.Path.walk()` | 3.12+ | Manual fallback needed |
| `distutils` (removed in 3.12) | 3.12 | Use `setuptools` as replacement |
| `warnings.deprecated()` | 3.13+ | No simple fallback |
| `copy.replace()` | 3.13+ | No simple fallback |
| PEP 594 removed modules | 3.13 | Manual migration needed |
| `annotationlib` | 3.14+ | No fallback |
| `frozendict` | 3.15+ | No fallback |
| `dbm.sqlite3` | 3.15+ | No fallback |

## fix_py38_c.py — C/C++ Source Fixes

### What It Fixes

**Strategy:**
1. Deploy `pythoncapi_compat.h` compatibility header to the project
2. Add `#include "pythoncapi_compat.h"` to files using Python 3.9+ C API
3. Fix direct usage of Python 3.9+ C API without going through the compat layer
4. Fix `CMakeLists.txt` / `setup.py` Python version constraints
5. Fix static/non-static declaration conflicts in `pythoncapi_compat.h` for functions already present in Python 3.8 system headers
6. Auto-detect and update incomplete `pythoncapi_compat.h` files
7. Add per-function `#ifndef` guards to `pythoncapi_compat.h` to prevent redefinition errors when multiple projects (e.g., numpy + scipy) each include their own copy

### Python 3.9+ C API Changes Covered

| API | Version | Compat Strategy |
|-----|---------|-----------------|
| `PyObject_CallNoArgs()` | 3.9+ | Inline wrapper via `pythoncapi_compat.h` |
| `PyObject_CallOneArg()` | 3.9+ | Inline wrapper |
| `Py_IS_TYPE()` | 3.9+ | Macro wrapper |
| `Py_SET_TYPE()` / `Py_SET_SIZE()` / `Py_SET_REFCNT()` | 3.9+ | Macro wrappers |
| `PyModule_AddType()` | 3.9+ | Inline wrapper |
| `PyModule_AddObjectRef()` | 3.10+ | Inline wrapper |
| `PyObject_Vectorcall()` | 3.9+ | Inline wrapper |
| `PyType_GetModule()` | 3.9+ | Compat implementation via `__module__` lookup |
| `PyType_GetModuleByDef()` | 3.9+ | Stub implementation (needs manual review) |
| `PyType_GetSlot()` | 3.9+ | Full compat via `tp_base` chain traversal |
| `Py_NewRef()` / `Py_XNewRef()` | 3.10+ | Inline wrappers |
| `Py_Is()` / `Py_IsNone()` / `Py_IsTrue()` / `Py_IsFalse()` | 3.10+ | Macro wrappers |
| `PyFrame_GetCode()` / `PyFrame_GetBack()` | 3.9+ | Inline wrappers |
| `PyErr_GetRaisedException()` / `PyErr_SetRaisedException()` | 3.12+ | Inline wrappers |
| `PyObject_VectorcallDict()` / `PyObject_VectorcallMethod()` | 3.12+ | `PyObject_Call` fallback |
| `PyDict_GetItemRef()` / `PyDict_GetItemStringRef()` | 3.13+ | `PyDict_GetItemWithError` fallback |
| `PyList_GetItemRef()` | 3.13+ | `PyList_GetItem` + `Py_XINCREF` fallback |
| `PyLong_AsInt()` | 3.13+ | `PyLong_AsLong` + range check fallback |
| `Py_MOD_GIL_NOT_USED` / `PyUnstable_Module_SetGIL()` | 3.13+ | `#ifdef Py_GIL_DISABLED` or version check guard |

### Python 3.8 System Header Conflicts

The following functions are already present in Python 3.8 system headers. The script automatically adjusts version checks in `pythoncapi_compat.h` to avoid static/non-static declaration conflicts:

- `PyType_GetSlot` — present in `object.h` since Python 3.8
- `PyModule_AddFunctions` — present in `modsupport.h` since Python 3.8
- `PyInterpreterState_GetDict` — present in `pystate.h` since Python 3.8
- `PyErr_GetExcInfo` / `PyErr_SetExcInfo` — present in `pyerrors.h` since Python 3.8

### GCC Compiler Compatibility Fixes

- `#pragma warning(disable:...)` → wrap with `#ifdef _MSC_VER`
- `__declspec(deprecated)` → add GCC `__attribute__((deprecated))` alternative
- `_aligned_malloc` → wrap with `#ifdef _MSC_VER` guard
- `PY_SSIZE_T_CLEAN` → ensure defined before `#include <Python.h>`

## pythoncapi_compat.h

The `pythoncapi_compat.h` file included in this suite is sourced from the [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat) project, licensed under the **Zero Clause BSD (0BSD)** license.

We have added extra compatibility implementations (`EXTRA_COMPAT` section) for APIs not covered by the upstream header, including Python 3.12–3.15 APIs.

## Internationalization (i18n)

The scripts support multiple languages for console output. Language files are stored as JSON in the `lang/` directory:

```
lang/
├── en.json    # English (default)
├── zh.json    # Chinese (中文)
└── ru.json    # Russian (Русский)
```

**How it works:**
- The script auto-detects your system language via `locale.getdefaultlocale()`
- If your language has a translation file, it will be used
- If no translation file is found, English is used as the default
- You can add new languages by creating a `lang/<code>.json` file with the same keys as `en.json`

**To add a new language:**
1. Copy `lang/en.json` to `lang/<your_language_code>.json`
2. Translate the values (not the keys) to your language
3. Place the file in the `lang/` directory — it will be auto-detected

## Usage

### Prerequisites

- Python 3.8+
- The `i18n.py` module and `lang/` directory must be in the same directory as the scripts

### Fix Python Source Code

```bash
# Fix the current directory
python fix_py38_python.py

# Fix a specific project directory
python fix_py38_python.py /path/to/project
```

### Fix C/C++ Source Code

```bash
# Fix the current directory
python fix_py38_c.py

# Fix a specific project directory
python fix_py38_c.py /path/to/project
```

### Recommended Workflow

1. **Backup your code** (git commit or copy)
2. Run `fix_py38_python.py` first to fix Python syntax
3. Run `fix_py38_c.py` to fix C/C++ extensions
4. **Manually review** all changes
5. Compile and test
6. Fix any remaining issues manually

## ⚠️ Important Warnings

1. **These scripts modify source files in-place.** Always backup or use version control before running.
2. **Manual review is required.** Automated fixes cannot handle all cases correctly, especially:
   - Complex type annotations with nested generics
   - `PyCMethod` / `METH_METHOD` (Python 3.9+) — replaced with comment markers
   - `PyType_GetModuleByDef` — stub implementation, may fail at runtime
   - Dictionary merge operators in non-dict contexts (numpy arrays, sets, etc.)
3. **Not all Python 3.9+ features can be automatically fixed.** See the detection-only lists above.
4. **Test thoroughly after running.** Compile all C extensions and run the project's test suite.
5. **The `pythoncapi_compat.h` is from [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat)** under the Zero Clause BSD license. We added extra compat implementations on top of it.

## File Structure

```
python38_compat_fix_suite/
├── fix_py38_python.py       # Python source fix script
├── fix_py38_c.py            # C/C++ source fix script
├── pythoncapi_compat.h      # C API compatibility header (upstream + extras)
├── i18n.py                  # Internationalization module
├── lang/
│   ├── en.json              # English translations
│   ├── zh.json              # Chinese translations
│   └── ru.json              # Russian translations
├── README.md                # This file (English)
├── README_ru.md             # Russian documentation
└── README_zh.md             # Chinese documentation
```

## License

- **Scripts** (`fix_py38_python.py`, `fix_py38_c.py`, `i18n.py`): MIT License
- **`pythoncapi_compat.h`**: Zero Clause BSD (0BSD) — from [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat)
