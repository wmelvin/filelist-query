@default:
  @just --list

# Check formatting
@check:
  hatch fmt --check

# Remove dist
@clean:
  rm dist/*
  rmdir dist

# Apply formatting with hatch
@format:
  hatch fmt

# Lint with hatch
@lint:
  hatch fmt --linter

@ui:
  hatch run python3 src/filelist_query/ui.py
