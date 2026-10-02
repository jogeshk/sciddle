"""Sciddle â€” Hardware-Accelerated Spatial Graph Document Extraction Engine."""

from ._version import __version__
from .api import load
from .core import (
    BoundingBox,
    Document,
    DocumentElement,
    DocumentPage,
    ElementType,
    SciddleError,
    ValidationError,
)

__all__ = [
    "__version__",
    "load",
    "BoundingBox",
    "Document",
    "DocumentElement",
    "DocumentPage",
    "ElementType",
    "SciddleError",
    "ValidationError",
]
