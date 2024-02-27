@default:
  @just --list

# Run test, lint, check, hatch build
@build: test lint check
  hatch build

# Check formatting
@check:
  hatch run ruff format --check

# Run check and lint
@checks: check lint

# Remove dist
@clean:
  rm dist/*
  rmdir dist

# Apply formatting with ruff
@format:
  hatch run ruff format

# Lint with ruff
@lint:
  hatch run ruff check

# Run pytest
@test:
  hatch run test

# Run ui.py
@ui:
  hatch run python3 src/filelist_query/ui.py

# Run ui.py with textual --dev
@tui:
  hatch run textual run --dev src/filelist_query/ui.py
