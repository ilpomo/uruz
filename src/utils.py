from numpy import ndarray
from matplotlib.pyplot import figure, show, subplots
from matplotlib.tri import Triangulation


def plot_solution_2d(
    nodes: ndarray,
    solution: ndarray,
    title: str = "FEM Solution in 2D"
) -> None:

    """
    Plot the 2D surface of the FEM solution.

    Parameters:
    - nodes: ndarray, the node coordinates.
    - solution: ndarray, the solution vector of nodal values.
    - title: str, title of the plot.
    """

    fig, ax = subplots()
    tcf = ax.tripcolor(nodes[:, 0], nodes[:, 1], solution, shading="flat")
    fig.colorbar(tcf)
    ax.set_title(title)
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    show()


def plot_solution_3d(
    nodes: ndarray,
    solution: ndarray,
    triangles: ndarray,
    title: str = "FEM Solution in 3D"
) -> None:

    """
    Plot the 3D surface of the FEM solution.

    Parameters:
    - nodes: ndarray, the node coordinates.
    - solution: ndarray, the solution vector of nodal values.
    - elements: ndarray, array of elements defined by node indices.
    - title: str, title of the plot.
    """

    fig = figure()
    ax = fig.add_subplot(111, projection="3d")

    # create a triangulation object to plot the surface
    tri = Triangulation(nodes[:, 0], nodes[:, 1], triangles=triangles)
    surf = ax.plot_trisurf(tri, solution, cmap="viridis", edgecolor="none")
    fig.colorbar(surf)
    ax.set_title(title)
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.set_zlabel("Potential")
    show()
