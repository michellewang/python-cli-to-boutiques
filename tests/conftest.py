import argparse
import sys
import types
from pathlib import Path

import click
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def make_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--name", help="Your name")
    return p


@click.command()
@click.option("--name", help="Your name")
def test_cli(name):
    """A test click command."""


@pytest.fixture
def parser():
    return make_parser()


@pytest.fixture
def cli():
    return test_cli


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
