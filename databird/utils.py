def render_dict(d: dict, context: dict):
    d2 = dict()
    for key, value in d.items():
        if isinstance(value, str):
            d2[key] = value.format(**context)
        elif isinstance(value, dict):
            d2[key] = render_dict(value, context)
        else:
            d2[key] = value
    return d2
