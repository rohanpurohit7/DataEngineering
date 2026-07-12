from __future__ import annotations
import os
import subprocess
from pathlib import Path
from typing import Sequence

DRY_RUN = os.getenv("DRY_RUN", "true").lower() != "false"

def run(command: Sequence[str], check: bool = True) -> subprocess.CompletedProcess:
    printable = " ".join(str(x) for x in command)
    print(f"$ {printable}")
    if DRY_RUN:
        return subprocess.CompletedProcess(command, 0, stdout="DRY_RUN", stderr="")
    return subprocess.run(command, check=check, text=True, capture_output=True)

def require_file(path: str | Path) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Required file not found: {p}")
    return p
