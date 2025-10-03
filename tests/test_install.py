#!/usr/bin/env python3
"""Tests for install.py module."""

import unittest


def barebones(content: str) -> list[str]:
    """Remove comments and blank lines from content (copied from install.py)."""
    lines: list[str] = []
    for line in content.split("\n"):
        line = line.strip()
        if (len(line) == 0) or (line[0] == "#"):
            continue
        lines.append(line)
    return lines


class TestBarebones(unittest.TestCase):
    """Test the barebones function."""

    def test_removes_comments(self):
        """Test that comments are removed."""
        content = "line1\n# comment\nline2"
        result = barebones(content)
        self.assertEqual(result, ["line1", "line2"])

    def test_removes_blank_lines(self):
        """Test that blank lines are removed."""
        content = "line1\n\nline2\n   \nline3"
        result = barebones(content)
        self.assertEqual(result, ["line1", "line2", "line3"])

    def test_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        content = "  line1  \n\tline2\t\n   line3   "
        result = barebones(content)
        self.assertEqual(result, ["line1", "line2", "line3"])

    def test_mixed_content(self):
        """Test with mixed content."""
        content = """
        # Comment line
        actual line 1

        # Another comment
        actual line 2
        """
        result = barebones(content)
        self.assertEqual(result, ["actual line 1", "actual line 2"])

    def test_empty_string(self):
        """Test with empty string."""
        content = ""
        result = barebones(content)
        self.assertEqual(result, [])

    def test_only_comments(self):
        """Test with only comments."""
        content = "# comment 1\n# comment 2\n# comment 3"
        result = barebones(content)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
