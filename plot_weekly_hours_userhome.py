import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch


def get_weekly_data():
    """
    Retrieves and processes weekly data input from the user.

    Returns:
        list: A list of floats representing hours read per day for a week.

    Usage:
        This function prompts the user to enter hours read sequentially per day for a week.
        It expects input in a single line separated by spaces, where each value represents
        hours read on each corresponding day (Sunday to Saturday). The input is converted
        to a list of floats representing the hours read per day. If any error occurs
        during the input or conversion process, it may raise an exception.

        Note:
        - Hours should be between 0.0 and 24.0.
        - The length of the returned list will be 7, corresponding to each day of the week.
    """
    input_data = map(
        float,
        input(
            "Enter hours read sequentially per day for a week (between 0.0 and 24.0): "
        ).split(),
    )
    weekly_data = []
    for hours in input_data:
        weekly_data.append(float(hours))
    return weekly_data


def verify_weekly_data(weekly_data: list):
    """
    Verifies the validity of weekly data for hours read per day.

    Args:
        weekly_data (list): A list of floats representing hours read per day for a week.

    Returns:
        bool: True if the data is valid (7 elements, each between 0.0 and 24.0), False otherwise.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function checks if the input list `weekly_data`:
        - Contains exactly 7 elements.
        - Each element is a float between 0.0 and 24.0, representing hours read per day.

        It returns True if these conditions are met, indicating valid data for a week.
        If the conditions are not met, it prints an error message specifying the requirement
        for 7 elements and valid float values, and returns False. If any error occurs during
        the verification process, it catches the exception and prints an error message with details.
    """
    try:
        if len(weekly_data) == 7:
            verification = False
            for hours in weekly_data:
                if isinstance(hours, float) and 0.0 < hours < 24.00:
                    verification = True
            return verification
        else:
            print(
                "The data list should have 7 elements, each corresponding sequentially to a day of the week."
            )
            return False
    except Exception as error:
        print(error)
        return False


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
        if max_value <= 5:
            return 1
        elif max_value <= 10:
            return 2
        elif max_value <= 15:
            return 3
        elif max_value <= 20:
            return 4
        elif max_value <= 24:
            return 5
        else:
            return 8
    except Exception as error:
        print(error)


def plot_hours_spent_per_day(hours_spent):
    """
    Plots the hours spent per day in a week using rounded bar chart with a gradient background.

    Args:
        hours_spent (list): A list of 7 integers or floats representing hours spent per day for a week.

    Raises:
        ValueError: If the length of hours_spent list is not equal to 7.

    Usage:
        This function visualizes the weekly data of hours spent per day (`hours_spent`) using a rounded
        bar chart with a gradient background for aesthetic appeal:
        - Custom colormap for gradient background.
        - Rounded bar chart bars representing hours spent each day.
        - Labels and ticks customized for days of the week and y-axis intervals.

        The function ensures the plot is visually appealing with white-on-color contrasts,
        gridlines for clarity, and removes unnecessary plot spines (borders). If any error
        occurs during the plotting process, it prints the error message.

    Note:
        - Ensure the length of `hours_spent` list is exactly 7, corresponding to each day of the week.
        - Each element in `hours_spent` should be an integer or float representing hours spent per day.
    """
    try:
        # Ensure days and hours_spent have the same length
        if len(hours_spent) != 7:
            raise ValueError(
                "The length hours_spent lists must be equal to 7, corresponding to 7 days of a week."
            )

        days = ["M", "T", "W", "T ", "F", "S", "S "]
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create a custom colormap for the gradient background
        cmap = LinearSegmentedColormap.from_list(
            "custom_gradient", ["#b083ff", "#640dfb", "#5d00ff"]
        )

        # Generate gradient background
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        ytick_interval = calculate_ytick_interval(max(hours_spent))
        ax.imshow(
            gradient,
            aspect="auto",
            cmap=cmap,
            extent=[-0.5, 6.5, 0, max(hours_spent) + 1],
        )

        # Define bar properties
        bar_width = 0.4
        bar_color = "white"
        bar_alpha = 0.6
        rounded_radius = 0.15

        # Plot the bars with rounded tops
        for i, (day, hours) in enumerate(zip(days, hours_spent)):
            bbox = FancyBboxPatch(
                (i - bar_width / 2, 0),
                bar_width,
                hours,
                boxstyle=f"round,pad=0,rounding_size={rounded_radius}",
                edgecolor="none",
                facecolor=bar_color,
                alpha=bar_alpha,
            )
            ax.add_patch(bbox)

        hour_list = np.arange(0, max(hours_spent) + 1, ytick_interval)
        hr_list = []
        for hour in hour_list:
            hr_list.append("{} hr".format(hour))

        # Customizing the plot
        ax.set_xlim(-0.5, 6.5)  # Adjust x-axis limits to fit all days
        ax.set_ylim(0, max(hours_spent) + 1)
        ax.set_xticks(range(7))  # Set x-ticks to match the number of days
        ax.set_xticklabels(days, color="white", fontsize=10)
        ax.set_yticks(np.arange(0, max(hours_spent) + 1, ytick_interval))
        ax.set_yticklabels(
            hr_list,
            color="white",
            fontsize=10,
        )

        # Move the y-axis to the left and make y-axis line invisible
        ax.yaxis.tick_left()
        ax.yaxis.set_ticks_position("none")

        # Set the color of the ticks
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")

        # Set the labels and title
        ax.set_xlabel("")
        ax.set_ylabel("")
        fig.patch.set_facecolor(cmap(0.5))  # Set the face color of the figure

        # Keep only the bottom spine (x-axis)
        for spine in ax.spines.values():
            if spine.spine_type == "bottom":
                spine.set_visible(True)
                spine.set_color("white")
            else:
                spine.set_visible(False)

        # Add gridlines
        ax.grid(axis="y", linestyle="-", linewidth=0.5, color="white")

        plt.show()
    except Exception as error:
        print(error)


def main():
    """
    Executes the main workflow to plot hours spent per day over a week.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function serves as the main entry point to execute the workflow for plotting
        hours spent per day over a week:
        - Calls `get_weekly_data()` to retrieve hours spent per day input from the user.
        - Calls `verify_weekly_data(weekly_data)` to validate the retrieved data.
        - If the data is valid (returned True), calls `plot_hours_spent_per_day(weekly_data)`
          to generate and display the plot.

        If any error occurs during the execution of these functions, it catches the exception
        and prints an error message with details.
    """
    try:
        weekly_data = get_weekly_data()
        ver = verify_weekly_data(weekly_data)
        if ver is True:
            plot_hours_spent_per_day(weekly_data)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
