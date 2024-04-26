from numpy import cos, exp, pi, sin, sqrt


def gaussian_heat_source(
    x: int | float,
    y: int | float,
    center_x: int | float = 0.5,
    center_y: int | float = 0.5,
    intensity: int | float = 1,
    spread: int | float = 0.1
) -> int | float:

    """
    This function simulates a localized heat source or sink, ideal for modeling phenomena such as concentrated heat or
    energy sources within a specified area.

    Calculate a Gaussian heat source distribution.

    Parameters:
    - x, y: int | float
        Coordinates at which to evaluate the function.
    - center_x, center_y: int | float
        The x and y coordinates of the center of the heat source.
    - intensity: int | float
        The maximum intensity of the heat source.
    - spread: int | float
        The spread of the Gaussian distribution.

    Returns:
    - int | float
        The intensity of the heat source at the given coordinates.
    """

    return intensity * exp(-((x - center_x) ** 2 + (y - center_y) ** 2) / (2 * spread ** 2))


def multi_wave_interference(
    x: int | float,
    y: int | float,
    coefficients: tuple[tuple[int | float, ...], tuple[int | float, ...]] = ((1, 2, 3, 0.5, 0.5), (0.5, 5, 1, 0, 0))
) -> int | float:

    """
    This function generates a multi-wave interference pattern using a combination of sine and cosine waves with
    varying frequencies and phases. It's designed to model phenomena where multiple wave sources interact, such as in
    water waves, sound waves, or electromagnetic fields.

    Generate a complex wave interference pattern based on multiple wave components.

    Parameters:
    - x, y: int | float
        Coordinates at which to evaluate the function.
    - coefficients: tuple[tuple[int | float, ...], tuple[int | float, ...]]
        A tuple of tuples where each tuple contains the amplitude, frequency, and phase shift for each wave component.
        Each tuple is in the form (amplitude, frequency_x, frequency_y, phase_x, phase_y).

    Returns:
    - int | float
        The combined wave interference value at the given coordinates.

    Example:
    - coefficients = ((1, 2, 3, 0.5, 0.5), (0.5, 5, 1, 0, 0))
        This represents two wave components with specified amplitudes, frequencies along x and y, and phase shifts.
    """

    result = 0

    for amplitude, frequency_x, frequency_y, phase_x, phase_y in coefficients:
        result += amplitude * sin(pi * frequency_x * x + phase_x) * cos(pi * frequency_y * y + phase_y)

    return result


def radial_symmetric_function(
    x: int | float,
    y: int | float,
    center_x: int | float = 0.5,
    center_y: int | float = 0.5,
    intensity: int | float = 1
) -> int | float:

    """
    This function models radial effects like a pressure or gravitational field emanating from or concentrating towards
    a central point.

    Calculate a radial symmetric function that simulates effects like pressure or gravity fields.

    Parameters:
    - x, y: int | float
        Coordinates at which to evaluate the function.
    - center_x, center_y: int | float
        The x and y coordinates of the center of the radial effect.
    - intensity: int | float
        The intensity of the radial effect, which diminishes with distance from the center.

    Returns:
    - int | float
        The calculated intensity of the radial effect at the given coordinates.
    """

    distance = sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    return intensity / (1 + distance)


def sine_wave_pattern(
    x: int | float,
    y: int | float,
    frequency_x: int | float = 2,
    frequency_y: int | float = 2
) -> int | float:

    """
    This function creates a sinusoidal pattern over the domain, useful for simulating periodic processes like waves or
    oscillations across a surface.

    Generate a sinusoidal wave pattern based on x and y frequencies.

    Parameters:
    - x, y: int | float
        Coordinates at which to evaluate the function.
    - frequency_x, frequency_y: int | float
        The frequency of the sinusoidal pattern along the x and y axes.

    Returns:
    - int | float
        The value of the sinusoidal function at the given coordinates.
    """

    return sin(pi * frequency_x * x) * sin(pi * frequency_y * y)
