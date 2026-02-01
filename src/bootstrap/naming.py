# ABOUTME: Normalizes project names across different naming conventions (snake_case, PascalCase, kebab-case).
# ABOUTME: Provides derived name variants for polyglot package naming.

import re
from dataclasses import dataclass


@dataclass
class ProjectNames:
    """Holds all derived naming variants for a project."""

    original: str  # The original input as-is
    snake: str  # my_project (Python convention)
    pascal: str  # MyProject (Swift convention)
    kebab: str  # my-project (TypeScript convention)
    lower: str  # myproject (Go convention)


def _split_into_words(name: str) -> list[str]:
    """
    Split a name into lowercase words, handling various conventions.

    Handles:
    - snake_case: split on underscores
    - kebab-case: split on hyphens
    - PascalCase/camelCase: split on case transitions
    - Mixed: split on all separators
    """
    # First, replace hyphens and underscores with a common separator
    # Then handle camelCase/PascalCase transitions
    normalized = name.replace("-", "_")

    # Split camelCase/PascalCase: insert underscore before uppercase letters
    # that follow lowercase letters (myProject -> my_Project)
    # or before uppercase letters followed by lowercase (APIProject -> API_Project)
    normalized = re.sub(r"([a-z])([A-Z])", r"\1_\2", normalized)
    normalized = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", normalized)

    # Split on underscores and filter empty strings
    words = [w.lower() for w in normalized.split("_") if w]

    return words


def parse_project_name(name: str) -> ProjectNames:
    """
    Parse a project name in any format and return all naming variants.

    Handles:
    - snake_case: my_project
    - kebab-case: my-project
    - PascalCase: MyProject
    - camelCase: myProject
    - lowercase: myproject (treated as single word)

    Args:
        name: The project name in any supported format

    Returns:
        ProjectNames with all derived variants
    """
    words = _split_into_words(name)

    return ProjectNames(
        original=name,
        snake="_".join(words),
        pascal="".join(word.capitalize() for word in words),
        kebab="-".join(words),
        lower="".join(words),
    )
