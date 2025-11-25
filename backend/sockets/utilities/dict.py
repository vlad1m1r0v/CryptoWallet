def exclude_none_factory(data):
    return {k: v for k, v in data if v is not None}