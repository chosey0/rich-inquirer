from rich.console import Console

from rich_inquirer.context import PromptContext


class StubPrompt:
    def __init__(self, result):
        self.result = result

    def ask(self):
        return self.result


def test_prompt_context_returns_partial_results_on_cancel():
    console = Console(record=True)
    context = PromptContext(console=console)
    context.add("name", StubPrompt("Ada"))
    context.add("confirm", StubPrompt(None))
    context.add("ignored", StubPrompt("value"))

    assert context.run() == {"name": "Ada"}
    assert context.get("ignored") is None
    assert "cancelled" in console.export_text()
