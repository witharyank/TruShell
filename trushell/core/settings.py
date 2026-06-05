from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_SETTINGS: dict[str, Any] = {
    "theme": "dark",
    "prompt_symbol": "➜",
    "show_git_status": True,
    "auto_complete": True,
    "csv_max_rows": 50,
}


class SettingsManager:
    """Load and save TruShell configuration from ~/.trushell/config.json."""

    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or Path.home() / ".trushell" / "config.json"
        self.settings: dict[str, Any] = {}

    def _ensure_directory(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        self._ensure_directory()
        if not self.config_path.exists():
            self.settings = DEFAULT_SETTINGS.copy()
            self.save()
            return self.settings

        try:
            raw = self.config_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (json.JSONDecodeError, OSError):
            self.settings = DEFAULT_SETTINGS.copy()
            self.save()
            return self.settings

        self.settings = {**DEFAULT_SETTINGS, **data}
        return self.settings

    def save(self) -> None:
        self._ensure_directory()
        self.config_path.write_text(
            json.dumps(self.settings, indent=2, sort_keys=True), encoding="utf-8"
        )

    def get(self, key: str) -> Any:
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value


def launch_settings() -> None:
    try:
        from trushell.commands.settings import SettingsApp

        try:
            SettingsApp().run(inline=True)
        except TypeError:
            SettingsApp().run()
    except Exception as error:
        from rich.console import Console

        Console().print(f"[red]Unable to launch settings: {error}[/red]")
