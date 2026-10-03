"""
Core document model for Sciddle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sciddle.core.exceptions import ValidationError
from sciddle.core.page import DocumentPage


@dataclass(slots=True)
class Document:
    """
    Root document representation used by Sciddle.
    """

    source: str | None = None
    pages: list[DocumentPage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.source is not None and not isinstance(
            self.source,
            str,
        ):
            raise ValidationError(
                "Document source must be a string or None."
            )

        if not isinstance(self.pages, list):
            raise ValidationError(
                "pages must be a list."
            )

        if not isinstance(self.metadata, dict):
            raise ValidationError(
                "metadata must be a dictionary."
            )

        page_numbers: set[int] = set()

        for page in self.pages:
            if not isinstance(page, DocumentPage):
                raise ValidationError(
                    "Document pages must be DocumentPage instances."
                )

            if page.number in page_numbers:
                raise ValidationError(
                    f"Duplicate page number: {page.number}"
                )

            page_numbers.add(page.number)

    @property
    def page_count(self) -> int:
        """Return the number of pages."""
        return len(self.pages)

    @property
    def element_count(self) -> int:
        """Return the total number of elements."""
        return sum(len(page.elements) for page in self.pages)

    def add_page(
        self,
        page: DocumentPage,
    ) -> None:
        """Add a page while enforcing unique page numbers."""
        if not isinstance(page, DocumentPage):
            raise ValidationError(
                "page must be a DocumentPage."
            )

        if any(existing.number == page.number for existing in self.pages):
            raise ValidationError(
                f"Duplicate page number: {page.number}"
            )

        self.pages.append(page)

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Set one document metadata value."""
        if not isinstance(key, str):
            raise ValidationError(
                "Metadata key must be a string."
            )

        if not key.strip():
            raise ValidationError(
                "Metadata key cannot be empty."
            )

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Return a document metadata value."""
        return self.metadata.get(key, default)