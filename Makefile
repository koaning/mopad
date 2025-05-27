.PHONY: help install install-dev build clean docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install the package"
	@echo "  install-dev  Install development dependencies"
	@echo "  build        Build the package"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Generate documentation"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Build targets
build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Documentation target
docs:
	marimo export html-wasm --output docs --show-code --mode edit demo.py

pypi: clean
	uv build
	uv publish
