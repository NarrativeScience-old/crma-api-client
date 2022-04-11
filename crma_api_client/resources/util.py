"""Contains utility functions for working with resources"""


def to_camel(string: str) -> str:
    """Change a snake case string to camel case

    Args:
        string: String to change case

    Returns:
        camelCase string

    """
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
    )
