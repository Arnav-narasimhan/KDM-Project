def calculate_steering(
    lateral_error,
    heading_error,
    lateral_gain,
    heading_gain
):

    steering_angle = (
        lateral_gain * lateral_error
        +
        heading_gain * heading_error
    )

    return steering_angle