from numpy import pi, sin, cos
from src import *
from typing import Literal


def force_function(
    x: int | float,
    y: int | float
) -> int | float:

    return cos(pi * x * cos(x)) * sin(pi * y * sin(y))


def main(
    x_min: int | float,
    x_max: int | float,
    y_min: int | float,
    y_max: int | float,
    x_div: int | float,
    y_div: int | float,
    plot: Literal["2D", "3D"]
) -> None:

    nodes, triangles = get_nodes_and_triangles(
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        x_div=x_div,
        y_div=y_div
    )

    global_stiffness_matrix = get_global_stiffness_matrix(
        nodes=nodes,
        triangles=triangles
    )

    boundary_nodes = get_boundary_nodes(
        nodes=nodes,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max
    )

    stiffness_matrix = apply_boundary_conditions(
        global_stiffness_matrix=global_stiffness_matrix,
        boundary_nodes=boundary_nodes
    )

    rhs = construct_rhs(
        nodes=nodes,
        elements=triangles,
        force_function=force_function
    )

    solution = solve_fem_system(
        stiffness_matrix=stiffness_matrix,
        rhs=rhs
    )

    if plot == "2D":
        plot_solution_2d(
            nodes=nodes,
            solution=solution
        )

    else:
        plot_solution_3d(
            nodes=nodes,
            solution=solution,
            triangles=triangles
        )


if __name__ == "__main__":

    main(
        x_min=0,
        x_max=10,
        y_min=0,
        y_max=10,
        x_div=100,
        y_div=100,
        plot="3D"
    )
