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

We have successfully used this suite to backport major scientific computing and AI libraries to Python 3.8:

| Project | Version | Status | Repository |
|---------|---------|--------|------------|
| **NumPy** | 2.x (latest main) | Compiled & tested on Python 3.8 | [numpy_backport_py38](https://github.com/Lanurence666/numpy_backport_py38) |
| **SciPy** | 1.x (latest main) | Compiled & tested on Python 3.8 | [scipy_backport_py38](https://github.com/Lanurence666/scipy_backport_py38) |
| **PyTorch** | 2.13.0a0 (latest main) | Compiled & tested on Python 3.8 | [pytorch_backport_py38](https://github.com/Lanurence666/pytorch_backport_py38) |
| **Transformers** | 5.8.0.dev0 (latest main) | Compiled & tested on Python 3.8 | — |
| **HuggingFace Hub** | 1.17.0.dev0 (latest main) | Compiled & tested on Python 3.8 | — |
| **PEFT** | 0.19.2.dev0 (latest main) | Compiled & tested on Python 3.8 | [peft_backport_py38](https://github.com/Lanurence666/peft_backport_py38) |
| **ModelScope** | 2.0.0+main (latest main) | Compiled & tested on Python 3.8 | — |

All projects were compiled with maximum optimization flags and released as installable wheels. PyTorch was installed in editable (development) mode for testing.

### Transformers + HuggingFace Hub Test Results (Python 3.8)

The latest **Transformers 5.8.0.dev0** and **HuggingFace Hub 1.17.0.dev0** were verified with comprehensive testing on Python 3.8.10 + PyTorch 2.13:

**✅ Verified Functionality:**
- Core imports: `AutoConfig`, `AutoTokenizer`, `AutoModel`, `AutoModelForCausalLM`, `AutoModelForSequenceClassification`
- Specific models: `BertModel`, `BertTokenizer`, `GPT2Model`, `GPT2Tokenizer`, `T5Model`, `T5Config`, `LlamaConfig`
- Model forward inference: BertModel, GPT2Model (with random tensors)
- Config operations: `to_dict()`, `to_json_string()`, `from_dict()`, `for_model()`
- Training infrastructure: `Trainer`, `TrainingArguments`, `pipeline`
- Processors: `ProcessorMixin`, `FeatureExtractionMixin`, `ImageProcessingMixin`
- HuggingFace Hub API: `HfApi`, `hf_hub_download`, `snapshot_download`

**🔧 Additional Manual Fixes Required (beyond automated script):**
- `match/case` → `if/elif` conversion (in huggingface_hub)
- `isinstance(x, A|B)` → `isinstance(x, (A, B))` conversion
- `from typing import Annotated` → `from typing_extensions import Annotated` (22 files)
- `torch.distributed` conditional imports (for PyTorch builds without distributed support)
- `functools.cached_property` fallback for Python 3.8
- `get_type_hints()` try/except protection for PEP 585/604 annotations
- `dataclass(kw_only=True)` conditional handling
- Module-level PEP 585 type aliases in base classes (e.g., `OrderedDict[str, str | None]`)

### PEFT Test Results (Python 3.8)

The latest **PEFT 0.19.2.dev0** was verified with comprehensive testing on Python 3.8.10 + PyTorch 2.13:

**✅ Verified Functionality:**
- Core import: `import peft`
- All config classes: `LoraConfig`, `AdaLoraConfig`, `IA3Config`, `LoHaConfig`, `LoKrConfig`, `OFTConfig`, `BOFTConfig`, `VeraConfig`, `VBLoRAConfig`, `FourierFTConfig`, `HRAConfig`, `C3AConfig`, `RandLoraConfig`, `RoadConfig`, `ShiraConfig`, `MissConfig`, `BdLoraConfig`, `CartridgeConfig`, `WaveFTConfig`, and more
- LoRA: application, forward pass, multiple target modules
- Save & load adapter
- Multiple adapters: add/set
- IA3, AdaLora
- Merge/unmerge adapter
- Disable adapter context manager
- Config serialization
- Trainable parameters count

**🔧 Additional Manual Fixes Required (beyond automated script):**
- `tuple[...]`/`dict[...]` in `TypeAlias` assignments (e.g., `WaveletCoeff2d: TypeAlias = tuple[...]`) — `from __future__ import annotations` does NOT affect TypeAlias value expressions
- `Literal["zero"] | None` in dataclass fields — `from __future__ import annotations` does NOT prevent runtime evaluation of dataclass field types
- `itertools.pairwise()` import (Python 3.10+) — now auto-fixed by the script
- `torch.distributed.tensor` availability check for custom PyTorch builds

### ModelScope Test Results (Python 3.8)

The latest **ModelScope 2.0.0+main** was verified on Python 3.8.10 + PyTorch 2.13:

**✅ Verified Functionality:**
- Core import: `import modelscope` (v2.0.0+main)
- `importlib.metadata` compatibility: `import_utils`, `plugins`
- `zoneinfo` compatibility: `hub/utils/utils` (timestamp conversion)
- Audio models: `zipformer.Zipformer2EncoderLayer`
- Streaming: `streaming_output.StreamingOutputMixin`
- Data loading: `data_loader.OssDownloader`
- Full compilation: 2859 `.py` files compiled with 0 errors

**🔧 Additional Manual Fixes Required (beyond automated script):**
- `import importlib.metadata` top-level import + direct `importlib.metadata.xxx` references → need `importlib_metadata` alias replacement
- Function-level `import zoneinfo` → need `try/except` with `backports.zoneinfo` (now auto-fixed in v2)
- `from X import \` (backslash continuation) → causes syntax errors when other fixers modify imports (now auto-fixed in v2)
- `from X import *` + `from X import (specific)` → syntax conflict after import merging (now auto-fixed in v2)
- `pyproject.toml` `license = "XXX"` format → incompatible with older setuptools (now auto-fixed in v2)
- `pyproject.toml` `license-files = [...]` → not supported by older setuptools (now auto-fixed in v2)
- `x**2(y)` missing `*` operator → `x**2*(y)` (now auto-fixed in v2)
- `'\?'` invalid escape sequence → `'\\?'` (now auto-fixed in v2)

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
| 32 | Type alias union (`X: TypeAlias = A \| B`) | 3.10+ | Convert to `X: TypeAlias = Union[A, B]` with auto `Union` import |
| 33 | `dataclass(kw_only=True)` | 3.10+ | Remove `kw_only` parameter |
| 34 | `inspect.get_annotations()` | 3.10+ | `try/except` fallback to manual annotation extraction |
| 35 | `TypeAliasType` (PEP 695 `type X = Y`) | 3.12+ | Convert to `typing.TypeAlias` assignment |
| 36 | Runtime type union (`X \| Y` outside annotations) | 3.10+ | Convert to `Union[X, Y]` at runtime-evaluated positions |
| 37 | PEP 604 non-annotation union (class body, default values) | 3.10+ | Convert to `Union[X, Y]` with `from __future__ import annotations` awareness |
| 38 | PEP 695 generic class (`class X[T]:`) | PEP 695 / 3.12+ | Convert to `Generic[T]` base class with `TypeVar` |
| 39 | PEP 695 generic function (`def f[T]():`) | PEP 695 / 3.12+ | Convert to `TypeVar` with `@overload` where needed |
| 40 | PEP 695 type statement (`type X = Y`) | PEP 695 / 3.12+ | Convert to `X: TypeAlias = Y` |
| 41 | Lambda decorator (`@lambda x: x`) | 3.9+ syntax | Wrap in regular function |
| 42 | `match`/`case` statement | PEP 634 / 3.10+ | Mark with TODO comment (requires manual rewrite as `if/elif`) |
| 43 | `typing` 3.11+ features (`NotRequired`, `TypeVarTuple`, etc.) | 3.11+ | `try/except` fallback to `typing_extensions` |
| 44 | `enum.StrEnum` | 3.11+ | `try/except` fallback with manual implementation |
| 45 | `contextlib.chdir()` | 3.11+ | `try/except` fallback implementation |
| 46 | `operator.call()` | 3.11+ | `try/except` fallback implementation |
| 47 | `hashlib.file_digest()` | 3.11+ | `try/except` fallback implementation |
| 48 | `collections.abc.Iterator[...]` subscripting | 3.9+ | Replace with `typing.Iterator[...]` |
| 49 | Regex flag merge (`re.X \| re.I` etc. in module-level constants) | 3.11+ | Convert to `re.compile()` with combined flags |
| 50 | `from __future__ import annotations` position fix | — | Move to top of file if not first import |
| 51 | Broken `# noqa` comments after import rewrites | — | Clean up stale `# noqa` directives |
| 52 | Type alias PEP 585 + 604 combined (`X = dict[str, int \| str]`) | 3.9+ | Recursive conversion: `dict` → `Dict`, `\|` → `Union`, with nested bracket handling |
| 53 | Dict merge with improved variable detection (`self.kwargs \| other`) | 3.9+ | Detect dotted variable names and `kwargs`-style variables for dict merge conversion |
| 54 | `ExceptionGroup` / `BaseExceptionGroup` | 3.11+ | `try/except` fallback to `exceptiongroup` |
| 55 | `itertools.pairwise()` | 3.10+ | `try/except` fallback with `_itertools_pairwise_compat()` implementation |
| 56 | Dataclass field union (`X \| None` in dataclass fields) | 3.10+ | Convert to `Optional[X]` / `Union[X, Y]` — `from __future__ import annotations` does NOT prevent runtime evaluation of dataclass field types |
| 57 | TypeAlias PEP 585 without `from __future__ import annotations` | 3.9+ | Direct replacement: `tuple[...]` → `Tuple[...]`, `dict[...]` → `Dict[...]` in TypeAlias values — `from __future__ import annotations` does NOT affect TypeAlias value expressions |
| 58 | Backslash continuation imports (`from X import \`) | — | Convert to parenthesised multi-line imports to prevent syntax errors when other fixers modify imports |
| 59 | `from X import *` + `from X import (specific)` conflict | — | Remove `import *` when specific imports from the same module exist — prevents syntax errors after import merging |
| 60 | Invalid escape sequences (`'\?'`, `'\d'` etc.) | 3.12+ warning | Double the backslash in invalid escape sequences inside string literals |
| 61 | Missing operator before paren (`x**2(y)`) | — | Insert missing `*` operator between power expressions and parentheses |
| 62 | `importlib.metadata.xxx` direct references | 3.9+ | Replace `importlib.metadata.version()` etc. with `importlib_metadata.version()` after adding compat import |
| 63 | Function-level `import zoneinfo` | 3.9+ | `try/except` fallback to `backports.zoneinfo` with proper indentation |
| 64 | `pyproject.toml` license format | — | Convert `license = "XXX"` → `license = {text = "XXX"}` for older setuptools compat; remove `license-files`; lower `setuptools>=69` → `setuptools>=64` |
| 65 | Revert log file | — | When a file is reverted due to syntax errors, write details to `python38-pythonfix-log.txt` for manual review |

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
| `compression.zstd` | 3.15+ | No fallback |
| `concurrent` interpreters module | 3.14+ | No fallback |
| `annotationlib` | 3.14+ | No fallback |
| `frozendict` | 3.15+ | No fallback |
| `dbm.sqlite3` | 3.15+ | No fallback |
| `base64.z85` | 3.15+ | No fallback |
| `sentinel` | 3.14+ | No fallback |
| `profiling` module | 3.15+ | No fallback |
| `typing` 3.13+ / 3.15+ features | 3.13+ | Requires manual `typing_extensions` version check |

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
| `PyObject_GetAIter()` | 3.10+ | `PyObject_CallMethod(o, "__aiter__", NULL)` fallback |
| `Py_tp_*` slot constants | 3.9+ | `#ifndef` guarded definitions for `PyType_GetSlot` compat |

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

### Per-Function Guards

All compatibility functions in `pythoncapi_compat.h` (both upstream and our extra implementations) are wrapped with per-function `#ifndef` guards:

```c
#ifndef _PYCAPI_COMPAT_PyType_GetSlot
#define _PYCAPI_COMPAT_PyType_GetSlot
// ... implementation ...
#endif /* _PYCAPI_COMPAT_PyType_GetSlot */
```

This prevents redefinition errors when multiple projects (e.g., NumPy + SciPy + PyTorch) each include their own copy of `pythoncapi_compat.h`. The `fix_py38_c.py` script automatically adds these guards to any existing `pythoncapi_compat.h` that lacks them.

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
