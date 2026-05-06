from rich_inquirer import (
    BasePrompt,
    Choice,
    ConfirmPrompt,
    FuzzyPrompt,
    PromptContext,
    SelectPrompt,
    TextPrompt,
)


def test_top_level_exports():
    assert BasePrompt is not None
    assert Choice is not None
    assert ConfirmPrompt is not None
    assert FuzzyPrompt is not None
    assert PromptContext is not None
    assert SelectPrompt is not None
    assert TextPrompt is not None
