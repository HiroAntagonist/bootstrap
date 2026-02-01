# ABOUTME: Tests for the project name normalization utility.
# ABOUTME: Covers snake_case, PascalCase, kebab-case, camelCase, and single-word inputs.

import pytest
from bootstrap.naming import parse_project_name, ProjectNames


class TestParseProjectName:
    """Test parse_project_name with various input formats."""

    def test_snake_case_input(self):
        """snake_case input like my_project"""
        result = parse_project_name("my_project")
        assert result == ProjectNames(
            original="my_project",
            snake="my_project",
            pascal="MyProject",
            kebab="my-project",
            lower="myproject",
        )

    def test_kebab_case_input(self):
        """kebab-case input like my-project"""
        result = parse_project_name("my-project")
        assert result == ProjectNames(
            original="my-project",
            snake="my_project",
            pascal="MyProject",
            kebab="my-project",
            lower="myproject",
        )

    def test_pascal_case_input(self):
        """PascalCase input like MyProject"""
        result = parse_project_name("MyProject")
        assert result == ProjectNames(
            original="MyProject",
            snake="my_project",
            pascal="MyProject",
            kebab="my-project",
            lower="myproject",
        )

    def test_camel_case_input(self):
        """camelCase input like myProject"""
        result = parse_project_name("myProject")
        assert result == ProjectNames(
            original="myProject",
            snake="my_project",
            pascal="MyProject",
            kebab="my-project",
            lower="myproject",
        )

    def test_single_word_lowercase(self):
        """Single word lowercase like tracker"""
        result = parse_project_name("tracker")
        assert result == ProjectNames(
            original="tracker",
            snake="tracker",
            pascal="Tracker",
            kebab="tracker",
            lower="tracker",
        )

    def test_single_word_capitalized(self):
        """Single word capitalized like Tracker"""
        result = parse_project_name("Tracker")
        assert result == ProjectNames(
            original="Tracker",
            snake="tracker",
            pascal="Tracker",
            kebab="tracker",
            lower="tracker",
        )

    def test_multiple_words_snake(self):
        """Multiple words in snake_case like my_cool_project"""
        result = parse_project_name("my_cool_project")
        assert result == ProjectNames(
            original="my_cool_project",
            snake="my_cool_project",
            pascal="MyCoolProject",
            kebab="my-cool-project",
            lower="mycoolproject",
        )

    def test_multiple_words_pascal(self):
        """Multiple words in PascalCase like MyCoolProject"""
        result = parse_project_name("MyCoolProject")
        assert result == ProjectNames(
            original="MyCoolProject",
            snake="my_cool_project",
            pascal="MyCoolProject",
            kebab="my-cool-project",
            lower="mycoolproject",
        )

    def test_acronym_handling(self):
        """Acronyms like MyAPIProject should split reasonably"""
        result = parse_project_name("MyAPIProject")
        # API stays together as one "word" in the split
        assert result.lower == "myapiproject"
        assert result.original == "MyAPIProject"

    def test_numbers_in_name(self):
        """Names with numbers like project2go"""
        result = parse_project_name("project2go")
        assert result == ProjectNames(
            original="project2go",
            snake="project2go",
            pascal="Project2go",
            kebab="project2go",
            lower="project2go",
        )

    def test_mixed_separators(self):
        """Mixed separators should normalize - use first detected convention"""
        # This is an edge case - my_cool-project has both _ and -
        # We'll split on both and normalize
        result = parse_project_name("my_cool-project")
        assert result.snake == "my_cool_project"
        assert result.kebab == "my-cool-project"
        assert result.lower == "mycoolproject"
