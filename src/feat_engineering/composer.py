from typing import Callable

import pandas as pd
import functools

ComposableFunction = Callable[[pd.DataFrame], pd.DataFrame]


def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)
