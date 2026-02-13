from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Document:
    """Text chunk with metadata used across the system.

    Attributes:
        id: unique chunk id
        text: chunk text
        metadata: arbitrary metadata (e.g., page number)
        source: original document path
    """
    id: str
    text: str
    metadata: Dict[str, Any]
    source: str
