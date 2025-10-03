# Contributing to SSHTunnel

Thank you for considering contributing to SSHTunnel! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone git@github.com:YOUR_USERNAME/SSHTunnel.git
   cd SSHTunnel
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the code style guidelines below

3. Add tests for your changes in the `tests/` directory

4. Run tests to ensure they pass:
   ```bash
   pytest tests/ -v
   ```

5. Run linters and type checkers:
   ```bash
   ruff check .
   mypy tunnel.py install.py
   ```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use f-strings for string formatting
- Add docstrings to all functions and modules
- Use descriptive variable names

### Testing

- Write unit tests for all new functionality
- Ensure existing tests still pass
- Aim for high test coverage
- Test edge cases and error conditions

### Commit Messages

Write clear, concise commit messages:

```
Short (50 chars or less) summary

More detailed explanatory text, if necessary. Wrap it to about 72
characters. The blank line separating the summary from the body is
critical.

- Bullet points are okay too
- Use a hyphen or asterisk for bullets
```

## Submitting Changes

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub

3. Ensure CI tests pass

4. Wait for review and address any feedback

## Pull Request Guidelines

- Keep pull requests focused on a single feature or fix
- Update documentation for new features
- Add entries to CHANGELOG.md
- Ensure tests pass and coverage doesn't decrease
- Respond to review feedback promptly

## Reporting Issues

- Use GitHub Issues to report bugs
- Include detailed steps to reproduce the issue
- Include system information (OS, Python version, etc.)
- Include relevant log output

### Bug Report Template

```
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS:
- Python version:
- SSHTunnel version:

**Logs:**
```
relevant log output
```
```

## Feature Requests

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the use case
- Explain why it would be useful to others

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards other community members

## Questions?

If you have questions about contributing, feel free to open an issue with the `question` label.

## License

By contributing to SSHTunnel, you agree that your contributions will be licensed under the GPL-3.0 license.
