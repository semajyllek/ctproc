from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class LabValue:
    """A lab value extracted from clinical text."""
    analyte: str
    value: float
    value_high: Optional[float] = None
    unit: str = ""
    start: int = 0
    end: int = 0
    raw_text: str = ""


@dataclass
class ReferenceRange:
    """A reference range for a single demographic group."""
    low: Optional[float] = None
    high: Optional[float] = None
    unit: str = ""


@dataclass
class LabTest:
    """A lab test definition with canonical name, aliases, and reference ranges."""
    name: str
    aliases: List[str] = field(default_factory=list)
    si_range: Optional[ReferenceRange] = None
    conventional_range: Optional[ReferenceRange] = None
    demographic_ranges: Dict[str, ReferenceRange] = field(default_factory=dict)
    default_unit: str = ""
