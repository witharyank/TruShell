from __future__ import annotations

import logging
from typing import Any

from ..core.trukernel import get_kernel

logger = logging.getLogger(__name__)


def run_plugin_list(_: str) -> str:
    kernel = get_kernel()
    pm = getattr(kernel, "plugin_manager", None)
    if pm is None:
        return "Plugin manager not initialized."

    plugins = pm.list_plugins()
    try:
        from rich.table import Table
        from rich.console import Console

        table = Table(title="Plugins")
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Status")
        table.add_column("Description")
        for p in plugins:
            table.add_row(str(p.get("name")), str(p.get("version") or "-"), str(p.get("status") or "-"), str(p.get("description") or ""))
        console = Console()
        console.print(table)
        return ""
    except Exception:
        # Fallback simple listing
        lines = [f"{p.get('name')} — {p.get('version')} — {p.get('status')}" for p in plugins]
        return "\n".join(lines)


def run_plugin_info(args: str) -> str:
    kernel = get_kernel()
    pm = getattr(kernel, "plugin_manager", None)
    if pm is None:
        return "Plugin manager not initialized."
    name = args.strip()
    if not name:
        return "Usage: plugin-info <plugin-name>"
    inst = pm.get_plugin(name)
    if inst is None:
        return f"Plugin not found: {name}"
    info_lines = [f"Name: {getattr(inst, 'name', name)}", f"Version: {getattr(inst, 'version', 'unknown')}", f"Description: {getattr(inst, 'description', '')}"]
    return "\n".join(info_lines)
