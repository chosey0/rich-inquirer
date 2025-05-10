from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Choice:
    """Represents an item in a SelectPrompt list.

    Args:
        value (Any): Internal value returned when selected.
        name (Optional[str]): Display name shown in prompt. Defaults to str(value).
        enabled (bool): Preselected (for multiselect). Not used in single select.
    """

    value: Any
    name: Optional[str] = None
    enabled: bool = False  # for future multiselect support

    def __post_init__(self):
        if self.name is None:
            self.name = str(self.value)

    def __str__(self) -> str:
        return self.name
