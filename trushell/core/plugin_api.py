from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from .trukernel import TruKernel


logger = logging.getLogger(__name__)


class TruPlugin(ABC):
    """Base class for TruShell plugins.

    Developers should inherit this class and implement lifecycle hooks.
    All public hooks are wrapped to prevent plugin exceptions from
    propagating into the kernel.
    """

    name: str = "unnamed"
    version: str = "0.0.0"
    description: str = ""

    def __init__(self) -> None:
        # internal state
        self._active = False

    def safe_call(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # catch-all to protect the kernel
            logger.exception("Plugin '%s' raised in %s: %s", self.name, fn.__name__, exc)
            return None

    def on_load(self, kernel: 'TruKernel') -> None:  # pragma: no cover - simple wrapper
        return self.safe_call(self._on_load, kernel)

    def on_unload(self) -> None:  # pragma: no cover - simple wrapper
        self._active = False
        return self.safe_call(self._on_unload)

    def pre_exec(self, command: str, args: str) -> Optional[Tuple[str, str]]:
        return self.safe_call(self._pre_exec, command, args)

    def post_exec(self, command: str, output: str) -> None:
        return self.safe_call(self._post_exec, command, output)

    # --- Methods plugin authors override ---
    def _on_load(self, kernel: 'TruKernel') -> None:
        """Called when the plugin is loaded. Override to register commands."""
        self._active = True

    def _on_unload(self) -> None:
        """Called when the plugin is unloaded. Override to cleanup resources."""
        self._active = False

    def _pre_exec(self, command: str, args: str) -> Optional[Tuple[str, str]]:
        """Intercept a command before execution. Return modified (command,args) or None."""
        return None

    def _post_exec(self, command: str, output: str) -> None:
        """Called after command execution. Override to inspect/transform output."""
        return None


__all__ = ["TruPlugin"]
