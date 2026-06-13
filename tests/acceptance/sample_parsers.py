"""Sample argparse parsers covering a range of features, for pipeline testing."""
import argparse


def simple():
    """Baseline: one positional, one option, one flag."""
    p = argparse.ArgumentParser(prog="simple")
    p.add_argument("input")
    p.add_argument("--name", default="x")
    p.add_argument("--verbose", action="store_true")
    return p


def rich():
    """Kitchen sink of common, well-behaved argparse features."""
    p = argparse.ArgumentParser(prog="rich")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--ratio", type=float, default=0.5)
    p.add_argument("--mode", choices=["a", "b", "c"], default="a")
    p.add_argument("--tags", nargs="+")
    p.add_argument("--maybe", nargs="?")
    p.add_argument("--flag", action="store_true")
    p.add_argument("--required-opt", required=True)
    return p


def count_action():
    """The -v / -vvv repeatable verbosity counter."""
    p = argparse.ArgumentParser(prog="counter")
    p.add_argument("input")
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p


def append_action():
    """Repeatable --include that accumulates into a list."""
    p = argparse.ArgumentParser(prog="appender")
    p.add_argument("input")
    p.add_argument("--include", action="append")
    return p


def mutually_exclusive():
    """A mutually exclusive group."""
    p = argparse.ArgumentParser(prog="mutex")
    p.add_argument("input")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--json", action="store_true")
    g.add_argument("--yaml", action="store_true")
    return p


def filetype_arg():
    """argparse.FileType arguments."""
    p = argparse.ArgumentParser(prog="filer")
    p.add_argument("infile", type=argparse.FileType("r"))
    p.add_argument("--out", type=argparse.FileType("w"))
    return p


def subcommands():
    """Subparsers / subcommands."""
    p = argparse.ArgumentParser(prog="multi")
    sub = p.add_subparsers(dest="command")
    a = sub.add_parser("run")
    a.add_argument("target")
    b = sub.add_parser("clean")
    b.add_argument("--force", action="store_true")
    return p


def no_prog():
    """No prog set: argparse falls back to sys.argv[0] (the runner script)."""
    p = argparse.ArgumentParser()  # deliberately no prog=
    p.add_argument("input")
    return p


def nargs_optional():
    """A single optional-value argument (nargs='?')."""
    p = argparse.ArgumentParser(prog="maybe_tool")
    p.add_argument("input")
    p.add_argument("--maybe", nargs="?")
    return p
