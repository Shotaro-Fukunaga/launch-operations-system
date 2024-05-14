 # ruff: noqa

from functools import wraps
from typing import Any


def round_output(func):
    """デコレーター関数で、関数からの出力を再帰的に丸めます。

    Args:
        func: 丸める対象のデータを出力する関数。

    Returns:
        同じ型の丸められたデータ。
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)
        return round_recursive(result, 2)

    return wrapper


def round_recursive(data, ndigits):
    """データ構造内の浮動小数点数を再帰的に丸めます。

    Args:
        data: 丸めるデータ（辞書、リスト、浮動小数点数など）。
        ndigits: 丸める小数点の桁数。

    Returns:
        同じ構造を持つデータで、浮動小数点数が指定された桁数で丸められています。
    """
    if isinstance(data, dict):
        return {k: round_recursive(v, ndigits) for k, v in data.items()}
    elif isinstance(data, list):
        return [round_recursive(v, ndigits) for v in data]
    elif isinstance(data, float):
        return round(data, ndigits)
    return data
