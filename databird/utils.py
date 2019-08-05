import hashlib
from databird import dtutil


def hash_dict(d: dict):
    m = hashlib.sha1()
    for k in sorted(d):
        v = d[k]
        if not isinstance(k, str) or not isinstance(v, str):
            raise NotImplementedError("hash for other than dict(str->str)")
        m.update(v.encode())
    return m.hexdigest()


def get_context(time):
    context = {
        "time": time,
        "month_last_date": dtutil.month_last_day(time),
        "month_first_date": dtutil.month_first_day(time),
        "iso_date": dtutil.iso_date(time),
    }
    return context


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
