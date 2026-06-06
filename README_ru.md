# Набор инструментов для совместимости с Python 3.8

**Русский** | [中文](README_zh.md) | [English](README.md)

Набор автоматизированных скриптов для обратного портирования Python-проектов с 3.9+ на Python 3.8, охватывающий как исходный код Python, так и модули расширений C/C++.

## Что делает этот набор?

Когда у вас есть Python-проект, требующий Python 3.9+, но вам нужно запустить его на Python 3.8, вы сталкиваетесь с двумя категориями несовместимостей:

1. **Изменения синтаксиса Python и стандартной библиотеки** (PEP 585, 604, 584, 616 и т.д.)
2. **Изменения Python C API** (новые функции, изменённые сигнатуры, удалённые макросы и т.д.)

Этот набор предоставляет два скрипта, которые автоматически обнаруживают и исправляют эти проблемы:

- **`fix_py38_python.py`** — исправляет исходный код Python (файлы `.py`)
- **`fix_py38_c.py`** — исправляет исходный код расширений C/C++ (файлы `.c`, `.h`, `.cpp`)

Оба скрипта поддерживают **интернационализацию**: сообщения выводятся на языке вашей системы (английский, китайский или русский). Вы можете добавить новые языки, создав JSON-файлы в каталоге `lang/`.

## Наши результаты

Мы успешно использовали этот набор для обратного портирования крупных библиотек научных вычислений и ИИ на Python 3.8:

