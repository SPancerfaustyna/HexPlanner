# HexPlanner – Copilot Instructions

## Project Overview

HexPlanner is a desktop application built with **Python + PySide6** for creating and editing large hex-based maps.

This project is intended as a **planning tool for the game BitCraft**, focused on helping towns **pre-plan their layouts** before building them in-game.

The tool supports:

- Large hex-based terrain maps
- Road planning
- Efficient editing of large grids (50k–300k tiles)
- Future structure placement aligned with BitCraft mechanics

---

## Core Concept

HexPlanner is **not just a map editor**.
It is a **town layout planning tool**.

The design must support **multiple aligned hex layers**:

### 1. Base Map Layer

- Terrain type
- Height
- Roads
- Large-scale planning

### 2. Structure Overlay Layer (planned)

- Smaller hex grid aligned to base grid
- Used for placing BitCraft buildings/structures
- Represents actual town layout

The architecture must **not assume a single grid forever**.

---

## Architecture Pattern

The project follows **Model–View–Presenter (MVP)**:

- **Model** → Data and logic only (no Qt)
- **View** → UI and rendering (Qt)
- **Presenter** → Handles interactions and coordinates model + view

---

## Project Structure

```text
hexplanner/
    model/
    view/
    presenter/
    services/
    utils/
    resources/

tests/
main.py
```

---

## Architecture Rules

### Model (hexplanner/model/)

- Contains **no Qt imports**

- Stores all map data

- Uses arrays (NumPy or lists), NOT per-tile objects

- Responsible for:
    - tile data access
    - neighbor logic
    - road connections
    - bulk operations (fill, clear, resize)

- Must support future **multi-layer design**

- Must NOT assume only one grid exists

---

### View (hexplanner/view/)

- Contains all PySide6 UI code

- Responsible for:
    - rendering hex grids
    - handling user input (mouse, keyboard)
    - zoom and pan
    - UI panels and dialogs

- Must NOT contain business logic

- Should be designed for **layered rendering**

Future rendering layers:

- terrain layer
- road overlay
- structure overlay

---

### Presenter (hexplanner/presenter/)

- Connects View and Model

- Handles:
    - user actions
    - tool selection
    - model updates
    - triggering redraws

- No rendering code

- No direct data storage

---

### Services (hexplanner/services/)

- Application-level logic
- Not part of core model

Examples:

- MapFileService (save/load)
- Road analysis (connected components)
- ExportService (image export)

---

### Utils (hexplanner/utils/)

- Pure helper functions
- No knowledge of model internals

Examples:

- hex geometry math
- coordinate helpers

---

### Resources (hexplanner/resources/)

- Static assets:
    - icons
    - styles
    - images

---

## Naming Conventions

### General

- `snake_case` → functions, variables
- `PascalCase` → classes
- `UPPER_CASE` → constants

---

### Files

Use descriptive names:

- `map_model.py`
- `tile_bits.py`
- `main_presenter.py`
- `map_view.py`

Avoid generic names like `helpers.py`.

---

### Classes

- `MapModel`
- `MapConfig`
- `TileData`
- `MainPresenter`
- `MapView`
- `MapFileService`

Future:

- `StructureLayerModel`
- `MapDocument`

---

### Functions (Model)

Use explicit names:

```python
get_height(x, y)
set_height(x, y, value)
get_type(x, y)
set_type(x, y, tile_type)
has_road(x, y)
set_road(x, y, enabled)
toggle_road(x, y)
get_neighbors(x, y)
get_road_connections(x, y)
```

---

### Boolean Functions

Always prefix:

- `is_`
- `has_`
- `can_`

Example:

```python
has_road(x, y)
is_in_bounds(x, y)
```

---

## Bit Packing Rules (tile_bits.py)

- Lower 4 bits → tile type
- Bit 4 → road flag
- Remaining bits reserved

Rules:

- Never overwrite unrelated bits
- Validate input ranges
- Keep functions pure (no side effects)

Example constants:

```python
TYPE_MASK = 0x0F
ROAD_MASK = 0x10
TYPE_MAX = 15
```

---

## Model Design Rules

Model MUST:

- store data
- modify data
- return data

Model MUST NOT:

- import Qt
- handle UI
- perform rendering
- open files/dialogs

---

## Coordinate System

Separate three concepts:

1. **Index coordinates**
    - array indices (x, y)

2. **Logical map coordinates**
    - user-visible coordinates
    - derived from `MapConfig`

3. **Screen coordinates**
    - used only in rendering (view)

Do not mix these.

---

## Multi-Layer Design Guidelines

- Design models to support **multiple map layers**
- Do not hardcode logic assuming a single grid
- Keep terrain and structure data separate
- Future structure layer uses smaller aligned hex grid

---

## Performance Guidelines

- Do NOT create one Python object per tile
- Use arrays (NumPy preferred)
- Avoid full-map copies
- Use delta-based changes for undo/redo
- Minimize redraw area when possible

---

## Testing Guidelines

Use **pytest**

### TDD Workflow (Model-First)

When working on model features, follow a strict red-green-refactor loop:

1. **Red**: Write or update a failing test that describes the desired behavior.
2. **Green**: Implement the smallest change needed to make that test pass.
3. **Refactor**: Improve code clarity/structure while keeping tests green.

Additional rules:

- Start from behavior and contracts, not current implementation details.
- Prefer boundary and validation tests before happy-path expansion.
- Keep each test focused on one behavior.
- Do not skip the failing-test step unless fixing a broken test.
- For bugs, first add a regression test that fails, then fix the bug.

Test:

- tile_bits logic
- MapConfig conversions
- MapModel operations
- save/load round-trip

Each test:

- tests one behavior
- is independent
- uses clear naming

Example:

```python
def test_set_type_does_not_affect_road():
```

---

## Import Rules

Use absolute imports:

```python
from hexplanner.model.map_model import MapModel
```

Avoid relative imports:

```python
from ..model import map_model
```

---

## Code Style

- Keep functions small
- Avoid deep nesting
- Prefer explicit logic
- Do not over-engineer early

---

## Future Extensions

- Structure/building placement
- Secondary smaller hex grid overlay
- Multi-layer editing
- Road curve rendering
- Road network analysis
- Undo/redo system
- Map export to image
- BitCraft-specific rules and constraints

---

## What to Avoid

- Mixing UI and model logic
- Using global state
- Per-tile objects
- Putting domain logic in utils
- Overusing inheritance

---

## Summary

HexPlanner is a **BitCraft town planning tool**, not just a map editor.

It must support:

- large-scale terrain editing
- efficient performance
- clean architecture
- future multi-layer hex grids
- structure placement systems

When generating code:

- keep Model pure
- keep View simple
- keep Presenter in control
- design with future layers in mind

---
