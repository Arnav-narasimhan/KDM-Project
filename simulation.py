import numpy as np

from vehicle import Vehicle

from trajectory import (
    desired_lane_change
)

from controller import (
    calculate_steering
)

from ackermann import (
    calculate_allowable_steering,
    apply_steering_constraint
)


# ============================================================
# SINGLE SPEED SIMULATION
# ============================================================

def simulate_lane_change(speed_kmh, parameters):

    # ========================================================
    # READ PARAMETERS FROM USER INPUT
    # ========================================================

    wheelbase = parameters["wheelbase"]

    track_width = parameters["track_width"]

    lane_width = parameters["lane_width"]

    lane_change_length = parameters[
        "lane_change_length"
    ]

    time_step = parameters[
        "time_step"
    ]

    lateral_gain = parameters[
        "lateral_gain"
    ]

    heading_gain = parameters[
        "heading_gain"
    ]

    max_lateral_acceleration = parameters[
        "max_lateral_acceleration"
    ]

    failure_threshold = parameters[
        "failure_threshold"
    ]


    # ========================================================
    # CONVERT SPEED
    # ========================================================

    # User enters speed in km/h.
    #
    # Vehicle model uses SI units:
    #
    # m/s = km/h / 3.6

    speed = speed_kmh / 3.6


    # ========================================================
    # CALCULATE SIMULATION TIME
    # ========================================================

    # Time required for vehicle to travel the
    # lane-change distance.

    lane_change_time = (
        lane_change_length
        / speed
    )


    # Add 2 seconds after the lane change so that
    # the vehicle has time to settle.

    simulation_time = (
        lane_change_time
        + 2.0
    )


    # ========================================================
    # CREATE TIME ARRAY
    # ========================================================

    time = np.arange(
        0,
        simulation_time,
        time_step
    )


    # ========================================================
    # CREATE VEHICLE
    # ========================================================

    vehicle = Vehicle(
        wheelbase
    )


    # ========================================================
    # RESULT STORAGE
    # ========================================================

    x_history = []

    y_history = []

    desired_y_history = []

    lateral_error_history = []

    steering_angle_history = []

    required_steering_history = []

    allowable_steering_history = []

    lateral_acceleration_history = []

    yaw_rate_history = []


    # ========================================================
    # STEERING SATURATION FLAG
    # ========================================================

    steering_saturation = False


    # ========================================================
    # MAIN SIMULATION LOOP
    # ========================================================

    for current_time in time:

        # ----------------------------------------------------
        # DESIRED LANE-CHANGE TRAJECTORY
        # ----------------------------------------------------

        desired_y, desired_yaw = (
            desired_lane_change(
                vehicle.x,
                lane_width,
                lane_change_length
            )
        )


        # ----------------------------------------------------
        # LATERAL ERROR
        # ----------------------------------------------------

        lateral_error = (
            desired_y
            - vehicle.y
        )


        # ----------------------------------------------------
        # HEADING ERROR
        # ----------------------------------------------------

        heading_error = (
            desired_yaw
            - vehicle.yaw
        )


        # Keep heading error between
        # -pi and +pi.

        heading_error = np.arctan2(
            np.sin(heading_error),
            np.cos(heading_error)
        )


        # ----------------------------------------------------
        # CONTROLLER
        # ----------------------------------------------------

        # Required steering:
        #
        # delta_required =
        #
        # Ky * lateral_error
        # +
        # Kpsi * heading_error

        required_steering = (
            calculate_steering(
                lateral_error,
                heading_error,
                lateral_gain,
                heading_gain
            )
        )


        # ----------------------------------------------------
        # SPEED-DEPENDENT STEERING LIMIT
        # ----------------------------------------------------

        # delta_max =
        #
        # atan(
        #     L * ay_max / v^2
        # )

        allowable_steering = (
            calculate_allowable_steering(
                wheelbase,
                speed,
                max_lateral_acceleration
            )
        )


        # ----------------------------------------------------
        # APPLY STEERING CONSTRAINT
        # ----------------------------------------------------

        actual_steering, saturated = (
            apply_steering_constraint(
                required_steering,
                allowable_steering
            )
        )


        # Record whether steering saturation
        # occurred at any point.

        if saturated:

            steering_saturation = True


        # ----------------------------------------------------
        # KINEMATIC BICYCLE MODEL
        # ----------------------------------------------------

        _, _, yaw_rate = vehicle.update(
            speed,
            actual_steering,
            time_step
        )


        # ----------------------------------------------------
        # LATERAL ACCELERATION
        # ----------------------------------------------------

        # ay =
        #
        # v^2 * tan(delta) / L

        lateral_acceleration = (
            speed**2
            * np.tan(actual_steering)
            / wheelbase
        )


        # ----------------------------------------------------
        # STORE RESULTS
        # ----------------------------------------------------

        x_history.append(
            vehicle.x
        )

        y_history.append(
            vehicle.y
        )

        desired_y_history.append(
            desired_y
        )

        lateral_error_history.append(
            lateral_error
        )

        steering_angle_history.append(
            np.degrees(
                actual_steering
            )
        )

        required_steering_history.append(
            np.degrees(
                required_steering
            )
        )

        allowable_steering_history.append(
            np.degrees(
                allowable_steering
            )
        )

        lateral_acceleration_history.append(
            lateral_acceleration
        )

        yaw_rate_history.append(
            yaw_rate
        )


    # ========================================================
    # CONVERT RESULTS TO NUMPY ARRAYS
    # ========================================================

    x_history = np.array(
        x_history
    )

    y_history = np.array(
        y_history
    )

    desired_y_history = np.array(
        desired_y_history
    )

    lateral_error_history = np.array(
        lateral_error_history
    )

    steering_angle_history = np.array(
        steering_angle_history
    )

    required_steering_history = np.array(
        required_steering_history
    )

    allowable_steering_history = np.array(
        allowable_steering_history
    )

    lateral_acceleration_history = np.array(
        lateral_acceleration_history
    )

    yaw_rate_history = np.array(
        yaw_rate_history
    )


    # ========================================================
    # MAXIMUM VALUES
    # ========================================================

    maximum_lateral_acceleration = np.max(
        np.abs(
            lateral_acceleration_history
        )
    )


    maximum_steering_angle = np.max(
        np.abs(
            steering_angle_history
        )
    )


    maximum_lateral_deviation = np.max(
        np.abs(
            lateral_error_history
        )
    )


    maximum_yaw_rate = np.max(
        np.abs(
            yaw_rate_history
        )
    )


    # ========================================================
    # LANE-CHANGE FAILURE
    # ========================================================

    # Failure occurs when:
    #
    # max(|e_y|) > failure threshold

    lane_change_failed = (
        maximum_lateral_deviation
        > failure_threshold
    )


    # ========================================================
    # RETURN COMPLETE SINGLE-SPEED RESULTS
    # ========================================================

    return {

        "speed_kmh":
            speed_kmh,

        "time":
            time,

        "x":
            x_history,

        "y":
            y_history,

        "desired_y":
            desired_y_history,

        "lateral_error":
            lateral_error_history,

        "steering_angle":
            steering_angle_history,

        "required_steering":
            required_steering_history,

        "allowable_steering":
            allowable_steering_history,

        "lateral_acceleration":
            lateral_acceleration_history,

        "yaw_rate":
            yaw_rate_history,

        "maximum_lateral_acceleration":
            maximum_lateral_acceleration,

        "maximum_steering_angle":
            maximum_steering_angle,

        "maximum_lateral_deviation":
            maximum_lateral_deviation,

        "maximum_yaw_rate":
            maximum_yaw_rate,

        "steering_saturation":
            steering_saturation,

        "lane_change_failed":
            lane_change_failed
    }


