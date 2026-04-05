# HexPlanner

HexPlanner is a desktop planning tool for large hex-based maps, intended for BitCraft town layout planning.

The project is built in Python with PySide6 and follows a Model-View-Presenter (MVP) architecture.

## Current State

This repository is in an early implementation phase.

What is currently implemented:

- Tile metadata bit-packing logic in hexplanner/model/tile_bits.py
- Test coverage for tile metadata behavior in tests/test_tile_bits.py

What is scaffolded for upcoming implementation:

- Core model modules in hexplanner/model/
- Presenter layer in hexplanner/presenter/
- View layer in hexplanner/view/
- Application services in hexplanner/services/

Legacy prototype code is available in Old/.

## Project Structure

- hexplanner/model/: data model, tile metadata, map logic
- hexplanner/view/: UI and rendering (PySide6)
- hexplanner/presenter/: coordination between UI and model
- hexplanner/services/: save/load and analysis services
- hexplanner/utils/: pure helper functions
- tests/: pytest test suite
- Old/: legacy prototype implementation

## Requirements

- Python 3.10+

Pinned dependencies are listed in requirements.txt:

- numpy==2.2.6
- PySide6==6.10.2
- pytest==8.3.5

## Setup

Windows PowerShell example:

1. Create virtual environment
   python -m venv .venv

2. Activate virtual environment
   .\.venv\Scripts\Activate.ps1

3. Install dependencies
   python -m pip install -r requirements.txt

## Running Tests

Run all tests:

pytest

Run only tile bit tests:

pytest tests/test_tile_bits.py -q

Pytest configuration is defined in pytest.ini with:

- pythonpath = .
- testpaths = tests

## Running the Application

The root entry file main.py currently exists but is empty.

The new MVP app startup flow is still being wired.
For historical reference, a runnable older prototype exists in Old/main.py.

## Architecture Principles

- Model code should remain free of Qt dependencies.
- View handles rendering and user interaction only.
- Presenter coordinates behavior between model and view.
- Design should support future multi-layer map overlays.

## Near-Term Roadmap

- Create a dedicated `model` branch to implement MapConfig and MapModel core operations
- Create a dedicated `view` branch to implement map rendering and UI interaction flow
- Keep model and view work independent, with clear interfaces agreed up front
- Merge `model` and `view` branches together into the main integration branch
- Implement presenter wiring after merge to connect user actions, model updates, and redraw flow
- Add save/load round-trip service
- Add road network analysis workflows
- Add export pipeline for map snapshots

## Development Notes

- Use absolute imports for standard module usage under the hexplanner package.
- In package **init**.py files, use in-package imports (from . import module).
- Keep model-side logic testable and framework-agnostic.
