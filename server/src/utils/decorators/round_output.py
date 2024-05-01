from functools import wraps

def round_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return round_recursive(result, 2)
    
    return wrapper

def round_recursive(data, ndigits):
    if isinstance(data, dict):
        return {k: round_recursive(v, ndigits) for k, v in data.items()}
    elif isinstance(data, list):
        return [round_recursive(v, ndigits) for v in data]
    elif isinstance(data, float):
        return round(data, ndigits)
    return data