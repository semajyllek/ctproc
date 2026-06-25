import re
from typing import List

from .types import LabValue
from .reference_ranges import get_lab_test
from .patterns import ANALYTE_PATTERN, parse_number, parse_unit


# Words/symbols between an analyte name and its value in clinical text.
# Includes eligibility comparators as noise to skip through.
_FILLER_WORDS = re.compile(
    r"^(?:count|level|of|is|was|"
    r"at\s+least|greater\s+than(?:\s+or\s+equal\s+to)?|"
    r"less\s+than(?:\s+or\s+equal\s+to)?|"
    r"no\s+greater\s+than|no\s+less\s+than|no\s+more\s+than|"
    r"equal\s+to|above|below|over|under|approximately"
    r")[\s:]*",
    re.IGNORECASE,
)

# Symbols/punctuation between analyte and value
_FILLER_SYMBOLS = re.compile(
    r"^(?:\([A-Z]{2,6}\)\s*)?"     # optional parenthesized abbreviation like (LDH)
    r"[\s:]*"                       # colon, whitespace
    r"(?:≥|>=|≤|<=|>|<|=)?\s*",    # optional comparator symbol
)


def extract_lab_values(text: str) -> List[LabValue]:
    """
    Extract lab values from clinical text.

    Finds mentions of known lab tests and their associated numeric values.
    Works on any clinical text: lab reports, clinical notes, eligibility criteria,
    patient descriptions.

    Returns a list of LabValue objects with analyte name, value(s), unit, and
    position in the source text.
    """
    results = []
    for m in ANALYTE_PATTERN.finditer(text):
        analyte_text = m.group(1)
        lab_test = get_lab_test(analyte_text)
        if lab_test is None:
            continue

        after = text[m.end():m.end() + 150]
        extracted = _extract_value(after, lab_test, m.start(), m.end(), text)
        if extracted:
            results.append(extracted)

    return results


def _extract_value(after: str, lab_test, match_start: int, match_end: int, full_text: str) -> LabValue | None:
    """Try to extract a numeric value (and optional unit) from text following an analyte name."""

    # strip symbols (colon, parens, comparator symbols), then filler words, repeat
    cleaned = after.strip()
    changed = True
    while changed:
        changed = False
        result = _FILLER_SYMBOLS.sub("", cleaned).strip()
        if result != cleaned:
            cleaned = result
            changed = True
        result = _FILLER_WORDS.sub("", cleaned, count=1).strip()
        if result != cleaned:
            cleaned = result
            changed = True

    # handle ULN pattern: "2.5 times upper limit of normal" or "2.5 x ULN"
    num = parse_number(cleaned)
    if num is None:
        return None

    val, rest = num

    # check for ULN — treat the multiplier as the value, unit as "x ULN"
    uln_match = re.match(
        r"\s*(?:x\s+|times?\s+)?(?:the\s+)?(?:upper\s+limit\s+of\s+normal|ULN|institutional\s+normal)",
        rest, re.IGNORECASE,
    )
    if uln_match:
        end_pos = match_end + len(after) - len(cleaned) + len(str(val)) + uln_match.end()
        return LabValue(
            analyte=lab_test.name, value=val, unit="x ULN",
            start=match_start, end=end_pos,
            raw_text=full_text[match_start:end_pos].strip(),
        )

    # check for range: "9-12" or "9–12"
    range_match = re.match(r"\s*[-–]\s*", rest)
    if range_match:
        rest2 = rest[range_match.end():]
        num2 = parse_number(rest2)
        if num2:
            val2, rest3 = num2
            unit = parse_unit(rest3) or lab_test.default_unit
            end_pos = match_end + len(after) - len(rest3)
            return LabValue(
                analyte=lab_test.name, value=val, value_high=val2, unit=unit,
                start=match_start, end=end_pos,
                raw_text=full_text[match_start:end_pos].strip(),
            )

    # single value with optional unit
    unit = parse_unit(rest) or lab_test.default_unit
    end_pos = match_end + len(after) - len(rest) + (len(unit) if unit in rest else 0)
    return LabValue(
        analyte=lab_test.name, value=val, unit=unit,
        start=match_start, end=end_pos,
        raw_text=full_text[match_start:end_pos].strip(),
    )