| Проект | Версия | Статус | Репозиторий |
|---------|---------|--------|------------|
| **NumPy** | 2.x (последний main) | Скомпилирован и протестирован на Python 3.8 | [numpy_backport_py38](https://github.com/Lanurence666/numpy_backport_py38) |
| **SciPy** | 1.x (последний main) | Скомпилирован и протестирован на Python 3.8 | [scipy_backport_py38](https://github.com/Lanurence666/scipy_backport_py38) |
| **PyTorch** | 2.13.0a0 (последний main) | Скомпилирован и протестирован на Python 3.8 | [pytorch_backport_py38](https://github.com/Lanurence666/pytorch_backport_py38) |
| **Transformers** | 5.8.0.dev0 (последний main) | Скомпилирован и протестирован на Python 3.8 | — |
| **HuggingFace Hub** | 1.17.0.dev0 (последний main) | Скомпилирован и протестирован на Python 3.8 | — |
| **PEFT** | 0.19.2.dev0 (последний main) | Скомпилирован и протестирован на Python 3.8 | [peft_backport_py38](https://github.com/Lanurence666/peft_backport_py38) |
| **ModelScope** | 2.0.0+main (последний main) | Скомпилирован и протестирован на Python 3.8 | — |

Все проекты были скомпилированы с максимальными флагами оптимизации и выпущены как устанавливаемые wheel-пакеты. PyTorch был установлен в режиме редактирования (разработки) для тестирования.

### Результаты тестирования Transformers + HuggingFace Hub (Python 3.8)

Последние версии **Transformers 5.8.0.dev0** и **HuggingFace Hub 1.17.0.dev0** были проверены комплексным тестированием на Python 3.8.10 + PyTorch 2.13:

**✅ Проверенная функциональность:**
- Основные импорты: `AutoConfig`, `AutoTokenizer`, `AutoModel`, `AutoModelForCausalLM`, `AutoModelForSequenceClassification`
- Конкретные модели: `BertModel`, `BertTokenizer`, `GPT2Model`, `GPT2Tokenizer`, `T5Model`, `T5Config`, `LlamaConfig`
- Прямой проход моделей: BertModel, GPT2Model (со случайными тензорами)
- Операции Config: `to_dict()`, `to_json_string()`, `from_dict()`, `for_model()`
- Инфраструктура обучения: `Trainer`, `TrainingArguments`, `pipeline`
- Процессоры: `ProcessorMixin`, `FeatureExtractionMixin`, `ImageProcessingMixin`
- HuggingFace Hub API: `HfApi`, `hf_hub_download`, `snapshot_download`

**🔧 Дополнительные ручные исправления (помимо автоматического скрипта):**
- Конвертация `match/case` → `if/elif` (в huggingface_hub)
- Конвертация `isinstance(x, A|B)` → `isinstance(x, (A, B))`
- `from typing import Annotated` → `from typing_extensions import Annotated` (22 файла)
- Условный импорт `torch.distributed` (для сборок PyTorch без поддержки распределённых вычислений)
- Резервная реализация `functools.cached_property` для Python 3.8
- Защита `get_type_hints()` через try/except (аннотации PEP 585/604)
- Условная обработка `dataclass(kw_only=True)`
- Использование PEP 585 псевдонимов типов на уровне модуля в базовых классах (например, `OrderedDict[str, str | None]`)

### Результаты тестирования PEFT (Python 3.8)

Последняя версия **PEFT 0.19.2.dev0** была проверена комплексным тестированием на Python 3.8.10 + PyTorch 2.13:

**✅ Проверенная функциональность:**
- Основной импорт: `import peft`
- Все классы конфигурации: `LoraConfig`, `AdaLoraConfig`, `IA3Config`, `LoHaConfig`, `LoKrConfig`, `OFTConfig`, `BOFTConfig`, `VeraConfig`, `VBLoRAConfig`, `FourierFTConfig`, `HRAConfig`, `C3AConfig`, `RandLoraConfig`, `RoadConfig`, `ShiraConfig`, `MissConfig`, `BdLoraConfig`, `CartridgeConfig`, `WaveFTConfig` и др.
- LoRA: применение, прямой проход, несколько целевых модулей
- Сохранение и загрузка адаптера
- Управление несколькими адаптерами: добавление/переключение
- IA3, AdaLora
- Слияние/разъединение адаптера
- Контекстный менеджер отключения адаптера
- Сериализация конфигурации
- Подсчёт обучаемых параметров

**🔧 Дополнительные ручные исправления (помимо автоматического скрипта):**
- `tuple[...]`/`dict[...]` в присваиваниях TypeAlias (например, `WaveletCoeff2d: TypeAlias = tuple[...]`) — `from __future__ import annotations` НЕ влияет на выражения значений TypeAlias
- `Literal["zero"] | None` в полях dataclass — `from __future__ import annotations` НЕ предотвращает вычисление типов полей dataclass во время выполнения
- Импорт `itertools.pairwise()` (Python 3.10+) — теперь автоматически исправляется скриптом
- Проверка доступности `torch.distributed.tensor` для пользовательских сборок PyTorch

### Результаты тестирования ModelScope (Python 3.8)

Последняя версия **ModelScope 2.0.0+main** была проверена на Python 3.8.10 + PyTorch 2.13:

**✅ Проверенная функциональность:**
- Основной импорт: `import modelscope` (v2.0.0+main)
- Совместимость `importlib.metadata`: `import_utils`, `plugins`
- Совместимость `zoneinfo`: `hub/utils/utils` (преобразование временных меток)
- Аудиомодели: `zipformer.Zipformer2EncoderLayer`
- Потоковый вывод: `streaming_output.StreamingOutputMixin`
- Загрузка данных: `data_loader.OssDownloader`
- Полная компиляция: 2859 файлов `.py` скомпилировано с 0 ошибками

**🔧 Дополнительные ручные исправления (помимо автоматического скрипта):**
- Импорт верхнего уровня `import importlib.metadata` + прямые ссылки `importlib.metadata.xxx` → требуется замена на псевдоним `importlib_metadata`
- `import zoneinfo` внутри функций → требуется `try/except` с `backports.zoneinfo` (теперь автоматически исправляется в v2)
- `from X import \` (продолжение через обратную косую черту) → вызывает синтаксические ошибки при модификации импортов другими исправлениями (теперь автоматически исправляется в v2)
- `from X import *` + `from X import (конкретные)` → синтаксический конфликт после слияния импортов (теперь автоматически исправляется в v2)
- Формат `license = "XXX"` в `pyproject.toml` → несовместим со старыми версиями setuptools (теперь автоматически исправляется в v2)
- `license-files = [...]` в `pyproject.toml` → не поддерживается старыми версиями setuptools (теперь автоматически исправляется в v2)
- Пропущенный оператор `x**2(y)` → `x**2*(y)` (теперь автоматически исправляется в v2)
- Недопустимая escape-последовательность `'\?'` → `'\\?'` (теперь автоматически исправляется в v2)

## fix_py38_python.py — Исправления исходного кода Python

### Что исправляется

| № | Функция | PEP/Версия | Стратегия исправления |
|---|---------|-------------|--------------|
| 1 | Встроенные дженерики (`list[X]`, `dict[K,V]` и т.д.) | PEP 585 / 3.9+ | Замена на `typing.List[X]`, `typing.Dict[K,V]` и т.д. |
| 2 | Типы объединений (`X \| Y` в аннотациях) | PEP 604 / 3.10+ | Замена на `Union[X, Y]` |
| 3 | Операторы слияния словарей (`d1 \| d2`, `d1 \|= d2`) | PEP 584 / 3.9+ | Замена на `{**d1, **d2}` и `d1.update(d2)` |
| 4 | `str.removeprefix()` / `str.removesuffix()` | PEP 616 / 3.9+ | Резервная реализация через `str.startswith()`/`str.endswith()` |
| 5 | `typing.Annotated` | PEP 593 / 3.9+ | `try/except` с откатом на `typing_extensions` |
| 6 | `functools.cache` | 3.9+ | Замена на `functools.lru_cache(maxsize=None)` |
| 7 | `importlib.metadata` | 3.9+ | `try/except` с откатом на `importlib_metadata` |
| 8 | `typing.TypeAlias` / `TypeGuard` / `ParamSpec` / `Concatenate` | 3.9+ | `try/except` с откатом на `typing_extensions` |
| 9 | `isinstance(x, A \| B)` / `issubclass(x, A \| B)` | 3.10+ | Замена на `isinstance(x, (A, B))` |
| 10 | `zoneinfo` | 3.9+ | `try/except` с откатом на `backports.zoneinfo` |
| 11 | `graphlib` | 3.9+ | `try/except` с откатом |
| 12 | `math.lcm()` | 3.9+ | `try/except` с резервной реализацией |
| 13 | `math.nextafter()` / `math.ulp()` | 3.9+ | `try/except` с резервной реализацией |
| 14 | `collections.XXX` → `collections.abc.XXX` | Устарело в 3.9+ | Замена устаревших импортов |
| 15 | `random.randbytes()` | 3.9+ | `try/except` с резервной реализацией |
| 16 | `ast.unparse()` | 3.9+ | `try/except` с откатом на `astunparse` |
| 17 | `bytes/bytearray.removeprefix/removesuffix` | 3.9+ | Monkey-patch при выполнении |
| 18 | Скобочные контекстные менеджеры | 3.10+ | Убрать скобки |
| 19 | Ограничения версии Python в `setup.py` / `pyproject.toml` | — | Обновление требований к версии |
| 20 | `zip(..., strict=True)` | 3.10+ | Резервная реализация `_zip_strict()` |
| 21 | `int.bit_count()` | 3.10+ | Резервная реализация `_int_bit_count()` |
| 22 | `aiter()` / `anext()` | 3.10+ | Резервные реализации `_aiter_compat()` / `_anext_compat()` |
| 23 | Параметр `key=` модуля `bisect` | 3.10+ | Резервная реализация |
| 24 | `dataclass(slots=True)` | 3.10+ | Удалить параметр `slots` |
| 25 | Индексация `collections.abc.Callable[...]` | 3.9+ | Замена на `typing.Callable[...]` |
| 26 | `functools.lru_cached_property` | 3.9+ | `try/except` с полным резервным классом |
| 27 | `functools.cached_property` | 3.8+ | Автодобавление отсутствующего импорта |
| 28 | `types.GenericAlias` / `EllipsisType` / `NotImplementedType` | 3.9+ | Monkey-patch в `__init__.py` |
| 29 | Дублирующиеся импорты | — | Слияние операторов `from X import` |
| 30 | Типизация PEP 585 в `array_api_compat` | 3.9+ | Замена встроенных дженериков в аннотациях типов |
| 31 | `AttributeError(msg, name=..., obj=...)` именованные аргументы | 3.10+ | Удалить `name=None`/`obj=None` или использовать вспомогательную функцию `_AttributeError_compat()` |
| 32 | Объединение псевдонимов типов (`X: TypeAlias = A | B`) | 3.10+ | Замена на `X: TypeAlias = Union[A, B]` с автоимпортом `Union` |
| 33 | `dataclass(kw_only=True)` | 3.10+ | Удалить параметр `kw_only` |
| 34 | `inspect.get_annotations()` | 3.10+ | `try/except` с откатом на ручное извлечение аннотаций |
| 35 | `TypeAliasType` (PEP 695 `type X = Y`) | 3.12+ | Преобразование в присваивание `typing.TypeAlias` |
| 36 | Объединение типов времени выполнения (`X | Y` вне аннотаций) | 3.10+ | Преобразование в `Union[X, Y]` в позициях вычисления времени выполнения |
| 37 | Объединение PEP 604 вне аннотаций (тело класса, значения по умолчанию) | 3.10+ | Преобразование в `Union[X, Y]` с учётом `from __future__ import annotations` |
| 38 | Параметризованный класс PEP 695 (`class X[T]:`) | PEP 695 / 3.12+ | Преобразование в базовый класс `Generic[T]` с `TypeVar` |
| 39 | Параметризованная функция PEP 695 (`def f[T]():`) | PEP 695 / 3.12+ | Преобразование в `TypeVar`, при необходимости `@overload` |
| 40 | Оператор типа PEP 695 (`type X = Y`) | PEP 695 / 3.12+ | Преобразование в `X: TypeAlias = Y` |
| 41 | Лямбда-декоратор (`@lambda x: x`) | 3.9+ синтаксис | Обёртка в обычную функцию |
| 42 | Оператор `match`/`case` | PEP 634 / 3.10+ | Пометка комментарием TODO (требуется ручная переработка в `if/elif`) |
| 43 | Функции `typing` 3.11+ (`NotRequired`, `TypeVarTuple` и т.д.) | 3.11+ | `try/except` с откатом на `typing_extensions` |
| 44 | `enum.StrEnum` | 3.11+ | `try/except` с ручной реализацией |
| 45 | `contextlib.chdir()` | 3.11+ | `try/except` с резервной реализацией |
| 46 | `operator.call()` | 3.11+ | `try/except` с резервной реализацией |
| 47 | `hashlib.file_digest()` | 3.11+ | `try/except` с резервной реализацией |
| 48 | Индексация `collections.abc.Iterator[...]` | 3.9+ | Замена на `typing.Iterator[...]` |
| 49 | Слияние флагов регулярных выражений (`re.X | re.I` и т.д.) | 3.11+ | Преобразование в `re.compile()` с объединёнными флагами |
| 50 | Исправление позиции `from __future__ import annotations` | — | Перемещение в начало файла |
| 51 | Повреждённые комментарии `# noqa` после перезаписи импортов | — | Очистка устаревших директив `# noqa` |
| 52 | Комбинированный псевдоним типа PEP 585 + 604 (`X = dict[str, int | str]`) | 3.9+ | Рекурсивное преобразование: `dict` → `Dict`, `|` → `Union`, с обработкой вложенных скобок |
| 53 | Улучшенное определение переменных для слияния словарей (`self.kwargs | other`) | 3.9+ | Обнаружение составных имён переменных и переменных стиля `kwargs` |
| 54 | `ExceptionGroup` / `BaseExceptionGroup` | 3.11+ | `try/except` с откатом на `exceptiongroup` |
| 55 | `itertools.pairwise()` | 3.10+ | `try/except` с резервной реализацией `_itertools_pairwise_compat()` |
| 56 | Объединение в полях dataclass (`X \| None`) | 3.10+ | Преобразование в `Optional[X]` / `Union[X, Y]` — `from __future__ import annotations` НЕ предотвращает вычисление типов полей dataclass во время выполнения |
| 57 | PEP 585 в TypeAlias без `from __future__ import annotations` | 3.9+ | Прямая замена: `tuple[...]` → `Tuple[...]`, `dict[...]` → `Dict[...]` — `from __future__ import annotations` НЕ влияет на выражения значений TypeAlias |

### Функции Python 3.10–3.15 (обнаруживаются, но НЕ исправляются автоматически)

Скрипт обнаруживает следующие функции, но **не** исправляет их автоматически, так как они требуют ручного вмешательства:

| Функция | Версия | Причина |
|---------|---------|--------|
| `typing.NotRequired` | 3.11+ | Требуется `typing_extensions` с проверкой версии |
| `collections.abc.Buffer` | 3.12+ | Нет простого отката |
| `BaseException.add_note()` | 3.11+ | Откат невозможен |
| `tomllib` | 3.11+ | Используйте `tomli` как откат (вручную) |
| `asyncio.TaskGroup` | 3.11+ | Структурное изменение, нет простого отката |
| `math.exp2()` / `math.cbrt()` | 3.11+ | Требуется ручной откат |
| `datetime.UTC` | 3.11+ | Требуется ручной откат |
| `itertools.batched()` | 3.12+ | Требуется ручной откат |
| `pathlib.Path.walk()` | 3.12+ | Требуется ручной откат |
| `distutils` (удалён в 3.12) | 3.12 | Используйте `setuptools` как замену |
| `warnings.deprecated()` | 3.13+ | Нет простого отката |
| `copy.replace()` | 3.13+ | Нет простого отката |
| Удалённые модули PEP 594 | 3.13 | Требуется ручная миграция |
| `compression.zstd` | 3.15+ | Нет отката |
| `concurrent` модуль интерпретаторов | 3.14+ | Нет отката |
| `annotationlib` | 3.14+ | Нет отката |
| `frozendict` | 3.15+ | Нет отката |
| `dbm.sqlite3` | 3.15+ | Нет отката |
| `base64.z85` | 3.15+ | Нет отката |
| `sentinel` | 3.14+ | Нет отката |
| `profiling` модуль | 3.15+ | Нет отката |
| Функции `typing` 3.13+ / 3.15+ | 3.13+ | Требуется ручная проверка версии `typing_extensions` |

## fix_py38_c.py — Исправления исходного кода C/C++

### Что исправляется

**Стратегия:**
1. Развёртывание заголовка совместимости `pythoncapi_compat.h` в проект
2. Добавление `#include "pythoncapi_compat.h"` в файлы, использующие Python 3.9+ C API
3. Исправление прямого использования Python 3.9+ C API без прохождения через уровень совместимости
4. Исправление ограничений версии Python в `CMakeLists.txt` / `setup.py`
5. Исправление конфликтов статического/нестатического объявления в `pythoncapi_compat.h` для функций, уже присутствующих в системных заголовках Python 3.8
6. Автообнаружение и обновление неполных файлов `pythoncapi_compat.h`
7. Добавление пофункциональных `#ifndef` защит в `pythoncapi_compat.h` для предотвращения ошибок переопределения, когда несколько проектов (например, numpy + scipy) включают свои собственные копии

### Изменения Python 3.9+ C API

| API | Версия | Стратегия совместимости |
|-----|---------|-----------------|
| `PyObject_CallNoArgs()` | 3.9+ | Inline-обёртка через `pythoncapi_compat.h` |
| `PyObject_CallOneArg()` | 3.9+ | Inline-обёртка |
| `Py_IS_TYPE()` | 3.9+ | Макрос-обёртка |
| `Py_SET_TYPE()` / `Py_SET_SIZE()` / `Py_SET_REFCNT()` | 3.9+ | Макросы-обёртки |
| `PyModule_AddType()` | 3.9+ | Inline-обёртка |
| `PyModule_AddObjectRef()` | 3.10+ | Inline-обёртка |
| `PyObject_Vectorcall()` | 3.9+ | Inline-обёртка |
| `PyType_GetModule()` | 3.9+ | Реализация совместимости через поиск `__module__` |
| `PyType_GetModuleByDef()` | 3.9+ | Заглушка (требует ручной проверки) |
| `PyType_GetSlot()` | 3.9+ | Полная совместимость через обход цепочки `tp_base` |
| `Py_NewRef()` / `Py_XNewRef()` | 3.10+ | Inline-обёртки |
| `Py_Is()` / `Py_IsNone()` / `Py_IsTrue()` / `Py_IsFalse()` | 3.10+ | Макросы-обёртки |
| `PyFrame_GetCode()` / `PyFrame_GetBack()` | 3.9+ | Inline-обёртки |
| `PyErr_GetRaisedException()` / `PyErr_SetRaisedException()` | 3.12+ | Inline-обёртки |
| `PyObject_VectorcallDict()` / `PyObject_VectorcallMethod()` | 3.12+ | Откат через `PyObject_Call` |
| `PyDict_GetItemRef()` / `PyDict_GetItemStringRef()` | 3.13+ | Откат через `PyDict_GetItemWithError` |
| `PyList_GetItemRef()` | 3.13+ | Откат через `PyList_GetItem` + `Py_XINCREF` |
| `PyLong_AsInt()` | 3.13+ | Откат через `PyLong_AsLong` + проверка диапазона |
| `Py_MOD_GIL_NOT_USED` / `PyUnstable_Module_SetGIL()` | 3.13+ | Защита `#ifdef Py_GIL_DISABLED` или проверкой версии |
| `PyObject_GetAIter()` | 3.10+ | Откат через `PyObject_CallMethod(o, "__aiter__", NULL)` |
| Константы слотов `Py_tp_*` | 3.9+ | Определения с защитой `#ifndef` для совместимости `PyType_GetSlot` |

### Конфликты системных заголовков Python 3.8

Следующие функции уже присутствуют в системных заголовках Python 3.8. Скрипт автоматически корректирует проверки версий в `pythoncapi_compat.h`, чтобы избежать конфликтов статического/нестатического объявления:

- `PyType_GetSlot` — присутствует в `object.h` начиная с Python 3.8
- `PyModule_AddFunctions` — присутствует в `modsupport.h` начиная с Python 3.8
- `PyInterpreterState_GetDict` — присутствует в `pystate.h` начиная с Python 3.8
- `PyErr_GetExcInfo` / `PyErr_SetExcInfo` — присутствуют в `pyerrors.h` начиная с Python 3.8

### Исправления совместимости компилятора GCC

- `#pragma warning(disable:...)` → обёрнуть в `#ifdef _MSC_VER`
- `__declspec(deprecated)` → добавить альтернативу GCC `__attribute__((deprecated))`
- `_aligned_malloc` → обёрнуть в `#ifdef _MSC_VER`
- `PY_SSIZE_T_CLEAN` → обеспечить определение перед `#include <Python.h>`

## pythoncapi_compat.h

Файл `pythoncapi_compat.h`, входящий в этот набор, взят из проекта [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat) и лицензирован по лицензии **Zero Clause BSD (0BSD)**.

Мы добавили дополнительные реализации совместимости (секция `EXTRA_COMPAT`) для API, не охваченных апстрим-заголовком, включая API Python 3.12–3.15.

### Пофункциональные защиты

Все функции совместимости в `pythoncapi_compat.h` (как апстрим, так и наши дополнительные реализации) обёрнуты пофункциональными защитами `#ifndef`:

```c
#ifndef _PYCAPI_COMPAT_PyType_GetSlot
#define _PYCAPI_COMPAT_PyType_GetSlot
// ... реализация ...
#endif /* _PYCAPI_COMPAT_PyType_GetSlot */
```

Это предотвращает ошибки переопределения, когда несколько проектов (например, NumPy + SciPy + PyTorch) включают свои собственные копии `pythoncapi_compat.h`. Скрипт `fix_py38_c.py` автоматически добавляет эти защиты к существующим `pythoncapi_compat.h`, у которых они отсутствуют.

## Интернационализация (i18n)

Скрипты поддерживают несколько языков для консольного вывода. Языковые файлы хранятся в формате JSON в каталоге `lang/`:

```
lang/
├── en.json    # Английский (по умолчанию)
├── zh.json    # Китайский (中文)
└── ru.json    # Русский
```

**Как это работает:**
- Скрипт автоматически определяет язык вашей системы через `locale.getdefaultlocale()`
- Если для вашего языка есть файл перевода, он будет использован
- Если файл перевода не найден, используется английский по умолчанию
- Вы можете добавить новые языки, создав файл `lang/<код>.json` с теми же ключами, что и в `en.json`

**Чтобы добавить новый язык:**
1. Скопируйте `lang/en.json` в `lang/<код_вашего_языка>.json`
2. Переведите значения (не ключи) на ваш язык
3. Поместите файл в каталог `lang/` — он будет обнаружен автоматически

## Использование

### Предварительные требования

- Python 3.8+
- Модуль `i18n.py` и каталог `lang/` должны находиться в том же каталоге, что и скрипты

### Исправление исходного кода Python

```bash
# Исправить текущий каталог
python fix_py38_python.py

# Исправить указанный каталог проекта
python fix_py38_python.py /путь/к/проекту
```

### Исправление исходного кода C/C++

```bash
# Исправить текущий каталог
python fix_py38_c.py

# Исправить указанный каталог проекта
python fix_py38_c.py /путь/к/проекту
```

### Рекомендуемый порядок работы

1. **Сделайте резервную копию кода** (git commit или копия)
2. Сначала запустите `fix_py38_python.py` для исправления синтаксиса Python
3. Запустите `fix_py38_c.py` для исправления расширений C/C++
4. **Вручную проверьте** все изменения
5. Скомпилируйте и протестируйте
6. Вручную исправьте оставшиеся проблемы

## ⚠️ Важные предупреждения

1. **Эти скрипты изменяют исходные файлы на месте.** Всегда делайте резервную копию или используйте систему контроля версий перед запуском.
2. **Требуется ручная проверка.** Автоматические исправления не могут корректно обработать все случаи, особенно:
   - Сложные аннотации типов с вложенными дженериками
   - `PyCMethod` / `METH_METHOD` (Python 3.9+) — заменяются маркерами комментариев
   - `PyType_GetModuleByDef` — заглушка, может не работать при выполнении
   - Операторы слияния словарей в контекстах, отличных от dict (массивы numpy, множества и т.д.)
3. **Не все функции Python 3.9+ могут быть автоматически исправлены.** См. списки только для обнаружения выше.
4. **Тщательно тестируйте после запуска.** Скомпилируйте все расширения C и запустите набор тестов проекта.
5. **`pythoncapi_compat.h` из [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat)** по лицензии Zero Clause BSD. Мы добавили дополнительные реализации совместимости поверх него.

## Структура файлов

```
python38_compat_fix_suite/
├── fix_py38_python.py       # Скрипт исправления исходного кода Python
├── fix_py38_c.py            # Скрипт исправления исходного кода C/C++
├── pythoncapi_compat.h      # Заголовок совместимости C API (апстрим + дополнения)
├── i18n.py                  # Модуль интернационализации
├── lang/
│   ├── en.json              # Английские переводы
│   ├── zh.json              # Китайские переводы
│   └── ru.json              # Русские переводы
├── README.md                # Этот файл (английский)
├── README_ru.md             # Русская документация
└── README_zh.md             # Китайская документация
```

## Лицензия

- **Скрипты** (`fix_py38_python.py`, `fix_py38_c.py`, `i18n.py`): Лицензия MIT
- **`pythoncapi_compat.h`**: Zero Clause BSD (0BSD) — из [python/pythoncapi-compat](https://github.com/python/pythoncapi-compat)
