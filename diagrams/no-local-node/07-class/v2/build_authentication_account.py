"""Compatibility entry point (2026-11-03): runs build_class_diagrams.py (Mermaid only unless --drawio)."""
from build_class_diagrams import main

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
