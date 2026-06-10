"""Command: 10선 판정 (ECB Control)."""

MAGIC_CONSTANT = 34

LINE_IDS = (
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
)


def validate_lines(grid: list) -> dict:
    """4×4 격자 10선 판정.

    Returns:
        {"status": "pass"|"fail"|"incomplete", "failed_lines": list[str]}
        failed_lines: 깨진 선 ID (R1~R4, C1~C4, D1, D2). pass·incomplete 시 [].
    """
    ...
