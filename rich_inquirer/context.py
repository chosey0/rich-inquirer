from typing import Dict, Any, List, Tuple

from rich.console import Console

from .base import BasePrompt


class PromptContext:
    def __init__(self, console: Console = None):
        self.console = console or Console()
        self._flow: List[Tuple[str, BasePrompt]] = []
        self._results: Dict[str, Any] = {}

    def add(self, name: str, prompt: BasePrompt) -> "PromptContext":
        """Add a prompt step with a result name."""
        self._flow.append((name, prompt))
        return self

    def run(self) -> Dict[str, Any]:
        """Execute all prompts in order, stop on ESC (None)."""
        for name, prompt in self._flow:
            result = prompt.ask()
            if result is None:
                self.console.print(
                    f"[yellow][!] Prompt '{name}' was cancelled. Aborting flow.[/yellow]"
                )
                return self._results
            self._results[name] = result
        return self._results

    def get(self, name: str) -> Any:
        """Retrieve a result by name."""
        return self._results.get(name)

    def results(self) -> Dict[str, Any]:
        return self._results
