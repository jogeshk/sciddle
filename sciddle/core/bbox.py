"""
Sciddle 2D bounding-box model.

BoundingBox represents an axis-aligned rectangle in Sciddle's
document coordinate space.

The current Sciddle geometry model is strictly 2D.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from sciddle.core.coordinates import CoordinateSystem
from sciddle.core.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """
    Axis-aligned 2D bounding box.

    Parameters
    ----------
    x:
        X-coordinate of the left edge.
    y:
        Y-coordinate of the top edge.
    width:
        Non-negative width.
    height:
        Non-negative height.
    coordinate_system:
        Coordinate system used by the box.

    Zero-width and zero-height boxes are valid and represent
    degenerate geometry such as a point or line boundary.
    """

    x: float
    y: float
    width: float
    height: float
    coordinate_system: CoordinateSystem = CoordinateSystem.DOCUMENT_2D

    def __post_init__(self) -> None:
        values = (
            ("x", self.x),
            ("y", self.y),
            ("width", self.width),
            ("height", self.height),
        )

        for name, value in values:
            if not isinstance(value, (int, float)):
                raise ValidationError(
                    f"{name} must be an int or float."
                )

            if not math.isfinite(float(value)):
                raise ValidationError(
                    f"{name} must be finite."
                )

        if self.width < 0:
            raise ValidationError(
                "BoundingBox width cannot be negative."
            )

        if self.height < 0:
            raise ValidationError(
                "BoundingBox height cannot be negative."
            )

        if not isinstance(self.coordinate_system, CoordinateSystem):
            raise ValidationError(
                "coordinate_system must be a CoordinateSystem."
            )

    @property
    def x2(self) -> float:
        """Return the right edge coordinate."""
        return self.x + self.width

    @property
    def y2(self) -> float:
        """Return the bottom edge coordinate."""
        return self.y + self.height

    @property
    def area(self) -> float:
        """Return the area of the bounding box."""
        return self.width * self.height

    @property
    def center_x(self) -> float:
        """Return the horizontal center coordinate."""
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        """Return the vertical center coordinate."""
        return self.y + self.height / 2

    @property
    def center(self) -> tuple[float, float]:
        """Return the center as an (x, y) tuple."""
        return self.center_x, self.center_y

    def _validate_compatible(
        self,
        other: BoundingBox,
    ) -> None:
        if not isinstance(other, BoundingBox):
            raise TypeError(
                "BoundingBox operations require another BoundingBox."
            )

        if self.coordinate_system != other.coordinate_system:
            raise ValidationError(
                "Cannot perform geometry operations on BoundingBoxes "
                "from different coordinate systems."
            )

    def intersection(
        self,
        other: BoundingBox,
    ) -> BoundingBox | None:
        """
        Return the geometric intersection of two boxes.

        Touching boundaries produce a zero-area intersection box.

        Completely disjoint boxes return None.
        """
        self._validate_compatible(other)

        left = max(self.x, other.x)
        top = max(self.y, other.y)
        right = min(self.x2, other.x2)
        bottom = min(self.y2, other.y2)

        if right < left or bottom < top:
            return None

        return BoundingBox(
            x=left,
            y=top,
            width=right - left,
            height=bottom - top,
            coordinate_system=self.coordinate_system,
        )

    def overlaps(
        self,
        other: BoundingBox,
    ) -> bool:
        """
        Return True when the boxes share positive area.

        Merely touching at an edge or point does not count as overlap.
        """
        intersection = self.intersection(other)

        return (
            intersection is not None
            and intersection.width > 0
            and intersection.height > 0
        )

    def contains(
        self,
        other: BoundingBox,
    ) -> bool:
        """
        Return True when this box completely contains ``other``.

        Boundary contact is considered containment.
        """
        self._validate_compatible(other)

        return (
            self.x <= other.x
            and self.y <= other.y
            and self.x2 >= other.x2
            and self.y2 >= other.y2
        )

    def inside(
        self,
        other: BoundingBox,
    ) -> bool:
        """Return True when this box is completely inside ``other``."""
        return other.contains(self)

    def union(
        self,
        other: BoundingBox,
    ) -> BoundingBox:
        """
        Return the smallest axis-aligned box containing both boxes.
        """
        self._validate_compatible(other)

        left = min(self.x, other.x)
        top = min(self.y, other.y)
        right = max(self.x2, other.x2)
        bottom = max(self.y2, other.y2)

        return BoundingBox(
            x=left,
            y=top,
            width=right - left,
            height=bottom - top,
            coordinate_system=self.coordinate_system,
        )

    def distance_to(
        self,
        other: BoundingBox,
    ) -> float:
        """
        Return the minimum Euclidean distance between two boxes.

        Intersecting or touching boxes have distance 0.
        """
        self._validate_compatible(other)

        horizontal_gap = max(
            other.x - self.x2,
            self.x - other.x2,
            0.0,
        )

        vertical_gap = max(
            other.y - self.y2,
            self.y - other.y2,
            0.0,
        )

        return math.hypot(horizontal_gap, vertical_gap)
