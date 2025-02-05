from __future__ import annotations

import importlib.metadata

import ppigrf as m


def test_version():
    assert importlib.metadata.version("ppigrf") == m.__version__
