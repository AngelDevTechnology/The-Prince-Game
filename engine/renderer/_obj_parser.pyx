# cython: language_level=3

import numpy as np


# ================================================================
# OBJ FILE PARSING
# ================================================================

def load_obj(str path):
    """
    Charge la géométrie d'un fichier OBJ.

    Données extraites :
        - v : positions des sommets.
        - f : faces polygonales.

    Les faces sont converties en triangles par triangulation
    en éventail.

    Formats d'indices acceptés :
        - v
        - v/vt
        - v//vn
        - v/vt/vn

    Les indices positifs et négatifs sont pris en charge.

    Returns:
        positions_array : tableau float32 de forme (N, 3).
        indices_array   : tableau uint32 contenant les triangles.
    """

    # ============================================================
    # LOCAL VARIABLES
    # ============================================================

    cdef list vertices = []
    cdef list indices = []
    cdef list face_indices

    cdef str line
    cdef str token
    cdef str index_text

    cdef list parts

    cdef Py_ssize_t j
    cdef Py_ssize_t vertex_count
    cdef Py_ssize_t index

    # ============================================================
    # FILE READING
    # ============================================================

    with open(path, "r", encoding="utf-8") as file:

        for line in file:

            # ----------------------------------------------------
            # Remove comments and empty lines
            # ----------------------------------------------------

            line = line.partition("#")[0].strip()

            if not line:
                continue

            parts = line.split()

            # ----------------------------------------------------
            # Vertex Position
            # ----------------------------------------------------

            if parts[0] == "v":

                if len(parts) < 4:
                    raise ValueError("Invalid OBJ vertex.")

                vertex = (
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3]),
                )

                if not all(np.isfinite(component) for component in vertex):
                    raise ValueError("OBJ vertex contains non-finite values.")

                vertices.append(vertex)

            # ----------------------------------------------------
            # Face Parsing
            # ----------------------------------------------------

            elif parts[0] == "f":

                if len(parts) < 4:
                    raise ValueError(
                        "An OBJ face must contain at least 3 vertices."
                    )

                vertex_count = len(vertices)
                face_indices = []

                # ------------------------------------------------
                # Extract face vertex indices
                # ------------------------------------------------

                for token in parts[1:]:

                    index_text = token.split("/", 1)[0]

                    if not index_text:
                        raise ValueError(
                            "Missing OBJ position index."
                        )

                    index = int(index_text)

                    if index == 0:
                        raise ValueError(
                            "OBJ indices cannot be zero."
                        )

                    # OBJ indices are 1-based.
                    if index < 0:
                        index = vertex_count + index
                    else:
                        index -= 1

                    if index < 0 or index >= vertex_count:
                        raise ValueError(
                            "OBJ vertex index out of range."
                        )

                    face_indices.append(index)

                # ------------------------------------------------
                # Face Triangulation
                # ------------------------------------------------

                # Fan triangulation:
                # (0, 1, 2), (0, 2, 3), (0, 3, 4), ...

                for j in range(1, len(face_indices) - 1):

                    indices.extend((
                        face_indices[0],
                        face_indices[j],
                        face_indices[j + 1],
                    ))

    # ============================================================
    # DATA VALIDATION
    # ============================================================

    if not vertices:
        raise ValueError(
            "OBJ file contains no vertices."
        )

    if not indices:
        raise ValueError(
            "OBJ file contains no usable faces."
        )

    # ============================================================
    # NUMPY CONVERSION
    # ============================================================

    positions_array = np.ascontiguousarray(
        np.asarray(vertices, dtype=np.float32).reshape(-1, 3)
    )

    indices_array = np.ascontiguousarray(
        np.asarray(indices, dtype=np.uint32)
    )

    # ============================================================
    # RETURN GEOMETRY
    # ============================================================

    return positions_array, indices_array
