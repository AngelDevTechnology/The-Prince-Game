from __future__ import annotations

from pathlib import Path

import numpy as np

from ._obj_parser import load_obj as _load_obj

# ================================================================
# MESH LOADING
# ================================================================

def load_mesh_data(
    path: str | Path,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Charge les données géométriques d'un fichier OBJ.

    Args:
        path:
            Chemin vers le fichier OBJ.

    Returns:
        tuple[np.ndarray, np.ndarray]:
            positions : coordonnées des sommets (N, 3).
            indices   : indices des triangles (M, 3) ou tableau plat,
                        selon le format renvoyé par le parseur.

    Raises:
        FileNotFoundError:
            Si le fichier n'existe pas.

        ValueError:
            Si le contenu du fichier OBJ est invalide.
    """

    # ------------------------------------------------------------
    # PATH VALIDATION
    # ------------------------------------------------------------

    mesh_path = Path(path)

    if not mesh_path.is_file():
        raise FileNotFoundError(
            f"Mesh file not found: {mesh_path}"
        )

    # ------------------------------------------------------------
    # OBJ PARSING
    # ------------------------------------------------------------

    positions, indices = _load_obj(str(mesh_path))

    # ------------------------------------------------------------
    # DATA CONVERSION
    # ------------------------------------------------------------

    positions = np.asarray(positions, dtype=np.float32)
    indices = np.asarray(indices, dtype=np.uint32)

    return positions, indices
