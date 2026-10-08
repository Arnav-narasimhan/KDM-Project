import numpy as np


def desired_lane_change(
    x,
    lane_width,
    lane_change_length
):

    if x <= lane_change_length:

        desired_y = (
            lane_width / 2
            * (
                1
                - np.cos(
                    np.pi
                    * x
                    / lane_change_length
                )
            )
        )


        path_slope = (
            lane_width / 2
            * (
                np.pi
                / lane_change_length
            )
            * np.sin(
                np.pi
                * x
                / lane_change_length
            )
        )

    else:

        desired_y = lane_width

        path_slope = 0.0


    desired_yaw = np.arctan(
        path_slope
    )


    return (
        desired_y,
        desired_yaw
    )