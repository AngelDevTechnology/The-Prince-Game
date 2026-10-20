from pathlib import Path
import numpy as np

from ._obj_parser import load_obj as _load_obj

def load_mesh_data(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    positions, indices = _load_obj(str(path))
    return positions, indices