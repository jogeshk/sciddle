from __future__ import annotations

import json
from typing import Any

from .bbox import BoundingBox
from .coordinates import CoordinateSystem
from .document import Document
from .element import DocumentElement
from .element_type import ElementType
from .exceptions import ValidationError
from .page import DocumentPage


def _require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{name} must be a dictionary")
    return value


def _require_key(data: dict[str, Any], key: str) -> Any:
    if key not in data:
        raise ValidationError(f"Missing required field: {key}")
    return data[key]


def _bbox_to_dict(bbox: BoundingBox) -> dict[str, Any]:
    return {
        "x": bbox.x,
        "y": bbox.y,
        "width": bbox.width,
        "height": bbox.height,
        "coordinate_system": bbox.coordinate_system.value,
    }


def _bbox_from_dict(data: Any) -> BoundingBox:
    data = _require_mapping(data, "bbox")

    try:
        coordinate_system = CoordinateSystem(
            _require_key(data, "coordinate_system")
        )
    except (ValueError, TypeError) as exc:
        raise ValidationError("Invalid coordinate_system") from exc

    try:
        return BoundingBox(
            x=_require_key(data, "x"),
            y=_require_key(data, "y"),
            width=_require_key(data, "width"),
            height=_require_key(data, "height"),
            coordinate_system=coordinate_system,
        )
    except (TypeError, ValueError) as exc:
        raise ValidationError("Invalid bounding box") from exc


def _element_to_dict(element: DocumentElement) -> dict[str, Any]:
    return {
        "id": element.id,
        "element_type": element.element_type.value,
        "bbox": _bbox_to_dict(element.bbox),
        "text": element.text,
        "confidence": element.confidence,
        "page_number": element.page_number,
        "metadata": dict(element.metadata),
        "children": [
            _element_to_dict(child)
            for child in element.children
        ],
    }


def _element_from_dict(data: Any) -> DocumentElement:
    data = _require_mapping(data, "element")

    try:
        element_type = ElementType(
            _require_key(data, "element_type")
        )
    except (ValueError, TypeError) as exc:
        raise ValidationError("Invalid element_type") from exc

    children = data.get("children", [])

    if not isinstance(children, list):
        raise ValidationError("children must be a list")

    try:
        element = DocumentElement(
            id=_require_key(data, "id"),
            element_type=element_type,
            bbox=_bbox_from_dict(_require_key(data, "bbox")),
            text=data.get("text", ""),
            confidence=data.get("confidence", 1.0),
            page_number=data.get("page_number", 1),
            metadata=data.get("metadata", {}),
        )
    except (TypeError, ValueError) as exc:
        raise ValidationError("Invalid document element") from exc

    for child_data in children:
        child = _element_from_dict(child_data)
        element.add_child(child)

    return element


def document_to_dict(document: Document) -> dict[str, Any]:
    """Serialize a Document into a plain Python dictionary."""
    if not isinstance(document, Document):
        raise TypeError("document must be a Document")

    return {
        "source": document.source,
        "metadata": dict(document.metadata),
        "pages": [
            {
                "number": page.number,
                "width": page.width,
                "height": page.height,
                "elements": [
                    _element_to_dict(element)
                    for element in page.elements
                ],
            }
            for page in document.pages
        ],
    }


def document_from_dict(data: Any) -> Document:
    """Deserialize a Document from a dictionary."""
    data = _require_mapping(data, "document")

    pages = data.get("pages", [])

    if not isinstance(pages, list):
        raise ValidationError("pages must be a list")

    try:
        document = Document(
            source=data.get("source"),
            metadata=data.get("metadata", {}),
        )
    except (TypeError, ValueError) as exc:
        raise ValidationError("Invalid document") from exc

    for page_data in pages:
        page_data = _require_mapping(page_data, "page")

        try:
            page = DocumentPage(
                number=_require_key(page_data, "number"),
                width=_require_key(page_data, "width"),
                height=_require_key(page_data, "height"),
            )
        except (TypeError, ValueError) as exc:
            raise ValidationError("Invalid document page") from exc

        elements = page_data.get("elements", [])

        if not isinstance(elements, list):
            raise ValidationError("page elements must be a list")

        for element_data in elements:
            element = _element_from_dict(element_data)
            page.add_element(element)

        document.add_page(page)

    return document


def document_to_json(
    document: Document,
    *,
    indent: int | None = None,
) -> str:
    """Serialize a Document into deterministic JSON."""
    return json.dumps(
        document_to_dict(document),
        sort_keys=True,
        indent=indent,
        ensure_ascii=False,
        allow_nan=False,
    )


def document_from_json(data: str) -> Document:
    """Deserialize a Document from JSON."""
    if not isinstance(data, str):
        raise TypeError("data must be a string")

    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValidationError("Invalid JSON") from exc

    return document_from_dict(parsed)