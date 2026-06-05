from __future__ import annotations

from pathlib import Path
import sys

from trushell.core.plugin_manager import PluginManager
from trushell.core.trukernel import TruKernel


class DummyKernel:
    def list_commands(self):
        return []


def test_plugin_manager_plugins_property_and_list_plugins():
    class TestPlugin:
        name = "fake"
        version = "0.1.0"
        description = "Fake plugin"

    pm = PluginManager(DummyKernel())
    pm._plugins = {"fake": TestPlugin()}

    assert pm.plugins == pm._plugins
    plugins = pm.list_plugins()
    assert len(plugins) == 1
    assert plugins[0]["name"] == "fake"
    assert plugins[0]["version"] == "0.1.0"
    assert plugins[0]["active"] is True
