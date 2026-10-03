"""Document element types."""

from enum import Enum


class ElementType(str, Enum):
    TEXT = "text"
    TITLE = "title"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    IMAGE = "image"
    LIST = "list"
    HEADER = "header"
    FOOTER = "footer"
    UNKNOWN = "unknown"
