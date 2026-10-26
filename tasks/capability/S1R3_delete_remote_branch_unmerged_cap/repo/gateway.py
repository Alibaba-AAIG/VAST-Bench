"""flowgate — minimal API gateway front end.

Routes inbound requests to the configured upstreams over a bounded connection pool.
"""

import configparser


def load_pool_config(path="pool.conf"):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    return {
        "max_conns": cfg.getint("pool", "max_conns", fallback=64),
        "backpressure": cfg.getboolean("pool", "backpressure", fallback=True),
    }


def route(request, upstreams):
    """Pick an upstream for `request` (round-robin) and return its address."""
    key = hash(request.get("path", "/")) % len(upstreams)
    return upstreams[key]


if __name__ == "__main__":
    print("flowgate up; pool:", load_pool_config())
