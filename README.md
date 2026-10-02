# Sciddle

## Hardware-Accelerated Spatial Graph Document Extraction Engine

Sciddle is a local-first document processing engine designed to represent documents as **2D spatial structures** rather than treating them as plain text.

Instead of reducing a document to:

    Document → Text → Output

Sciddle is designed around:

    Document
        ↓
    Pages
        ↓
    Elements
        ↓
    Geometry
        ↓
    Layout
        ↓
    Spatial Relationships
        ↓
    2D Spatial Graph
        ↓
    Spatial Inference
        ↓
    Optional AI / GNN Reasoning
        ↓
    Structured Output

The central idea is simple:

> The physical arrangement of information inside a document is meaningful data.

A title above a paragraph, a caption below an image, a label beside a figure, a table inside a region, or two columns positioned next to each other all contain spatial information.

Sciddle is being engineered to preserve and reason about that information.

---

# Project Status

**Current development phase: Phase 1 — Python Foundation**

Phase 1 establishes the fundamental Sciddle package, data models, validation, public API foundation, packaging, and automated tests.

Current implemented foundation includes:

- Python package structure
- Version management
- Sciddle exception hierarchy
- Document element types
- 2D bounding boxes
- Document elements
- Document pages
- Documents
- Basic validation
- Public `sciddle` package API
- PyPI-compatible project configuration
- Editable installation
- Unit tests

The current implementation is intentionally small.

Advanced document parsing, layout analysis, spatial graph construction, native acceleration, GPU acceleration, and AI/GNN functionality are **not being falsely presented as implemented**.

---

# Why Sciddle?

Traditional document extraction often focuses primarily on text.

That approach can lose important information about where things are located.

For example, consider a document containing:

- a title
- multiple paragraphs
- two columns
- a table
- an image
- a caption
- headers
- footers
- labels

The text alone does not fully describe the document.

Sciddle aims to preserve the relationship between:

    What something is
    Where it is
    What surrounds it
    What it is spatially related to
    How it participates in the document structure

This creates a foundation for spatial document understanding.

---

# Core Concept

Sciddle's central representation is:

    Elements
        +
    Geometry
        +
    Layout
        +
    Spatial Relationships
        +
    Graph

A document can therefore eventually be represented as a 2D spatial graph.

Conceptually:

    ┌─────────────────────┐
    │      Document       │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │        Pages        │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │      Elements       │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │      Geometry       │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │       Layout        │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │Spatial Relationships│
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │   Spatial Graph     │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Spatial Inference   │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Structured Output   │
    └─────────────────────┘

---

# 2D First

Sciddle is currently a **2D document-processing system**.

The current architecture focuses on document geometry such as:

- X/Y coordinates
- width
- height
- bounding boxes
- page geometry
- element positions
- spatial relationships
- 2D graph structures

3D document processing is intentionally outside the current scope.

The project will not introduce unnecessary 3D abstractions merely for future possibilities.

This keeps the current architecture focused and easier to test, optimize, and maintain.

---

# Local-First Architecture

Sciddle is designed to process documents locally.

The core workflow is intended to work without requiring:

- a Sciddle server
- a Sciddle cloud service
- remote document processing
- uploading documents to a remote service
- external processing APIs
- an internet connection for core processing

PyPI is a distribution mechanism, not a remote processing backend.

The long-term goal is:

```python
import sciddle

doc = sciddle.load("document.pdf")
result = doc.extract()