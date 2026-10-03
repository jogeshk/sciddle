"""
Coordinate-system definitions for Sciddle.

Sciddle currently operates on 2D document geometry only.

The coordinate-system identity is kept explicit so that different
document sources cannot be silently mixed.

The exact origin and axis direction are defined by the document
source/parser and must not be assumed globally at this stage.
"""

from enum import Enum


class CoordinateSystem(str, Enum):
    """
    Coordinate systems supported by Sciddle.

    DOCUMENT_2D represents the native 2D coordinate space used for
    document geometry.

    Sciddle does not currently define or support any 3D coordinate
    systems.
    """

    DOCUMENT_2D = "document_2d"