import numpy as np


def calculate_ackermann_angles(
    wheelbase,
    track_width,
    steering_angle
):

    if abs(steering_angle) < 1e-8:

        return (
            0.0,
            0.0,
            np.inf
        )


    radius = (
        wheelbase
        / np.tan(steering_angle)
    )


    absolute_radius = abs(radius)


    if absolute_radius <= track_width / 2:

        return (
            np.nan,
            np.nan,
            radius
        )


    inner_angle = np.arctan(
        wheelbase
        / (
            absolute_radius
            - track_width / 2
        )
    )


    outer_angle = np.arctan(
        wheelbase
        / (
            absolute_radius
            + track_width / 2
        )
    )


    direction = np.sign(
        steering_angle
    )


    inner_angle *= direction
    outer_angle *= direction


    return (
        inner_angle,
        outer_angle,
        radius
    )


def calculate_allowable_steering(
    wheelbase,
    speed,
    maximum_lateral_acceleration
):

    if speed <= 0:

        return 0.0


    allowable_angle = np.arctan(
        wheelbase
        * maximum_lateral_acceleration
        / speed**2
    )


    return allowable_angle


def apply_steering_constraint(
    required_steering,
    allowable_steering
):

    saturated = (
        abs(required_steering)
        > allowable_steering
    )


    actual_steering = (
        np.sign(required_steering)
        * min(
            abs(required_steering),
            allowable_steering
        )
    )


    return (
        actual_steering,
        saturated
    )