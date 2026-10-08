import matplotlib.pyplot as plt


def plot_results(
    results,
    parameters
):

    speeds = results[
        "speeds"
    ]


    maximum_allowed_acceleration = (
        parameters[
            "max_lateral_acceleration"
        ]
    )


    failure_threshold = (
        parameters[
            "failure_threshold"
        ]
    )


    # ========================================================
    # PLOT 1
    # MAXIMUM LATERAL ACCELERATION
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )


    plt.plot(
        speeds,
        results[
            "maximum_lateral_acceleration"
        ],
        linewidth=2
    )


    plt.axhline(
        maximum_allowed_acceleration,
        linestyle="--",
        label="Maximum Allowed"
    )


    plt.xlabel(
        "Vehicle Speed (km/h)"
    )


    plt.ylabel(
        "Maximum Lateral Acceleration (m/s²)"
    )


    plt.title(
        "Maximum Lateral Acceleration vs Vehicle Speed"
    )


    plt.legend()

    plt.grid(True)


    # ========================================================
    # PLOT 2
    # MAXIMUM LANE DEVIATION
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )


    plt.plot(
        speeds,
        results[
            "maximum_lateral_deviation"
        ],
        linewidth=2,
        label="Maximum Lane Deviation"
    )


    plt.axhline(
        failure_threshold,
        linestyle="--",
        label="Failure Threshold"
    )


    critical_speed = results[
        "critical_speed"
    ]


    if critical_speed is not None:

        plt.axvline(
            critical_speed,
            linestyle="--",
            label=(
                f"Critical Speed = "
                f"{critical_speed} km/h"
            )
        )


    plt.xlabel(
        "Vehicle Speed (km/h)"
    )


    plt.ylabel(
        "Maximum Lateral Tracking Error (m)"
    )


    plt.title(
        "Maximum Lane Deviation vs Vehicle Speed"
    )


    plt.legend()

    plt.grid(True)


    # ========================================================
    # PLOT 3
    # MAXIMUM STEERING ANGLE
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )


    plt.plot(
        speeds,
        results[
            "maximum_steering_angle"
        ],
        linewidth=2
    )


    plt.xlabel(
        "Vehicle Speed (km/h)"
    )


    plt.ylabel(
        "Maximum Steering Angle (degrees)"
    )


    plt.title(
        "Maximum Steering Angle vs Vehicle Speed"
    )


    plt.grid(True)


    # ========================================================
    # SHOW ALL THREE
    # ========================================================

    plt.show()