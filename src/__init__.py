from src.fem import get_boundary_nodes, apply_boundary_conditions, construct_rhs, solve_fem_system
from src.mesh import get_nodes_and_triangles, get_local_stiffness_matrix, get_global_stiffness_matrix
from src.utils import plot_solution_2d, plot_solution_3d


__all__ = [
    "get_boundary_nodes", "apply_boundary_conditions", "construct_rhs", "solve_fem_system",
    "get_nodes_and_triangles", "get_local_stiffness_matrix", "get_global_stiffness_matrix",
    "plot_solution_2d", "plot_solution_3d"
]
