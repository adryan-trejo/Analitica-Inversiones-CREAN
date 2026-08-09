"""Punto de entrada para iniciar el tablero Streamlit local (implementación completa en Etapa 6)."""

import subprocess
import sys


def main() -> None:
    """Lanza el tablero Streamlit ubicado en `app/app.py`."""
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app/app.py"],
        check=True,
    )


if __name__ == "__main__":
    main()
