from numpy import add, arange, array, dot, ix_, linalg, linspace, meshgrid, ndarray, vstack, zeros


def get_nodes_and_triangles(
    x_min: int | float,
    x_max: int | float,
    y_min: int | float,
    y_max: int | float,
    x_div: int | float,
    y_div: int | float
) -> tuple[ndarray, ndarray]:

    """
    Get a structured mesh for a rectangular domain.

    Parameters:
    - x_min, x_max: int | float, the x-boundaries of the domain.
    - y_min, y_max: int | float, the y-boundaries of the domain.
    - x_div, y_div: int | float, the number of subdivisions along x and y axes.

    Returns:
    - nodes: ndarray, array of node coordinates.
    - triangles: ndarray, array of triangles defined by node indices.
    """

    # create a grid of points

    x = linspace(start=x_min, stop=x_max, num=x_div + 1)
    y = linspace(start=y_min, stop=y_max, num=y_div + 1)

    xv, yv = meshgrid(x, y, indexing="ij")

    # create node array

    nodes = vstack(tup=(xv.ravel(), yv.ravel())).T

    # generate vertices based on lower left indices

    indices = arange((x_div + 1) * (y_div + 1)).reshape((x_div + 1), (y_div + 1))

    lli = indices[:-1, :-1].ravel()  # lower-left indices
    lri = indices[:-1, 1:].ravel()   # lower-right indices
    uli = indices[1:, :-1].ravel()   # upper-left indices
    uri = indices[1:, 1:].ravel()    # upper-right indices

    # create triangles using indices, two triangles per cell

    lower_triangles = vstack(tup=(lli, lri, uri)).T
    upper_triangles = vstack(tup=(lli, uri, uli)).T

    # concatenate all triangles into one array

    triangles = vstack(tup=(lower_triangles, upper_triangles))

    return nodes, triangles


def get_local_stiffness_matrix(
    nodes: ndarray,
    triangle: ndarray
) -> ndarray:

    """
    Get the local stiffness matrix for a triangle.

    Parameters:
    - nodes: ndarray, array of node coordinates.
    - element: ndarray, indices of the nodes forming the triangle.

    Returns:
    - ndarray, the local stiffness matrix.
    """

    # extract the vertices of the triangle

    p1, p2, p3 = nodes[triangle, :]

    area = 0.5 * linalg.det(a=array((
            (1, p1[0], p1[1]),
            (1, p2[0], p2[1]),
            (1, p3[0], p3[1])
        )))

    # barycentric coordinates gradients

    grad = array(((p2[1] - p3[1], p3[1] - p1[1], p1[1] - p2[1]), (p3[0] - p2[0], p1[0] - p3[0], p2[0] - p1[0]))) / (2 * area)

    return dot(grad.T, grad) * area


def get_global_stiffness_matrix(
    nodes: ndarray,
    triangles: ndarray
) -> ndarray:

    """
    Assemble the global stiffness matrix from local stiffness matrices.

    Parameters:
    - nodes: ndarray, array of node coordinates.
    - triangles: ndarray, array of triangles defined by node indices.

    Returns:
    - ndarray, the global stiffness matrix.
    """

    n_nodes = nodes.shape[0]
    global_stiffness_matrix = zeros(shape=(n_nodes, n_nodes))

    # use advanced indexing and accumulation on numpy arrays

    for triangle in triangles:

        k_local = get_local_stiffness_matrix(nodes=nodes, triangle=triangle)
        add.at(global_stiffness_matrix, (ix_(triangle, triangle)), k_local)

    return global_stiffness_matrix
