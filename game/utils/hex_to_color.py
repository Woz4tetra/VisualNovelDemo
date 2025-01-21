def hex_to_color(hex: str) -> tuple[int, int, int]:
    """Converts a hex color string to a tuple of RGB values."""
    if len(hex) != 7 or hex[0] != "#":
        raise ValueError(f"Invalid color format: {hex}")
    return tuple(int(hex[i : i + 2], 16) for i in (1, 3, 5))  # type: ignore
