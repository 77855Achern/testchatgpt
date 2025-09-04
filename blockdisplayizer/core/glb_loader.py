"""Utilities for loading glTF/GLB meshes using trimesh."""
from __future__ import annotations

import trimesh


def load_glb(path: str) -> trimesh.Trimesh:
    """Load a .glb/.gltf file and return a trimesh mesh."""
    mesh = trimesh.load(path, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = mesh.dump().sum()
    return mesh


def triangulate_if_needed(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Ensure the mesh is fully triangulated."""
    if not mesh.is_watertight or mesh.faces.shape[1] != 3:
        mesh = mesh.subdivide_to_size(max_edge=0)
        mesh = mesh.triangulate()
    return mesh


def ensure_vertex_normals(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Ensure vertex normals are computed."""
    _ = mesh.vertex_normals  # accessing property forces computation
    return mesh
