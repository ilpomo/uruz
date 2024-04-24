from numpy import add, ndarray, where, zeros
from scipy.sparse import csr_matrix, issparse
from scipy.sparse.linalg import spsolve


def get_boundary_nodes(
    nodes: ndarray,
    x_min: int | float,
    x_max: int | float,
    y_min: int | float,
    y_max: int | float
) -> ndarray:

    """
    Identify the boundary nodes in the domain.

    Parameters:
    - nodes: ndarray, array of node coordinates.
    - x_min, x_max, y_min, y_max: int | float, the boundaries of the domain.

    Returns:
    - ndarray, indices of the boundary nodes.
    """

    return where(
        (nodes[:, 0] == x_min) | (nodes[:, 0] == x_max) |
        (nodes[:, 1] == y_min) | (nodes[:, 1] == y_max)
    )[0]


def apply_boundary_conditions(
    global_stiffness_matrix: ndarray,
    boundary_nodes: ndarray
) -> ndarray:

    """
    Apply zero boundary conditions to the global stiffness matrix.

    Parameters:
    - global_stiffness_matrix: ndarray, the global stiffness matrix.
    - boundary_nodes: ndarray, indices of the boundary nodes.

    Returns:
    - ndarray, the modified global stiffness matrix.
    """

    # zero out all rows and columns corresponding to the boundary nodes

    global_stiffness_matrix[boundary_nodes, :] = 0
    global_stiffness_matrix[:, boundary_nodes] = 0

    # set diagonal elements for boundary nodes to a large number

    global_stiffness_matrix[boundary_nodes, boundary_nodes] = 1e6

    return global_stiffness_matrix


def construct_rhs(
    nodes: ndarray,
    elements: ndarray,
    force_function: callable
) -> ndarray:

    """
    Construct the right-hand side vector for the FEM system.

    Parameters:
    - nodes: ndarray, array of node coordinates.
    - triangles: ndarray, array of triangles defined by node indices.
    - force_function: callable, a function that defines the force at any given point.

    Returns:
    - ndarray, the right-hand side vector.
    """

    rhs = zeros(nodes.shape[0])

    # vectorize computation of centroids and areas

    element_nodes = nodes[elements]  # shape: (num_elements, 3, 2)

    # calculate centroids of each element

    centroids = element_nodes.mean(axis=1)

    # calculate the areas of each element
    # using determinant formula: area = 0.5 * abs(det(A))
    # where A = [1 x1 y1; 1 x2 y2; 1 x3 y3]

    x1, x2, x3 = element_nodes[:, 0, 0], element_nodes[:, 1, 0], element_nodes[:, 2, 0]
    y1, y2, y3 = element_nodes[:, 0, 1], element_nodes[:, 1, 1], element_nodes[:, 2, 1]
    areas = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    # ensure force_function can handle vectorized input
    if centroids.ndim == 2:
        forces = force_function(*centroids.T)  # decompose centroids into x and y for function
    else:
        forces = force_function(centroids)

    forces = forces * areas / 3

    for i in range(3):  # distribute forces to the nodes
        add.at(rhs, elements[:, i], forces)

    return rhs


def solve_fem_system(
    stiffness_matrix: ndarray,
    rhs: ndarray
) -> ndarray:

    """
    Solve the FEM linear system.

    Parameters:
    - stiffness_matrix: ndarray, the global stiffness matrix.
    - rhs: ndarray, the right-hand side vector.

    Returns:
    - ndarray, the nodal values of the solution.
    """

    if not issparse(x=stiffness_matrix):
        stiffness_matrix = csr_matrix(stiffness_matrix)

    return spsolve(stiffness_matrix, rhs)
