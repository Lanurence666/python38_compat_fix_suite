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

我们已成功使用本套件将主要科学计算和AI库回移至 Python 3.8：

| 项目 | 版本 | 状态 | 仓库 |
|------|------|------|------|
| **NumPy** | 2.x（最新 main） | 在 Python 3.8 上编译并测试通过 | [numpy_backport_py38](https://github.com/Lanurence666/numpy_backport_py38) |
| **SciPy** | 1.x（最新 main） | 在 Python 3.8 上编译并测试通过 | [scipy_backport_py38](https://github.com/Lanurence666/scipy_backport_py38) |
| **PyTorch** | 2.13.0a0（最新 main） | 在 Python 3.8 上编译并测试通过 | [pytorch_backport_py38](https://github.com/Lanurence666/pytorch_backport_py38) |
| **Transformers** | 5.8.0.dev0（最新 main） | 在 Python 3.8 上编译并测试通过 | — |
| **HuggingFace Hub** | 1.17.0.dev0（最新 main） | 在 Python 3.8 上编译并测试通过 | — |
| **PEFT** | 0.19.2.dev0（最新 main） | 在 Python 3.8 上编译并测试通过 | [peft_backport_py38](https://github.com/Lanurence666/peft_backport_py38) |
| **ModelScope** | 2.0.0+main（最新 main） | 在 Python 3.8 上编译并测试通过 | — |

所有项目均以最大优化标志编译，并发布为可安装的 wheel 包。PyTorch 以可编辑（开发）模式安装进行测试。

### Transformers + HuggingFace Hub 测试结果（Python 3.8）

最新的 **Transformers 5.8.0.dev0** 和 **HuggingFace Hub 1.17.0.dev0** 已在 Python 3.8.10 + PyTorch 2.13 环境下通过全面测试验证：

**✅ 已验证功能：**
- 核心导入：`AutoConfig`、`AutoTokenizer`、`AutoModel`、`AutoModelForCausalLM`、`AutoModelForSequenceClassification`
- 具体模型：`BertModel`、`BertTokenizer`、`GPT2Model`、`GPT2Tokenizer`、`T5Model`、`T5Config`、`LlamaConfig`
- 模型前向推理：BertModel、GPT2Model（随机张量）
- Config 操作：`to_dict()`、`to_json_string()`、`from_dict()`、`for_model()`
- 训练基础设施：`Trainer`、`TrainingArguments`、`pipeline`
- 处理器：`ProcessorMixin`、`FeatureExtractionMixin`、`ImageProcessingMixin`
- HuggingFace Hub API：`HfApi`、`hf_hub_download`、`snapshot_download`

**🔧 需额外手动修复（超出自动脚本范围）：**
- `match/case` → `if/elif` 转换（huggingface_hub 中）
- `isinstance(x, A|B)` → `isinstance(x, (A, B))` 转换
- `from typing import Annotated` → `from typing_extensions import Annotated`（22 个文件）
- `torch.distributed` 条件导入（针对未启用分布式支持的 PyTorch 构建）
- `functools.cached_property` Python 3.8 回退
- `get_type_hints()` try/except 保护（PEP 585/604 注解）
- `dataclass(kw_only=True)` 条件处理
- 模块级 PEP 585 类型别名在基类中的使用（如 `OrderedDict[str, str | None]`）

### PEFT 测试结果（Python 3.8）

最新的 **PEFT 0.19.2.dev0** 已在 Python 3.8.10 + PyTorch 2.13 环境下通过全面测试验证：

**✅ 已验证功能：**
- 核心导入：`import peft`
- 所有配置类：`LoraConfig`、`AdaLoraConfig`、`IA3Config`、`LoHaConfig`、`LoKrConfig`、`OFTConfig`、`BOFTConfig`、`VeraConfig`、`VBLoRAConfig`、`FourierFTConfig`、`HRAConfig`、`C3AConfig`、`RandLoraConfig`、`RoadConfig`、`ShiraConfig`、`MissConfig`、`BdLoraConfig`、`CartridgeConfig`、`WaveFTConfig` 等
- LoRA：应用、前向传播、多目标模块
- 保存与加载 adapter
- 多 adapter 管理：添加/切换
- IA3、AdaLora
- 合并/取消合并 adapter
- 禁用 adapter 上下文管理器
- 配置序列化
- 可训练参数计数

**🔧 需额外手动修复（超出自动脚本范围）：**
- TypeAlias 赋值中的 `tuple[...]`/`dict[...]`（如 `WaveletCoeff2d: TypeAlias = tuple[...]`）— `from __future__ import annotations` 不影响 TypeAlias 值表达式
- dataclass 字段中的 `Literal["zero"] | None` — `from __future__ import annotations` 不阻止 dataclass 字段类型的运行时求值
- `itertools.pairwise()` 导入（Python 3.10+）— 现已由脚本自动修复
- 自定义 PyTorch 构建的 `torch.distributed.tensor` 可用性检查

### ModelScope 测试结果（Python 3.8）

最新的 **ModelScope 2.0.0+main** 已在 Python 3.8.10 + PyTorch 2.13 环境下通过验证：

**✅ 已验证功能：**
- 核心导入：`import modelscope`（v2.0.0+main）
- `importlib.metadata` 兼容性：`import_utils`、`plugins`
- `zoneinfo` 兼容性：`hub/utils/utils`（时间戳转换）
- 音频模型：`zipformer.Zipformer2EncoderLayer`
- 流式输出：`streaming_output.StreamingOutputMixin`
- 数据加载：`data_loader.OssDownloader`
- 完整编译：2859 个 `.py` 文件编译通过，0 错误

**🔧 需额外手动修复（超出自动脚本范围）：**
- `import importlib.metadata` 顶层导入 + `importlib.metadata.xxx` 直接引用 → 需要 `importlib_metadata` 别名替换
- 函数内 `import zoneinfo` → 需要 `try/except` 加 `backports.zoneinfo`（v2 已自动修复）
- `from X import \` 反斜杠续行 → 其他修复器修改导入时产生语法错误（v2 已自动修复）
- `from X import *` + `from X import (具体名)` → 导入合并后语法冲突（v2 已自动修复）
- `pyproject.toml` `license = "XXX"` 格式 → 旧版 setuptools 不兼容（v2 已自动修复）
- `pyproject.toml` `license-files = [...]` → 旧版 setuptools 不支持（v2 已自动修复）
- `x**2(y)` 缺少 `*` 运算符 → `x**2*(y)`（v2 已自动修复）
- `'\?'` 无效转义序列 → `'\\?'`（v2 已自动修复）

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
| 31 | `AttributeError(msg, name=..., obj=...)` keyword-only 参数 | 3.10+ | 移除 `name=None`/`obj=None` 或使用 `_AttributeError_compat()` 辅助函数 |
| 32 | 类型别名联合 (`X: TypeAlias = A \| B`) | 3.10+ | 转换为 `X: TypeAlias = Union[A, B]`，自动导入 `Union` |
| 33 | `dataclass(kw_only=True)` | 3.10+ | 移除 `kw_only` 参数 |
| 34 | `inspect.get_annotations()` | 3.10+ | `try/except` 回退到手动注解提取 |
| 35 | `TypeAliasType`（PEP 695 `type X = Y`） | 3.12+ | 转换为 `typing.TypeAlias` 赋值 |
| 36 | 运行时类型联合（注解外的 `X \| Y`） | 3.10+ | 在运行时求值位置转换为 `Union[X, Y]` |
| 37 | PEP 604 非注解联合（类体、默认值） | 3.10+ | 转换为 `Union[X, Y]`，感知 `from __future__ import annotations` |
| 38 | PEP 695 泛型类（`class X[T]:`） | PEP 695 / 3.12+ | 转换为 `Generic[T]` 基类 + `TypeVar` |
| 39 | PEP 695 泛型函数（`def f[T]():`） | PEP 695 / 3.12+ | 转换为 `TypeVar`，必要时添加 `@overload` |
| 40 | PEP 695 类型语句（`type X = Y`） | PEP 695 / 3.12+ | 转换为 `X: TypeAlias = Y` |
| 41 | Lambda 装饰器（`@lambda x: x`） | 3.9+ 语法 | 包装为常规函数 |
| 42 | `match`/`case` 语句 | PEP 634 / 3.10+ | 标记 TODO 注释（需手动改写为 `if/elif`） |
| 43 | `typing` 3.11+ 功能（`NotRequired`、`TypeVarTuple` 等） | 3.11+ | `try/except` 回退到 `typing_extensions` |
| 44 | `enum.StrEnum` | 3.11+ | `try/except` 回退并手动实现 |
| 45 | `contextlib.chdir()` | 3.11+ | `try/except` 回退实现 |
| 46 | `operator.call()` | 3.11+ | `try/except` 回退实现 |
| 47 | `hashlib.file_digest()` | 3.11+ | `try/except` 回退实现 |
| 48 | `collections.abc.Iterator[...]` 下标语法 | 3.9+ | 替换为 `typing.Iterator[...]` |
| 49 | 正则标志合并（模块级常量中的 `re.X \| re.I` 等） | 3.11+ | 转换为 `re.compile()` 组合标志 |
| 50 | `from __future__ import annotations` 位置修复 | — | 移至文件顶部（如果不是第一个导入） |
| 51 | 导入重写后损坏的 `# noqa` 注释 | — | 清理过时的 `# noqa` 指令 |
| 52 | 类型别名 PEP 585 + 604 组合（`X = dict[str, int \| str]`） | 3.9+ | 递归转换：`dict` → `Dict`，`\|` → `Union`，支持嵌套括号处理 |
| 53 | 改进的字典合并变量检测（`self.kwargs \| other`） | 3.9+ | 检测带点变量名和 `kwargs` 风格变量进行字典合并转换 |
| 54 | `ExceptionGroup` / `BaseExceptionGroup` | 3.11+ | `try/except` 回退到 `exceptiongroup` |
| 55 | `itertools.pairwise()` | 3.10+ | `try/except` 回退并使用 `_itertools_pairwise_compat()` 实现 |
| 56 | dataclass 字段联合类型（`X \| None`） | 3.10+ | 转换为 `Optional[X]` / `Union[X, Y]` — `from __future__ import annotations` 不阻止 dataclass 字段类型的运行时求值 |
| 57 | 无 `from __future__ import annotations` 时的 TypeAlias PEP 585 | 3.9+ | 直接替换：`tuple[...]` → `Tuple[...]`、`dict[...]` → `Dict[...]` — `from __future__ import annotations` 不影响 TypeAlias 值表达式 |

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
| `compression.zstd` | 3.15+ | 无回退 |
| `concurrent` 解释器模块 | 3.14+ | 无回退 |
| `annotationlib` | 3.14+ | 无回退 |
| `frozendict` | 3.15+ | 无回退 |
| `dbm.sqlite3` | 3.15+ | 无回退 |
| `base64.z85` | 3.15+ | 无回退 |
| `sentinel` | 3.14+ | 无回退 |
| `profiling` 模块 | 3.15+ | 无回退 |
| `typing` 3.13+ / 3.15+ 功能 | 3.13+ | 需手动检查 `typing_extensions` 版本 |

## fix_py38_c.py — C/C++ 源码修复

### 修复内容

**策略：**
1. 部署 `pythoncapi_compat.h` 兼容头文件到项目中
2. 在使用 Python 3.9+ C API 的 C/C++ 文件中添加 `#include`
3. 修复直接使用 Python 3.9+ C API 而未通过兼容层的代码
4. 修复 `CMakeLists.txt` / `setup.py` 中的 Python 版本约束
5. 修复 `pythoncapi_compat.h` 中 Python 3.8 已有函数的静态/非静态声明冲突
6. 自动检测并更新不完整的 `pythoncapi_compat.h` 文件
7. 为 `pythoncapi_compat.h` 添加逐函数 `#ifndef` 保护，防止多个项目（如 numpy + scipy）各自包含副本时的重定义错误

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
| `PyObject_GetAIter()` | 3.10+ | `PyObject_CallMethod(o, "__aiter__", NULL)` 回退 |
| `Py_tp_*` 槽常量 | 3.9+ | `#ifndef` 保护的 `PyType_GetSlot` 兼容定义 |

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

### 逐函数保护

`pythoncapi_compat.h` 中的所有兼容函数（包括上游和我们的额外实现）都使用逐函数 `#ifndef` 保护包裹：

```c
#ifndef _PYCAPI_COMPAT_PyType_GetSlot
#define _PYCAPI_COMPAT_PyType_GetSlot
// ... 实现 ...
#endif /* _PYCAPI_COMPAT_PyType_GetSlot */
```

这可以防止多个项目（如 NumPy + SciPy + PyTorch）各自包含 `pythoncapi_compat.h` 副本时的重定义错误。`fix_py38_c.py` 脚本会自动为缺少这些保护的现有 `pythoncapi_compat.h` 添加保护。

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
