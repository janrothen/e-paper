#!/bin/bash
# Activation script for LED strip project

echo "🔧 Activating LED Strip Controller environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo "📁 Project: LED Strip Controller"
echo "🐍 Python: $(python --version)"
echo "📦 Pip packages: $(pip list --format=freeze | wc -l) installed"
echo ""
echo "Available commands:"
echo "  ./run.py breathing --color red"
echo "  pytest"
echo "  pytest --cov=led"
echo ""
