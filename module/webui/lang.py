from typing import Dict

from module.config.utils import *
from module.webui.config import WebuiConfig

LANG = 'zh-CN'
TRANSLATE_MODE = False


def set_language(s: str, refresh=False):
    global LANG
    for i, lang in enumerate(LANGUAGES):
        # pywebio.session.info.user_language return `zh-CN` or `zh-cn`, depends on browser
        if lang.lower() == s.lower():
            LANG = LANGUAGES[i]
            break
    else:
        LANG = 'en-US'

    WebuiConfig().Language = LANG

    if refresh:
        from pywebio.session import run_js
        run_js('location.reload();')


def t(s):
    """
    Get translation.
    """
    if TRANSLATE_MODE:
        return s
    # print(_t(s, LANG))
    return _t(s, LANG)


def _t(s, lang=None):
    """
    Get translation, ignore TRANSLATE_MODE
    """
    if not lang:
        lang = LANG
    try:
        return dic_lang[lang][s]
    except KeyError:
        print(f"Language key ({s}) not found")
        return s


dic_lang: Dict[str, Dict[str, str]] = {}


def reload():
    for lang in LANGUAGES:
        if lang not in dic_lang:
            dic_lang[lang] = {}
        for path, v in deep_iter(read_file(filepath_i18n(lang)), depth=3):
            dic_lang[lang]['.'.join(path)] = v

    for key in dic_lang["ja-JP"].keys():
        if dic_lang["ja-JP"][key] == key:
            dic_lang["ja-JP"][key] = dic_lang["en-US"][key]