from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any

from trushell.core.plugin_api import TruPlugin


def _format_time(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def cmd_now(_: str) -> str:
    return _format_time(datetime.now())


def cmd_time(_: str) -> str:
    return cmd_now("")


def cmd_world(_: str) -> str:
    zones = {
        "UTC": ZoneInfo("UTC"),
        "New York": ZoneInfo("America/New_York"),
        "London": ZoneInfo("Europe/London"),
        "Tokyo": ZoneInfo("Asia/Tokyo"),
    }
    return "\n".join(f"{label}: {_format_time(datetime.now(tz))}" for label, tz in zones.items())


def cmd_tz(args: str) -> str:
    if not args.strip():
        return "Usage: tz <timezone>"
    try:
        zone = ZoneInfo(args.strip())
        return _format_time(datetime.now(zone))
    except Exception:
        return f"Unknown timezone: {args.strip()}"


def cmd_alarm(args: str) -> str:
    if not args.strip():
        return "No alarms configured. Use alarm <time> to set one."
    return f"Alarm command received: {args.strip()}"


def cmd_sw(args: str) -> str:
    command = args.strip() or "status"
    return f"Stopwatch command: {command}"


class ChronoTermPlugin(TruPlugin):
    name = "chronoterm"
    version = "0.1.0"
    description = "Time utilities for TruShell (now, world, tz, alarm, sw)."

    def _on_load(self, kernel: Any) -> None:
        # Register commands into kernel registry
        base = {
            "source": "plugin:chronoterm",
            "meta": {"plugin": "chronoterm"},
        }
        entries = [
            {"command": "now", "path": __file__, "function": "cmd_now", **base},
            {"command": "time", "path": __file__, "function": "cmd_time", **base},
            {"command": "world", "path": __file__, "function": "cmd_world", **base},
            {"command": "tz", "path": __file__, "function": "cmd_tz", **base},
            {"command": "alarm", "path": __file__, "function": "cmd_alarm", **base},
            {"command": "sw", "path": __file__, "function": "cmd_sw", **base},
        ]
        for entry in entries:
            # Use kernel's internal register to ensure consistent format
            try:
                kernel._register(entry, override=False)
            except Exception:
                # fall back to direct registry assignment
                kernel.registry[entry["command"]] = entry


__all__ = ["ChronoTermPlugin"]
