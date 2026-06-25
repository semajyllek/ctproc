import re
from .reference_ranges import LAB_TESTS

# Numeric value: handles "1.5", "100,000", "1,500", "3500"
NUMBER_PATTERN = r"(\d[\d,]*\.?\d*)"

# Units that appear in clinical text
UNIT_PATTERN = (
    r"(?:\s*"
    r"(?:g/[dD][lL]|mg/[dD][lL]|mg/dL|mL/min|IU/L|U/L|mIU/L|mU/L|"
    r"ng/mL|ng/dL|pg/mL|μg/L|μg/dL|µg/L|µg/dL|"
    r"mmol/L|μmol/L|µmol/L|nmol/L|pmol/L|mEq/L|"
    r"x\s*10[\^]?\d+/[Ll]|/mm3|/mm\^3|/μL|/µL|"
    r"mm/h|mm\s*Hg|mmHg|sec|fL|EU|%)"
    r")?"
)


def _build_analyte_pattern() -> re.Pattern:
    """Build a compiled regex that matches any known lab test name or alias."""
    names = set()
    for lt in LAB_TESTS.values():
        names.add(re.escape(lt.name))
        for alias in lt.aliases:
            names.add(re.escape(alias))
    # sort longest first so "Hemoglobin A1c" matches before "Hemoglobin"
    sorted_names = sorted(names, key=len, reverse=True)
    pattern = "|".join(sorted_names)
    return re.compile(rf"(?<![a-zA-Z])({pattern})(?![a-zA-Z])", re.IGNORECASE)


ANALYTE_PATTERN = _build_analyte_pattern()


def parse_number(text: str) -> tuple[float, str] | None:
    """Extract a number from text, handling commas. Returns (value, remaining_text)."""
    m = re.match(r"\s*" + NUMBER_PATTERN, text)
    if m:
        val_str = m.group(1).replace(",", "")
        return float(val_str), text[m.end():]
    return None


def parse_unit(text: str) -> str:
    """Extract a unit from text, or return empty string."""
    m = re.match(UNIT_PATTERN, text.strip())
    if m and m.group():
        return m.group().strip()
    return ""
