from column.api.backend import cache


def get_store():
    return cache.LocalMemoryCache()
