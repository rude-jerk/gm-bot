from contextlib import contextmanager


@contextmanager
def closing(this):
    try:
        yield this
    finally:
        if this:
            this.close()
