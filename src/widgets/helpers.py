import re
from bisect import bisect_right


# ── Search / find utilities ─────────────────────────────────────────────────
def _find_next(
    text: str, query: str, cursor_pos: int, case_sensitive: bool = True
) -> tuple[int, int]:  # Return (start, end) of next match
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(query), flags)
    match = pattern.search(text, cursor_pos)
    if not match:
        match = pattern.search(text, 0)
    if match is not None:
        return match.start(), match.end()
    return -1, -1


def _find_prev(
    text: str, query: str, cursor_pos: int, case_sensitive: bool = True
) -> tuple[int, int]:  # Return (start, end) of prev match
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(query), flags)
    match = pattern.search(text, cursor_pos)

    before, overall = None, None
    for match in pattern.finditer(text):
        overall = match
        if match.end() < cursor_pos:
            before = match
    result = before or overall
    if result is not None:
        return result.start(), result.end()
    return -1, -1


def _build_line_offsets(text: str) -> list[int]:
    offsets = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            offsets.append(i + 1)
    return offsets


def _text_offset_to_location(
    text: str,
    offset: int,
    line_starts: list[int] | None = None,  # like cache
) -> tuple[int, int]:
    if not line_starts:
        line_starts = _build_line_offsets(text)
    row = bisect_right(line_starts, offset) - 1
    return row, offset - line_starts[row]
