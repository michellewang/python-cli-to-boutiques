import sys
import types

import pytest


@pytest.fixture(name="_make_fake_module")
def _make_fake_module_fixture():
    created = []

    def _make(name: str, attr_name: str, attr):
        mod = types.ModuleType(name)
        setattr(mod, attr_name, attr)
        sys.modules[name] = mod
        created.append(name)
        return mod

    yield _make

    for name in created:
        sys.modules.pop(name, None)
