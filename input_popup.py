import tkinter as tk
from tkinter import messagebox

from config import DEFAULT_PARAMETERS


def get_parameters():

    root = tk.Tk()

    root.title("ADAS Lane Change Simulation")

    root.geometry("500x650")

    root.resizable(False, False)


    # ========================================================
    # TITLE
    # ========================================================

    title = tk.Label(
        root,
        text="ADAS Lane Change Simulation",
        font=("Arial", 16, "bold")
    )

    title.pack(
        pady=15
    )


    # ========================================================
    # DESCRIPTION
    # ========================================================

    description = tk.Label(
        root,
        text="Enter simulation parameters\n"
             "or use the default values.",
        font=("Arial", 10)
    )

    description.pack(
        pady=5
    )


    # ========================================================
    # INPUT FRAME
    # ========================================================

    frame = tk.Frame(root)

    frame.pack(
        padx=30,
        pady=10
    )


    # ========================================================
    # PARAMETER DEFINITIONS
    # ========================================================

    fields = [

        (
            "wheelbase",
            "Wheelbase",
            "m"
        ),

        (
            "track_width",
            "Track width",
            "m"
        ),

        (
            "lane_width",
            "Lane width",
            "m"
        ),

        (
            "lane_change_length",
            "Lane-change length",
            "m"
        ),

        (
            "time_step",
            "Time step",
            "s"
        ),

        (
            "lateral_gain",
            "Lateral gain",
            "rad/m"
        ),

        (
            "heading_gain",
            "Heading gain",
            "-"
        ),

        (
            "max_lateral_acceleration",
            "Max lateral acceleration",
            "m/s²"
        ),

        (
            "failure_threshold",
            "Failure threshold",
            "m"
        ),

        (
            "start_speed",
            "Start speed",
            "km/h"
        ),

        (
            "end_speed",
            "End speed",
            "km/h"
        ),

        (
            "speed_step",
            "Speed step",
            "km/h"
        )
    ]


    entries = {}


    # ========================================================
    # CREATE INPUT BOXES
    # ========================================================

    for row, (
        key,
        label,
        unit
    ) in enumerate(fields):

        label_widget = tk.Label(
            frame,
            text=f"{label} ({unit}):",
            anchor="w",
            width=28
        )

        label_widget.grid(
            row=row,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )


        entry = tk.Entry(
            frame,
            width=15
        )

        entry.insert(
            0,
            str(
                DEFAULT_PARAMETERS[key]
            )
        )

        entry.grid(
            row=row,
            column=1,
            padx=5,
            pady=5
        )


        entries[key] = entry


    # ========================================================
    # RESULT STORAGE
    # ========================================================

    parameters = {}


    # ========================================================
    # RUN BUTTON FUNCTION
    # ========================================================

    def run_simulation():

        try:

            for key, entry in entries.items():

                value = float(
                    entry.get()
                )

                parameters[key] = value


            # ----------------------------------------------
            # Basic validation
            # ----------------------------------------------

            if parameters["wheelbase"] <= 0:
                raise ValueError(
                    "Wheelbase must be greater than 0."
                )


            if parameters["track_width"] <= 0:
                raise ValueError(
                    "Track width must be greater than 0."
                )


            if parameters["lane_width"] <= 0:
                raise ValueError(
                    "Lane width must be greater than 0."
                )


            if parameters["lane_change_length"] <= 0:
                raise ValueError(
                    "Lane-change length must be greater than 0."
                )


            if parameters["time_step"] <= 0:
                raise ValueError(
                    "Time step must be greater than 0."
                )


            if parameters["max_lateral_acceleration"] <= 0:
                raise ValueError(
                    "Maximum lateral acceleration must be greater than 0."
                )


            if parameters["failure_threshold"] <= 0:
                raise ValueError(
                    "Failure threshold must be greater than 0."
                )


            if parameters["start_speed"] <= 0:
                raise ValueError(
                    "Start speed must be greater than 0."
                )


            if parameters["end_speed"] <= parameters["start_speed"]:
                raise ValueError(
                    "End speed must be greater than start speed."
                )


            if parameters["speed_step"] <= 0:
                raise ValueError(
                    "Speed step must be greater than 0."
                )


            root.destroy()


        except ValueError as error:

            messagebox.showerror(
                "Invalid Parameter",
                str(error)
            )


    # ========================================================
    # BUTTONS
    # ========================================================

    button_frame = tk.Frame(
        root
    )

    button_frame.pack(
        pady=20
    )


    run_button = tk.Button(
        button_frame,
        text="Run Simulation",
        command=run_simulation,
        width=18,
        height=2
    )

    run_button.pack(
        side="left",
        padx=10
    )


    def reset_defaults():

        for key, entry in entries.items():

            entry.delete(
                0,
                tk.END
            )

            entry.insert(
                0,
                str(
                    DEFAULT_PARAMETERS[key]
                )
            )


    reset_button = tk.Button(
        button_frame,
        text="Reset Defaults",
        command=reset_defaults,
        width=18,
        height=2
    )

    reset_button.pack(
        side="left",
        padx=10
    )


    # ========================================================
    # WAIT FOR USER
    # ========================================================

    root.mainloop()


    return parameters