# cython: language_level=3

import numpy as np


def load_obj(str path):

    cdef list vertices = []
    cdef list indices = []
    cdef list face_indices
    cdef str line
    cdef str token
    cdef str index_text
    cdef list parts
    cdef Py_ssize_t i
    cdef Py_ssize_t j
    cdef Py_ssize_t vertex_count
    cdef long index

    with open(path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            line = line.partition("#")[0].strip()

            if not line:
                continue

            parts = line.split()

            if parts[0] == "v":
                if len(parts) < 4:
                    raise ValueError("Sommet OBJ invalide.")

                vertices.append((
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3]),
                ))

            elif parts[0] == "f":
                if len(parts) < 4:
                    raise ValueError("Une face OBJ doit avoir au moins 3 sommets.")

                vertex_count = len(vertices)
                face_indices = []

                for token in parts[1:]:
                    index_text = token.split("/", 1)[0]

                    if not index_text:
                        raise ValueError("Indice de position OBJ manquant.")

                    index = int(index_text)

                    if index == 0:
                        raise ValueError("Les indices OBJ ne peuvent pas être nuls.")

                    if index < 0:
                        index = vertex_count + index
                    else:
                        index -= 1

                    if index < 0 or index >= vertex_count:
                        raise ValueError("Indice de sommet OBJ hors limites.")

                    face_indices.append(index)

                # Triangulation en éventail : (0, 1, 2), (0, 2, 3), etc.
                for j in range(1, len(face_indices) - 1):
                    indices.extend((
                        face_indices[0],
                        face_indices[j],
                        face_indices[j + 1],
                    ))

    if not vertices:
        raise ValueError("Le fichier OBJ ne contient aucun sommet.")

    if not indices:
        raise ValueError("Le fichier OBJ ne contient aucune face exploitable.")

    positions_array = np.ascontiguousarray(
        np.asarray(vertices, dtype=np.float32).reshape(-1, 3)
    )

    indices_array = np.ascontiguousarray(
        np.asarray(indices, dtype=np.uint32)
    )

    return positions_array, indices_array