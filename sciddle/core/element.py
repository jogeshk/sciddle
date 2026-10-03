"""
Core document element model for Sciddle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from sciddle.core.bbox import BoundingBox
from sciddle.core.element_type import ElementType
from sciddle.core.exceptions import ValidationError


@dataclass(slots=True)
class DocumentElement:
    """
    A single spatial element within a document page.

    Elements may form a deterministic parent/child hierarchy.
    """

    id: str
    element_type: ElementType
    bbox: BoundingBox
    text: str = ""
    confidence: float = 1.0
    page_number: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list["DocumentElement"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise ValidationError("Element id must be a string.")

        if not self.id.strip():
            raise ValidationError("Element id cannot be empty.")

        if not isinstance(self.element_type, ElementType):
            raise ValidationError(
                "element_type must be an ElementType."
            )

        if not isinstance(self.bbox, BoundingBox):
            raise ValidationError(
                "bbox must be a BoundingBox."
            )

        if not isinstance(self.text, str):
            raise ValidationError(
                "text must be a string."
            )

        if not isinstance(self.confidence, (int, float)):
            raise ValidationError(
                "confidence must be an int or float."
            )

        if not math.isfinite(float(self.confidence)):
            raise ValidationError(
                "confidence must be finite."
            )

        if not 0.0 <= self.confidence <= 1.0:
            raise ValidationError(
                "confidence must be between 0 and 1."
            )

        if (
            isinstance(self.page_number, bool)
            or not isinstance(self.page_number, int)
        ):
            raise ValidationError(
                "page_number must be an integer."
            )

        if self.page_number < 1:
            raise ValidationError(
                "page_number must be greater than or equal to 1."
            )

        if not isinstance(self.metadata, dict):
            raise ValidationError(
                "metadata must be a dictionary."
            )

        if not isinstance(self.children, list):
            raise ValidationError(
                "children must be a list."
            )

        for child in self.children:
            self._validate_child(child)

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Set one metadata value."""
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
        """Return a metadata value or the supplied default."""
        return self.metadata.get(key, default)

    def _validate_child(
        self,
        child: "DocumentElement",
    ) -> None:
        if not isinstance(child, DocumentElement):
            raise ValidationError(
                "Child must be a DocumentElement."
            )

        if child is self:
            raise ValidationError(
                "An element cannot be its own child."
            )

        if child.page_number != self.page_number:
            raise ValidationError(
                "Parent and child must belong to the same page."
            )

        if self._contains_element(child):
            raise ValidationError(
                "Adding this child would create a hierarchy cycle."
            )

    def _contains_element(
        self,
        target: "DocumentElement",
    ) -> bool:
        """
        Return True if target exists in this element's descendants.
        """
        for child in self.children:
            if child is target:
                return True

            if child._contains_element(target):
                return True

        return False

    def add_child(
        self,
        child: "DocumentElement",
    ) -> None:
        """
        Add a child element.

        Child IDs must be unique among direct children.
        """
        self._validate_child(child)

        if any(existing.id == child.id for existing in self.children):
            raise ValidationError(
                f"Duplicate child id: {child.id!r}"
            )

        if child._contains_element(self):
            raise ValidationError(
                "Adding this child would create a hierarchy cycle."
            )

        self.children.append(child)

    def remove_child(
        self,
        child: "DocumentElement",
    ) -> None:
        """Remove a direct child element."""
        if not isinstance(child, DocumentElement):
            raise ValidationError(
                "Child must be a DocumentElement."
            )

        for index, existing in enumerate(self.children):
            if existing is child:
                del self.children[index]
                return

        raise ValidationError(
            f"Element {child.id!r} is not a direct child."
        )

    @property
    def child_count(self) -> int:
        """Return the number of direct children."""
        return len(self.children)

    def descendants(self) -> list["DocumentElement"]:
        """
        Return descendants in deterministic depth-first order.
        """
        result: list[DocumentElement] = []

        for child in self.children:
            result.append(child)
            result.extend(child.descendants())

        return result

    def is_ancestor_of(
        self,
        element: "DocumentElement",
    ) -> bool:
        """Return whether this element is an ancestor of element."""
        return any(
            descendant is element
            for descendant in self.descendants()
        )

    def is_descendant_of(
        self,
        element: "DocumentElement",
    ) -> bool:
        """Return whether this element is a descendant of element."""
        return element.is_ancestor_of(self)