#!/usr/bin/env python3
"""
ARBORIS — Gestión inteligente de tareas y proyectos
Punto de entrada principal
"""
import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    missing = []
    required = [
        ("customtkinter", "customtkinter"),
        ("matplotlib", "matplotlib"),
        ("networkx", "networkx"),
        ("fpdf", "fpdf2"),
        ("openpyxl", "openpyxl"),
        ("groq", "groq"),
    ]
    for module, package in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    return missing


if __name__ == "__main__":
    missing = check_dependencies()
    if missing:
        print("Faltan dependencias. Instalalas con:")
        print(f"   pip install {' '.join(missing)}")
        sys.exit(1)

    from gui.app import main
    main()