# ============================================================
# SPEED SWEEP
# ============================================================

def run_speed_sweep(parameters):

    # ========================================================
    # READ SPEED-SWEEP PARAMETERS
    # ========================================================

    start_speed = int(
        parameters["start_speed"]
    )

    end_speed = int(
        parameters["end_speed"]
    )

    speed_step = int(
        parameters["speed_step"]
    )


    # ========================================================
    # CREATE SPEED ARRAY
    # ========================================================

    speeds = np.arange(
        start_speed,
        end_speed + 1,
        speed_step
    )


    # ========================================================
    # RESULT STORAGE
    # ========================================================

    results = []


    print()
    print(
        "Running speed sweep..."
    )

    print(
        f"Speed range: "
        f"{start_speed} → {end_speed} km/h"
    )

    print(
        f"Speed increment: "
        f"{speed_step} km/h"
    )

    print()


    # ========================================================
    # RUN SIMULATION AT EACH SPEED
    # ========================================================

    for speed in speeds:

        result = simulate_lane_change(
            speed,
            parameters
        )

        results.append(
            result
        )


    print(
        "Speed sweep complete."
    )


    # ========================================================
    # EXTRACT MAXIMUM LATERAL ACCELERATION
    # ========================================================

    maximum_lateral_acceleration = np.array([

        result[
            "maximum_lateral_acceleration"
        ]

        for result in results

    ])


    # ========================================================
    # EXTRACT MAXIMUM STEERING ANGLE
    # ========================================================

    maximum_steering_angle = np.array([

        result[
            "maximum_steering_angle"
        ]

        for result in results

    ])


    # ========================================================
    # EXTRACT MAXIMUM LATERAL DEVIATION
    # ========================================================

    maximum_lateral_deviation = np.array([

        result[
            "maximum_lateral_deviation"
        ]

        for result in results

    ])


    # ========================================================
    # EXTRACT MAXIMUM YAW RATE
    # ========================================================

    maximum_yaw_rate = np.array([

        result[
            "maximum_yaw_rate"
        ]

        for result in results

    ])


    # ========================================================
    # EXTRACT STEERING SATURATION
    # ========================================================

    steering_saturation = np.array([

        result[
            "steering_saturation"
        ]

        for result in results

    ])


    # ========================================================
    # EXTRACT FAILURE STATUS
    # ========================================================

    lane_change_failed = np.array([

        result[
            "lane_change_failed"
        ]

        for result in results

    ])


    # ========================================================
    # FIND CRITICAL SPEED
    # ========================================================

    failed_indices = np.where(
        lane_change_failed
    )[0]


    if len(failed_indices) > 0:

        critical_speed = speeds[
            failed_indices[0]
        ]

    else:

        critical_speed = None


    # ========================================================
    # PRINT CRITICAL SPEED
    # ========================================================

    print()

    print(
        "=============================================="
    )

    print(
        "           SPEED SWEEP SUMMARY"
    )

    print(
        "=============================================="
    )


    if critical_speed is not None:

        print(
            f"Critical speed: "
            f"{critical_speed:.0f} km/h"
        )

    else:

        print(
            "No lane-change failure detected."
        )


    print(
        "=============================================="
    )


    # ========================================================
    # RETURN SPEED-SWEEP RESULTS
    # ========================================================

    return {

        "speeds":
            speeds,

        "runs":
            results,

        "maximum_lateral_acceleration":
            maximum_lateral_acceleration,

        "maximum_steering_angle":
            maximum_steering_angle,

        "maximum_lateral_deviation":
            maximum_lateral_deviation,

        "maximum_yaw_rate":
            maximum_yaw_rate,

        "steering_saturation":
            steering_saturation,

        "lane_change_failed":
            lane_change_failed,

        "critical_speed":
            critical_speed
    }