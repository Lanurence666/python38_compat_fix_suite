import json
import os
import locale

_TRANSLATIONS = {}
_DEFAULT_LANG = "en"
_CURRENT_LANG = None


def _detect_language():
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            code = lang.split("_")[0].lower()
            return code
    except Exception:
        pass
    try:
        lang = locale.getlocale()[0]
        if lang:
            code = lang.split("_")[0].lower()
            return code
    except Exception:
        pass
    for env_var in ("LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES"):
        val = os.environ.get(env_var, "")
        if val:
            code = val.split("_")[0].split(".")[0].lower()
            return code
    return _DEFAULT_LANG


def _load_translations(lang_dir=None):
    global _TRANSLATIONS, _CURRENT_LANG
    if lang_dir is None:
        lang_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang")
    if not os.path.isdir(lang_dir):
        _CURRENT_LANG = _DEFAULT_LANG
        return
    for fname in os.listdir(lang_dir):
        if fname.endswith(".json"):
            code = fname[:-5]
            fpath = os.path.join(lang_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    _TRANSLATIONS[code] = json.load(f)
            except Exception:
                pass
    detected = _detect_language()
    available = set(_TRANSLATIONS.keys())
    if detected in available:
        _CURRENT_LANG = detected
    else:
        _CURRENT_LANG = _DEFAULT_LANG


def t(key, **kwargs):
    if not _TRANSLATIONS:
        _load_translations()
    lang = _CURRENT_LANG or _DEFAULT_LANG
    text = None
    if lang in _TRANSLATIONS:
        text = _TRANSLATIONS[lang].get(key)
    if text is None and _DEFAULT_LANG in _TRANSLATIONS:
        text = _TRANSLATIONS[_DEFAULT_LANG].get(key)
    if text is None:
        text = key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def get_lang():
    if not _TRANSLATIONS:
        _load_translations()
    return _CURRENT_LANG or _DEFAULT_LANG
