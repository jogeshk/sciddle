"""Sciddle public API."""

from pathlib import Path


def load(source: str | Path):
    """
    Load a document.

    Document parsing is intentionally not implemented
    during Phase 1.
    """

    raise NotImplementedError(
        "Document loading belongs to the Document I/O phase."
    )
