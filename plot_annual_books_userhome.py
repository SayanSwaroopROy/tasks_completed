"""
This script manages data input, validation, visualization, and main execution
for plotting monthly books read data.

Dependencies:
- matplotlib.pyplot as plt
- numpy as np
- LinearSegmentedColormap from matplotlib.colors
- interp1d from scipy.interpolate

Functions:
- get_yearly_data(): Retrieves and processes yearly data input from the user.
- verify_yearly_data(yearly_data: list): Verifies the validity of yearly data for books read.
- smooth_data(x_axis, y_axis, num_points=100): Smooths data points using cubic interpolation.
- calculate_ytick_interval(max_value): Calculates the optimal y-axis tick interval based on the maximum value.
- plot_books_per_month(books_read): Plots the number of books read per month in a line chart with a gradient background.
- main(): Executes the main workflow to plot monthly books read data.

Usage:
- Run the script to interactively prompt the user for yearly data on books read.
- Validates the input data to ensure it contains 12 elements of non-negative integers.
- Utilizes cubic interpolation to smooth data for a visually appealing plot.
- Generates a plot with a gradient background and customized axis ticks and labels.
- The main function integrates all steps, ensuring error handling and data validation.

Note: Ensure all dependencies are installed (`matplotlib`, `numpy`, `scipy`).

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import interp1d


def get_yearly_data():
    """
    Retrieves and processes yearly data input from the user.

    Returns:
        list: A list of integers representing the number of books read each month.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function prompts the user to enter the number of books read sequentially
        per month. It expects input in a single line separated by spaces. The input
        is converted to a list of integers representing the absolute values of the
        number of books read each month. If any error occurs during the input or
        conversion process, it catches the exception and prints an error message
        with details.
    """
    try:
        input_data = map(
            float,
            input("Enter the number of books read sequentially per month: ").split(),
        )
        yearly_data = []
        for books in input_data:
            yearly_data.append(abs(int(books)))
        return yearly_data
    except Exception as err:
        print("Error in accepting yearly data: ", err)


def verify_yearly_data(yearly_data: list):
    """
    Verifies the validity of yearly data for books read.

    Args:
        yearly_data (list): A list of integers representing books read per month.

    Returns:
        bool: True if the data is valid (12 elements, each a non-negative integer), False otherwise.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function checks if the input list `yearly_data`:
        - Contains exactly 12 elements.
        - Each element is an integer and non-negative.

        It returns True if these conditions are met, indicating valid data for 12 months
        of books read. If the conditions are not met, it prints an error message specifying
        the requirement for 12 elements and non-negative integers, and returns False. If any
        error occurs during the verification process, it catches the exception and prints
        an error message with details.
    """
    try:
        if len(yearly_data) == 12:
            verification = False
            for books in yearly_data:
                if isinstance(books, int) and books >= 0:
                    verification = True
            return verification
        else:
            print(
                "The data list should have 12 elements, each corresponding sequentially to books read in a month."
            )
            return False
    except Exception as error:
        print(error)
        return False


def smooth_data(x_axis, y_axis, num_points=100):
    """
    Smooths data points using cubic interpolation.

    Args:
        x_axis (array-like): 1-D array of x-coordinates of data points.
        y_axis (array-like): 1-D array of y-coordinates of data points.
        num_points (int, optional): Number of points to interpolate for smoothing.
                                    Defaults to 100.

    Returns:
        tuple: A tuple containing two arrays:
               - x_smooth (numpy.ndarray): Smoothed x-coordinates.
               - y_smooth (numpy.ndarray): Smoothed y-coordinates.

    Usage:
        This function uses cubic interpolation (`interp1d` with kind='cubic') to smooth
        the given data points (x_axis, y_axis). It generates a smooth curve by interpolating
        `num_points` points evenly spaced between the minimum and maximum values of x.
        The smoothed x and y coordinates are returned as numpy arrays in a tuple.

        Note: The input x_axis and y_axis should be array-like objects (lists, numpy arrays, etc.)
        containing numeric data points.
    """
    interpolated_fn = interp1d(x_axis, y_axis, kind="cubic")
    x_smooth = np.linspace(min(x_axis), max(x_axis), num=num_points)
    y_smooth = interpolated_fn(x_smooth)
    return x_smooth, y_smooth


def calculate_ytick_interval(max_value):
    """
    Calculates the optimal y-axis tick interval based on the maximum value.

    Args:
        max_value (int or float): The maximum value of the data range.

    Returns:
        int: The optimal y-axis tick interval based on the maximum value.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function determines the y-axis tick interval for plotting based on the
        maximum value (`max_value`).
        This approach ensures that the y-axis ticks are evenly spaced and appropriately
        scaled based on the range of data values. If any error occurs during the process,
        it catches the exception and prints an error message with details.
    """
    try:
        if max_value <= 10:
            return 1
        elif max_value <= 50:
            return 5
        elif max_value <= 100:
            return 10
        elif max_value <= 500:
            return 50
        else:
            return 100
    except Exception as error:
        print(error)


def plot_books_per_month(books_read):
    """
    Plots the number of books read per month in a line chart with a gradient background.

    Args:
        books_read (list): A list of 12 integers representing books read each month.

    Raises:
        ValueError: If the length of books_read list is not equal to 12.

    Usage:
        This function visualizes the monthly data of books read (`books_read`) using a line chart
        overlaid with scatter points. It also includes a gradient background and custom styling
        for aesthetic appeal:
        - Custom colormap for gradient background.
        - Smoothed line using cubic interpolation.
        - Labels and ticks customized for months and y-axis intervals.

        The function ensures the plot is visually appealing with white-on-color contrasts,
        gridlines for clarity, and removes unnecessary plot spines (borders). If any error
        occurs during the plotting process, it prints the error message.
    """
    try:
        if len(books_read) != 12:
            raise ValueError("The length of books_read lists must be 12.")

        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        fig, ax = plt.subplots(figsize=(10, 6))
        # Create a custom colormap for the gradient background
        cmap = LinearSegmentedColormap.from_list(
            "custom_gradient", ["#b083ff", "#640dfb", "#5d00ff"]
        )
        # Generate gradient background
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        ytick_interval = calculate_ytick_interval(max(books_read))
        ax.imshow(
            gradient,
            aspect="auto",
            cmap=cmap,
            extent=[0, 12, 0, max(books_read) + ytick_interval],
        )
        months_smooth, books_read_smooth = smooth_data(months, books_read)

        # Plot the line chart and scatter points
        ax.plot(months_smooth, books_read_smooth, color="white", linewidth=2)
        ax.scatter(
            months, books_read, color="white", s=30, edgecolors="grey"
        )  # Tiny scatter points

        # Customizing the plot
        ax.set_xlim(1, 12)
        ax.set_ylim(0, max(books_read) + ytick_interval)
        ax.set_xticks(range(1, 13))

        # Move the y-axis to the right
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.tick_params(
            axis="both", which="both", bottom=False, top=False, left=False, right=False
        )

        # Set month labels
        ax.set_xticklabels(
            [
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC",
            ],
            color="white",
            fontsize=10,
        )
        ax.set_yticks(range(0, max(books_read) + ytick_interval, ytick_interval))
        ax.set_yticklabels(
            range(0, max(books_read) + ytick_interval, ytick_interval),
            color="white",
            fontsize=10,
        )
        # Set the face color of the figure
        fig.patch.set_facecolor(cmap(0.5))

        # Remove the spines (borders) of the plot
        for spine in ax.spines.values():
            if spine.spine_type == "bottom":  # Keep only the bottom spine (x-axis)
                spine.set_visible(True)
                spine.set_color("white")
            else:
                spine.set_visible(False)

        # Add gridlines parallel to y-axis
        ax.grid(axis="y", linestyle="-", linewidth=0.5, color="white")

        plt.tight_layout()  # Adjust layout to prevent clipping of labels

        plt.show()

    except Exception as err:
        print(err)


def main():
    """
    Executes the main workflow to plot monthly books read data.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function serves as the main entry point to execute the workflow for plotting
        monthly books read data:
        - Calls `get_yearly_data()` to retrieve the number of books read per month.
        - Calls `verify_yearly_data(books_read)` to validate the retrieved data.
        - If the data is valid (returned True), calls `plot_books_per_month(books_read)`
          to generate and display the plot.

        If any error occurs during the execution of these functions, it catches the exception
        and prints an error message with details.
    """
    try:
        books_read = get_yearly_data()
        ver = verify_yearly_data(books_read)
        if ver is True:
            plot_books_per_month(books_read)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
