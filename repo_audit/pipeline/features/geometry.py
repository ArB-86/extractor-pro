from __future__ import annotations

from pipeline.layout.line import LayoutLine


def left_margin(line: LayoutLine) -> float:
    return line.x0


def right_margin(line: LayoutLine) -> float:
    return line.x1


def width(line: LayoutLine) -> float:
    return line.width


def center(line: LayoutLine) -> float:
    return line.center_x


def vertical_distance(a: LayoutLine, b: LayoutLine) -> float:
    return abs(b.y0 - a.y1)


def horizontal_overlap(a: LayoutLine, b: LayoutLine) -> float:

    left = max(a.x0, b.x0)
    right = min(a.x1, b.x1)

    return max(0.0, right - left)


def same_column(
    a: LayoutLine,
    b: LayoutLine,
    tolerance: float = 20.0,
) -> bool:

    return abs(a.indent - b.indent) <= tolerance


def is_indented(
    line: LayoutLine,
    body_indent: float,
    tolerance: float = 12.0,
) -> bool:

    return line.indent > body_indent + tolerance
