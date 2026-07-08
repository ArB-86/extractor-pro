from concurrent.futures import ThreadPoolExecutor


def parallel_map(fn, items, workers=8):
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, items))
