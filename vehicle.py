import numpy as np


class Vehicle:

    def __init__(self, wheelbase):

        self.wheelbase = wheelbase

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0


    def reset(self):

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0


    def update(
        self,
        speed,
        steering_angle,
        dt
    ):

        x_dot = (
            speed
            * np.cos(self.yaw)
        )


        y_dot = (
            speed
            * np.sin(self.yaw)
        )


        yaw_rate = (
            speed
            * np.tan(steering_angle)
            / self.wheelbase
        )


        self.x += (
            x_dot * dt
        )


        self.y += (
            y_dot * dt
        )


        self.yaw += (
            yaw_rate * dt
        )


        return (
            x_dot,
            y_dot,
            yaw_rate
        )